import numpy as np

from mesh import Mesh
from point import Point


class DooSabinFace:
    def __init__(self):
        self.verts = []


class DooSabin:
    def triangulation(self):
        return False

    def run(self, org):
        mesh = Mesh()
        dsFaces = []

        for f in org.faces:
            dsFace = DooSabinFace()

            for v in f.verts:
                mesh.add_vertex(self.get_ds_point(v, f))
                dsFace.verts.append(mesh.verts[len(mesh.verts) - 1])

            dsFaces.append(dsFace)

        for f in dsFaces:
            v_size = len(f.verts)
            v_ids = [None] * v_size

            for i in range(v_size):
                v_ids[i] = f.verts[i].id_

            mesh.add_face(v_ids, v_size)

        for e in org.edges:
            if len(e.faces) == 2:
                dsf1 = dsFaces[e.faces[0].id_]
                dsf2 = dsFaces[e.faces[1].id_]

                mesh.add_face([
                    dsf1.verts[e.faces[0].get_vert_pos(e.verts[1])].id_,
                    dsf1.verts[e.faces[0].get_vert_pos(e.verts[0])].id_,
                    dsf2.verts[e.faces[1].get_vert_pos(e.verts[0])].id_,
                    dsf2.verts[e.faces[1].get_vert_pos(e.verts[1])].id_
                ], 4)

        for v in org.verts:
            f_size = len(v.faces)
            if len(v.edges) == f_size:
                v_idx = [0] * f_size
                v_itr = 0

                f = v.faces[0]

                while True:
                    v_idx[v_itr] = dsFaces[f.id_].verts[f.get_vert_pos(v)].id_
                    v_itr += 1
                    f = v.get_next_face_cc(f)
                    if f == v.faces[0]:
                        break

                mesh.add_face(v_idx, f_size)

        return mesh

    def get_ds_point(self, v, f):
        p = Point()

        v_size = len(f.verts)
        v_f_size = float(v_size)
        v_idx = f.get_vert_pos(v)

        for i in range(v_size):
            if i == v_idx:
                coeff = (5.0 + v_f_size) / (4.0 * v_f_size)
            else:
                    coeff = (3.0 + (2.0 * np.cos(6.2831853 * (float(v_idx - i) / v_f_size)))) / (4.0 * v_f_size)

            p = p + (f.verts[i].coords * coeff)

        return p
