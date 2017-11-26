import collections
import random
from abc import ABC, abstractmethod

from triest.graph import EdgeSample
from triest.stream_graph import EdgeStreamElement, Symbol


class AbstractTriest(ABC):
    def __init__(self, edge_stream, M):
        self.edge_stream = edge_stream
        self.M = M
        self.S = EdgeSample()
        self.t = 0
        self.tau = 0
        self.local_tau = collections.defaultdict(int)

    @abstractmethod
    def run(self):
        for edge_stream_element in self.edge_stream:
            self.t += 1
            if isinstance(self, TriestImpr):
                self.update_counters(edge_stream_element)

            if self.should_sample_edge(self.t):
                self.S.append(edge_stream_element.edge)
                if isinstance(self, TriestBase):
                    self.update_counters(edge_stream_element)

    def should_sample_edge(self, t):
        if t <= self.M:
            return True
        elif self.flip_biased_coin(self.M / t):
            random_int = random.randint(0, len(self.S) - 1)
            random_edge = self.S.pop(random_int)

            if isinstance(self, TriestBase):
                new_stream_element = EdgeStreamElement(Symbol.MINUS, random_edge)
                self.update_counters(new_stream_element)
            return True
        return False

    def update_counters(self, edge_stream_element):
        shared_neighborhood = self.S.get_shared_neighborhood(edge_stream_element.edge)

        if isinstance(self, TriestBase):
            operator = 1 if edge_stream_element.symbol == Symbol.PLUS else -1
        elif isinstance(self, TriestImpr):
            operator = int(max(1, ((self.t - 1) * (self.t - 2)) / (self.M * (self.M - 1))))
        else:
            raise BaseException("Unsupported subclass algorithm: {}".format(self.__class__.__name__))

        for c in shared_neighborhood:
            self.tau += operator
            self.local_tau[c] += operator
            self.local_tau[edge_stream_element.edge.u] += operator
            self.local_tau[edge_stream_element.edge.v] += operator

    @staticmethod
    def flip_biased_coin(head_prob):
        return random.random() <= head_prob

    def triangles_estimation(self):
        if isinstance(self, TriestBase):
            xi = max(1, (self.t * (self.t - 1) * (self.t - 2)) / (self.M * (self.M - 1) * (self.M - 2)))
            return int(xi) * self.tau
        elif isinstance(self, TriestImpr):
            return self.tau
        else:
            raise BaseException("Unsupported subclass algorithm: {}".format(self.__class__.__name__))


class TriestBase(AbstractTriest):
    def run(self):
        super().run()


class TriestImpr(AbstractTriest):
    def run(self):
        super().run()
