import sys
sys.path.append("/usr/lib/freecad/lib") # example for Linux
import FreeCAD
import FreeCADGui  


doc = FreeCAD.openDocument("tmp.fcstd")
partFeature = doc.getObjectsByLabel("sth")[0]

mutableShape = partFeature.Shape.copy()
disc = mutableShape.Faces[0].Wires[1].discretize(40)
for vect in disc:
    print vect.x, vect.y

