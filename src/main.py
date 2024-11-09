from src.entities.graph import Graph
from heuristics.NearestNeighbor import NearestNeighbor
import os
from time import perf_counter


if __name__ == '__main__':
    folder = 'files/benchmark'
    file_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.tsp')]

    for arquivo in file_list:
        graph = Graph.load_graph(arquivo)
        nn = NearestNeighbor(graph)

        inicio = perf_counter()
        nn.solve_nearest_neighbor(0)
        fim = perf_counter()

        nn.run_time = fim - inicio

        print(graph.name, nn.total_distance, nn.run_time)
