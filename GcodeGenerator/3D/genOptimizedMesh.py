import pymesh
import sys
sys.path.append('../Common/')
sys.path.append("/usr/lib/freecad/lib") # example for Linux
import polyFromMeshCreator as pc
import numpy as np
from meshpy import geometry
from meshpy.tet import MeshInfo, build
import math
import xml.etree.ElementTree as ET
from utils import *
import ReadWritePolysFromFile as RWPolys
import os
import subprocess

def moveAllVertices(mesh, moveValVec):
    return pymesh.form_mesh(mesh.vertices + moveValVec, mesh.faces)

baseOffset = 1
millDiameter = 3

meshFile = "../../Projekt/szkola/Podstawa/Drzewka/drzewko1_meshed.stl"
mesh = pymesh.load_mesh(meshFile)
mesh = pc.moveToGround(mesh)
pymesh.save_mesh(meshFile, mesh, ascii=True);

offset = baseOffset + millDiameter
python3_command = "python " + os.path.abspath("../3rdPartyScripts/freecadApi/freecadOffset.py") + " " + os.path.abspath(meshFile) + "  " + str(offset)  # launch your python2 script using bash
process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()  # receive output from the python2 script

bbox = mesh.bbox
xMin = bbox[0][0]
yMin = bbox[0][1]
zMin = bbox[0][2]

xMax = bbox[1][0]
yMax = bbox[1][1]
zMax = bbox[1][2]

bbox[0][0] -= (baseOffset + millDiameter)
bbox[0][1] -= (baseOffset + millDiameter)
bbox[1][0] += (baseOffset + millDiameter)
bbox[1][1] += (baseOffset + millDiameter)

root = ET.parse("../Configs/tools/Cutters.xml").getroot()
cutterConfig = root.findall("type_"      + str(90) + 
                            "/"          + "balsa" + 
                            "/diameter_" + str(6.35) +
                            "/params")
maxCutDepth = float(cutterConfig[0].get("maxDepth"))
materialThickness = abs(zMax - zMin)
numOfCuts = math.ceil(materialThickness / maxCutDepth)

minHeight = 3
if (materialThickness < (maxCutDepth + minHeight)):
    print("No optimization due to not enough material thickness")

boxMesh = pymesh.generate_box_mesh(bbox[0], bbox[1])
diff = pymesh.boolean(boxMesh, mesh, "difference")

halfBox = pymesh.generate_box_mesh([bbox[0][x], bbox[0][y], bbox[0][z]],  [(bbox[1][x] + bbox[0][x])/2, bbox[1][y], bbox[1][z]])

newBox = pymesh.generate_box_mesh([bbox[0][x], bbox[0][y], bbox[0][z] + (bbox[1][z] - bbox[0][z])*2/3],  [bbox[1][x], bbox[1][y], bbox[0][z] + (bbox[1][z] - bbox[0][z])*2/3 + 1])
pymesh.save_mesh("newBox.stl", newBox, ascii=True);


#pymesh.save_mesh("scaledMesh.stl", scaledMesh, ascii=True);
#pymesh.save_mesh("mesh.stl", mesh, ascii=True);
#
#pDiff = pymesh.boolean(newBox, mesh, "difference")
##pDiff = pymesh.boolean(newBox, scaledMesh, "difference")
#for i in range(0,4):
#    pDiff = pymesh.boolean(pDiff, moveAllVertices(pDiff, [0, 0, 1]), "union")
#pymesh.save_mesh("pDiff.stl", pDiff, ascii=True);
#
#genMesh = pymesh.boolean(diff, pDiff, "difference")
#pymesh.save_mesh("genMesh.stl", genMesh, ascii=True);
#print("dupa2!")
#
#genHalfMesh = pymesh.boolean(genMesh, halfBox, "difference")
##genHalfMesh, inf = pymesh.remove_degenerated_triangles(genHalfMesh, 10)
#pymesh.save_mesh("genHalfMesh.stl", genHalfMesh, ascii=True);
#
#selfIntMesh = pymesh.resolve_self_intersection(genHalfMesh)
##genHalfMesh, inf = pymesh.remove_degenerated_triangles(genHalfMesh, 10)
#pymesh.save_mesh("selfIntMesh.stl", selfIntMesh, ascii=True);
#
#tetterdMesh = pymesh.tetrahedralize(selfIntMesh, 0.5)
#pymesh.save_mesh("tetteredMesh.stl", tetterdMesh, ascii=True);


print("dupa3!")
##
##minReso = 10.0
##maxReso = 4.0
##sliced = pymesh.slice_mesh(mesh, np.array([0, 0, 1], np.int32), 1)
##
##polyCreator = pc.polyFromMeshCreator(genMesh, minReso, maxReso)
##print("dupa4!")
##print("poly Created!")
##polylinesMap, verticesMap = polyCreator.genPolylines()
##
##keys = polylinesMap.keys()
##key = list(keys)[0]
##polyVal = polylinesMap[key]
##vertice = verticesMap[key]
##
##polylinesCoordMap = {}
##for key, polylines in polylinesMap.items():
##    vertice = polylinesMap[key]
##
##    polylineCoord = []
##    for line in polylines:
##        lineCoord = []
##        for point in line:
##            lineCoord.append(verticesMap[key][point])
##        line.append(line[0])
##        polylineCoord.append(lineCoord)
##    polylinesCoordMap.update({key : polylineCoord}) 
##
##
##RWPolys.writePolyCoordsMapIntoFile('MeshOffsetsMap', polylinesCoordMap)

