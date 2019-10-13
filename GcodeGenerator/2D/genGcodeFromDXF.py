import sys
sys.path.append('../Common/')

import GcodeCommandGenerator as gg
import DxfPolyCreator as dpc


#dxf = dg.readfile("../TestFiles/DuzaSala.dxf")

#material = input("Choose material plexi/balsa/plywood: ")
#if not material in ["plexi", "balsa", "plywood"]:
#    print("Wrong material!") 
#    quit()
#
#cutterDeg = int(input("Choose cutter degree 45/90: "))
#if not cutterDeg in [45, 90]:
#    print("Wrong cutter degree!") 
#    quit()
#
#cutterDiameter = None
#if cutterDeg == 90:
#    cutterDiameter = int(input("Choose cutter diameter[mm] 1/3/6: "))
#
#if not cutterDiameter in [1, 3, 6]:
#    print("Wrong cutter diameter!") 
#    quit()
material = "balsa"
cutterDeg = 90
cutterDiameter = 1
material_thickness = 9.0

commandGenerator = gg.CommandGenerator("../Configs/tools/Cutters.xml", material, material_thickness, cutterDeg, cutterDiameter) 
entityToLayerMap = dpc.createPolyFromDxf("../TestFiles/DuzaSala.dxf", cutterDiameter)

commandGenerator.genGcode2D("./", entityToLayerMap)
