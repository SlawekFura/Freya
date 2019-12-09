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
        else:
            print("not added:", point)
    return newLineList

def mergeEdgesInsidePolys(polys):
    polylines = []
    for poly in polys:
        partPoly = poly[0]
        for edge in poly[1:]:
            partPoly.extend(edge)
        polylines.append(partPoly)
    return polylines

def genPolyFromSlices(slices):
    polylines = []
    print(len(slices.Wires[11:16]))
    for wire in slices.Wires[:3]:
        polyFromEdge = []
        print("wire " + str(wire.Edges[0].Vertexes[0].Z))
        for edge in wire.Edges:
            polyFromVertexes = []
            for vertex in edge.Vertexes:
                polyFromVertexes.append(vertex.Point)
            polyFromEdge.append(polyFromVertexes)
        polylines.append(polyFromEdge)

    return polylines

def mapPolysToZ(polys):
    polysMapToZ = {}
    for poly in polys:
        key = poly[0][z]
        print("key", key)
        poly = removeDuplicates(poly)
        if key in polysMapToZ.keys():

            polysMapToZ[key].append(poly)
        else:
            polysMapToZ[key] = [poly]
    return polysMapToZ


def genAndMapPolyFromSlices(slices): 
    polys = gop.genPolyFromShape(slices)
    polys = mergeEdgesInsidePolys(polys)
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
    return polysMapToZ


def genPolyFromFaces(shape, minThickness, maxThickness):

    bbox = bmo.genBBox(shape)
    basePoint = Base.Vector(bbox.XMax, bbox.YMin, bbox.ZMax)
    box = Part.makeBox(bbox.XLength, bbox.YLength, bbox.ZMax - bbox.ZMin, basePoint, Base.Vector(0,0,-1))
    partToCut = box.cut(shape)
    bmo.saveModel(partToCut.exportBrep, "partToCut.brep")

    #polys = pfc.genPolyFromFaces(box.cut(shape), minThickness)
    #mesh = MeshPart.meshFromShape(shape, 0.1, 0.1, 0.1)#MinLength= 1, MaxLength = 10.5, 2)

    #mesh.write("./mesh.stl")
    #print(inspect.getmembers(Part.Compound))
    #bmo.saveModel(mesh.write, "mesh.stl")
    partToCut.tessellate(1)
    bbox = partToCut.BoundBox

    multVal = 10
    valBegin = int(-abs(bbox.ZMax - bbox.ZMin) / 2 * multVal)
    valEnd = int( abs(bbox.ZMax - bbox.ZMin) / 2 * multVal)
    by = int((bbox.ZMax - bbox.ZMin)*minThickness)
    #print("begin", valBegin, "end", valEnd, "by", by)

    sliceCoord = range(valBegin, valEnd, by)
    sliceCoord = [float(elem) / multVal for elem in sliceCoord]
    print("sliceCoord", sliceCoord)
    
    polysMapToZ = genAndMapPolyFromSlices(partToCut.slices(Base.Vector(0,0,-1), sliceCoord))
    #polys = genPolyFromSlices(partToCut.slices(Base.Vector(0,0,-1), sliceCoord))
    polys = gop.genPolyFromShape(partToCut.slices(Base.Vector(0,0,-1), sliceCoord))
    gen = partToCut.slices(Base.Vector(0,0,-1), sliceCoord)
    #print(polys)

    bmo.saveModel(gen.exportBrep, "polys.brep")
    polys = mergeEdgesInsidePolys(polys)
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
    #polysMapToZ = {}
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
        
    return polysMapToZ

