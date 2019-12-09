import xml.etree.ElementTree as ET

numOfSavedModels = 0
smallestDiscLength = 0.8

x = 0
y = 1
z = 2
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def match2FloatLists(floatList1, floatList2):
    for i in range(len(floatList1)):
        if not isclose(floatList1[i], floatList2[i], abs_tol = 0.001):
            return False
    return True

def getCutterConfig(cutterType, material, millDiameter):
    root = ET.parse("../../Configs/tools/Cutters.xml").getroot()
    return root.findall("type_"      + str(cutterType) + 
                        "/"          + material + 
                        "/diameter_" + str(millDiameter) +
                        "/params")

