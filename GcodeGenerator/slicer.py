import pymesh
import numpy as np
import collections
import math
import plotly.graph_objects as go
from baseStructureGenerator import *

            
mesh = pymesh.load_mesh("schody_stl_p2_rotated.stl")
#mesh = pymesh.load_mesh("schody_stl_p2.stl")

fig = go.Figure()
crossSections = pymesh.slice_mesh(mesh, np.array([0, 0, 1], np.int32), 2)
for crossSect in crossSections:

    structure = generateStructFromCrossSection(crossSect)
    
    vertices = [[float('%.3f' % coord) for coord in elem] for elem in crossSect.vertices]
    structure = removeDoubledPoints(structure, vertices)

    structure = removePointsOnSameLine(structure, vertices)
    coordStructure = []
    [coordStructure.append([vertices[point][x], vertices[point][y]]) for point in structure]
    print(coordStructure)
    
    #print(coordStructure)
    #offsetStructure = oc.generateOffset(coordStructure, 5.0)
    offsetStructure = oc.generateOffset(coordStructure, 0.8)
    print(offsetStructure)

    offsetStructureDataX = []
    offsetStructureDataY = []
    for point in offsetStructure[0]:
        offsetStructureDataX.append(point[x])
        offsetStructureDataY.append(point[y])
 
    print(offsetStructureDataX)
    print(offsetStructureDataY)
    fig.add_trace(go.Scatter(x=[point[x] for point in coordStructure], y=[point[y] for point in coordStructure]))
    fig.add_trace(go.Scatter(x=offsetStructureDataX, y=offsetStructureDataY))

fig.show()

