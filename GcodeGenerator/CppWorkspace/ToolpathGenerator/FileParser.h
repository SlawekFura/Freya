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

typedef CGAL::Exact_predicates_inexact_constructions_kernel K ;
typedef K::Point_2                    Point ;
typedef CGAL::Polygon_2<K>            Polygon_2 ;

std::map<float, std::vector<Polygon_2>> parse(std::ifstream& inputFile)
{
    std::string line;
    std::map<float, std::vector<Polygon_2>> crossSections;
    boost::optional<Polygon_2> polyg;
    boost::optional<std::vector<Polygon_2>> polygons;
    float key;
    
    while(std::getline(inputFile, line))
    {   
        std::stringstream ss(line);
        if(ss.peek() == 'p')
        {
            if(polyg)
            {
                if(!polygons)
                    polygons = std::vector<Polygon_2>{*polyg};
                else
                    polygons->push_back(*polyg);
                polyg.reset();
            }
        }
        else if (ss.peek() != '\t')
        {
            if(polygons)
            {                    
                polygons->push_back(*polyg);
                polyg.reset();
                
                crossSections.insert({key, *polygons});
                polygons.reset();
            }
            ss >> key;
        }
        else
        {
            ss.get();
            ss.get();
            float x, y; ss >> x; ss.get(); ss >> y;
            if(!polyg)
                polyg = Polygon_2();
            polyg->push_back({x, y});
        }
    }
            
    crossSections.insert({key, *polygons});
    return crossSections;
}