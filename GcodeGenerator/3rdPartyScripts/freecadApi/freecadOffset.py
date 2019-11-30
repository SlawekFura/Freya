import sys
import os

# add folder containing FreeCAD.pyd, FreeCADGui.pyd to sys.path
sys.path.append("/usr/lib/freecad/lib") # example for Linux

import FreeCAD
import FreeCADGui
import Mesh

inputStl = os.path.abspath(sys.argv[1])
offset = float(sys.argv[2])

#print inputStl
#mesh = Mesh.Mesh("../../3D/Generated/meshClenup.stl")
scriptPath = os.getcwd()
mesh = Mesh.Mesh(inputStl)
step = 1
for i in range(0, int(offset), step):
    mesh.offset(step)
#mesh.offset(offset)
mesh.write(os.path.abspath(scriptPath + "/Generated/StlOffset.stl"))
