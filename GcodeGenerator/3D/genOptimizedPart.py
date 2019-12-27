import FreeCAD
import FreeCADGui  
import Part
import inspect
import Mesh
import MeshPart
from FreeCAD import Base
import baseModelOperations as bmo
import utilsConfig as uc
import math
import sys
sys.path.append('../../Common/')
import utils
import polyFromFaceCreator as pfc


def genBaseFace(shape):
    facesWithNormalZ = None
    lowestZ = 0
    for face in shape.Faces:
        if (face.normalAt(0,0)[2] in [-1,1] and face.Vertexes[0].Z < lowestZ):
            lowestZ = face.Vertexes[0].Z
            facesWithNormalZ = face

    return facesWithNormalZ

def reorientPolys(polys):
    for poly in polys[1:]:
        prevPoly = polys[polys.index(poly) - 1]
        if uc.match2FloatLists(prevPoly[-1], poly[0]):
            continue
        elif uc.match2FloatLists(prevPoly[0], poly[0]):
            prevPoly = prevPoly.reverse()
        elif uc.match2FloatLists(prevPoly[-1], poly[-1]):
            poly = poly.reverse()
        elif uc.match2FloatLists(prevPoly[0], poly[-1]):
            prevPoly = prevPoly.reverse()
            poly = poly.reverse()
    return polys

def sortPolyFromWire(edges):
    print("edges", edges)
    newPoly = [edges[0]]
    edges.remove(edges[0])

    while len(edges) > 0:
        newEdge = []
        flag = False
        edgeDebug = None
        edgesDebug = None
        for edge in edges:
            lastPointOfLastEdge = newPoly[-1][-1]
            print("edge[0]", edge[0], " edge[-1]:", edge[-1], "lasPointOfLastEdge[-1]:", lastPointOfLastEdge)
            edgesDebug = edges
            edgeDebug = edge

            if uc.match2FloatLists(lastPointOfLastEdge, edge[0]):
                edges.remove(edge)
                newPoly.append(edge)
                flag = True
            if uc.match2FloatLists(lastPointOfLastEdge, edge[-1]):
                #print("reverse", edge)
                #print("DEBUG edges:", edgesDebug)
                #print("DEBUG edge:", edgeDebug) 
                edges.remove(edge)
                edge.reverse()
                print("reverse after", edge)
                newPoly.append(edge)
                flag = True
        #print("\n\n")
        #print("newpoly", newPoly)
        #print("\n")
        #print("edges", edges)
        #newPoly.extend(newEdge)
        if not flag:

            input("asdsad")

    #print("end")
    #print("after sorting", newPoly)
    return newPoly
        

def genPolyFromShape(face):
    #print("genPolyFromShape begin")
    polylines = []
    for wire in face.Wires:
        polyFromWire = []
        #print("polyFromWire AAAA") 
        for edge in wire.Edges:
            polyFromEdge = []
            if type(edge.Curve) is Part.BSplineCurve:
                numOfPoints = int(edge.Curve.length() / uc.smallestDiscLength)
                for point in edge.Curve.discretize(numOfPoints):
                    point = utils.roundFloatList([point.x, point.y, point.z])
                    polyFromEdge.append(point)
                    #print("edge curve:", point) 
            else:
                for point in edge.Vertexes:
                    point = utils.roundFloatList([point.Point.x, point.Point.y, point.Point.z])
                    polyFromEdge.append(point)
                    #print("edge line:", point) 
                #if (polyFromEdge[0][2] == 0.7):
                    #input("some")
            
        #    polyFromWire.append(wire.discretize(50))
        #print("polyFromWire:", polyFromWire) 
        #polylines.append(sortPolyFromWire(polyFromWire))
        #polylines.append(polyFromWire)
        poly = []
        for point in wire.discretize(50):
            point = utils.roundFloatList([point.x, point.y, point.z], 3)
            poly.append(point)
        polylines.append(poly)


    #for poly in polylines:
    #    print "\nafter:"
    #    print poly

    print("genPolyFromShape end")
    return polylines

def genPolyFromShapeRough(face):
    print("genPolyFromShape begin")
    polylines = []
    for wire in face.Wires:
        numOfPoints = int(wire.Length / uc.smallestDiscLength)
        poly = []

        isAnyCurve = False
        for edge in wire.Edges:
            #print("type:", type(edge.Curve) in [Part.BSplineCurve, Part.Circle])
            if type(edge.Curve) in [Part.BSplineCurve, Part.Circle]:
                isAnyCurve = True
                break

        if isAnyCurve:
            for point in wire.discretize(numOfPoints):
                point = utils.roundFloatList([point.x, point.y, point.z])
                poly.append(point)
            polylines.append(poly)
        else:
            for edge in wire.Edges:
                polyFromEdge = []
                print("edge line") 
                for point in edge.Vertexes:
                    point = utils.roundFloatList([point.Point.x, point.Point.y, point.Point.z])
                    #print("point", point)
                    polyFromEdge.append(point)
                    #print("edge line:", point) 
                #if (polyFromEdge[0][2] == 0.7):
                    #input("some")
                poly.append(polyFromEdge)
            
            #print("poly:", poly)
            polylines.append(pfc.mergeEdgesInsidePolysRough(sortPolyFromWire(poly)))


###############################################################
        #for edge in wire.Edges:
        #    polyFromEdge = []
        #    if type(edge.Curve) is Part.BSplineCurve:
        #        #print("edge curve") 
        #        #numOfPoints = int(edge.Curve.length() / uc.smallestDiscLength)
        #        #print("edge curve:", edge.Curve.discretize(Number = numOfPoints)) 
        #        #for point in edge.Curve.discretize(numOfPoints):
        #        #    point = utils.roundFloatList([point.x, point.y, point.z])
        #        #    polyFromEdge.append(point)
        #        #    #print("edge curve:", point) 
        #    #else:
        #    #    print("edge line") 
        #    #    for point in edge.Vertexes:
        #    #        point = utils.roundFloatList([point.Point.x, point.Point.y, point.Point.z])
        #    #        polyFromEdge.append(point)
        #    #        #print("edge line:", point) 
        #    #    #if (polyFromEdge[0][2] == 0.7):
        #    #        #input("some")
            
        #    polyFromWire.append(polyFromEdge)
        #print("polyFromWire:", polyFromWire) 
        
        #polylines.append(pfc.mergeEdgesInsidePolysRough(sortPolyFromWire(polyFromWire)))
        #polylines.append(wire.discretize(50))
###################################################################
    print("genPolyFromShape end")
    return polylines


def genOptimizedPart(shape, offsetShape, millDiameter, additionalZHight = 0):
    preprocessedShape = shape#.removeSplitter()# = bmo.preprocess(shape, millDiameter)
    
    #baseOffset = 1
    #offset = baseOffset + millDiameter
    offset = millDiameter

    ##offsetPart = Part.makeSolid(preprocessedShape.makeOffsetShape(offset=offset, tolerance=0.01, inter=True))#, fill=True))
    #solidPrepShape = Part.makeSolid(preprocessedShape.removeSplitter())
    #offsetPart = solidPrepShape.makeOffsetShape(offset=offset, tolerance=0.01, inter=True)
    offsetPart = offsetShape
    bmo.saveModel(offsetPart.exportBrep, "offsetPart.brep")
    print("Done offset!")
    
    minModelHeight = 2
    enlargedBBox, modelThickness = bmo.genEnlargedBBox(preprocessedShape, offset, additionalZHight, minHeight = minModelHeight)
    bmo.saveModel(enlargedBBox.exportBrep, "enlargedBBox.brep")
    
    cutterConfig = uc.getCutterConfig(cutterType = 90, material = "balsa", millDiameter = millDiameter)

    maxCutDepth = float(cutterConfig[0].get("maxDepth"))
    numOfCuts = math.ceil(modelThickness / maxCutDepth)

    crossSectionsList = []
    wholeStructure = []
    maxWorkableDepth = modelThickness - minModelHeight
    layersToMerge = list(range(int(maxCutDepth) * 10, int(maxWorkableDepth * 10), int(maxCutDepth * 10)))
    layersToMerge.append(int(maxWorkableDepth * 10))
    layersToMerge = [float(x) / 10 for x in layersToMerge]

    newBoxHeight = 0.5
    i = 0
    print("layersToMerge:", layersToMerge, "\tmaxCutDepth:", maxCutDepth, "\tmaxWorkableDepth:", maxWorkableDepth)
    for depth in layersToMerge: 
        newBox = bmo.genBaseBoxDiff(enlargedBBox, depth, newBoxHeight)
        bmo.saveModel(newBox.exportBrep, "_" + str(i) + "_newBox.brep")

        #diffBox_OffsetModel = newBox.cut(offsetPart.Solids[0])
        diffBox_OffsetModel = newBox.cut(offsetPart)
        bmo.saveModel(diffBox_OffsetModel.exportBrep, "_" + str(i) + "_diffBox_OffsetModel.brep")
        print("len of Shells:", len(diffBox_OffsetModel.Faces))
        #print(inspect.getmembers(diffBox_OffsetModel.Faces[0]))
        #for face in diffBox_OffsetModel.Faces:
        #    print(face.normalAt(0,0))

        print("--------------------------------------")

        #print(inspect.getmembers(Part.BSplineCurve))
        
        face = genBaseFace(diffBox_OffsetModel)
        bmo.saveModel(face.exportBrep, "_" + str(i) + "_face.brep")
        #print("polyFromShape:", genPolyFromShape(face))
        crossSectionsList.append(genPolyFromShapeRough(face))
        wholeDiff = face.extrude(FreeCAD.Vector(0, 0, maxCutDepth))
        wholeStructure.append(wholeDiff)

        i += 1
    finalStructure = wholeStructure[0]
    i = 1;
    for elem in wholeStructure[1:]:
        #finalStructure = pymesh.boolean(finalStructure, elem, "union")
        finalStructure = finalStructure.fuse(elem)
        print("final structure processing", i, "of", len(wholeStructure) - 1)
        i += 1

    #for polysInLayer in crossSectionsList:
    #    print "+++++++++++++++++++++"
    #    for poly in polysInLayer:
    #        print "$$$$$$$$$$$$$$$$$$$"
    #        print poly
    bmo.saveModel(finalStructure.exportBrep, "finalStructure.brep")
    #crossSectionsList = pfc.mergeEdgesInsidePolys(crossSectionsList)
    #print("crossSectionsList:", crossSectionsList)

    return finalStructure, pfc.crossSectionsToZRough(crossSectionsList)

