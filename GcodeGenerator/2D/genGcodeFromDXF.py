import sys

sys.path.append('../Common/')
import os

import GcodeCommandGenerator3 as gg
import DxfPolyCreator as dpc
import dxfgrabber as dg

inputDxfIdx = 1
outputDirIdx = 2
serialGcodeIdx = 3

inputDxf = os.path.abspath(sys.argv[inputDxfIdx])
outputDir = os.path.abspath(sys.argv[outputDirIdx])
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

print("inputDxf", inputDxf)
print("outputDir", outputDir)

materialLayersInfo = {}

offset = 10.0
entityToLayerMap, layerConfig = dpc.createPolyAndConfigFromDxf(inputDxf, offset)
for layer in entityToLayerMap.keys():
    materialThickness = float(layerConfig[layer]["thickness"])
    toolType = None
    toolDiameter = None
    bothSideMilled = None

    if "45" in layer:
        toolType = "45"
    elif "90" in layer:
        toolType = "90"
        toolDiameter = float(layerConfig[layer]["toolDiameter"])
        if toolDiameter not in [1.0, 2.0, 3.0, 6.35]:
            print("Wrong cutter diameter!")
            quit()

        bothSideMilled = layerConfig[layer]["bothSideMilled"]
        if bothSideMilled not in ['yes', 'no']:
            print("Wrong bothSideMilled option - choose 'yes' or 'no'!")
            quit()
        bothSideMilled = True if layerConfig[layer]["bothSideMilled"] == "yes" else False

    elif "Drill" in layer:
        toolType = "Drill"
        toolDiameter = float(layerConfig[layer]["toolDiameter"])
        if toolDiameter not in [1.0, 2.0, 3.0, 6.0]:
            print("Wrong Drill diameter!")
            quit()
    else:
        print("Tool type attribute not set in layer name!")
        quit()

    shouldGenSerialGcode = layerConfig[layer]["shouldGenSerialGcode"]
    if shouldGenSerialGcode not in ['yes', 'no']:
        print("Wrong shouldGenSerialGcode option: ", layer, "  ", shouldGenSerialGcode, "- choose 'yes' or 'no'!")
        quit()
    shouldGenSerialGcode = True if layerConfig[layer]["shouldGenSerialGcode"] == "yes" else False

    materialLayersInfo.update({layer: {"thickness": materialThickness,
                                       "toolType": toolType,
                                       "toolDiameter": toolDiameter,
                                       "bothSideMilled": bothSideMilled,
                                       "shouldGenSerialGcode": shouldGenSerialGcode}})

material = layerConfig["MATERIAL"]
commandGenerator = gg.CommandGenerator("../Configs/tools/Cutters.xml", material, materialLayersInfo)
commandGenerator.genGcode2D(outputDir, entityToLayerMap)
