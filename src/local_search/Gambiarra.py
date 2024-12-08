import os
from time import perf_counter

from src.intervalo_confianca import ConfidenceInterval
from src.graphic_run_time import Graphic
from src.heuristics.NearestNeighbor import NearestNeighbor
from src.entities.graph import Graph


# from src.heuristics.PrimPreOrderMST import PrimPreOrderMST
# from src.heuristics.Insertion import Insertion


def gap(objective_function, optimal_solution):
    return 100 * ((objective_function - optimal_solution) / optimal_solution)


# Função para calcular a distância total, considerando o retorno ao nó inicial
def calculate_distance(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i], route[i + 1]]
    total_distance += distance_matrix[route[-1], route[0]]
    return total_distance


def two_opt(route, distance_matrix, best_distance):

    n = len(route)

    # Loop de busca local
    improved_counter = 0
    improved = True
    while improved:
        improved = False
        for i in range(0, n - 1):
            for j in range(i + 2, n):

                new_route = route[:i] + list(reversed(route[i:j])) + route[j:]  # Opção 1
                # new_route = route[:i + 1] + list(reversed(route[i + 1:j + 1])) + route[j + 1:]  # Opção 2
                new_distance = calculate_distance(new_route, distance_matrix)

                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
                    improved = True
                    improved_counter += 1

    return route, best_distance


def delete_and_insert(route, distance_matrix, best_distance):

    n = len(route)

    improved_counter = 0
    improved = True
    while improved:
        improved = False
        for i in range(0, n - 1):
            for j in range(i + 1, n):

                new_route = route[:]

                # Remove o elemento no índice i
                node = new_route.pop(i)
                # Insere o valor na posição j
                new_route.insert(j, node)

                new_distance = calculate_distance(new_route, distance_matrix)

                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
                    improved = True
                    improved_counter += 1

    return route, best_distance


def reverse(route, distance_matrix, best_distance):

    n = len(route)

    improved_counter = 0
    improved = True
    while improved:
        improved = False
        for i in range(0, n - 1):
            for j in range(i + 1, n):

                new_route = route[:]

                new_route[i:j + 1] = new_route[i:j + 1][::-1]

                new_distance = calculate_distance(new_route, distance_matrix)

                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
                    improved = True
                    improved_counter += 1

    return route, best_distance


if __name__ == '__main__':

    folder = '../files/benchmark'
    file_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.tsp')]

    run_time = []
    gaps = []

    for arquivo in file_list:

        graph = Graph.load_graph(arquivo)
        graph.load_optimal_solution('../optimal_solutions.txt')
        # graph.start_node = 0

        tsp_solver = NearestNeighbor(graph, 0)

        begin_1 = perf_counter()
        tsp_solver.solve_nearest_neighbor()
        end_1 = perf_counter()

        # tsp_solver = PrimPreOrderMST(graph)
        # tsp_solver.solve_prim_pre_order_mst()

        # tsp_solver = Insertion(graph)
        # tsp_solver.solve_insertion()

        begin_2 = perf_counter()
        # route, best_distance = two_opt(tsp_solver.path, tsp_solver.graph.graph, tsp_solver.total_cost)
        route, best_distance = delete_and_insert(tsp_solver.path, tsp_solver.graph.graph, tsp_solver.total_cost)
        end_2 = perf_counter()

        time = (end_1 - begin_1) + (end_2 - begin_2)

        print(
                f'NAME: {graph.name: <10} LS_2-OPT: {best_distance: <20} BEST: {graph.optimal_solution: <10}'
                f' RUN_TIME: {time: <25} GAP: {gap(best_distance, graph.optimal_solution)}'
        )

        run_time.append(time)
        gaps.append(gap(graph.optimal_solution, best_distance))

    graphic = Graphic('2-OPT', run_time)
    Graphic.plot_graphic(graphic, graphic, graphic)

    graphic_ic = ConfidenceInterval(gaps)
    ConfidenceInterval.calculate_ci(gaps)
