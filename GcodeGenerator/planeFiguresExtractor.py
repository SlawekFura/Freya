import pymesh
import collections
import numpy
import math

def isFaceOnZPlane(face, vertices):
    return (math.isclose(vertices[face[0]][ZCoord], vertices[face[1]][ZCoord], abs_tol = 0.01) and math.isclose(vertices[face[1]][ZCoord], vertices[face[2]][ZCoord], abs_tol = 0.01))

def arePointsMatching(pointA, pointB):
    return math.isclose(pointA, pointB, abs_tol = 0.01)
        
    
def createFigureFromFaces(trianglesMap):
    genFaces = {}
    for zCoord, triangles in trianglesMap.items():
        print(triangles)
        matchingPoints = []
        i = 0
        for pointA in (triangles[i]):
            for pointB in triangles[i - 1]:
                if arePointsMatching(pointA, pointB):
                    matchingPoints += pointA;
        if len(matchingPoints) == 2:
        tempFaces = {}
        shouldAddToFaces = False
            for point in triangles[i]:
                tempFaces += {zCoord: point}
                if matchingPoints.keys[point]:
                    matchingPoints = []
                    shouldAddToFaces = True

        i += 1

XCoord = 0
YCoord = 1
ZCoord = 2
mesh = pymesh.load_mesh("schody_stl_p2.stl")
vertices = mesh.vertices

zAxisFaceMap = collections.OrderedDict()
dummy = {0.1: [[111, 222]], 0.2: [222, 333]}
dummy[0.1] += [[542, 411]]
print (dummy)
for face in mesh.faces:
    if(isFaceOnZPlane(face, vertices)):
        if (round(vertices[face[0]][ZCoord], 2) in zAxisFaceMap.keys()):
            zAxisFaceMap[round(vertices[face[0]][ZCoord], 2)] += [[face[0], face[1], face[2]]]
        else: 
            zAxisFaceMap[round(vertices[face[0]][ZCoord], 2)] = [[face[0], face[1], face[2]]]

zAxisFaceMap = collections.OrderedDict(sorted(zAxisFaceMap.items()))
#for Z, XY in zAxisFaceMap.items():
#    print (str(Z) + ", " + str(XY))
createFigureFromFaces(zAxisFaceMap)


