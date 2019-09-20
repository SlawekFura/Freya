from utils import *
import OffsetCreator as oc

def detriangulize(structure, triangle):
    originalStruct = structure
    for i in range(0, len(structure)):
        point = structure[i]

        line = [structure[i-1], structure[i]]
        if all(point in triangle for point in line):
            #print("dupa triangle: " + str(triangle) + "\tstructure: " + str(structure) + "\tintersect: " + str(intersection(triangle, structure)))
            pointToAppend = difference(triangle, intersection(triangle, structure))
            #print ("difference: " + str(pointToAppend))
            if i == 0:
                #print ("dupa1 after diff: " + str(pointToAppend))
                structure.append(pointToAppend[0])
            else:
                structure.insert(i, pointToAppend[0])
            return structure


def generateStructFromCrossSection(crossSection):
    listOfFaces = crossSection.faces.tolist()
    structure = listOfFaces[0]
    listOfFaces.remove(listOfFaces[0])
    i = 1;
    while len(listOfFaces):
        generatedStruct = detriangulize(structure, listOfFaces[i])
        if generatedStruct is not None:
            structure = generatedStruct
            listOfFaces.remove(listOfFaces[i])
            i -= 1;
        i += 1;
        if i == len(listOfFaces):
            i = 0
    return structure
 
def removeDoubledPoints(primaryStructure, vertices):
    structure = list(primaryStructure)
    for i in range(0, len(primaryStructure)): 
        if vertices[primaryStructure[i-1]] == vertices[primaryStructure[i]]:
            structure.remove(primaryStructure[i])     
    return structure
            
def isThirdPointOnSameLine(p0, p1, p2):
    aCoe = (p0[y] - p2[y])/(p0[x] - p2[x]) 
    bCoe = p0[y] - aCoe * p0[x]
 #   print("p1[y]" + str(p1[y]) + "\taCoe*p1[x] + bCoe: " + str(aCoe*p1[x] + bCoe) + "\t T/F: " + str(oc.matchFloats(p1[y], (aCoe*p1[x] + bCoe))))
    return oc.matchFloats(p1[y], (aCoe*p1[x] + bCoe))
 
def removePointsOnSameLine(structure, vertices):
    newStructure = list(structure)

    for i in range(0, len(structure)):
        p0Index = structure[i-1]
        p1Index = structure[i]
        p2Index = structure[(i+1) % len(structure)]
        cond = False
        if oc.matchFloats(vertices[p0Index][x], vertices[p1Index][x], vertices[p2Index][x]) or oc.matchFloats(vertices[p0Index][y], vertices[p1Index][y],vertices[p2Index][y]) or isThirdPointOnSameLine(vertices[p0Index], vertices[p1Index], vertices[p2Index]):
            newStructure.remove(p1Index) 
            cond = True
        print("first: (" + str(vertices[p0Index][x]) + ", " + str(vertices[p0Index][y]) +  ")" + "\tsecond: (" + str(vertices[p1Index][x]) + ", " + str(vertices[p1Index][y]) + ")" + "\tthird: (" + str(vertices[p2Index][x]) + ", " + str(vertices[p2Index][y]) +  ")" + "\tT/F: " + str(cond)) 
    return newStructure

