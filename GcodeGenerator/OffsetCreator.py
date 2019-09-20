import collections
import numpy
import math
import pyclipper
from enum import Enum

def matchFloats(*floats):
    return all(math.isclose(floatToCompare, floats[0], abs_tol = 0.01) for floatToCompare in floats)

def generateOffset(vertStructure, offset):
    if(not pyclipper.Orientation(vertStructure)):
        print("WrongOrientation!!")

    print(vertStructure)

    pco = pyclipper.PyclipperOffset()
    coordinates_scaled = pyclipper.scale_to_clipper(vertStructure)
    pco.AddPath(coordinates_scaled, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDPOLYGON)
    new_coordinates = pco.Execute(pyclipper.scale_to_clipper(offset))
    new_coordinates_scaled = pyclipper.scale_from_clipper(new_coordinates)

    return new_coordinates_scaled
