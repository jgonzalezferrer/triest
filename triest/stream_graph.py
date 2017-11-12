from enum import Enum


class Symbol(Enum):
    PLUS = 1
    MINUS = 2


class EdgeStream:
    def __init__(self, raw_edges):
        self.raw_edges = raw_edges
        self.elements = self.convert_raw_edges()

    def convert_raw_edges(self):
        elements = [None]*len(self.raw_edges)
        for i, edge in enumerate(self.raw_edges):
            elements[i] = EdgeStreamElement(Symbol.PLUS, edge)

        return elements


class EdgeStreamElement:
    def __init__(self, symbol, edge):
        self.symbol = symbol
        self.edge = edge

    def __str__(self):
        return "({}, ({}, {}))".format(self.symbol, self.edge.u, self.edge.v)

    def __repr__(self):
        return str(self)
