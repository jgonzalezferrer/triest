from triest.algorithms import TriestBase, TriestImpr
from triest.graph import Graph

from triest.stream_graph import EdgeStream

open_file_as_graph = Graph.open_file_as_graph

if __name__ == "__main__":

    file = '../data/out.arenas-jazz'
    graph = open_file_as_graph(file)
    edge_stream = EdgeStream(graph.edges)

    M = 2500
    tb = TriestBase(edge_stream.elements, M)

    tb.run()
    print(tb.t)
    print(tb.triangles_estimation())

    ti = TriestImpr(edge_stream.elements, M)
    ti.run()
    print(ti.triangles_estimation())

    # if t <= M, then no error
    # if t > M, there is variance within the error
