import sys
sys.path.append('../Common/')

import utils
import ConfigReader as cr
import xml.etree.ElementTree as ET
import math

x = 0
y = 1
z = 2

safeHeight = 1.0
highSpeed = 1000.0
highSpeedZ = 200.0

commandsMap = { "FastMove"      : lambda point = [], *args        :"G00 X" + str(point[x]) + " Y" + str(point[y]) + " F" + str(highSpeed) + "\n",
                "FastMoveToBase":                                  "G00 X" + str(0.0) + " Y" + str(0.0) + " F" + str(highSpeed) + "\n",
                "FastMoveZ"     : lambda z                        :"G00 Z" + str(z) + "F" + str(highSpeedZ) + "\n",
                "Move"          : lambda point = [], *args, speed :"G01 X" + str(point[x]) + " Y" + str(point[y]) + " F" + str(speed) + "\n",
                "MoveZ"         : lambda z, speedZ                :"G01 Z" + str(z) + "F" + str(speedZ) + "\n",
                "SetCoordMM"    :                                  "G21\n\n",
                "EndProgram"    :                                  "\nM02\n" }

class CommandGenerator:
    def __init__(self, configPath, material, material_thickness, cutterType, cutterDiameter = None):
        self.material = material
        self.material_thickness = material_thickness
        self.cutterType = cutterType
        self.cutterDiameter = cutterDiameter
        self.cutterConfig = self.getCutterConfig(configPath)
        self.speed = self.cutterConfig[0].get('cutSpeed')
        self.speedZ = self.cutterConfig[0].get('drillSpeed')
    
    def readLayerConfig(self, filename, layer):
        root = ET.parse(filename).getroot()
        return root.findall(layer + "/property")

    def getCutterConfig(self, path):
        root = ET.parse(path).getroot()
        if not self.cutterDiameter: 
            return root.findall("type_" + str(self.cutterType) + "/" + str(self.material) + "/params")
        return root.findall("type_"      + str(self.cutterType) + 
                            "/"          + str(self.material) + 
                            "/diameter_" + str(self.cutterDiameter) +
                            "/params")

    def genGcode3D(outFile, polysMap): 
        fileToWrite = open(outFile,'w')
        keys = sorted(polysMap.keys(), reverse = True)
        print("keys gcode:", keys)
        fileToWrite.write(commandsMap["SetCoordMM"])
    
        for key in keys:
            for poly in polysMap[key]:
                fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
                fileToWrite.write(commandsMap["FastMove"](poly[0]))
                fileToWrite.write(commandsMap["MoveZ"](key), self.speedZ)
                for point in poly[1:]:
                    fileToWrite.write(commandsMap["Move"](point), self.speed)
        fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
        fileToWrite.write("\n" + commandsMap["FastMoveToBase"])
        fileToWrite.write(commandsMap["EndProgram"])
        fileToWrite.close()
    
    
    def generateMillingLevels(self, bot_margin, isDeepenLayer):
        cutLevels = []
        materialThickenss = self.material_thickness / 2.0 if isDeepenLayer else self.material_thickness
        if self.cutterType == "45":
            cutAmount = self.cutterConfig.get("cutAmount")
            
            baseMultipleParam = 1.0
            baseLevel = math.sqrt(cutAmount)
            
            level = baseLevel * math.sqrt(baseMultipleParam)
            while level < materialThickenss: 
                cutLevels.apped(level)
                baseMultipleParam += 1.0
            cutLevels.append(-materialThickenss)
        else:
            maxCutDepth = float(self.cutterConfig[0].get("maxDepth"))
            numOfCuts = math.ceil(materialThickenss / maxCutDepth)
            for i in range(1, numOfCuts):
                cutLevels.append(-i * maxCutDepth)

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
            levels = self.generateMillingLevels(float(layerConfig[0].get("bot_margin")), "Deepen" in layer.name)
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

