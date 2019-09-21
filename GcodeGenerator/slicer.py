import pymesh
import numpy as np
import collections
import math
import plotly.graph_objects as go
from baseStructureGenerator import *
from utils import *

            
mesh = pymesh.load_mesh("schody_stl_p2_rotated.stl")
#mesh = pymesh.load_mesh("schody_stl_p2.stl")
print(mesh.bbox)

fig = go.Figure()
crossSections = pymesh.slice_mesh(mesh, np.array([0, 0, 1], np.int32), 50)
for crossSect in crossSections:

    vertices = roundFloatList(crossSect.vertices, 3)
    structure = generateStructFromCrossSection(crossSect)
    
    coordStructure = []
    [coordStructure.append([vertices[point][x], vertices[point][y]]) for point in structure]
    
    offsetStructure = oc.generateOffset(coordStructure, 0.8)
    print(coordStructure)
    print(offsetStructure[0])

    offsetStructureDataX = []
    offsetStructureDataY = []
    for point in offsetStructure[0]:
        offsetStructureDataX.append(point[x])
        offsetStructureDataY.append(point[y])
 
    fig.add_trace(go.Scatter(x=[point[x] for point in coordStructure], y=[point[y] for point in coordStructure]))
    fig.add_trace(go.Scatter(x=offsetStructureDataX, y=offsetStructureDataY))

fig.show()

