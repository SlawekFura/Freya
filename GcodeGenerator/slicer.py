import numpy as np
import plotly.graph_objects as go
import pymesh
from utils import *
from OffsetCreator import *

#mesh = pymesh.load_mesh("schody_stl_p2_rotated.stl")
mesh = pymesh.load_mesh("schody_stl_p2.stl")
print(mesh.bbox)

fig = go.Figure()


numOfSlices = getNumOfSlices(mesh)
print(numOfSlices)

crossSections = pymesh.slice_mesh(mesh, np.array([0, 0, 1], np.int32), numOfSlices * 3)

zCoordList = genZCoordList(mesh)
print(zCoordList)

#offsetStructuresMap = {}
#[offsetStructuresMap.update({zCoord: None}) for zCoord in zCoordList]
#print(offsetStructuresMap)
zCoordIndex = 0

offsetGen = OffsetGenerator(mesh, 0.1)
coordStructureList = []

#for crossSect in crossSections:
#
#    vertices = roundFloatNestedList(crossSect.vertices, 4)
#    structure = generateStructFromCrossSection(crossSect)
#
#    coordStructure = []
#    [coordStructure.append([vertices[point][x], vertices[point][y], vertices[point][z]]) for point in structure]
#    coordStructureList.append(coordStructure)
#
#    offsetStructure = oc.generateOffset(coordStructure, 0.1)
#
#    fig.add_trace(go.Scatter(x=[point[x] for point in coordStructure], y=[point[y] for point in coordStructure]))
#    fig.add_trace(go.Scatter(x=[point[x] for point in offsetStructure[0]], y=[point[y] for point in offsetStructure[0]]))
#
#    if offsetStructuresMap.get(zCoordList[zCoordIndex]) is None:
#        offsetStructuresMap.update({zCoordList[zCoordIndex] : offsetStructure[0]})
#        #zCoordIndex += 1
#
#    #elif not offsetStructure[0] in offsetStructuresMap.get(zCoordList[zCoordIndex]):
#    elif not sorted(offsetStructure[0]) == sorted(offsetStructuresMap.get(zCoordList[zCoordIndex])):
#        offsetStructuresMap.update({zCoordList[zCoordIndex] : offsetStructure[0]})
#    if round(zCoordList[zCoordIndex], 3) < round(offsetStructure[0][0][z], 3):
#        zCoordIndex += 1
#print(coordStructureList)
#print(offsetGen.crossSectionsCoords)
#print(offsetGen.genOffsetMap())
offsetStructuresMap = offsetGen.genOffsetMap()
for elem in offsetStructuresMap:
    print(elem, offsetStructuresMap.get(elem))
offsetGen.printResults()
#fig.show()

