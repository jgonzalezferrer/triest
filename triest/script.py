import random
import collections

from triest.stream_graph import EdgeStream, EdgeStreamElement, Symbol
from triest.graph import Graph, EdgeSample
open_file_as_graph = Graph.open_file_as_graph


class Triest:
    def __init__(self, edge_stream, M):
        self.edge_stream = edge_stream
        self.M = M
        self.S = EdgeSample()
        self.t = 0
        self.tau = 0
        self.local_tau = collections.defaultdict(int)

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


if __name__ == "__main__":

    file = '../data/out.arenas-jazz'
    graph = open_file_as_graph(file)
    edge_stream = EdgeStream(graph.edges)

    M = 3000
    tr = Triest(edge_stream.elements, M)

    tr.init()
    print(tr.triangles_estimation())
    print(tr.t)

    # if t <= M, then no error
    # if t > M, there is variance within the error

