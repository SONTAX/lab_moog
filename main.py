from doo_sabin import DooSabin
from mesh import Mesh
from visualize import visualize

method = DooSabin()
initial_mesh = Mesh()
initial_mesh.load_off("model.off", method.triangulation())
subdivided_mesh = method.run(initial_mesh)
print(f"Mesh has {len(subdivided_mesh.faces)} faces, {len(subdivided_mesh.verts)} verts, "
      f"{len(subdivided_mesh.edges)} edges.")

visualize(initial_mesh)
visualize(subdivided_mesh)
