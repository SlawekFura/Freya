from OffsetCreator import *
import plotly.graph_objects as go
import utils
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import copy
import polyFromMeshCreator as pc
import pyclipper

#mesh = pymesh.load_mesh("schody_stl_p2_rotated.stl")
mesh = pymesh.load_mesh("complicatedShape.stl")
boxMesh = pymesh.generate_box_mesh(mesh.bbox[0], mesh.bbox[1])
diff = pymesh.boolean(boxMesh, mesh, "difference")

polyCreator = pc.polyFromMeshCreator(diff)
polylinesMap, verticesMap = polyCreator.genPolylines()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

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

coordList = []
for poly in polyVal:
    pointList = []
    for point in poly:
        coord = vertice[point]
        pointList.append(coord)
    coordList.append(pointList)

print(coordList[0])

polylinesCoordMap = {}
for key, polylines in polylinesMap.items():
    vertice = polylinesMap[key]

    polylineCoord = []
    for line in polylines:
        lineCoord = []
        for point in line:
            lineCoord.append(verticesMap[key][point])
        polylineCoord.append(lineCoord)
    polylinesCoordMap.update({key : polylineCoord}) 
#print(polylinesCoordMap)


offsetList = []
#for coordStructure in self.crossSectionsCoords:
print("dupa1")
pco = pyclipper.PyclipperOffset()
print("dupa2")
coordinates_scaled = pyclipper.scale_to_clipper(coordList)
print(coordinates_scaled)
print("dupa3")
for coord in coordinates_scaled:
    pco.AddPath(coord, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDPOLYGON)
print("dupa4")
newCoordinates = pco.Execute(pyclipper.scale_to_clipper(-20))
print("dupa5")
newCoordinatesScaled = pyclipper.scale_from_clipper(newCoordinates)
print("dupa6", newCoordinatesScaled)


offsetCoord = []
for figure in newCoordinatesScaled:
    offsetCoord.append(roundFloatNestedList(figure, 4))

for elem in offsetCoord[0]:
    elem.append(coordStructure[0][z])

offsetCoord[0] = self.joinBeginWithEnd(offsetCoord[0])
offsetLists.append(offsetCoord[0])


