import sys
import os

# add folder containing FreeCAD.pyd, FreeCADGui.pyd to sys.path
sys.path.append("/usr/lib/freecad/lib") # example for Linux

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

inputPart = sys.argv[1]
millDiameter = float(sys.argv[2])
outputStl = sys.argv[3]
additionalZHigh = 0
print("inputPart:", inputPart)


doc = FreeCAD.openDocument(inputPart)
partFeature = doc.getObjectsByLabel("PartToOffset")[0]

mutableShape = partFeature.Shape.copy()

optimizedPart = gop.genOptimizedPart(mutableShape, millDiameter, additionalZHigh)



dirSlice = Base.Vector(0,0,-1)
print(partFeature.Shape.slice(dirSlice, 5))

scriptPath = os.getcwd()
#print(partFeature, inspect.getmembers(type(partFeature)))
#newPart = None
#minLength = 0.3
#maxLength = 0.4
#if (offset > 0.001):
#    newPart = partFeature.Shape.makeOffsetShape(offset=offset, tolerance=0.05)
#else:
#    MeshPart.meshFromShape(partFeature.Shape, minLength, maxLength).write(outputStl)
#    exit()
#print("Saving mesh", inputPart)
#print(partFeature.getTopoShape())#slice([0,0,-1], 2))
#MeshPart.meshFromShape(newPart, minLength, maxLength).write(outputStl)
