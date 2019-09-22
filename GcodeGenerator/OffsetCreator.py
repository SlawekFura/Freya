import math
import pyclipper
from utils import *
from baseStructureGenerator import *
import pymesh
import numpy as np
import plotly.graph_objects as go

def generateOffset(vertStructure, offset):
    pco = pyclipper.PyclipperOffset()
    coordinates_scaled = pyclipper.scale_to_clipper(vertStructure)
    pco.AddPath(coordinates_scaled, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDPOLYGON)
    new_coordinates = pco.Execute(pyclipper.scale_to_clipper(offset))
    new_coordinates_scaled = pyclipper.scale_from_clipper(new_coordinates)


    offsetCoord = []
    for figure in new_coordinates_scaled:
        offsetCoord.append(roundFloatNestedList(figure, 4))

    for elem in offsetCoord[0]:
        elem.append(vertStructure[0][z])

    return offsetCoord

class OffsetGenerator:
    def __init__(self, mesh, offset):
        self.mesh = mesh
        self.numOfSlices = getNumOfSlices(self.mesh)
        self.crossSections = pymesh.slice_mesh(mesh, np.array([0, 0, 1], np.int32), self.numOfSlices * 3)
        self.crossSectionsCoords = self.genCrossSectionsCoords()
        self.offset = offset
        self.zCoordList = genZCoordList(mesh)
        self.offsetStructure = self.generateOffsetList()
        self.zCoordIndex = 0
        print(self.crossSectionsCoords)
        print("dupa")

    def genOffsetMap(self):
        offsetStructureMap = {}
        [offsetStructureMap.update({zCoord: None}) for zCoord in self.zCoordList]
        #for elem in self.offsetStructure:
        #    print("offsetStructure: ", elem)
        for offsetStruct in self.offsetStructure:
            print("offsetStructure: ", offsetStruct)

            print("self: ",self.zCoordList[self.zCoordIndex], "\toffset: ", offsetStruct[0][z])
            if offsetStructureMap.get(self.zCoordList[self.zCoordIndex]) is None:
                offsetStructureMap.update({self.zCoordList[self.zCoordIndex] : offsetStruct})
                print("dupa 1")
            elif not sorted(offsetStruct[0]) == sorted(offsetStructureMap.get(self.zCoordList[self.zCoordIndex])):
                offsetStructureMap.update({self.zCoordList[self.zCoordIndex] : offsetStruct})
                print("dupa 2")
            if round(self.zCoordList[self.zCoordIndex], 3) < round(offsetStruct[0][z], 3):
                self.zCoordIndex += 1
                print("dupa 3")
        return offsetStructureMap

    def generateOffsetList(self):
        offsetLists = []
        for coordStructure in self.crossSectionsCoords:
            pco = pyclipper.PyclipperOffset()
            coordinates_scaled = pyclipper.scale_to_clipper(coordStructure)
            pco.AddPath(coordinates_scaled, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDPOLYGON)
            new_coordinates = pco.Execute(pyclipper.scale_to_clipper(self.offset))
            new_coordinates_scaled = pyclipper.scale_from_clipper(new_coordinates)


            offsetCoord = []
            for figure in new_coordinates_scaled:
                offsetCoord.append(roundFloatNestedList(figure, 4))

            for elem in offsetCoord[0]:
                elem.append(coordStructure[0][z])
            offsetLists.append(offsetCoord[0])

        return offsetLists


    def genCrossSectionsCoords(self):
        coordStructList = []
        for crossSect in self.crossSections:
            vertices = roundFloatNestedList(crossSect.vertices, 4)
            structure = generateStructFromCrossSection(crossSect)
            coordStructList.append([[vertices[point][x], vertices[point][y], vertices[point][z]] for point in structure])
        return coordStructList

    def printResults(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[point[x] for point in self.crossSectionsCoords], y=[point[y] for point in self.crossSectionsCoords]))
        fig.add_trace(go.Scatter(x=[point[x] for point in self.offsetStructure[0]], y=[point[y] for point in self.offsetStructure[0]]))