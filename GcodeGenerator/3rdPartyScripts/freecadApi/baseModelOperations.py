import FreeCAD
import Part
from FreeCAD import Base
import inspect
import utilsConfig as uc
import polyFromFaceCreator as pmc


def saveModel(savingFunction, savingName):
    savingFunction("./Generated/_" + str(uc.numOfSavedModels) + "_" + savingName)
    uc.numOfSavedModels += 1

def moveToBase(shape, offset):
    shape = shape.copy()

    maxZ = shape.BoundBox.ZMax

    maxX = shape.BoundBox.XMax
    minX = shape.BoundBox.XMin

    maxY = shape.BoundBox.YMax
    minY = shape.BoundBox.YMin
    print("biggest model Z coordinate before move:", maxZ)

    #print(inspect.getmembers(shape.Solids[0]))
    #print(inspect.getmembers(shape.Solids[0].BoundBox))
    shape.translate(Base.Vector(-(maxX - minX)/2, -(maxY - minY)/2 + offset, -maxZ))
    print("biggest model Z coordinate after move::", shape.BoundBox.ZMax)

    saveModel(shape.exportBrep, "moveToBase.brep")
    return shape

def genEnlargedBBox(shape, enlargeBy = 0, additionalSpaceToCutOut = 0 , minHeight = 0):
    shape.tessellate(2)
    print("Max:", shape.BoundBox.XMax, "\tMin:", shape.BoundBox.XMin)
    basePoint = Base.Vector(shape.BoundBox.XMin - enlargeBy, shape.BoundBox.YMin - enlargeBy, shape.BoundBox.ZMin + minHeight)
    baseVector = Base.Vector(0, 0, 1)
    shapeThickness = shape.BoundBox.ZLength + additionalSpaceToCutOut - minHeight
    if (shapeThickness < minHeight):
        print("No optimization due to not enough material thickness")
    return Part.makeBox(shape.BoundBox.XLength + 2 * enlargeBy,
                        shape.BoundBox.YLength + 2 * enlargeBy,
                        shapeThickness, basePoint, baseVector), shapeThickness

def genBaseBoxDiff(shape, zOffset, height):
    shape.tessellate(1)
    bbox = shape.BoundBox
    basePoint = Base.Vector(bbox.XMin, bbox.YMin, bbox.ZMax - zOffset)
    baseVector = Base.Vector(0, 0, 1)
    return Part.makeBox(bbox.XLength, bbox.YLength, height, basePoint, baseVector)

def genBBox(shape):
    shape.tessellate(1)
    return shape.BoundBox

def preprocess(shape, offset):
    shape = moveToBase(shape, offset)
    return shape
