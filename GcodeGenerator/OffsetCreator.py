import collections
import numpy
import math
import pyclipper
from utils import *
from enum import Enum

def matchFloats(*floats):
    return all(math.isclose(floatToCompare, floats[0], abs_tol = 0.01) for floatToCompare in floats)

def generateOffset(vertStructure, offset):
    pco = pyclipper.PyclipperOffset()
    coordinates_scaled = pyclipper.scale_to_clipper(vertStructure)
    pco.AddPath(coordinates_scaled, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDPOLYGON)
    new_coordinates = pco.Execute(pyclipper.scale_to_clipper(offset))
    new_coordinates_scaled = pyclipper.scale_from_clipper(new_coordinates)

    for figure in new_coordinates_scaled:
        figure.append(figure[0])
        figure = roundFloatList(figure, 3)
    return new_coordinates_scaled
