import sys
sys.path.append('../Common/')

import dxfgrabber as dg

x = 0
y = 1

def getExtremeCoords(entities):
    lowestXY = [entities[0][0][x], entities[0][0][y]]
    highestXY = [entities[0][0][x], entities[0][0][y]]
    for entity in entities:
        if entity.dxftype == 'LWPOLYLINE':
            for point in entity:
                if point[x] > highestXY[x]:
                    highestXY[x] = point[x]
                if point[y] > highestXY[y]:
                    highestXY[y] = point[y]
                if point[x] < lowestXY[x]:
                    lowestXY[x] = point[x]
                if point[y] < lowestXY[y]:
                    lowestXY[y] = point[y]
    return lowestXY, highestXY 
                
        
        

def createPolyFromDxf(path, cutterDiameter):
    dxf = dg.readfile(path)

    lowestXY, highestXY = [], []
    for layer in dxf.layers:
        lowestXY, highestXY = getExtremeCoords(dxf.entities)
    midX = (lowestXY[x] + highestXY[x]) / 2
    midY = (lowestXY[y] + highestXY[y]) / 2
    print("mid: ", midX, midY, "lowestXY: ", lowestXY, "highest: ", highestXY)

    entityToLayerMap = {}
    for layer in dxf.layers:
        for entity in dxf.entities:
            if entity.layer == layer.name and entity.dxftype == 'LWPOLYLINE':
                print("before: ", entity[0])
                movedEntity = [[point[x] - midX, point[y] - lowestXY[y] + 2 * cutterDiameter] for point in entity] 
                print("after: ", movedEntity[0])
                if layer in entityToLayerMap:
                    entityToLayerMap[layer].append(movedEntity) 
                else:
                    entityToLayerMap.update({layer : [movedEntity]})
    return entityToLayerMap
