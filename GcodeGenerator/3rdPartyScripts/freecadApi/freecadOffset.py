import sys
import os

# add folder containing FreeCAD.pyd, FreeCADGui.pyd to sys.path
sys.path.append("/usr/lib/freecad/lib") # example for Linux

import FreeCAD
import FreeCADGui
import Mesh

#inputStl = os.path.abspath(sys.argv[1])
#offset = float(sys.argv[2])
#
#print inputStl
#mesh = Mesh.Mesh(inputStl)
mesh = Mesh.Mesh("../../../Projekt/szkola/Podstawa/Drzewka/drzewko1_meshed.stl")
mesh.offset(4)
mesh.write(os.path.abspath("../../3D/Generated/StlOffset.stl"))
