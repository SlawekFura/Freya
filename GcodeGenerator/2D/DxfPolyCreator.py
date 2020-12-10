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
    while entities[0].dxftype not in ['LWPOLYLINE', 'POINT']:
        entities = entities[1:]

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


def generateMovedPolyline(layer, midX, lowestXY, entity, offset):
    if "BOT" in layer:
        return [[-(point[x] - midX), point[y] - lowestXY[y] + offset] for point in entity]
    elif "TOP" in layer:
        return [[point[x] - midX, point[y] - lowestXY[y] + offset] for point in entity]
    else:
        sys.exit("Unsupported layer name: " + layer + "!")


def generateMovedPoint(layer, midX, lowestXY, entity, offset):
    if "BOT" in layer:
        return [[-(entity.point[x] - midX), entity.point[y] - lowestXY[y] + offset]]
    elif "TOP" in layer:
        return [[entity.point[x] - midX, entity.point[y] - lowestXY[y] + offset]]
    else:
        sys.exit("Unsupported layer name: " + layer + "!")


def createPolyAndConfigFromDxf(path, offset):
    dxf = dg.readfile(path)

    # for layer in dxf.layers:
    lowestXY, highestXY = getExtremeCoords(dxf.entities)

    midX = (lowestXY[x] + highestXY[x]) / 2
    entityToLayerMap = {}
    layerConfig = {}
    for entity in dxf.entities:
        if entity.dxftype == 'LWPOLYLINE':
            movedEntity = generateMovedPolyline(entity.layer, midX, lowestXY, entity, offset)
            if entity.is_closed:
                movedEntity.append(movedEntity[0])
            if entity.layer in entityToLayerMap:
                entityToLayerMap[entity.layer].append(movedEntity)
                continue
            entityToLayerMap.update({entity.layer: [movedEntity]})

        elif entity.dxftype == 'POINT':
            movedPoint = generateMovedPoint(entity.layer, midX, lowestXY, entity, offset)
            if entity.layer in entityToLayerMap:
                entityToLayerMap[entity.layer].append(movedPoint)
                continue
            entityToLayerMap.update({entity.layer: [movedPoint]})

        elif entity.dxftype == 'MTEXT':
            layerConfig = cg.ConfigGenerator().generate(entity.plain_text())

        elif entity.dxftype == 'LINE':
            print("Unsupported type of object: " + entity.dxftype + ", but continue")
        else:
            sys.exit("Unsupported type of object: " + entity.dxftype + "!")
    return entityToLayerMap, layerConfig
