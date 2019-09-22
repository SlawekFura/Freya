from OffsetCreator import *

#mesh = pymesh.load_mesh("schody_stl_p2_rotated.stl")
mesh = pymesh.load_mesh("schody_stl_p2.stl")
print(mesh.bbox)

numOfSlices = getNumOfSlices(mesh)
crossSections = pymesh.slice_mesh(mesh, np.array([0, 0, 1], np.int32), numOfSlices * 3)
offsetGen = OffsetGenerator(mesh, 0.1)
offsetStructuresMap = offsetGen.genOffsetMap()
for elem in offsetStructuresMap:
    print(elem, offsetStructuresMap.get(elem))
offsetGen.printResults()

