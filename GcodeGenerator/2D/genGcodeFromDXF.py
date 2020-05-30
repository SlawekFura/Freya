import sys
sys.path.append('../Common/')
import os

import GcodeCommandGenerator3 as gg
import DxfPolyCreator as dpc
import dxfgrabber as dg


#print('Number of arguments:', len(sys.argv), 'arguments.') 
#print('Argument List:', str(sys.argv))

#if len(sys.argv) < 3:
#    print("not enough arguments provided!")
#    quit()

inputDxfIdx = 1
outputDirIdx = 2

inputDxf = os.path.abspath(sys.argv[inputDxfIdx])
outputDir = os.path.abspath(sys.argv[outputDirIdx])
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

print("inputDxf", inputDxf)
print("outputDir", outputDir)

material = input("Choose material plexi/balsa/plywood/brass: ")
if not material in ["plexi", "balsa", "plywood", "brass"]:
    print("Wrong material!") 
    quit()

materialLayersInfo = {}

offset = 10.0
entityToLayerMap = dpc.createPolyFromDxf(inputDxf, offset)
for key in entityToLayerMap.keys():
    materialThickness = float(input("Insert material thickness for layer " + key + ": "))
    toolType = None
    toolDiameter = None
    if "45" in key:
        toolType = "90"
    elif "90" in key:
        toolType = "90"
        toolDiameter = float(input("Choose cutter diameter[mm] 1/2/3/6.35: "))
        if not toolDiameter in [1.0, 2.0, 3.0, 6.35]:
            print("Wrong cutter diameter!") 
            quit()
    elif "Drill" in key:
        toolType = "Drill"
        toolDiameter = float(input("Choose cutter diameter[mm] 3/6: "))
        if not toolDiameter in [3.0, 6.0]:
            print("Wrong Drill diameter!") 
            quit()
    else:
        print("Tool type attribute not set in layer name!")
        quit()
    materialLayersInfo.update({key : {"thickness" : materialThickness,
                                      "toolType" : toolType,
                                      "toolDiameter" : toolDiameter}})


commandGenerator = gg.CommandGenerator("../Configs/tools/Cutters.xml", material, materialLayersInfo)
commandGenerator.genGcode2D(outputDir, entityToLayerMap)
