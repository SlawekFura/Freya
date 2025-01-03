import pymesh
import os
import subprocess

def generateMeshOffsetFile(inputStl, offset, output):
    #meshWithSplitEngesLocation = "./Generated/meshCleanup.stl"
    #
    #meshWithSplitLong = pymesh.load_mesh(inputStl)
    #newMesh, inf = pymesh.split_long_edges(meshWithSplitLong, 1.8)
    #pymesh.save_mesh(meshWithSplitEngesLocation, newMesh)
    
    #python3_command = "python " + os.path.abspath("../3rdPartyScripts/freecadApi/freecadOffset.py") + " " + os.path.abspath(meshWithSplitEngesLocation) + "  " + str(offset) + " " + output  # launch your python2 script using bash
    python3_command = "python " + os.path.abspath("../3rdPartyScripts/freecadApi/freecadOffsetPart.py") + " " + os.path.abspath(inputStl) + "  " + str(offset) + " " + os.path.abspath(output)  # launch your python2 script using bash
    process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()  # receive output from the python2 script
