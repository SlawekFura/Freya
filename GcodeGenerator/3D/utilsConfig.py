import xml.etree.ElementTree as ET

import sys
sys.path.append('../Common/')
import ReadWritePolysFromFile as RWPolys
import subprocess
import GcodeCommandGenerator as gGen
import finalGcodeOptimizer as fgo
import time

numOfSavedModels = 0
smallestDiscLength = 0.2
prefix = ""

def genGcodeFromCoordMap(coordMap, outputFilename, offset, millDiameter, optimization = False):
    start = time.time()
    RWPolys.writePolyCoordsMapIntoFile('MeshOffsetsMap', coordMap)
    #args = ("../CppWorkspace/ToolpathGenerator/build-debug/ToolpathGenerator", str(offset) , str(millDiameter))
    #print("args: ", args)
    numOfProcesses = 10
    processes = []
    for i in xrange(numOfProcesses):
        args = ("../CppWorkspace/ToolpathGeneratorOpt/build-debug/ToolpathGeneratorOpt", str(offset) , str(millDiameter), str(i), str(numOfProcesses))
        print("args: ", args)
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        processes.append(popen)

    for p in processes:
        p.wait()

    end = time.time()
    print "Passed time for cpp engine is: " + str(end - start)
    with open("dataFromCgal.txt", "wb") as outfile:
        for i in xrange(numOfProcesses):
            with open("dataFromCgal_" + str(i) + ".txt", "rb") as infile:
                outfile.write(infile.read())

    #popen.wait()
    #output = popen.stdout.read()
    #print(output)
    offsetPolygonsMap = RWPolys.readPolysFromFile("dataFromCgal.txt")
    if optimization:
        tree = fgo.genOptimizationTree(offsetPolygonsMap, offset + 0.1)
        gGen.genGcode3DOpt(outputFilename, tree, 100, 300, millDiameter)
    else:
        gGen.genGcode3D(outputFilename, offsetPolygonsMap, 100, 300)

x = 0
y = 1
z = 2
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def match2FloatLists(floatList1, floatList2, tol = 0.001):
    for i in range(len(floatList1)):
        if not isclose(floatList1[i], floatList2[i], abs_tol = tol):
            return False
    return True

def getCutterConfig(cutterType, material, millDiameter):
    root = ET.parse("../Configs/tools/Cutters.xml").getroot()
    return root.findall("type_"      + str(cutterType) + 
                        "/"          + material + 
                        "/diameter_" + str(millDiameter) +
                        "/params")

