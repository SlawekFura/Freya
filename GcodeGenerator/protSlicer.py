from OffsetCreator import *
import plotly.graph_objects as go
import utils
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import copy
import polyFromMeshCreator as pc

#mesh = pymesh.load_mesh("schody_stl_p2_rotated.stl")
mesh = pymesh.load_mesh("complicatedShape.stl")
boxMesh = pymesh.generate_box_mesh(mesh.bbox[0], mesh.bbox[1])
diff = pymesh.boolean(boxMesh, mesh, "difference")

polyCreator = pc.polyFromMeshCreator(diff)
polylines, verticesMap = polyCreator.genPolylines()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for key, values in polylines.items():
    #print(key, values)
    for poly in values:
        for i in range(0, len(poly) - 1):
            p1 = [verticesMap[key][poly[i]][x], verticesMap[key][poly[i]][y], verticesMap[key][poly[i]][z]]
            p2 = [verticesMap[key][poly[i+1]][x], verticesMap[key][poly[i+1]][y], verticesMap[key][poly[i+1]][z]]
            print("p1(", poly[i], ") :", p1, "\tp2(", poly[i+1], ") :", p2)
            ax.plot([p1[x], p2[x]], [p1[y], p2[y]], [p1[z], p2[z]])

plt.show()
