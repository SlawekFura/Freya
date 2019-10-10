import sys
sys.path.append('../Common/')

import utils
import ConfigReader as cr

x = 0
y = 1
z = 2

materialThickness = 3.0
safeHeight = 1.0
highSpeed = 1000.0
highSpeedZ = 200.0
speed = 400.0;
speedZ = 50.0;
commandsMap = { "FastMove"      : lambda point = [], *args : "G00 X" + str(point[x]) + " Y" + str(point[y]) + " F" + str(highSpeed) + "\n",
                "FastMoveToBase": "G00 X" + str(0.0) + " Y" + str(0.0) + " F" + str(highSpeed) + "\n",
                "FastMoveZ"     : lambda z      : "G00 Z" + str(z) + "F" + str(highSpeedZ) + "\n",
                "Move"          : lambda point = [], *args : "G01 X" + str(point[x]) + " Y" + str(point[y]) + " F" + str(speed) + "\n",
                "MoveZ"         : lambda z      : "G01 Z" + str(z) + "F" + str(speedZ) + "\n",
                "SetCoordMM"    :                 "G21\n\n",
                "EndProgram"    :                 "\nM02\n" }


def genGcode3D(outFile, polysMap): 
    fileToWrite = open(outFile,'w')
    keys = sorted(polysMap.keys(), reverse = True)
    print("keys gcode:", keys)
    fileToWrite.write(commandsMap["SetCoordMM"])

    for key in keys:
        for poly in polysMap[key]:
            fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
            fileToWrite.write(commandsMap["FastMove"](poly[0]))
            fileToWrite.write(commandsMap["MoveZ"](key))
            for point in poly[1:]:
                fileToWrite.write(commandsMap["Move"](point))
    fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
    fileToWrite.write("\n" + commandsMap["FastMoveToBase"])
    fileToWrite.write(commandsMap["EndProgram"])
    fileToWrite.close()


def genGcode2D(outFile, polysToLayerMap): 
    layerConfig = cr.readLayerConfig("../2D/LayersConfig")        

    fileToWrite = open(outFile,'w')
    fileToWrite.write(commandsMap["SetCoordMM"])
    for layer, polys in polysToLayerMap.items():
        config = layerConfig[layer.name]

        fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
        fileToWrite.write(commandsMap["FastMove"](poly[0]))
        fileToWrite.write(commandsMap["MoveZ"](key))
        for point in polys[1:]:
            fileToWrite.write(commandsMap["Move"](point))
    fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
    fileToWrite.write("\n" + commandsMap["FastMoveToBase"])
    fileToWrite.write(commandsMap["EndProgram"])
    fileToWrite.close()

