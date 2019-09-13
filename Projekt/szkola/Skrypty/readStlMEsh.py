import numpy
import pymesh

# Using an existing stl file:
mesh = pymesh.load_mesh('C:/Users/SlawekFura/Desktop/Freya/Projekt/szkola/Biblioteka/Schody/schody_stl_p1.stl')
print(mesh.num_vertices, mesh.num_faces, mesh.num_voxels)