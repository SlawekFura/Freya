import xml.etree.ElementTree as ET

def readLayerConfig(filename):
    layerConfig = {}
        
    configToRead = open(filename,'r')
    layerToAdd = ""
    configToAdd = []
    for line in configToRead:
        firstChar = line[0]
        if firstChar != '\t' and firstChar != '\n':
            if configToAdd:
                layerConfig.update({layerToAdd : configToAdd}) 
                configToAdd.clear()
            layerToAdd = line 
        elif firstChar == '\t':  
            configToAdd.append(line)

    if configToAdd:
        layerConfig.update({layerToAdd : configToAdd}) 

    return layerConfig
            


