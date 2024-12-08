import os
from time import perf_counter

from src.intervalo_confianca import ConfidenceInterval
from src.graphic_run_time import Graphic
from src.heuristics.NearestNeighbor import NearestNeighbor
from src.entities.graph import Graph
import matplotlib.pyplot as plt


# from src.heuristics.PrimPreOrderMST import PrimPreOrderMST
# from src.heuristics.Insertion import Insertion


def box_plot(dados):
    # Criando o boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot(dados, tick_labels=['2-OPT', 'REVERSE', '3-OPT'], patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='red', linewidth=1.5),
                whiskerprops=dict(color='blue'),
                capprops=dict(color='blue'),
                flierprops=dict(marker='o', color='blue', alpha=0.5))

    # Adicionando título e rótulos
    plt.title('Boxplot de Gaps dos Algoritmos de Busca Local', fontsize=14)
    plt.ylabel('Gap', fontsize=12)
    plt.xlabel('Busca Local', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Mostrando o gráfico
    plt.tight_layout()
    plt.show()


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

    start_node = 0

    run_time_1 = []
    run_time_2 = []
    run_time_3 = []

    gaps_1 = []
    gaps_2 = []
    gaps_3 = []

    for arquivo in file_list:

        graph = Graph.load_graph(arquivo)
        graph.load_optimal_solution('../optimal_solutions.txt')

        tsp_solver = NearestNeighbor(graph, start_node)
        # tsp_solver = PrimPreOrderMST(graph, start_node)
        # tsp_solver = Insertion(graph, start_node)

        # Nearest Neighbor
        begin_11 = perf_counter()
        tsp_solver.solve_nearest_neighbor()
        end_11 = perf_counter()

        begin_21 = perf_counter()
        route_1, best_distance_1 = two_opt(tsp_solver.path, tsp_solver.graph.graph, tsp_solver.total_cost)
        end_21 = perf_counter()

        begin_22 = perf_counter()
        route_2, best_distance_2 = reverse(tsp_solver.path, tsp_solver.graph.graph, tsp_solver.total_cost)
        end_22 = perf_counter()

        begin_33 = perf_counter()
        route_3, best_distance_3 = delete_and_insert(tsp_solver.path, tsp_solver.graph.graph, tsp_solver.total_cost)
        end_33 = perf_counter()

        time_1 = (end_11 - begin_11) + (end_21 - begin_21)
        time_2 = (end_11 - begin_11) + (end_22 - begin_22)
        time_3 = (end_11 - begin_11) + (end_33 - begin_33)

        # print(
        #         f'NAME: {graph.name: <15} LS_2-Opt: {best_distance_1: <20} BEST: {graph.optimal_solution: <10}'
        #         f' RUN_TIME: {time_1: <25} GAP: {gap(best_distance_1, graph.optimal_solution)}'
        # )

        print(
            f'NAME: {graph.name: <15} LS_Rev: {best_distance_2: <20} BEST: {graph.optimal_solution: <10}'
            f' RUN_TIME: {time_2: <25} GAP: {gap(best_distance_2, graph.optimal_solution)}'
        )
        #
        # print(
        #     f'NAME: {graph.name: <15} LS_DnI: {best_distance_3: <20} BEST: {graph.optimal_solution: <10}'
        #     f' RUN_TIME: {time_3: <25} GAP: {gap(best_distance_3, graph.optimal_solution)}'
        # )

        run_time_1.append(time_1)
        run_time_2.append(time_2)
        run_time_3.append(time_3)

        gaps_1.append(gap(best_distance_1, graph.optimal_solution))
        gaps_2.append(gap(best_distance_2, graph.optimal_solution))
        gaps_3.append(gap(best_distance_3, graph.optimal_solution))

    graphic_1 = Graphic('RUN TIME - 2-OPT', run_time_1)
    graphic_2 = Graphic('RUN TIME - REVERSE', run_time_2)
    graphic_3 = Graphic('RUN TIME - DELETE AND INSERT', run_time_3)

    Graphic.plot_graphic(graphic_1, graphic_2, graphic_3)

    ConfidenceInterval.calculate_ci(gaps_1, '2-OPT')
    ConfidenceInterval.calculate_ci(gaps_2, 'REVERSE')
    ConfidenceInterval.calculate_ci(gaps_3, 'DELETE AND INSERT')

    box_plot([gaps_1, gaps_2, gaps_3])
