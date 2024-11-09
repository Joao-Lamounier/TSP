import os

from src.entities.graph import Graph

from src.heuristics.PrimPreorderMST import PrimPreorderMST

if __name__ == '__main__':
    folder = 'files/benchmark'
    file_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.tsp')]

    graph = Graph.load_graph(file_list[1])
    tsp_heuristic = PrimPreorderMST(graph)
    tsp_solution = tsp_heuristic.mst_heuristic()
    tsp_heuristic.show_solution(tsp_solution)
