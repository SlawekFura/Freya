import sys
sys.path.append('../Common/')
import os

import GcodeCommandGenerator as gg
import DxfPolyCreator as dpc


print('Number of arguments:', len(sys.argv), 'arguments.') 
print('Argument List:', str(sys.argv))

if len(sys.argv) < 3:
    print("not enough arguments provided!")
    quit()

inputDxf = os.path.abspath(sys.argv[1])
outputDir = os.path.abspath(sys.argv[2])
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

material = input("Choose material plexi/balsa/plywood: ")
if not material in ["plexi", "balsa", "plywood"]:
    print("Wrong material!") 
    quit()

cutterDeg = int(input("Choose cutter degree 45/90: "))
if not cutterDeg in [45, 90]:
    print("Wrong cutter degree!") 
    quit()

cutterDiameter = None
if cutterDeg == 90:
    cutterDiameter = int(input("Choose cutter diameter[mm] 1/3/6: "))
    if not cutterDiameter in [1, 3, 6]:
        print("Wrong cutter diameter!") 
        quit()

material_thickness = float(input("Insert material thickness: "))

#material = "balsa"
#cutterDeg = 90
#cutterDiameter = 1
#material_thickness = 9.0


entityToLayerMap = dpc.createPolyFromDxf("../../Projekt/szkola/CzescDlaStarszychDzieci/budynek_doFrezowania.dxf", cutterDiameter)

commandGenerator = gg.CommandGenerator("../Configs/tools/Cutters.xml", material, material_thickness, cutterDeg, cutterDiameter) 
commandGenerator.genGcode2D(outputDir, entityToLayerMap)
