import pymesh
import sys
sys.path.append('../../Common/')
sys.path.append("/usr/lib/freecad/lib") # example for Linux
import polyFromMeshCreator as pc
import numpy as np
from meshpy import geometry
from meshpy.tet import MeshInfo, build
import math
import xml.etree.ElementTree as ET
from utils import *
import ReadWritePolysFromFile as RWPolys
import os
import subprocess
import offsetMesh as om

def combineCrossSectionsIntoMesh(crossSections):
    verticesCombined = crossSections[0].vertices
    facesCombined = crossSections[0].faces
    faceValToMove = 0
    for i in range(1, len(crossSections)):
        faceValToMove += len(crossSections[i-1].vertices)
        for face in crossSections[i].faces:
            facesCombined = np.append(facesCombined, [[point + faceValToMove for point in face]], axis=0)

        for vertice in crossSections[i].vertices:
            verticesCombined = np.append(verticesCombined, [vertice], axis=0)

    return pymesh.form_mesh(verticesCombined, facesCombined)

def moveAllVertices(mesh, moveValVec):
    return pymesh.form_mesh(mesh.vertices + moveValVec, mesh.faces)

def genBaseBoxDiff(bbox, zOffset, height):
    return pymesh.generate_box_mesh([bbox[0][x], bbox[0][y], bbox[1][z] - zOffset - height],
                                    [bbox[1][x], bbox[1][y], bbox[1][z] - zOffset])

def genPulledMesh(mesh, pullVal):
    zValues = [vertice[z] for vertice in mesh.vertices]
    maxZ = max(zValues)
    newVertices = []
    for vertice in mesh.vertices:
        if int(vertice[z]) * 100 == int(maxZ) * 100:
            newVertices.append([vertice[x], vertice[y], vertice[z] + pullVal])
        else:
            newVertices.append(vertice) 

    return pymesh.form_mesh(newVertices, mesh.faces)

def genMeshWithFilteredBasePart(mesh):
    zValues = [vertice[z] for vertice in mesh.vertices]
    minZ = min(zValues)
    #vertices = list(filter(lambda vertice : vertice[z] == minZ, mesh.vertices))

    vertices = mesh.vertices.tolist()
    vertices2 = mesh.vertices.tolist()
    faces = [face.tolist() for face in mesh.faces if matchFloats(vertices[face[0]][z], vertices[face[1]][z], vertices[face[2]][z])]
    
    i = 0
    for vertice in vertices:
        if not matchFloats(vertice[z], minZ):
            faces = [face for face in faces if i not in face]
            faces = [[facePoint - 1 if facePoint > i else facePoint for facePoint in specificFace] for specificFace in faces]
            vertices2.remove(vertice)
        else:
            i += 1
            
    return pymesh.form_mesh(np.array(vertices2), np.array(faces))

def genOptimizedMesh(baseMeshPath, filename, millDiameter):
    baseOffset = 1
    #millDiameter = 3
    
    #filename = "../../../Projekt/szkola/Podstawa/Drzewka/drzewko1.stl"
    mesh = pymesh.load_mesh(baseMeshPath)
    mesh = pc.moveToGround(mesh)
    
    offset = baseOffset + millDiameter
    print("dupaGen")
    om.generateMeshOffsetFile(filename, offset, os.path.abspath("./Generated/StlOffset.stl"))
    
    bbox = mesh.bbox
    zMin = bbox[0][z]
    zMax = bbox[1][z]
    print("zMax:", zMax)
    bbox[0][0] -= (baseOffset + millDiameter)
    bbox[0][1] -= (baseOffset + millDiameter)
    bbox[1][0] += (baseOffset + millDiameter)
    bbox[1][1] += (baseOffset + millDiameter)
    
    root = ET.parse("../Configs/tools/Cutters.xml").getroot()
    cutterConfig = root.findall("type_"      + str(90) + 
                                "/"          + "balsa" + 
                                "/diameter_" + str(millDiameter) +
                                "/params")
    maxCutDepth = float(cutterConfig[0].get("maxDepth"))
    materialThickness = abs(zMax - zMin)
    numOfCuts = math.ceil(materialThickness / maxCutDepth)
    
    minHeight = 1
    if (materialThickness < (maxCutDepth + minHeight)):
        print("No optimization due to not enough material thickness")
    
    newBoxHeight = 1.0
    maxWorkableDepth = materialThickness - minHeight
    offsetMesh = pymesh.load_mesh("./Generated/StlOffset.stl");

    offsetMesh = moveAllVertices(offsetMesh, [0, 0, zMax - offset])
    pymesh.save_mesh("offsetMesh.stl", offsetMesh, ascii=True);
    
    crossSectionsList = []
    wholeStructure = []
    layersToMerge = list(range(int(maxCutDepth) * 10, int(maxWorkableDepth * 10), int(maxCutDepth * 10)))
    layersToMerge.append(int(maxWorkableDepth * 10))
    layersToMerge = [float(x) / 10 for x in layersToMerge]
    
    i = 0
    print("layersToMerge:", layersToMerge, "\tmaxCutDepth:", maxCutDepth, "\tmaxWorkableDepth:", maxWorkableDepth)
    for depth in layersToMerge: 
        newBox = genBaseBoxDiff(bbox, depth, newBoxHeight)
        pymesh.save_mesh("newBox" + str(i) + ".stl", newBox, ascii=True);
        
    
        pDiff = pymesh.boolean(newBox, offsetMesh, "difference")
        pymesh.save_mesh("pDiff" + str(i) + ".stl", pDiff, ascii=True);

        crossSectionsList.append(genMeshWithFilteredBasePart(pDiff))
    
        #wholeDiff = pymesh.boolean(newBox, offsetMesh, "difference")
        wholeDiff = genPulledMesh(pDiff, math.ceil(maxCutDepth / newBoxHeight))
        pymesh.save_mesh("wholeDiff" + str(i) + ".stl", wholeDiff, ascii=True);

        wholeStructure.append(wholeDiff)

        print(depth + maxCutDepth)
        i += 1
    
    finalStructure = wholeStructure[0]
    i = 1;
    for elem in wholeStructure[1:]:
        finalStructure = pymesh.boolean(finalStructure, elem, "union")
        print("final structure processing", i, "of", len(wholeStructure) - 1)
        i+=1
        
    meshCombined = combineCrossSectionsIntoMesh(crossSectionsList)
        
    pymesh.save_mesh("finalStructure.stl", finalStructure, ascii=True);
    pymesh.save_mesh("meshCombined.stl", meshCombined, ascii=True);

    return finalStructure, meshCombined
