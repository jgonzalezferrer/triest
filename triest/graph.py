class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v

    def __str__(self):
        return "({}, {})".format(self.u, self.v)

    def __repr__(self):
        return str(self)


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



