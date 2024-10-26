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

def genMergedStructureAndCrossSectionsList():
    i = 0
    crossSectionsList = []
    wholeStructure = []
    print("layersToMerge:", layersToMerge, "\tmaxCutDepth:", maxCutDepth, "\tmaxWorkableDepth:", maxWorkableDepth)
    for depth in layersToMerge: 
        newBox = bmo.genBaseBoxDiff(enlargedBBox, depth, newBoxHeight)
        bmo.saveModel(newBox.exportBrep, "_" + str(i) + "_newBox.brep")

        diffBox_OffsetModel = newBox.cut(offsetPart.Solids[0])
        bmo.saveModel(diffBox_OffsetModel.exportBrep, "_" + str(i) + "_diffBox_OffsetModel.brep")

        crossSectionsList.append(genMeshWithFilteredBasePart(pDiff))
    
    return wholeStructure, crossSectionsList

def genBaseFace(shape):
    facesWithNormalZ = None
    lowestZ = 0
    for face in shape.Faces:
        if (face.normalAt(0,0)[2] in [-1,1] and face.Vertexes[0].Z < lowestZ):
            lowestZ = face.Vertexes[0].Z
            facesWithNormalZ = face

    return facesWithNormalZ

def genPolyFromWires(wires):
    polys = []
    for wire in wires:
        polyFromEdge
        if type(edge.Curve) is Part.BSplineCurve:
            numOfPoints = int(edge.Curve.length() / uc.smallestDiscLength)
            for point in edge.Curve.discretize(numOfPoints):
                point = utils.roundFloatList([point.x, point.y, point.z])
                polyFromEdge.append(point)
        else:
            for point in edge.Vertexes:
                point = utils.roundFloatList([point.Point.x, point.Point.y, point.Point.z])
                polyFromEdge.append(point)
    return polys

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

def genPolyFromShape(face):
    polylines = []
    for wire in face.Wires:
        polyFromWire = []
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
            polyFromWire.append(polyFromEdge)
        polylines.append(polyFromWire)

    #for poly in polylines:
    #    print "\nbefore:"
    #    print poly
    for polyFromWires in polylines:
        #polyFromWires = reorientePolys(polyFromWires)
        for poly in polyFromWires[1:]:
            prevPoly = polyFromWires[polyFromWires.index(poly) - 1]
            if uc.match2FloatLists(prevPoly[-1], poly[0]):
                continue
            elif uc.match2FloatLists(prevPoly[0], poly[0]):
                prevPoly = prevPoly.reverse()
            elif uc.match2FloatLists(prevPoly[-1], poly[-1]):
                poly = poly.reverse()
            elif uc.match2FloatLists(prevPoly[0], poly[-1]):
                prevPoly = prevPoly.reverse()
                poly = poly.reverse()

    #for poly in polylines:
    #    print "\nafter:"
    #    print poly

    return polylines

def genOptimizedPart(shape, millDiameter, additionalZHight = 0):
    preprocessedShape = bmo.preprocess(shape, millDiameter)
    
    baseOffset = 1
    offset = baseOffset + millDiameter

    offsetPart = Part.makeSolid(preprocessedShape.makeOffsetShape(offset=offset, tolerance=0.01, join = True, fill = True))
    bmo.saveModel(offsetPart.exportBrep, "offsetPart.brep")
    
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

        diffBox_OffsetModel = newBox.cut(offsetPart.Solids[0])
        bmo.saveModel(diffBox_OffsetModel.exportBrep, "_" + str(i) + "_diffBox_OffsetModel.brep")
        print("len of Shells:", len(diffBox_OffsetModel.Faces))
        #print(inspect.getmembers(diffBox_OffsetModel.Faces[0]))
        #for face in diffBox_OffsetModel.Faces:
        #    print(face.normalAt(0,0))

        print("--------------------------------------")

        #print(inspect.getmembers(Part.BSplineCurve))
        
        face = genBaseFace(diffBox_OffsetModel)
        bmo.saveModel(face.exportBrep, "_" + str(i) + "_face.brep")
        crossSectionsList.append(genPolyFromShape(face))
        wholeDiff = face.extrude(FreeCAD.Vector(0, 0, maxCutDepth))
        wholeStructure.append(wholeDiff)

        i += 1
    finalStructure = wholeStructure[0]
    i = 1;
    #for elem in wholeStructure[1:]:
    #    #finalStructure = pymesh.boolean(finalStructure, elem, "union")
    #    finalStructure = finalStructure.fuse(elem)
    #    print("final structure processing", i, "of", len(wholeStructure) - 1)
    #    i+=1

    bmo.saveModel(finalStructure.exportBrep, "finalStructure.brep")


    return finalStructure, crossSectionsList

