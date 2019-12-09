import os

def writePolyCoordsMapIntoFile(fileToWrite, polylinesCoordMap):
    strToAdd = ""
    for key, value in sorted(polylinesCoordMap.items()):
        strToAdd += str(key) + "\n"
        index = 0;
        for polyline in value:
            strToAdd += "p" + "\n"
            index += 1
            for coords in polyline:
                strToAdd += "\t" + str(coords) + "\n"
    strToAdd += "p" + "\n"
    
    fileToWrite = open('MeshOffsetsMap','w')
    fileToWrite.write(strToAdd[:-1])
    fileToWrite.close()

def readPolysFromFile(filename):
    fileToRead = open(filename,'r')
    key = 0.0
    offsetPolygonsMap = {}
    polygon = []
    for line in fileToRead:
        firstChar = line[0]
        if firstChar.isdigit() or firstChar == '-':
            key = float(line)
        elif firstChar == "\t":
            point = line[1:-1].split(" ")
            point = [float(point[0]), float(point[1])]
            polygon.append([float(point[0]), float(point[1])])
        elif firstChar == "\n":
            if key in offsetPolygonsMap.keys():
                offsetPolygonsMap[key].append(list(polygon));
            else:
                offsetPolygonsMap.update({key : [list(polygon)]});
            polygon.clear()
    return offsetPolygonsMap
            
