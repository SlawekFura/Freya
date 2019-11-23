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

commandsMap = { "FastMove"      : lambda point = [], *args        :"G0 X" + str(point[x]) + " Y" + str(point[y]) + " F" + str(highSpeed) + "\n",
                "FastMoveToBase":                                  "G0 X" + str(0.0) + " Y" + str(0.0) + " F" + str(highSpeed) + "\n",
                "FastMoveZ"     : lambda z                        :"G0 Z" + str(z) + "F" + str(highSpeedZ) + "\n",
                "Move"          : lambda point = [], *args, speed :"G01 X" + str(point[x]) + " Y" + str(point[y]) + " F" + str(speed) + "\n",
                "MoveZ"         : lambda z, speedZ                :"G01 Z" + str(z) + "F" + str(speedZ) + "\n",
                "SetCoordMM"    :                                  "G21\n\n",
                "EndProgram"    :                                  "\nM02\n" }

class CommandGenerator:
    def __init__(self, configPath, material, material_thickness, cutterDiameter = None):
        self.material = material
        self.material_thickness = material_thickness
        self.cutterDiameter = cutterDiameter
        self.configPath = configPath
        self.speed = None
        self.speedZ = None
    
    def readLayerConfig(self, filename, layer):
        root = ET.parse(filename).getroot()
        return root.findall(layer + "/property")

    def getCutterConfig(self, path, cutterType):
        root = ET.parse(path).getroot()
        if cutterType == "45":
            return root.findall("type_" + str(cutterType) + "/" + str(self.material) + "/params")
        return root.findall("type_"      + str(cutterType) + 
                            "/"          + str(self.material) + 
                            "/diameter_" + str(self.cutterDiameter) +
                            "/params")

    
    
    def generateMillingLevels(self, bot_margin, layerName):
        cutLevels = []
        cutterConfig = None
        materialThickenss = self.material_thickness / 2.0 if "Deepen" in layerName else self.material_thickness

        if "45" in layerName:
            cutterConfig = self.getCutterConfig(self.configPath, "45")
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
            cutterConfig = self.getCutterConfig(self.configPath, "90")
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


            print("out :", outfileDir + "/" + layer.name + ".gcode")
            fileToWrite = open(outfileDir + "/" + layer.name + ".gcode",'w')
            fileToWrite.write(commandsMap["SetCoordMM"])
            
            layerConfig = self.readLayerConfig("../2D/LayersConfig.xml", layer.name)
            levels = self.generateMillingLevels(float(layerConfig[0].get("bot_margin")), layer.name)
            print("levels: ", levels)
            
            for level in levels: 
                for poly in polys:
                    #level = 0.0
                    fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
                    fileToWrite.write(commandsMap["FastMove"](poly[0]))
                    fileToWrite.write(commandsMap["MoveZ"](level, self.speedZ))
    
                    for point in poly:
                        fileToWrite.write(commandsMap["Move"](point, speed = self.speed))
    
            fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
            fileToWrite.write("\n" + commandsMap["FastMoveToBase"])
            fileToWrite.write(commandsMap["EndProgram"])
            fileToWrite.close()

def genGcode3D(outFile, polysMap, speedZ, speed): 
    fileToWrite = open(outFile,'w')
    keys = sorted(polysMap.keys(), reverse = True)
    print("keys gcode:", keys)
    fileToWrite.write(commandsMap["SetCoordMM"])

    for key in keys:
        for poly in polysMap[key]:
            fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
            fileToWrite.write(commandsMap["FastMove"](poly[0]))
            fileToWrite.write(commandsMap["MoveZ"](key, speedZ))
            for point in poly[1:]:
                fileToWrite.write(commandsMap["Move"](point, speed = speed))
    fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
    fileToWrite.write("\n" + commandsMap["FastMoveToBase"])
    fileToWrite.write(commandsMap["EndProgram"])
    fileToWrite.close()
