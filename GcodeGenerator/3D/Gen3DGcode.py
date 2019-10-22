import sys
sys.path.append('../Common/')

from OffsetCreator import *
import plotly.graph_objects as go
import utils
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

if len(sys.argv) < 3:
    print("not enough arguments provided!")
    quit()

inputStl = os.path.abspath(sys.argv[1])
outputDir = os.path.abspath(sys.argv[2])

millDiameter = float(input("Choose cutter diameter[mm] 1/3/6: "))
if not millDiameter in [1.0, 3.0, 6.0]:
    print("Wrong cutter diameter!") 
    quit()

baseOffset = 1

materialHeight = float(input("Insert material thickness: "))
fillCoefficient = 0.8

#mesh = pymesh.load_mesh("schody_stl_p2_rotated.stl")
#mesh = pymesh.load_mesh("complicatedShape.stl")
mesh = pymesh.load_mesh(inputStl)

mesh = pc.moveToGround(mesh)

bbox = mesh.bbox
print("bbox[0][x]: ", bbox[0][x], "\tbbox[0][y]: ", bbox[0][y],  "\tbbox[1][x]: ", bbox[1][x], "\tbbox[1][y]: ", bbox[1][y])
bbox[0][x] -= (baseOffset + millDiameter * 2 / 3)
bbox[0][y] -= (baseOffset + millDiameter * 2 / 3)
bbox[1][x] += (baseOffset + millDiameter * 2 / 3)
bbox[1][y] += (baseOffset + millDiameter * 2 / 3)


boxMesh = pymesh.generate_box_mesh(bbox[0], bbox[1])
diff = pymesh.boolean(boxMesh, mesh, "difference")

polyCreator = pc.polyFromMeshCreator(diff)
polylinesMap, verticesMap = polyCreator.genPolylines()

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')

#for key, values in polylinesMap.items():
    #print(key, values)
#    for poly in values:
#        for i in range(0, len(poly) - 1):
#            p1 = [verticesMap[key][poly[i]][x], verticesMap[key][poly[i]][y], verticesMap[key][poly[i]][z]]
#            p2 = [verticesMap[key][poly[i+1]][x], verticesMap[key][poly[i+1]][y], verticesMap[key][poly[i+1]][z]]
#            print("p1(", poly[i], ") :", p1, "\tp2(", poly[i+1], ") :", p2)
#            ax.plot([p1[x], p2[x]], [p1[y], p2[y]], [p1[z], p2[z]])

#plt.show()

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
    polylinesCoordMap.update({key : polylineCoord}) 


RWPolys.writePolyCoordsMapIntoFile('MeshOffsetsMap', polylinesCoordMap)

args = ("../CppWorkspace/ToolpathGenerator/build-debug/ToolpathGenerator", str(millDiameter * fillCoefficient))
print("args: ", args)
popen = subprocess.Popen(args, stdout=subprocess.PIPE)
popen.wait()
output = popen.stdout.read()
print(output)

offsetPolygonsMap = RWPolys.readPolysFromFile("dataFromCgal.txt")

gGen.genGcode3D(outputDir + "/gcode.gcode", offsetPolygonsMap, 100, 300)
