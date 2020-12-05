import sys

sys.path.append('../Common/')
import os

import GcodeCommandGenerator3 as gg
import DxfPolyCreator as dpc
import dxfgrabber as dg

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))

# if len(sys.argv) < 3:
#    print("not enough arguments provided!")
#    quit()

inputDxfIdx = 1
outputDirIdx = 2
serialGcodeIdx = 3

inputDxf = os.path.abspath(sys.argv[inputDxfIdx])
outputDir = os.path.abspath(sys.argv[outputDirIdx])
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

print("inputDxf", inputDxf)
print("outputDir", outputDir)

# material = input("Choose material plexi/balsa/plywood/brass: ")
# if not material in ["plexi", "balsa", "plywood", "brass"]:
#     print("Wrong material!")
#     quit()

material = ""
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
        if not toolDiameter in [1.0, 2.0, 3.0, 6.35]:
            print("Wrong cutter diameter!")
            quit()

        bothSideMilled = True if layerConfig[layer]["bothSideMilled"] == "yes" else False
        if not bothSideMilled in [True, False]:
            print("Wrong bothSideMilled option - chose 'yes' or 'no'!")
            quit()
        bothSideMilled = True if bothSideMilled == "yes" else "no"

    elif "Drill" in layer:
        toolType = "Drill"
        toolDiameter = float(layerConfig[layer]["toolDiameter"])
        if not toolDiameter in [1.0, 2.0, 3.0, 6.0]:
            print("Wrong Drill diameter!")
            quit()
    else:
        print("Tool type attribute not set in layer name!")
        quit()
    materialLayersInfo.update({layer: {"thickness": materialThickness,
                                        "toolType": toolType,
                                        "toolDiameter": toolDiameter,
                                        "bothSideMilled": bothSideMilled}})

material = layerConfig["MATERIAL"]
commandGenerator = gg.CommandGenerator("../Configs/tools/Cutters.xml", material, materialLayersInfo)
commandGenerator.genGcode2D(outputDir, entityToLayerMap)
