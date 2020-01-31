import FreeCAD
import Part
from FreeCAD import Base
import inspect
from utilsConfig import *
import MeshPart
import genOptimizedPart as gop
import baseModelOperations as bmo
import sys

def removeDuplicates(line):
    newLineList = []
    for point in line:
        if not point in newLineList:
            newLineList.append(point)
        #else:
        #    print("not added:", point)
    #print("additional:", newLineList[0])
    #newLineList.append(newLineList[0])
    return newLineList

def mergeEdgesInsidePolys(polys):
    #print("before merge", polys)
    polylines = []
    for polyInLayer in polys:
        for wire in polyInLayer:
            wirePoly = []
            for edge in wire:
                for point in edge:
                    wirePoly.append(point)
            polylines.append(wirePoly)
    #print("after merge:", polylines)
    return polylines

def mergeEdgesInsidePolysRough(wire):
    #print("before merge", polys)
    polyline = []
    for edge in wire:
        for point in edge:
            polyline.append(point)
    #print("wirePoly", polyline)
    #print("after merge:", polylines)
    return polyline

def mergeEdgesInsideSlices(polys):
    #print("before merge", polys)
    polylines = []
    #for polyInLayer in polys:
    #    for wire in polyInLayer:
    for wire in polys:
        wirePoly = []
        for edge in wire:
            for point in edge:
                wirePoly.append(point)
        polylines.append(wirePoly)
    #print("after merge:", polylines)
    #input("slices")
    return polylines

def mapPolysToZ(polys):
    polysMapToZ = {}
    #print("before poly", polys)
    for poly in polys:
        key = poly[0][z]
        #print("key", key)
        
        #print("before remove", poly)
        poly = removeDuplicates(poly)
        if match2FloatLists(poly[0], poly[-1], 0.01):
            poly = poly[:-1]
        #print("after remove", poly)
        if key in polysMapToZ.keys():
            polysMapToZ[key].append(poly)
        else:
            #print("key", key, "poly", poly)
            polysMapToZ[key] = [poly]

    #print("map ================================= poly")
    #for key, value in polysMapToZ.items():
    #    print("key:", key)
    #    for val in value:
    #        print "--->",val
    
    return polysMapToZ


def crossSectionsToZRough(polys):
    polysMapToZ = {}
    #print("before poly", polys)
    for polyPerLayer in polys:
        for poly in polyPerLayer:
            key = poly[0][z]
            #print("key", key)
            poly = removeDuplicates(poly)
            if key in polysMapToZ.keys():
                polysMapToZ[key].append(poly)
            else:
                #print("key", key, "poly", poly)
                polysMapToZ[key] = [poly]

    #print("map ================================= poly")
    #for key, value in polysMapToZ.items():
    #    print("key:", key)
    #    for val in value:
    #        print "--->",val
    
    return polysMapToZ


def genAndMapPolyFromSlices(slices): 
    bmo.saveModel(slices.exportBrep, "sliced.brep")
    #print("begin genAndMapPolyFromSlices")
    #for wire in slices.Wires:
    #    print("\nwire")
    #    for edge in wire.Edges:
    #        print("wire: ", [vertex.Point for vertex in edge.Vertexes])
    #input("some")
    polys = gop.genPolyFromShape(slices)
    #print("polys", polys)
    #polys = mergeEdgesInsideSlices(polys)
    #for poly in polys:
    #    print "poly for " + str(poly[0][z])
    #    for point in poly:
    #        print("\tpoint" + str(point)) 
    #for layer in polys:
    #    print("layer " + str(layer[0][z]))
    #    for poly in layer:
    #        print("\tpoly")
    #        for point in poly:
    #            print("\t\tpoint"+ str(point))
    polysMapToZ = mapPolysToZ(polys)
    #for poly in polys:
    #    key = poly[0][z]
    #    poly = removeDuplicates(poly)
    #    if key in polysMapToZ.keys():

    #        polysMapToZ[key].append(poly)
    #    else:
    #        polysMapToZ[key] = [poly]
    #for key, value in polysMapToZ.items():
    #    print("key", key)
    #    for val in value:
    #        print("\tvalue " + str(val))
    #print("genAndMapPolyFromSlices end")
    return polysMapToZ


def genPolyFromFaces(shape, minThickness, maxThickness):
    shape.tessellate(2)
    bbox = bmo.genBBox(shape)
    #basePoint = Base.Vector(bbox.XMax + 0.5, bbox.YMin - 0.5, bbox.ZMax)
    #box = Part.makeBox(bbox.XLength + 1.0, bbox.YLength +  1.0, bbox.ZMax - bbox.ZMin, basePoint, Base.Vector(0,0,-1))
    basePoint = Base.Vector(bbox.XMax, bbox.YMin, bbox.ZMax)
    box = Part.makeBox(bbox.XLength, bbox.YLength, bbox.ZMax - bbox.ZMin, basePoint, Base.Vector(0,0,-1))
    partToCut = box.cut(shape)
    bmo.saveModel(partToCut.exportBrep, "partToCut.brep")

    partToCut.tessellate(1)
    bbox = partToCut.BoundBox

    multVal = 10
    #valBegin = int(-abs(bbox.ZMax + bbox.ZMin) / 2 * multVal)
    valBegin = 0
    #valEnd = int( abs(bbox.ZMax + bbox.ZMin) / 2 * multVal)
    valEnd = int( abs(bbox.ZMin) * multVal) 
    #by = int((bbox.ZMax - bbox.ZMin)*minThickness)
    by = int(minThickness * 10)
    #print("begin", valBegin, "end", valEnd, "by", by)

    sliceCoord = range(valBegin, valEnd, by)
    sliceCoord = [float(elem) / multVal for elem in sliceCoord]
    #print("sliceCoord", sliceCoord)
    #sliceCoord = [3]
    polysMapToZ = genAndMapPolyFromSlices(partToCut.slices(Base.Vector(0,0,-1), sliceCoord))

    sliced = partToCut.slices(Base.Vector(0,0,-1), sliceCoord)
    bmo.saveModel(sliced.exportBrep, "sliced.brep")
    polys = gop.genPolyFromShape(sliced)
    gen = partToCut.slices(Base.Vector(0,0,-1), sliceCoord)
    #print("Poly", polys)

    bmo.saveModel(gen.exportBrep, "polys.brep")
    #polys = mergeEdgesInsidePolys(polys)
        
    return polysMapToZ

