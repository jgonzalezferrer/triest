import random
import collections

from enum import Enum


class Symbol(Enum):
    PLUS = 1
    MINUS = 2


class EdgeStream:
    def __init__(self, raw_edges):
        self.edges = self.convert_raw_edges(edges)

    def convert_raw_edges(self, raw_edges):
        edges = [None]*len(raw_edges)
        for i, edge in enumerate(raw_edges):
            edges[i] = EdgeStreamElement(Symbol.PLUS, edge)
        return edges


class EdgeStreamElement:
    def __init__(self, symbol, edge):
        self.symbol = symbol
        self.edge = edge

    def __str__(self):
        return "({}, ({}, {}))".format(self.symbol, self.edge.u, self.edge.v)

    def __repr__(self):
        return str(self)


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


class Triest:
    def __init__(self, edge_stream, M):
        self.edge_stream = edge_stream
        self.M = M
        self.S = EdgeSample()
        self.t = 0
        self.tau = 0
        self.local_tau = collections.defaultdict(int)
        self.caca = 0

    def init(self):
        for edge_stream_element in self.edge_stream:
            self.t += 1
            if self.sample_edge(edge_stream_element.edge, self.t):
                self.S.append(edge_stream_element.edge)
                self.update_counters(edge_stream_element)

    def sample_edge(self, edge, t):
        if t <= self.M:
            return True
        elif self.flip_biased_coin(self.M/t):
            random_int = random.randint(0, len(self.S)-1)
            random_edge = self.S.pop(random_int)

            new_stream_element = EdgeStreamElement(Symbol.MINUS, random_edge)
            self.update_counters(new_stream_element)
            return True
        return False

    def update_counters(self, edge_stream_element):
        shared_neighborhood = self.S.get_shared_neighborhood(edge_stream_element.edge)
        operator = 1 if edge_stream_element.symbol == Symbol.PLUS else -1

        for c in shared_neighborhood:
            self.tau += operator
            self.local_tau[c] += operator
            self.local_tau[edge_stream_element.edge.u] += operator
            self.local_tau[edge_stream_element.edge.v] += operator

    @staticmethod
    def flip_biased_coin(head_prob):
        return random.random() <= head_prob

    def triangles_estimation(self):
        estimation = (self.t * (self.t - 1) * (self.t - 2)) / (self.M * (self.M - 1) * (self.M - 2))
        xi = int(max(1, estimation))
        return xi * self.tau


def open_file_as_graph(filename):
    edges = []
    with open(filename) as f:
        content = f.read()

        for i, line in enumerate(content.splitlines()):
            if line.startswith('%'): continue
            info = line.split()

            edges.append(Edge(info[0], info[1]))

    return edges

if __name__ == "__main__":
    file = '../data/out.arenas-jazz'
    edges = open_file_as_graph(file)
    edges_stream = EdgeStream(edges)

    # print(edges_stream.edges)
    M = 3000
    tr = Triest(edges_stream.edges, M)

    tr.init()
    print(tr.triangles_estimation())
    print(tr.t)

    # if t <= M, then no error
    # if t > M, there is variance within the error

