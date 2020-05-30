import sys
sys.path.append('../Common/')

import utils
import ConfigReader as cr
import xml.etree.ElementTree as ET
import math
from utils import *

safeHeight = 1.0
highSpeed = 1000.0
highSpeedZ = 200.0

commandsMap = { "FastMove"      : lambda point        :"G0 X" + str(point[x]) + " Y" + str(point[y]) + " F" + str(highSpeed) + "\n",
                "FastMoveToBase":                                  "G0 X" + str(0.0) + " Y" + str(0.0) + " F" + str(highSpeed) + "\n",
                "FastMoveZ"     : lambda z                        :"G0 Z" + str(z) + "F" + str(highSpeedZ) + "\n",
                "Move"          : lambda point, speed :"G01 X" + str(point[x]) + " Y" + str(point[y]) + " F" + str(speed) + "\n",
                "MoveZ"         : lambda z, speedZ                :"G01 Z" + str(z) + "F" + str(speedZ) + "\n",
                "SetCoordMM"    :                                  "G21\n\n",
                "EndProgram"    :                                  "\nM02\n" }


class CommandGenerator:
    def __init__(self, configPath, material, materialLayersInfo):
        self.material = material
        self.materialLayersInfo = materialLayersInfo
        self.configPath = configPath
        self.speed = None
        self.speedZ = None

    def readLayerConfig(self, filename, layer):
        root = ET.parse(filename).getroot()
        return root.findall(layer + "/property")

    def getCutterConfig(self, path, toolType, toolDiameter = None):
        root = ET.parse(path).getroot()
        if toolType == "45":
            return root.findall("type_" + str(toolType) + "/" + str(self.material) + "/params")
        return root.findall("type_"      + str(toolType) +
                            "/"          + str(self.material) +
                            "/diameter_" + str(toolDiameter) +
                            "/params")


    def generateMillingLevels(self, bot_margin, layerName):
        cutLevels = []
        cutterConfig = None
        layerNameIdx = 0
        materialThickenss = self.materialLayersInfo[layerName]["thickness"]
        toolType = self.materialLayersInfo[layerName]["toolType"]
        toolDiameter = self.materialLayersInfo[layerName]["toolDiameter"]

        if "45" in layerName:
            cutterConfig = self.getCutterConfig(self.configPath, toolType)
            cutAmount = float(cutterConfig[0].get("cutAmount"))


            baseMultipleParam = 1.0
            baseLevel = -math.sqrt(cutAmount)

            level = baseLevel * math.sqrt(baseMultipleParam)
            while level > -materialThickenss:
                cutLevels.append(level)
                baseMultipleParam += 1.0
                level = baseLevel * math.sqrt(baseMultipleParam)
            cutLevels.append(-materialThickenss)
        else:
            cutterConfig = self.getCutterConfig(self.configPath, toolType, toolDiameter)
            maxCutDepth = float(cutterConfig[0].get("maxDepth"))
            numOfCuts = math.ceil(materialThickenss / maxCutDepth)
            for i in range(1, numOfCuts):
                cutLevels.append(-i * maxCutDepth)

        self.speed = cutterConfig[0].get('cutSpeed')
        self.speedZ = cutterConfig[0].get('drillSpeed')

        if cutLevels:
            if (materialThickenss - bot_margin) > abs(cutLevels[-1]):
                cutLevels.append(-(materialThickenss - bot_margin))
        else:
            cutLevels.append(-(materialThickenss - bot_margin))
        return cutLevels

    def genGcode2D(self, outfileDir, polysToLayerMap):

        for layer, polys in polysToLayerMap.items():
            print("out :", outfileDir + "/" + layer + ".gcode")
            fileToWrite = open(outfileDir + "/" + layer + ".gcode",'w')
            fileToWrite.write(commandsMap["SetCoordMM"])

            #layerConfig = self.readLayerConfig("../2D/LayersConfig.xml", layer)
            #levels = self.generateMillingLevels(float(layerConfig[0].get("bot_margin")), layer)
            levels = self.generateMillingLevels(0, layer)
            print("levels: ", levels)

            for level in levels:
                for poly in polys:
                    poly = roundFloatNestedList(poly, 3)
                    fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
                    fileToWrite.write(commandsMap["FastMove"](poly[0]))
                    fileToWrite.write(commandsMap["MoveZ"](level, self.speedZ))

                    for point in poly:
                        fileToWrite.write(commandsMap["Move"](point, speed = self.speed))

            fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
            fileToWrite.write("\n" + commandsMap["FastMoveToBase"])
            fileToWrite.write(commandsMap["EndProgram"])
            fileToWrite.close()
