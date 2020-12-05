import sys

sys.path.append('../Common/')

import dxfgrabber as dg
import ConfigGenerator as cg

x = 0
y = 1


def getExtremes(highestXY, lowestXY, point):
    return [max(highestXY[x], point[x]), max(highestXY[y], point[y])], \
           [min(lowestXY[x], point[x]), min(lowestXY[y], point[y])]


def getExtremeCoords(entities):
    lowestXY = []
    highestXY = []
    if entities[0].dxftype == 'LWPOLYLINE':
        lowestXY = highestXY = [entities[0][0][x], entities[0][0][y]]
    elif entities[0].dxftype == 'POINT':
        lowestXY = highestXY = [entities[0].point[x], entities[0].point[y]]

    print("len :", len(entities))
    for entity in entities:
        if entity.dxftype == 'LWPOLYLINE':
            for point in entity:
                highestXY, lowestXY = getExtremes(highestXY, lowestXY, point)

        elif entity.dxftype == 'POINT':
            highestXY, lowestXY = getExtremes(highestXY, lowestXY, entity.point)

    return lowestXY, highestXY


def createPolyAndConfigFromDxf(path, offset):
    dxf = dg.readfile(path)

    lowestXY, highestXY = [], []
    # for layer in dxf.layers:
    lowestXY, highestXY = getExtremeCoords(dxf.entities)

    midX = (lowestXY[x] + highestXY[x]) / 2
    midY = (lowestXY[y] + highestXY[y]) / 2
    entityToLayerMap = {}
    layerConfig = {}
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
                entityToLayerMap.update({layer: [movedEntity]})
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
                entityToLayerMap.update({layer: [movedEntity]})
        elif entity.dxftype == 'MTEXT':
            print("dupa")
            layerConfig = cg.ConfigGenerator().generate(entity.plain_text())

        elif entity.dxftype == 'LINE':
            print("Unsupported type of object: " + entity.dxftype + ", but continue")
        else:
            sys.exit("Unsupported type of object: " + entity.dxftype + "!")
    return entityToLayerMap, layerConfig
