from src.entities.graph import Graph
from heuristics.NearestNeighbor import NearestNeighbor
import os
from time import perf_counter


if __name__ == '__main__':
    folder = 'files/benchmark'
    file_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.tsp')]

    solutions_path = 'optimal_solutions'

    lista = []

    for arquivo in file_list:

        graph = Graph.load_graph(arquivo)
        graph.start_node = 0

        graph.load_optimal_solution('optimal_solutions.txt')

        nn = NearestNeighbor(graph)

        inicio = perf_counter()
        nn.solve_nearest_neighbor()
        fim = perf_counter()

        nn.run_time = fim - inicio

        total = 0.0
        for i in range(len(nn.path) - 1):
            total += nn.graph.graph[nn.path[i], nn.path[i + 1]]

        lista.append(nn)

        print(nn.graph.name, total, nn.total_cost)

        # print(
        #     f'NAME: {nn.graph.name: <10} NN: {nn.total_cost: <20} BEST: {nn.graph.optimal_solution: <10}'
        #     f' RUN_TIME: {nn.run_time: <25} GAP: {Graph.gap_calc(nn.graph.optimal_solution, nn.total_cost)}'
        # )


