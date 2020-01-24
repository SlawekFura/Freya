#include <boost/shared_ptr.hpp>
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Polygon_with_holes_2.h>
#include <CGAL/create_straight_skeleton_from_polygon_with_holes_2.h>
#include <CGAL/create_offset_polygons_from_polygon_with_holes_2.h>
#include <CGAL/Polygon_2_algorithms.h>

#include <fstream>
#include <vector>
#include <map>
#include <boost/optional.hpp>
#include <algorithm>
#include <iostream>
#include <boost/optional.hpp>
#include <chrono>

#include "DatafileParser.h"
#include "WritePolysIntoFile.h"
#include "FileSearch/FileSearch/ThreadPool.hpp"
#include "FileSearch/FileSearch/ParametersValidator.h"
#include "FileSearch/FileSearch/Task.hpp"
#include "FileSearch/FileSearch/Result.h"

auto getNthMapElemIt(std::map<float, std::vector<Polygon_2>>& p_map, int n)
{
    auto l_ref = p_map.begin();
    while(n-- > 0)
        ++l_ref;
    return l_ref;
}


int main(int argc, char* argv[])
{
    #ifdef CGAL_HAS_THREADS
        printf ("Test mode\n");
    #endif
 
    if(argc < 3)
    {
        std::cout << "Not enough arguments" << std::endl;
        return -1;
    }
    std::cout << "Dupa1" << std::endl;
    std::ifstream inputFile;
    inputFile.open("/home/slawek/workspace/Frez/Freya/GcodeGenerator/3D/MeshOffsetsMap", std::ios_base::in);
    
    
    float offset = atof(argv[1]);
    float millDiameter = atof(argv[2]);
    int processNum = atoi(argv[3]);
    int numOfProcesses = atoi(argv[4]);

    std::map<float, std::vector<Polygon_2>> baseMap = parse(inputFile);
    int numOfElements = baseMap.size();
    int multiplicator = ceil(float(numOfElements) / numOfProcesses);

    auto range_begin = getNthMapElemIt(baseMap, processNum * multiplicator);
    int endIdx = ((processNum + 1) * multiplicator);    
    auto range_end = (endIdx >= numOfElements) ? baseMap.end() : getNthMapElemIt(baseMap, endIdx);
    
    std::map<float, std::vector<Polygon_2>> crossSections(range_begin, range_end);
    
    std::cout << "size: " << crossSections.size() << std::endl;
    auto polyWithHolesMap = createPolygonsWithHoles(crossSections);

    std::cout << "range_start: " << processNum * multiplicator << "\tendIdx: " << endIdx << "\tbaseSize: "<< baseMap.size() << "\tsize: " << crossSections.size()<< std::endl;
    std::cout << "Offset is: " << offset << std::endl;
    std::cout << "Mill diameter is: " << millDiameter << std::endl;
    std::ofstream outfile;
    outfile.open("../3D/dataFromCgal_" + std::to_string(processNum) + ".txt", std::ofstream::out | std::ofstream::trunc);//std::ios_base::app

	std::mutex printMutex;
	auto threadSafePrint = [&](std::string p_string)
	{
		std::unique_lock<std::mutex>l_lock(printMutex);
		std::cout << p_string << std::endl;
	};
    
    Result result;
    TaskFactory l_taskFactory(threadSafePrint, result);
    
    auto startTime = std::chrono::system_clock::now();

	//unsigned int numOfAvailableThreads = std::thread::hardware_concurrency();
	unsigned int numOfAvailableThreads = 1;
    
  	{
        std::cout << "offset: " << offset << "\tmillDiameter: " << millDiameter << std::endl; 
        int i = 0;
        ThreadPool l_threadPool(numOfAvailableThreads, startTime);
        for (std::pair<float, std::vector<Polygon_with_holes>>  polyWithHolesPair : polyWithHolesMap)
        {
            //if (!(i % 10))
                l_threadPool.enqueue(l_taskFactory.createTask(std::move(polyWithHolesPair), offset, millDiameter));
            ++i;
//            if(i == 2)
//                break;
        }
    }
    std::cout << "endtime: " << static_cast<std::chrono::duration<double>>(std::chrono::system_clock::now() - startTime).count() << std::endl;
    for(auto& layer : result.resultContainer)
    {
        outfile << layer.second.str();// << std::endl;
        std::cout << "dupa: " << layer.first << std::endl;
    }
    return 0;
}