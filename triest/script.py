import random
import collections

from enum import Enum


class Symbol(Enum):
    PLUS = 1
    MINUS = 2


class EdgeStreamElement:
    def __init__(self, symbol, edge):
        self.symbol = symbol
        self.edge = edge


class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v


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
        return neighborhood_u.intersect(neighborhood_v)

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

    def triest_base(self):
        for edge_stream_element in self.edge_stream:
            self.t += 1
            if self.sample_edge(edge_stream_element.edge, self.t):
                self.S.append(edge_stream_element.edge)
                self.update_counters(Symbol.PLUS, edge_stream_element)

    def sample_edge(self, edge, t):
        if t <= self.M:
            return True
        elif self.flip_biased_coin(self.M/t):
            random_int = random.randint(0, len(self.S)-1)
            random_edge = self.S.pop(random_int)

            new_stream_element = EdgeStreamElement(Symbol.MINUS, random_edge)
            self.update_counters(Symbol.MINUS, new_stream_element)
            return True
        return False

    def update_counters(self, symbol, edge_stream_element):
        shared_neighborhood = self.S.get_shared_neighborhood(edge_stream_element.edge)
        operator = 1 if symbol == Symbol.PLUS else -1

        for c in shared_neighborhood:
            self.tau += operator
            self.local_tau[c] += operator
            self.local_tau[edge_stream_element.edge.u]
            self.local_tau[edge_stream_element.edge.v]

    @staticmethod
    def flip_biased_coin(head_prob):
        return random.random() <= head_prob


