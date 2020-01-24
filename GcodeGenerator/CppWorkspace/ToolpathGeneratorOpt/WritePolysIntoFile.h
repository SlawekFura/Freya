#pragma once
#include "PolyWithHolesCreator.h"
//#define DEBUG_VERSION

void generateAndSavePoly(std::ostream& outfile, Polygon_with_holes polyg, float zCoord,
                         double offset, bool isFirstPass, float millDiameter)
{
    bool isPolyWithHoleEmpty = polyg.outer_boundary().vertices_begin() == polyg.outer_boundary().vertices_end();
    //std::cout << "isPolyWithHoleEmpty: " << isPolyWithHoleEmpty << std::endl;
    if(not isPolyWithHoleEmpty)
    {
//        std::fstream debugFile;
//        debugFile.open("data3.txt", std::ofstream::out | std::ofstream::trunc);//std::ios_base::app
//        for(auto vertIter = polyg.outer_boundary().vertices_begin(); vertIter !=  polyg.outer_boundary().vertices_end(); ++vertIter)
//        {
//            debugFile << *vertIter << std::endl;
//        }
//        debugFile << std::endl;
//
//        for(auto holeIter = polyg.holes_begin(); holeIter !=  polyg.holes_end(); ++holeIter)
//        {
//            for(auto vertIter = holeIter->vertices_begin(); vertIter !=  holeIter->vertices_end(); ++vertIter)
//                debugFile << *vertIter << std::endl;    
//            debugFile << std::endl;
//        }
//            
        auto newOffset = offset;
        if(isFirstPass)
        {
            newOffset = millDiameter / 2;
            isFirstPass = false;
        }
        //std::cout << polyg << std::endl;
        auto iss = CGAL::create_interior_skeleton_and_offset_polygons_2(newOffset, polyg); 
        std::cout << "firstPass --------------" << std::endl;
        size_t size = iss.size();
        if(iss.empty())
        {
            iss = CGAL::create_interior_skeleton_and_offset_polygons_2(newOffset / 2, polyg);
            //std::cout << "half offset" << std::endl;
        }
        
        //std::cout << "\nnewVect" << std::endl;
        
        //std::fstream debugFile;
        //debugFile.open("/home/slawek/workspace/Frez/Freya/GcodeGenerator/CppWorkspace/ToolpathGenerator/data.txt", std::ofstream::out | std::ofstream::trunc);//std::ios_base::app

//        for (const auto& elem : iss)
//        {        
//            for (auto iter = elem->vertices_begin(); iter != elem->vertices_end(); ++iter)
//            {
//                debugFile << *iter << std::endl;
//            }        
//        }
//        debugFile.close();
      
 //       std::cout << "size: " << size << std::endl;
        for (const auto& elem : iss)
        {

            for (auto iter = elem->vertices_begin(); iter != elem->vertices_end(); ++iter)
            {
                outfile << "\t" << *iter << std::endl;
            }
            bool areAnyVertices = elem->vertices_begin() != elem->vertices_end();
            if(areAnyVertices)
                outfile << "\t" << *(elem->vertices_begin()) << std::endl;
            outfile << std::endl;
        }
        
        std::vector<Polygon_2> polyVect;
        for(auto elem : iss)
        {
            polyVect.push_back(*elem);
        }
        float dummyVal = -1.0;
        
        auto polyWithHolesMap = createPolygonsWithHoles({{dummyVal, polyVect}});
        for(auto& polyWithHolesPair : polyWithHolesMap)
        {
//            debugFile << "=================================" << std::endl;    
            for(auto& polyWithHoles : polyWithHolesPair.second)
            {
//                debugFile << "outer:" << std::endl;
//                for(auto vertIter = polyWithHoles.outer_boundary().vertices_begin(); vertIter != polyWithHoles.outer_boundary().vertices_end(); ++vertIter)
//                {
//                    debugFile << *vertIter << std::endl;
//                }
//                debugFile << std::endl;
//                debugFile << "holes:" << std::endl;
//                for(auto holeIter = polyWithHoles.holes_begin(); holeIter !=  polyWithHoles.holes_end(); ++holeIter)
//                {
//                    for(auto vertIter = holeIter->vertices_begin(); vertIter !=  holeIter->vertices_end(); ++vertIter)
//                        debugFile << *vertIter << std::endl;    
//                    debugFile << std::endl;
//                }
           
                generateAndSavePoly(outfile, polyWithHoles, zCoord, offset, isFirstPass, millDiameter);
            }
        }                
    }
}