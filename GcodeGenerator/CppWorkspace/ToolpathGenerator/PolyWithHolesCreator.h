#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Polygon_with_holes_2.h>
#include <CGAL/create_straight_skeleton_from_polygon_with_holes_2.h>
#include <CGAL/create_offset_polygons_from_polygon_with_holes_2.h>
#include <CGAL/Polygon_2_algorithms.h>

#include <fstream>
#include <vector>
#include <map>
#include <algorithm>
#include <iostream>

typedef CGAL::Exact_predicates_inexact_constructions_kernel K ;
typedef K::Point_2                    Point ;
typedef CGAL::Polygon_2<K>            Polygon_2 ;
typedef CGAL::Polygon_with_holes_2<K> Polygon_with_holes ;

bool check_inside(Point pt, Point *pgn_begin, Point *pgn_end, K traits)
{
  switch(CGAL::bounded_side_2(pgn_begin, pgn_end,pt, traits)) {
    case CGAL::ON_BOUNDED_SIDE :
      return true;
      break;
    case CGAL::ON_BOUNDARY:
      return false;
      break;
    case CGAL::ON_UNBOUNDED_SIDE:
      return false;
      break;
  }
}

std::map<float, std::vector<Polygon_with_holes>> createPolygonsWithHoles(std::map<float, std::vector<Polygon_2>> polygonsMap)
{
    std::map<float, std::vector<Polygon_with_holes>> polygonsWithHolesMap;
    std::map<float, std::vector<Polygon_2>> holesMap;
    for(auto& polygonsInLayer : polygonsMap)
    {
        float key = polygonsInLayer.first;
        auto& polygVect = polygonsInLayer.second;
        
        for(auto it = polygonsInLayer.second.begin(); it != polygonsInLayer.second.end(); ++it)
        {
            auto checkIfPointIsInsidePoly = [&](const Point& point)
            {
                return std::none_of(polygVect.begin(), polygVect.end(),[&point](const Polygon_2& polygon){
                        return check_inside(point, &(*polygon.vertices_begin()), &(*polygon.vertices_end()), K());
                });
            };
            
            bool isOuterPoly = std::all_of(it->vertices_begin(), it->vertices_end(), checkIfPointIsInsidePoly);            
            if(isOuterPoly)
            {     
                if(it->orientation() == CGAL::CLOCKWISE)
                    it->reverse_orientation();
                polygonsWithHolesMap[key].push_back(Polygon_with_holes{*it});                
            }
            else
            {
                if(it->orientation() == CGAL::COUNTERCLOCKWISE)
                    it->reverse_orientation();                                
                holesMap[key].push_back(Polygon_2{*it});
            }
        };
    }

    for(auto& elem : polygonsWithHolesMap)
    {
        float key =  elem.first;
        auto& polygonsWithHolesVect = elem.second;
        

        for(auto& polyWithHoles : polygonsWithHolesVect)
        {
            auto checkIfPointIsInsidePolyWithHoles = [&](const Point& point)
            {
                return check_inside(point, 
                                    &(*polyWithHoles.outer_boundary().vertices_begin()), 
                                    &(*polyWithHoles.outer_boundary().vertices_end()), 
                                    K());
            };
            
            for(auto holeIter = holesMap[key].begin(); holeIter != holesMap[key].end(); ++holeIter)
            {            
                if(holeIter->is_empty())
                    break;
                bool isInnerPoly = std::all_of(&(*holeIter->vertices_begin()), &(*holeIter->vertices_end()), checkIfPointIsInsidePolyWithHoles);
                if(isInnerPoly)
                {
                    if(holeIter->orientation() == CGAL::COUNTERCLOCKWISE)
                        holeIter->reverse_orientation();                                       
                    polyWithHoles.add_hole(*holeIter);
                }
            }       
        }
    }
    
    return polygonsWithHolesMap;
}

