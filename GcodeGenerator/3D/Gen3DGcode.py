import sys
sys.path.append('../Common/')
sys.path.append('./OptimizedMesh/')

import plotly.graph_objects as go
from utils import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import copy
import polyFromMeshCreator as pc
import pyclipper
import os
import ReadWritePolysFromFile as RWPolys
import subprocess
import GcodeCommandGenerator as gGen
import pymesh
import genOptimizedMesh as gom
import offsetMesh as om

if len(sys.argv) < 3:
    print("not enough arguments provided!")
    quit()

inputFreecadFile = os.path.abspath(sys.argv[1])

print("inputFreecadFile:", inputFreecadFile)
outputDir = os.path.abspath(sys.argv[2])
optimization = ""
print("input mesh:", inputFreecadFile)
print("output directory:", outputDir)

if len(sys.argv) > 3:
    optimization = sys.argv[3]

isOptimizitationOn = True if optimization == "-opt" else False
print("Optimization set to:", isOptimizitationOn)

millDiameter = float(input("Choose cutter diameter[mm] 1/3/6.35: "))
if not millDiameter in [1.0, 3.0, 6.35]:
    print("Wrong cutter diameter!") 
    quit()

baseOffset = 1

materialHeight = float(input("Insert material thickness: "))
fillCoefficient = 0.8

#mesh = pymesh.load_mesh("schody_stl_p2_rotated.stl")
#mesh = pymesh.load_mesh("complicatedShape.stl")

baseMeshPath = os.path.abspath("./Generated/BaseMesh.stl")
print("baseMeshPath:", baseMeshPath) 
zeroOffsetting = 0
om.generateMeshOffsetFile(inputFreecadFile, zeroOffsetting, baseMeshPath)
mesh = pymesh.load_mesh(baseMeshPath)
mesh = pc.moveToGround(mesh)
pymesh.save_mesh("mesh.stl", mesh, ascii=True);

bbox = mesh.bbox
bbox[0][x] -= (baseOffset + millDiameter)
bbox[0][y] -= (baseOffset + millDiameter)
bbox[1][x] += (baseOffset + millDiameter)
bbox[1][y] += (baseOffset + millDiameter)

optimisedCutOutMesh, meshCrossSectionOptimised = gom.genOptimizedMesh(baseMeshPath, inputFreecadFile, millDiameter)

boxMesh = pymesh.generate_box_mesh(bbox[0], bbox[1])
print("dupa2!")
#diff = pymesh.boolean(boxMesh, mesh, "difference")
#diff = pymesh.boolean(diff, optimisedCutOutMesh, "difference")

diff = pymesh.boolean(boxMesh, mesh, "difference")
diff = pymesh.boolean(diff, optimisedCutOutMesh, "difference")
pymesh.save_mesh("diff.stl", diff, ascii=True);
halfDiff = pymesh.boolean(diff, pymesh.generate_box_mesh([bbox[0][x], (bbox[1][y] + bbox[0][y])/2, bbox[0][z]], bbox[1]), "difference")
pymesh.save_mesh("halfDiff.stl", halfDiff, ascii=True);
print("dupa3!")

minSliceThickness = 1.3
maxSliceThickness = 4.0
polyCreator = pc.polyFromMeshCreator(diff, minSliceThickness, maxSliceThickness)

print("poly Created!")
polylinesMap, verticesMap = polyCreator.genPolylines()

keys = polylinesMap.keys()
key = list(keys)[0]
polyVal = polylinesMap[key]
vertice = verticesMap[key]

polylinesCoordMap = {}
for key, polylines in polylinesMap.items():
    vertice = polylinesMap[key]

    polylineCoord = []
    for line in polylines:
        lineCoord = []
        for point in line:
            lineCoord.append(verticesMap[key][point])
        line.append(line[0])
        polylineCoord.append(lineCoord)
    polylinesCoordMap.update({key : polyCreator.removeDuplicates(polylineCoord)})


RWPolys.writePolyCoordsMapIntoFile('MeshOffsetsMap', polylinesCoordMap)

args = ("../CppWorkspace/ToolpathGenerator/build-debug/ToolpathGenerator", str(millDiameter * fillCoefficient))
#args = ("/home/slawek/workspace/CppWorkspace/ToolpathGenerator/build-debug/ToolpathGenerator", str(millDiameter * fillCoefficient))
print("args: ", args)
popen = subprocess.Popen(args, stdout=subprocess.PIPE)
popen.wait()
output = popen.stdout.read()
print(output)

offsetPolygonsMap = RWPolys.readPolysFromFile("dataFromCgal.txt")

gGen.genGcode3D(outputDir + "/gcode.gcode", offsetPolygonsMap, 100, 300)
