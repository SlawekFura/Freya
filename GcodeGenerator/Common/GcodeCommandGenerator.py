import sys
sys.path.append('../Common/')

import utils
import ConfigReader as cr
import xml.etree.ElementTree as ET
import math
from utils import *
from anytree import Node, RenderTree, AnyNode, PostOrderIter, search, LevelOrderIter, AsciiStyle

safeHeight = 1.0
highSpeed = 1000.0
highSpeedZ = 200.0

#commandsMap = { "FastMove"      : lambda point = [], *args        :"G0 X" + str(point[x]) + " Y" + str(point[y]) + " F" + str(highSpeed) + "\n",
#                "FastMoveToBase":                                  "G0 X" + str(0.0) + " Y" + str(0.0) + " F" + str(highSpeed) + "\n",
#                "FastMoveZ"     : lambda z                        :"G0 Z" + str(z) + "F" + str(highSpeedZ) + "\n",
#                "Move"          : lambda point = [], *args, speed :"G01 X" + str(point[x]) + " Y" + str(point[y]) + " F" + str(speed) + "\n",
#                "MoveZ"         : lambda z, speedZ                :"G01 Z" + str(z) + "F" + str(speedZ) + "\n",
#                "SetCoordMM"    :                                  "G21\n\n",
#                "EndProgram"    :                                  "\nM02\n" }

commandsMap = { "FastMove"      : lambda point        :"G0 X" + str(point[x]) + " Y" + str(point[y]) + " F" + str(highSpeed) + "\n",
                "FastMoveToBase":                                  "G0 X" + str(0.0) + " Y" + str(0.0) + " F" + str(highSpeed) + "\n",
                "FastMoveZ"     : lambda z                        :"G0 Z" + str(z) + "F" + str(highSpeedZ) + "\n",
                "Move"          : lambda point, speed :"G01 X" + str(point[x]) + " Y" + str(point[y]) + " F" + str(speed) + "\n",
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


def getIndexesOfClosestPointsForPolygons(poly1, poly2, millDiameter):
    #print("mill diameter:", millDiameter)
    index1 = 0 
    index2 = 0
    distance = sys.maxint
    for i in range(0, len(poly1)):    
        x1 = poly1[i][x]
        y1 = poly1[i][y]
        for j in range(0, len(poly2)):    
            x2 = poly2[j][x]
            y2 = poly2[j][y]
            newDist = math.hypot(x2 - x1, y2 - y1)
            if newDist < distance:
                #index1 = i
                #index2 = j
                distance = newDist
            if newDist < millDiameter:
                #print("newDist = ", newDist)
                index1 = i
                index2 = j
                return index1, index2
    #print("distance = ", distance)

    return index1, index2

def genSimpleGcode(poly, fileToWrite, speed):
    #poly.append(poly[0])
    for point in poly:
        fileToWrite.write(commandsMap["Move"](point, speed = speed))

def goToIndexNew(poly, fileToWrite, prevIdx, destIdx, speed):
    #print("prev:", prevIdx, "dest:", destIdx)
    routeToIndex = []
    if abs(destIdx - prevIdx) <= (len(poly)/2):
        if destIdx >= prevIdx:
            #print "dupa if 1"
            routeToIndex = poly[prevIdx:destIdx+1]
        else:
            #print "dupa if 2"
            routeToIndex = poly[destIdx:prevIdx+1][::-1]
    else:
        if destIdx >= prevIdx:
            #print "dupa else 1"
            routeToIndex = poly[:prevIdx+1][::-1] + poly[destIdx:][::-1]
            #routeToIndex.reverse()
        else:
            #print "dupa else 2"
            routeToIndex = poly[prevIdx:] + poly[:destIdx]
            
    #print("after", routeToIndex)
    #print(routeToIndex)
    fileToWrite.write("goToIndex--------------\n")
    fileToWrite.write("prev: " + str(prevIdx) + " " + str(poly[prevIdx]) + "\tdest: " + str(destIdx) + " " + str(poly[destIdx]) + "\n")
    genSimpleGcode(routeToIndex, fileToWrite, speed)
    fileToWrite.write("----------------goToIndex\n")

def genGcodeForNode(_node, fileToWrite, key, speedZ, speed, millDiameter, isFirstIteration = False):
    #print("id", _node.id)
    poly = _node.poly
    #fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
    #fileToWrite.write(commandsMap["FastMove"](poly[0]))
    #fileToWrite.write(commandsMap["MoveZ"](key, speedZ))
    genSimpleGcode(poly, fileToWrite, speed)

    
    nodeIds = [node.id for node in LevelOrderIter(_node, filter_=lambda n: not n.id == _node.id,  maxlevel=2)]
    if not nodeIds:
        return
    #print nodeIds
    currentIdx = 0
    for nodeId in nodeIds:
        #print "\n"
        #print("nodeId", nodeId, "ids", nodeIds)
        
        nextNode = search.findall(_node, lambda node: node.id == nodeId)[0]
        if nextNode:
            closestPolyIdx, newPolyIdx = getIndexesOfClosestPointsForPolygons(poly, nextNode.poly, millDiameter)
            goToIndexNew(poly, fileToWrite, prevIdx = currentIdx, destIdx = closestPolyIdx, speed = speed)
            currentIdx = closestPolyIdx

            #print(routeToNextPoly)
            nextNode.poly = nextNode.poly[newPolyIdx:] + nextNode.poly[:newPolyIdx] + [nextNode.poly[newPolyIdx]]
            genGcodeForNode(nextNode, fileToWrite, key, speedZ, speed, millDiameter)

    #print("current idx", currentIdx)
    goToIndexNew(poly,fileToWrite, prevIdx=currentIdx, destIdx=0, speed = speed)
    return poly[0]
          

def genGcode3DOpt(outFile, polysTree, speedZ, speed, millDiameter): 
    fileToWrite = open(outFile,'w')
    keys = sorted(polysTree.keys(), reverse = True)
    print("keys gcode:", keys)
    fileToWrite.write(commandsMap["SetCoordMM"])

    lastPoint = []
    for key in keys:
        mainNode = polysTree[key]
        #print(mainNode)
        nodeIds = [node.id for node in LevelOrderIter(mainNode, filter_=lambda n: not n.id == mainNode.id,  maxlevel=2)]
        #print("mainNodeIds", nodeIds)
        for nodeId in nodeIds:
            nextNode = search.findall(mainNode, lambda node: node.id == nodeId)[0]
            #print(nodeId)

            nextNodeFirstPoint = nextNode.poly[0]
            shouldBackZAxis = True
            if lastPoint:
                shouldBackZAxis = math.hypot(nextNodeFirstPoint[x] - lastPoint[x], nextNodeFirstPoint[y] - lastPoint[y]) > 0.0001
                #print("val:", math.hypot(nextNodeFirstPoint[x] - lastPoint[x], nextNodeFirstPoint[y] - lastPoint[y]), shouldBackZAxis)

            if shouldBackZAxis:
                fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
                fileToWrite.write(commandsMap["FastMove"](nextNode.poly[0]))
            fileToWrite.write(commandsMap["MoveZ"](key, speedZ))

            lastPoint = genGcodeForNode(nextNode, fileToWrite, key, speedZ, speed, millDiameter, True)

            #fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
    
    #    for poly in polysMap[key]:
    #        fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
    #        fileToWrite.write(commandsMap["FastMove"](poly[0]))
    #        fileToWrite.write(commandsMap["MoveZ"](key, speedZ))
    #        for point in poly[1:]:
    #            fileToWrite.write(commandsMap["Move"](point, speed = speed))
    fileToWrite.write("\n" + commandsMap["FastMoveZ"](safeHeight))
    fileToWrite.write("\n" + commandsMap["FastMoveToBase"])
    fileToWrite.write(commandsMap["EndProgram"])
    fileToWrite.close()
