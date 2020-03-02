import sys
sys.path.append('../Common/')
import os

import GcodeCommandGenerator3 as gg
import DxfPolyCreator as dpc
import dxfgrabber as dg


print('Number of arguments:', len(sys.argv), 'arguments.') 
print('Argument List:', str(sys.argv))

if len(sys.argv) < 3:
    print("not enough arguments provided!")
    quit()

inputDxf = os.path.abspath(sys.argv[1])
outputDir = os.path.abspath(sys.argv[2])
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

material = input("Choose material plexi/balsa/plywood/brass: ")
if not material in ["plexi", "balsa", "plywood", "brass"]:
    print("Wrong material!") 
    quit()

materialThicknessMap = {}

cutterDiameter = None
if any([ "90" in layer.name or "Deepen" in layer.name for layer in dg.readfile(inputDxf).layers]):
    cutterDiameter = float(input("Choose cutter diameter[mm] 1/2/3/6.35: "))
    if not cutterDiameter in [1.0, 2.0, 3.0, 6.35]:
        print("Wrong cutter diameter!") 
        quit()

offset = 10.0
entityToLayerMap = dpc.createPolyFromDxf(inputDxf, offset)
for key in entityToLayerMap.keys():
    materialThicknessMap.update({key : float(input("Insert material thickness for layer " + key + ": "))})
    

commandGenerator = gg.CommandGenerator("../Configs/tools/Cutters.xml", material, materialThicknessMap, cutterDiameter) 
commandGenerator.genGcode2D(outputDir, entityToLayerMap)
