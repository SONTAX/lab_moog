class MeshData:
    def __init__(self, id_):
        self.id_ = id_
        self.faces = []
        self.edges = []
        self.verts = []

    def get_face_by_id(self, index):
        for i in range(len(self.faces)):
            if self.faces[i].id_ == index:
                return self.faces[i]
        return None

    def get_edge_by_id(self, index):
        for i in range(len(self.edges)):
            if self.edges[i].id_ == index:
                return self.edges[i]
        return None

    def get_vert_by_id(self, index):
        for i in range(len(self.verts)):
            if self.verts[i].id_ == index:
                return self.verts[i]
        return None

    def get_face_pos(self, face):
        for i in range(len(self.faces)):
            if self.faces[i] == face:
                return i
        return -1

    def get_edge_pos(self, edge):
        for i in range(len(self.edges)):
            if self.edges[i] == edge:
                return i
        return -1

    def get_vert_pos(self, vert):
        for i in range(len(self.verts)):
            if self.verts[i] == vert:
                return i
        return -1

    def get_next_face(self, face):
        pos = self.get_face_pos(face)
        return self.faces[pos + 1 if pos < len(self.faces) - 1 else 0]

    def get_next_edge(self, edge):
        pos = self.get_edge_pos(edge)
        return self.edges[pos + 1 if pos < len(self.edges) - 1 else 0]

    def get_next_vert(self, vert):
        pos = self.get_vert_pos(vert)
        return self.verts[pos + 1 if pos < len(self.verts) - 1 else 0]

    def get_prev_face(self, face):
        pos = self.get_face_pos(face)
        return self.faces[len(self.faces) - 1 if pos == 0 else pos - 1]

    def get_prev_edge(self, edge):
        pos = self.get_edge_pos(edge)
        return self.edges[len(self.edges) - 1 if pos == 0 else pos - 1]

    def get_prev_vert(self, vert):
        pos = self.get_vert_pos(vert)
        return self.verts[len(self.verts) - 1 if pos == 0 else pos - 1]


class Face(MeshData):
    def __init__(self, id_):
        super().__init__(id_)

    def __eq__(self, other):
        if isinstance(other, Face):
            return self.id_ == other.id_
        return False


class Edge(MeshData):
    def __init__(self, id_, length):
        super().__init__(id_)
        self.length = length

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.id_ == other.id_
        return False


class Vertex(MeshData):
    def __init__(self, id_, coords):
        super().__init__(id_)
        self.coords = coords

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.id_ == other.id_
        return False

    def get_next_vert_cc(self, v):
        for f in self.faces:
            if f.get_next_vert(self) == v:
                return f.get_prev_vert(self)

        for f in self.faces:
            vn = f.get_next_vert(self)
            if len(vn.verts) != len(vn.faces):
                return vn

        return None

    def get_next_edge_cc(self, e):
        for f in e.faces:
            e_prev = f.get_prev_edge(e)
            if e_prev.get_vert_pos(self) != -1:
                return e_prev

        for en in self.edges:
            if len(en.faces) != 2 and en != e:
                return en

        return None

    def get_next_face_cc(self, f):
        for e in self.edges:
            if len(e.faces) == 2:
                if (e.verts[0] == self and e.faces[1] == f) or (e.verts[1] == self and e.faces[0] == f):
                    return e.faces[1] if e.faces[0] == f else e.faces[0]

        for e in self.edges:
            if len(e.faces) != 2 and f.get_edge_pos(e) == -1:
                return e.faces[0]

        return None
