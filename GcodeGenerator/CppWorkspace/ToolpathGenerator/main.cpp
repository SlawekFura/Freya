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

#include "FileParser.h"
#include "WritePolysIntoFile.h"

int main(int argc, char* argv[])
{
    if(argc < 2)
    {
        std::cout << "Not enough arguments" << std::endl;
        return -1;
    }
    
    std::ifstream inputFile;
    inputFile.open("/home/slawek/workspace/Frez/Freya/GcodeGenerator/3D/MeshOffsetsMap", std::ios_base::in);
    
    std::map<float, std::vector<Polygon_2>> crossSections = parse(inputFile);
    auto polyWithHolesMap = createPolygonsWithHoles(crossSections);
    
    float offset = atof(argv[1]);
    //float offset = 0.8;
    std::cout << "Offset is[*]: " << argv[1] << std::endl;
    std::cout << "Offset is: " << offset << std::endl;
    std::ofstream outfile;
    outfile.open("/home/slawek/workspace/Frez/Freya/GcodeGenerator/3D/dataFromCgal.txt", std::ofstream::out | std::ofstream::trunc);//std::ios_base::app

    #ifndef DEBUG_VERSION
    for (auto& polyWithHolesPair : polyWithHolesMap)
    #endif
    {
#ifdef DEBUG_VERSION
        float zCoord = 4.99289989;
        auto& polyWithHolesVect = polyWithHolesMap[4.99289989];
#else

        float zCoord = polyWithHolesPair.first;
        outfile << zCoord << std::endl;
        
        auto& polyWithHolesVect = polyWithHolesPair.second; 
#endif
        bool shouldDivideOffset = true;
        std::map<float, std::vector<Polygon_2>> layerGeneralOutput;
        
        for(auto& polyWithHole : polyWithHolesVect)
        {        
            generateAndSavePoly(outfile, polyWithHole, zCoord, offset, shouldDivideOffset);
        }
    }
    return 0;
}