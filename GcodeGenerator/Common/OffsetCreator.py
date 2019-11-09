import pyclipper
from baseStructureGenerator import *
import pymesh
import numpy as np
import plotly.graph_objects as go

class OffsetGenerator:
    def __init__(self, mesh, offset, minReso):
        self.mesh = mesh
        self.numOfSlices = getNumOfSlices(self.mesh, minReso)
        self.crossSections = pymesh.slice_mesh(mesh, np.array([0, 0, 1], np.int32), self.numOfSlices * 3)
        self.crossSectionsCoords = self.genCrossSectionsCoords()
        self.offset = offset
        self.zCoordList = genZCoordList(mesh)
        self.offsetStructure = self.generateOffsetList()
        self.zCoordIndex = 0

    def genOffsetMap(self):
        offsetStructureMap = {}
        [offsetStructureMap.update({zCoord: None}) for zCoord in self.zCoordList]
        #for elem in self.offsetStructure:
        #    print("offsetStructure: ", elem)
        for offsetStruct in self.offsetStructure:
            if offsetStructureMap.get(self.zCoordList[self.zCoordIndex]) is None:
                offsetStructureMap.update({self.zCoordList[self.zCoordIndex] : offsetStruct})
            elif not sorted(offsetStruct[0]) == sorted(offsetStructureMap.get(self.zCoordList[self.zCoordIndex])):
                offsetStructureMap.update({self.zCoordList[self.zCoordIndex] : offsetStruct})
            if round(self.zCoordList[self.zCoordIndex], 3) < round(offsetStruct[0][z], 3):
                self.zCoordIndex += 1
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

            offsetCoord[0] = self.joinBeginWithEnd(offsetCoord[0])
            offsetLists.append(offsetCoord[0])

        return offsetLists


    def genCrossSectionsCoords(self):
        coordStructList = []
        for crossSect in self.crossSections:
            vertices = roundFloatNestedList(crossSect.vertices, 4)
            structure = generateStructFromCrossSection(crossSect)
            coordStructList.append([[vertices[point][x], vertices[point][y], vertices[point][z]] for point in structure])
        return coordStructList

    def joinBeginWithEnd(self, offsetLists):
        offsetLists.extend([offsetLists[0]])
        return offsetLists


    def printResults(self):
        fig = go.Figure()
        for crossSectionCoord in self.crossSectionsCoords:
            fig.add_trace(go.Scatter(x=[point[x] for point in crossSectionCoord], y=[point[y] for point in crossSectionCoord]))
        for offset in self.offsetStructure:
            fig.add_trace(go.Scatter(x=[point[x] for point in offset], y=[point[y] for point in offset]))
        fig.show()
