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
                
        
        

def createPolyFromDxf(path, offset):
    dxf = dg.readfile(path)

    lowestXY, highestXY = [], []
    for layer in dxf.layers:
        lowestXY, highestXY = getExtremeCoords(dxf.entities)
    midX = (lowestXY[x] + highestXY[x]) / 2
    midY = (lowestXY[y] + highestXY[y]) / 2

    entityToLayerMap = {}
    for entity in dxf.entities:
        if entity.dxftype == 'LWPOLYLINE':
            layer = entity.layer
            if "BOT" in layer:
                movedEntity = [[-(point[x] - midX), point[y] - lowestXY[y] + offset] for point in entity]
            elif "TOP" in layer:
                movedEntity = [[point[x] - midX, point[y] - lowestXY[y] + offset] for point in entity] 
            else:
                sys.exit("Unsupported layer name: " + layer + "!")

            if entity.is_closed:
                movedEntity.append(movedEntity[0])
                
            if layer in entityToLayerMap:
                entityToLayerMap[layer].append(movedEntity) 
            else:
                entityToLayerMap.update({layer : [movedEntity]})
        elif entity.dxftype == 'POINT':
            layer = entity.layer
            if "BOT" in layer:
                movedEntity = [[-(entity.point[x] - midX), entity.point[y] - lowestXY[y] + offset]]
            elif "TOP" in layer:
                movedEntity = [[entity.point[x] - midX, entity.point[y] - lowestXY[y] + offset]]
            else:
                sys.exit("Unsupported layer name: " + layer + "!")

            if layer in entityToLayerMap:
                entityToLayerMap[layer].append(movedEntity) 
            else:
                entityToLayerMap.update({layer : [movedEntity]})
        else:
            sys.exit("Unsupported type of object: " + entity.dxftype + "!")
    return entityToLayerMap
