import baseModelOperations





def genOptimizedMesh(baseModel, filename, millDiameter):
    model = moveToGround(baseModel)
    
    offset = baseOffset + millDiameter
    print("dupaGen")
    om.generateMeshOffsetFile(filename, offset, os.path.abspath("./Generated/StlOffset.stl"))


