import sys
import os

# add folder containing FreeCAD.pyd, FreeCADGui.pyd to sys.path
sys.path.append("/usr/lib/freecad/lib") # example for Linux
sys.path.append('../Common/')
import ReadWritePolysFromFile as RWPolys

import FreeCAD
import FreeCADGui  
import Part
import inspect
import Mesh
import MeshPart
from FreeCAD import Base
import baseModelOperations as bmo
import utilsConfig as uc
import genOptimizedPart as gop
import polyFromFaceCreator as pfc
import baseModelOperations as bmo
#import GcodeCommandGenerator as gGen

if len(sys.argv) < 3:
    print("not enough arguments provided!")
    quit()


inputPart = os.path.abspath(sys.argv[1])
outputDir = os.path.abspath(sys.argv[2])


print("inputPart:", inputPart)
print("output directory:", outputDir)

additionalZHigh = 0.0
if len(sys.argv) > 3:
    additionalZHigh = float(sys.argv[3])
    optimization = sys.argv[3]

#isOptimizitationOn = True if optimization == "-opt" else False
#print("Optimization set to:", isOptimizitationOn)

millDiameter = float(input("Choose cutter diameter[mm] 1/3/6.35: "))
if not millDiameter in [1.0, 3.0, 6.35]:
    print("Wrong cutter diameter!") 
    quit()

doc = FreeCAD.openDocument(inputPart)
partFeature = doc.getObjectsByLabel("Part")[0]
partFeatureOffset = doc.getObjectsByLabel("OffsetPart")[0]

mutableShape = partFeature.Shape.copy()
mutableOffsetShape = partFeatureOffset.Shape.copy()

mutableShape, mutableOffsetShape = bmo.moveToBase(mutableShape, mutableOffsetShape, 2.0 * millDiameter)

bmo.setSavingPrefix("Rough")

optimizedPart, roughProcessingCoordMap = gop.genOptimizedPart(mutableShape, mutableOffsetShape, millDiameter, additionalZHigh)
offset = millDiameter * 0.8
print "------------Gen rough gcode ------------------"
uc.genGcodeFromCoordMap(roughProcessingCoordMap, outputDir + "/rough.gcode", offset, millDiameter)

bmo.setSavingPrefix("Final")

finalOptimized = mutableShape.fuse(optimizedPart)
#finalOptimized = mutableShape
bmo.saveModel(optimizedPart.exportBrep, "optimizedPart_next.brep")
bmo.saveModel(mutableShape.exportBrep, "mutable.brep")
bmo.saveModel(finalOptimized.exportBrep, "finalOptimized.brep")

finalProcessingCoordMap = pfc.genPolyFromFaces(finalOptimized, 0.5, 0.8)
print "------------Gen finish gcode ------------------"
uc.genGcodeFromCoordMap(finalProcessingCoordMap, outputDir + "/finish.gcode", offset, millDiameter, optimization = True)
