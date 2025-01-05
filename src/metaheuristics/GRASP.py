import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from time import perf_counter
import random

from src.local_search.TwoOpt import TwoOpt
from src.entities.graph import Graph

class Grasp:
    def __init__(self, graph, start_node, alpha=0.5, max_iter=15):
        self.graph = graph
        self.start_node = start_node  # Nó inicial fornecido como parâmetro
        self.alpha = alpha  # Parâmetro de aleatoriedade para construção
        self.max_iter = max_iter  # Número máximo de iterações
        self.best_solution = None
        self.best_cost = float('inf')

    def greedy_randomized_construction(self):
        solution = [self.start_node]  # Começa a solução a partir do nó inicial
        candidate_set = set(range(self.graph.dimension))
        candidate_set.remove(self.start_node)  # Remove o nó inicial do conjunto de candidatos

        current_node = self.start_node

        while len(solution) < self.graph.dimension:
            candidate_costs = []
            for node in candidate_set:
                cost = self.graph.graph[current_node, node]  # Cálculo do custo incremental
                candidate_costs.append((node, cost))

            # Ordena candidatos com base no custo
            candidate_costs.sort(key=lambda x: x[1])
            min_cost = candidate_costs[0][1]
            max_cost = candidate_costs[-1][1]

            # Cria a RCL (Lista de Candidatos Restritos)
            rcl = [node for node, cost in candidate_costs if cost <= min_cost + self.alpha * (max_cost - min_cost)]
            selected_node = random.choice(rcl)  # Escolhe aleatoriamente da RCL
            solution.append(selected_node)
            candidate_set.remove(selected_node)
            current_node = selected_node

        # Cálculo do custo da solução construída
        #cost = self.calculate_cost(solution)
        #print(f"Custo da solução construída: {cost}")  # Print do custo após a fase construtiva
        return solution

    def local_search(self, solution):
        # Realiza uma busca local usando a técnica de 3-opt
        best_solution = solution[:]
        best_cost = self.calculate_cost(solution)

        #print(f"Iniciando a busca local com custo: {best_cost}")  # Print do custo inicial

        # Criação do objeto ThreeOpt
        three_opt_solver = TwoOpt(self.graph.graph, 100, best_solution, best_cost)

        # Resolve com o 3-opt
        improved_solution, improved_cost = three_opt_solver.solve_two_opt()

        # Verifica se houve melhoria
        if improved_cost < best_cost:
            best_solution = improved_solution
            best_cost = improved_cost

        #print(f"Custo da solução após busca local com 2-opt: {best_cost}")  # Print do custo após a busca local
        return best_solution, best_cost

    def calculate_cost(self, solution):
        # Calcula o custo total de uma solução (soma das distâncias entre os nós)
        cost = 0
        for i in range(len(solution) - 1):
            cost += self.graph.graph[solution[i], solution[i + 1]]
        cost += self.graph.graph[solution[-1], solution[0]]  # Retorna ao ponto de partida
        return cost

    def run(self):
        best_iteration = 1

        for iteration in range(self.max_iter):
            begin = perf_counter()
            #print(f"\nIteração {iteration + 1}:")
            # Fase Construtiva
            solution = self.greedy_randomized_construction()
            # Fase Busca Local
            solution, cost = self.local_search(solution)

            # Atualiza a melhor solução encontrada
            if cost < self.best_cost:
                self.best_solution = solution
                self.best_cost = cost
                best_iteration = iteration + 1

            #print(f"Melhor custo até agora: {self.best_cost}")  # Print do melhor custo encontrado
            end = perf_counter()
        return self.best_solution, self.best_cost


if __name__ == '__main__':

    folder = '../files/benchmark'
    file_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.tsp')]

    for arquivo in file_list:

        if arquivo in ['../files/benchmark\\berlin52.tsp', '../files/benchmark\\eil51.tsp',
                       '../files/benchmark\\eil76.tsp', '../files/benchmark\\pr76.tsp',
                       '../files/benchmark\\st70.tsp']:

            for i in range(10):

                graph = Graph.load_graph(arquivo)
                graph.load_optimal_solution('../optimal_solutions.txt')
                graph.start_node = 0

                grasp = Grasp(graph, 0)

                begin = perf_counter()
                best_tour, best_cost = grasp.run()
                end = perf_counter()

                # print(
                #     f'NAME: {graph.name: <10} GRASP: {grasp.best_cost: <20} BEST: {graph.optimal_solution: <10}'
                #     f' RUN_TIME: {end - begin: <25} GAP: '
                #     f'{100 * ((grasp.best_cost - graph.optimal_solution) / graph.optimal_solution)} '
                #     # f'ITERAÇÃO: {best_iteration}'
                # )
                print(
                    f"{graph.name + '.tsp': <15}{'GRASP-15-0.5': <15}{'15-0.5': <10}{grasp.best_cost: <20}"
                    f"{end - begin: <25}{100 * ((grasp.best_cost - graph.optimal_solution) / graph.optimal_solution): <20}"
                    f"{graph.dimension: <10}{graph.arcs: <5}"
                )