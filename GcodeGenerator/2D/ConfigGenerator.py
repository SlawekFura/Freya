import dxfgrabber as dg
import sys
import re

ParameterList = ["thickness", "toolDiameter", "bothSideMilled", "shouldGenSerialGcode"]


class ConfigGenerator:

    def __init__(self):
        pass

    def generate(self, baseString):
        return self.extractConfig(baseString)

    def extractConfig(self, stringToProcess):
        # print("String to process: ", stringToProcess)
        # lines = stringToProcess.split("^J")
        # lines = stringToProcess.split("\n")
        lines = stringToProcess
        # print("-----------before split:", lines)
        lines = re.split('\^J|\n', lines)
        # print("----------after split:", lines)
        newLines = []
        for line in lines:
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            line = line.replace("^S", '')
            if line != "":
                newLines.append(line)

        layerToconfigMap = {}

        for line in newLines:
            layerToconfigMap.update(self.extractConfigElement(line))

        for key, value in layerToconfigMap.items():
            print(key, value)

        return layerToconfigMap

    def extractConfigElement(self, stringLine):
        print("String to split: ", stringLine)
        [leftSide, rightSide] = stringLine.split("=")

        splitParameters = leftSide.replace(')', '').split("(")
        layerName = splitParameters[0]
        params = splitParameters[1].split(",")

        splitValues = rightSide.split(",")

        configMap = {layerName: {}}
        valueSideIdx = 0
        for param in params:
            if layerName == "MATERIAL":
                configMap[layerName] = splitValues[0]
                break
            if param not in ParameterList:
                sys.exit("Unsupported param name: " + param + " for layer:" + layerName)

            configMap[layerName].update({param: splitValues[valueSideIdx]})
            valueSideIdx += 1

        return configMap
