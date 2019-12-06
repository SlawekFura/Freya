import xml.etree.ElementTree as ET

numOfSavedModels = 0

def getCutterConfig(cutterType, material, millDiameter):
    root = ET.parse("../../Configs/tools/Cutters.xml").getroot()
    return root.findall("type_"      + str(cutterType) + 
                        "/"          + material + 
                        "/diameter_" + str(millDiameter) +
                        "/params")

