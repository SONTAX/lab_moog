from meshdata import MeshData, Face, Edge, Vertex
from point import Point, distance


class Mesh:
    def __init__(self):
        self.faces = []
        self.edges = []
        self.verts = []

    def add_face(self, vertices, side_count):
        face = Face(len(self.faces))
        for i in range(side_count):
            v = self.verts[vertices[i]]
            v_next = self.verts[i + 1 if i < (side_count - 1) else 0]

            face.verts.append(v)
            v.faces.append(face)

            v_next_pos = v.get_vert_pos(v_next)

            if v_next_pos == -1:
                edge = self.add_edge(v, v_next)
            else:
                edge = v.edges[v_next_pos]
                face.faces.append(edge.faces[0])
                edge.faces[0].faces.append(face)

            face.edges.append(edge)
            edge.faces.append(face)

            if i > 0:
                edge.edges.append(face.edges[i - 1])
            else:
                face.edges[0].edges.append(edge)

        self.faces.append(face)

    def add_vertex(self, p):
        self.verts.append(Vertex(len(self.verts), p))

    def add_edge(self, v1, v2):
        v1.verts.append(v2)
        v2.verts.append(v1)

        edge = Edge(len(self.edges), distance(v1.coords, v2.coords))

        self.edges.append(edge)

        v1.edges.append(edge)
        v2.edges.append(edge)

        edge.verts.append(v1)
        edge.verts.append(v2)

        return edge

    def sort_counter_clockwise(self):
        for v in self.verts:
            f = v.faces[0]
            e_itr = 0
            e_pos = 0
            while True:
                e1 = None
                e2 = None

                for e in f.edges:
                    if e.get_vert_pos(v) != -1:
                        if e1 == None:
                            e1 = e
                        else:
                            e2 = e

                edge = e1 if f.get_next_edge(e1) == e2 else e2
                e_pos = v.get_edge_pos(edge)

                if e_pos != e_itr:
                    temp = v.edges[e_pos]
                    v.edges[e_pos] = v.edges[e_itr]
                    v.edges[e_itr] = temp
                    temp = v.verts[e_pos]
                    v.verts[e_pos] = v.verts[e_itr]
                    v.verts[e_itr] = temp
                    e_itr += 1

                temp = v.faces[e_pos]
                v.faces[e_pos] = v.faces[v.get_face_pos(f)]
                v.faces[v.get_face_pos(f)] = temp

                if len(edge.faces) == 2:
                    f = edge.faces[1 if f == edge.faces[0] else 0]
                else:
                    f = v.faces[0]

                if f == v.faces[0]:
                    break

    def load_off(self, filepath, quad_to_tri):
        f = open(filepath, "r")
        f.readline()
        vert_size, face_size, dummy = list(map(int, f.readline().split()))

        for i in range(vert_size):
            x, y, z = list(map(float, f.readline().split()))
            self.add_vertex(Point(x, y, z))

        if quad_to_tri:
            for i in range(face_size):
                v_ids = list(map(int, f.readline().split()))[1:]
                self.add_face([v_ids[0], v_ids[1], v_ids[2]], 3)
                self.add_face([v_ids[0], v_ids[2], v_ids[3]], 3)

        else:
            for i in range(face_size):
                v_ids = list(map(int, f.readline().split()))[1:]
                self.add_face(v_ids, 4)

        print(f"Mesh has {len(self.faces)} faces, {len(self.verts)} verts, {len(self.edges)} edges.")
        f.close()
