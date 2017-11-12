class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v

    def __str__(self):
        return "({}, {})".format(self.u, self.v)

    def __repr__(self):
        return str(self)


class EdgeSample:
    def __init__(self):
        self.S = []

    def __len__(self):
        return len(self.S)

    def append(self, elem):
        self.S.append(elem)

    def pop(self, ind):
        return self.S.pop(ind)

    def get_shared_neighborhood(self, edge):
        neighborhood_u = self._get_neighborhood(edge.u)
        neighborhood_v = self._get_neighborhood(edge.v)

        shared_neighborhood = neighborhood_u.intersection(neighborhood_v)
        return shared_neighborhood

    def _get_neighborhood(self, node):
        neighborhood = set()
        for elem in self.S:
            if elem.u == node:
                neighborhood.add(elem.v)
            elif elem.v == node:
                neighborhood.add(elem.u)

        return neighborhood


class Vertex:
    def __init__(self, n):
        self.n = n

    def __str__(self):
        return self.n

    def __repr__(self):
        return str(self)


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

    @staticmethod
    def open_file_as_graph(filename):
        vertices = set()
        edges = []

        with open(filename) as f:
            content = f.read()
            for line in content.splitlines():
                if line.startswith('%'):
                    continue

                info = line.split()
                edges.append(Edge(info[0], info[1]))
                vertices.add(info[0])
                vertices.add(info[1])

        return Graph(list(vertices), edges)
