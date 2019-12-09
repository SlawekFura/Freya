import sys
import os

# add folder containing FreeCAD.pyd, FreeCADGui.pyd to sys.path
sys.path.append("/usr/lib/freecad/lib") # example for Linux
sys.path.append('../../Common/')
import ReadWritePolysFromFile as RWPolys

import FreeCAD
import FreeCADGui  
import Part
import inspect
import Mesh
import MeshPart
from FreeCAD import Base
import baseModelOperations as bmo
#import utilsConfig as uc
import genOptimizedPart as gop
import polyFromFaceCreator as pfc
#import GcodeCommandGenerator as gGen

inputPart = sys.argv[1]
millDiameter = float(sys.argv[2])
outputStl = sys.argv[3]
additionalZHigh = 0
print("inputPart:", inputPart)


doc = FreeCAD.openDocument(inputPart)
partFeature = doc.getObjectsByLabel("PartToOffset")[0]

mutableShape = partFeature.Shape.copy()


bbox = bmo.genEnlargedBBox(mutableShape)[0]
diff = bbox.cut(mutableShape)
bmo.saveModel(diff.exportBrep, "diff.brep")

optimizedPart, crossSecOptimized = gop.genOptimizedPart(mutableShape, millDiameter, additionalZHigh)

polylinesCoordMap = pfc.genPolyFromFaces(mutableShape, 0.5, 0.8)

polylinesCoordMap = pfc.genPolyFromFaces(crossSecOptimized, 0.5, 0.8)

RWPolys.writePolyCoordsMapIntoFile('MeshOffsetsMap', polylinesCoordMap)

offsetPolygonsMap = RWPolys.readPolysFromFile("../../3D/dataFromCgal.txt")

#args = ("../CppWorkspace/ToolpathGenerator/build-debug/ToolpathGenerator", str(millDiameter * fillCoefficient))
##args = ("/home/slawek/workspace/CppWorkspace/ToolpathGenerator/build-debug/ToolpathGenerator", str(millDiameter * fillCoefficient))
#print("args: ", args)
#popen = subprocess.Popen(args, stdout=subprocess.PIPE)
#popen.wait()
#output = popen.stdout.read()
#print(output)

offsetPolygonsMap = RWPolys.readPolysFromFile("dataFromCgal.txt")

gGen.genGcode3D(outputDir + "/gcode.gcode", offsetPolygonsMap, 100, 300)
