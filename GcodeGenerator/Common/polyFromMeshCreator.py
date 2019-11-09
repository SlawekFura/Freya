from OffsetCreator import *
import plotly.graph_objects as go
import utils
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import copy



class polyFromMeshCreator:
    def __init__(self, mesh, minSliceThickness):
        self.mesh = mesh
        self.numOfSlices = getNumOfSlices(self.mesh, minSliceThickness)
        print("numOfSlices: ", self.numOfSlices)
        self.crossSections = pymesh.slice_mesh(mesh, np.array([0, 0, 1], np.int32), self.numOfSlices * 1)
        self.zCoordList = genZCoordList(mesh)
        print(self.zCoordList)
        self.vertices = roundFloatNestedList(mesh.vertices.tolist(), 4)
        self.trianglesToZMap, self.verticesMap = self.mapTrianglesToZ()
        self.linesMap = self.getLinesMapFromZMap()
        

    def mapTrianglesToZ(self):
        trianglesToZMap = {}
        #for triangle in self.mesh.faces:
        #print("crossSec: ", self.crossSections)
        #print("selfMesh: ", self.mesh.faces)

        prevVertices = []
        verticesMap = {}
        crossSectToZ = {}
        for mesh in self.crossSections:
            vertices = roundFloatNestedList(mesh.vertices.tolist(), 4)
            key = vertices[mesh.faces[0][0]][z]
            val = mesh.faces.tolist()
            crossSectToZ.update({key : val})
            verticesMap.update({key : vertices})
            
        return crossSectToZ, verticesMap

    def getLinesMapFromZMap(self):
        linesList = {}
        for key, triangles in self.trianglesToZMap.items():
            linesPerLayer = []
            for triangle in triangles:
                for i in range(-1, len(triangle) -1):
                    line = [triangle[i], triangle[i+1]]
                    linesPerLayer.append(line)    
            
            linesList.update({key : linesPerLayer})
            linesList[key] = self.filterInnerLines(linesList[key])
        return linesList
    
    def filterInnerLines(self, linesList):
        for line in list(linesList):
            numOfRepetitions = linesList.count(line) + linesList.count(line.reverse())
            if numOfRepetitions > 1:
                linesList = list(filter((line.reverse()).__ne__, filter((line).__ne__, linesList)))
        return linesList
    
    def genPolylines(self):
        polyMap = {}
    
        for key, values in self.linesMap.items():
            linesList = list(values)
            polylines = [list(linesList[0][1:])]
            linesList.remove(linesList[0])
            for polyline in polylines:
                token = True
                while(token):
                    token = False
                    for lineIt in reversed(linesList):
                        line = copy.deepcopy(lineIt)
                        if polyline[0] == line[0]:
                            polyline.insert(0, line[1])
                        elif polyline[-1] == line[0]:
                            polyline.append(line[1])
                        elif polyline[0] == line[1]:
                            polyline.insert(0, line[0])
                        elif polyline[-1] == line[1]:
                            polyline.append(line[0])
                        else:
                            continue
                        linesList.remove(line)
                        token = True
                if linesList:
                    polylines.append(list(linesList[0][1:]))
                    linesList.remove(linesList[0])
            polyMap.update({key : polylines})
        return polyMap, self.verticesMap
 
def moveToGround(mesh):
    maxZCoord = mesh.bbox[1][z]
    print("maxZ: ", maxZCoord)
    #return pymesh.form_mesh(mesh.vertices + [[0, 0, 0]], mesh.faces)
    return pymesh.form_mesh(mesh.vertices + [[0, 0, -maxZCoord]], mesh.faces)
    #return pymesh.form_mesh(mesh.vertices, mesh.faces)
