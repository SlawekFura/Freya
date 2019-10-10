import sys
sys.path.append('../Common/')

import dxfgrabber as dg
import GcodeCommandGenerator as gg


dxf = dg.readfile("../TestFiles/DuzaSala2.dxf")

for layer in dxf.layers:
    print("layer: ", layer.name)


for entity in dxf.entities:
    print("entity: ", entity.dxftype, "\tlayer: ", entity.layer)

entityToLayerMap = {}

for layer in dxf.layers:
    for entity in dxf.entities:
        if entity.layer == layer.name and entity.dxftype == 'LWPOLYLINE':
            if layer in entityToLayerMap:
                entityToLayerMap[layer].append(entity) 
            else:
                entityToLayerMap.update({layer : [entity]})

for key, val in entityToLayerMap.items():
    print("layer: ", key.name) 
    for entity in val:
        print("\tentity: ", entity)

gg.genGcode2D(".gcode", entityToLayerMap)
