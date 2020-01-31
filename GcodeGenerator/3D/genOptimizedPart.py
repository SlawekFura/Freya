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

def sortPolyFromWire(edges):
    #print("edges", edges)
    newPoly = [edges[0]]
    edges.remove(edges[0])

    while len(edges) > 0:
        newEdge = []
        flag = False
        for edge in edges:
            lastPointOfLastEdge = newPoly[-1][-1]

            if uc.match2FloatLists(lastPointOfLastEdge, edge[0]):
                edges.remove(edge)
                newPoly.append(edge)
                flag = True
            if uc.match2FloatLists(lastPointOfLastEdge, edge[-1]):
                edges.remove(edge)
                edge.reverse()
                print("reverse after", edge)
                newPoly.append(edge)
                flag = True
        if not flag:
            input("asdsad")

    return newPoly
        

def genPolyFromShape(face):
    #print("genPolyFromShape begin")
    polylines = []
    for wire in face.Wires:
        polyFromWire = []
        #print("polyFromWire AAAA") 
        #for edge in wire.Edges:
        #    polyFromEdge = []
        #    if type(edge.Curve) is Part.BSplineCurve:
        #        numOfPoints = int(edge.Curve.length() / uc.smallestDiscLength)
        #        for point in edge.Curve.discretize(numOfPoints):
        #            point = utils.roundFloatList([point.x, point.y, point.z])
        #            polyFromEdge.append(point)
        #            #print("edge curve:", point) 
        #    else:
        #        for point in edge.Vertexes:
        #            point = utils.roundFloatList([point.Point.x, point.Point.y, point.Point.z])
        #            polyFromEdge.append(point)
        poly = []

        multiplier = 1 
        minNumOfPoints = 4
        #numOfPoints = 0
        numOfPoints = int(wire.Length / uc.smallestDiscLength)
        if numOfPoints < minNumOfPoints:
            continue
        #while numOfPoints < minNumOfPoints:
        #    numOfPoints = int(wire.Length / uc.smallestDiscLength * multiplier)
        #    multiplier += 2
        #print("wireLength", wire.Length, "num of points", numOfPoints)
        numOfPoints *= multiplier
        for point in wire.discretize(numOfPoints):
            point = utils.roundFloatList([point.x, point.y, point.z], 3)
            poly.append(point)
        polylines.append(poly)

    return polylines

def genPolyFromShapeRough(face):
    polylines = []
    for wire in face.Wires:
        numOfPoints = int(wire.Length / uc.smallestDiscLength)
        poly = []

        isAnyCurve = True
        #isAnyCurve = False
        #for edge in wire.Edges:
        #    #print("type:", type(edge.Curve) in [Part.BSplineCurve, Part.Circle])
        #    if type(edge.Curve) in [Part.BSplineCurve, Part.Circle]:
        #        isAnyCurve = True
        #        break

        if isAnyCurve:
            for point in wire.discretize(numOfPoints):
                point = utils.roundFloatList([point.x, point.y, point.z])
                poly.append(point)
            polylines.append(poly)
        else:
            for edge in wire.Edges:
                polyFromEdge = []
                for point in edge.Vertexes:
                    point = utils.roundFloatList([point.Point.x, point.Point.y, point.Point.z])
                    #print("point", point)
                    polyFromEdge.append(point)
                    #print("edge line:", point) 
                #if (polyFromEdge[0][2] == 0.7):
                    #input("some")
                poly.append(polyFromEdge)
            
            polylines.append(pfc.mergeEdgesInsidePolysRough(sortPolyFromWire(poly)))
    return polylines


def genOptimizedPart(shape, offsetShape, millDiameter, additionalZHight = 0):
    preprocessedShape = shape
    
    baseOffset = 0.1
    offset = baseOffset + 2 * millDiameter
    #offset = millDiameter

    ##offsetPart = Part.makeSolid(preprocessedShape.makeOffsetShape(offset=offset, tolerance=0.01, inter=True))#, fill=True))
    #solidPrepShape = Part.makeSolid(preprocessedShape.removeSplitter())
    #offsetPart = solidPrepShape.makeOffsetShape(offset=offset, tolerance=0.01, inter=True)
    offsetPart = offsetShape
    bmo.saveModel(offsetPart.exportBrep, "offsetPart.brep")
    
    minModelHeight = 0
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

    bmo.saveModel(finalStructure.exportBrep, "finalStructure.brep")

    return finalStructure, pfc.crossSectionsToZRough(crossSectionsList)

