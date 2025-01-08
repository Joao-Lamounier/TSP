import random


class Grasp:
    def __init__(self, graph, start_node, alpha, max_iter):
        self.graph = graph
        self.start_node = start_node
        self.alpha = alpha  # Parâmetro de aleatoriedade para construção
        self.max_iter = max_iter
        self.path = []
        self.objective_function = float('inf')
        self.run_time = 0.0

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

        return solution

    def calculate_distance(self, solution):
        total_cost = 0.0
        for i in range(len(solution) - 1):
            total_cost += self.graph.graph[solution[i], solution[i + 1]]
        total_cost += self.graph.graph[solution[-1], solution[0]]  # Retorna ao ponto de partida
        return total_cost

    def two_opt_best_improvement(self, inicial_solution):
        best_route = inicial_solution[:]
        best_distance = self.calculate_distance(inicial_solution)

        improved = True
        while improved:
            improved = False
            route = best_route[:]
            for i in range(0, self.graph.dimension - 1):
                for j in range(i + 1, self.graph.dimension):

                    new_route = route[:i] + list(reversed(route[i:j])) + route[j:]
                    new_distance = self.calculate_distance(new_route)

                    if new_distance < best_distance:
                        best_route = new_route
                        best_distance = new_distance
                        improved = True

        return best_route, best_distance

    def local_search(self, solution):
        # Realiza uma busca local usando a técnica 2-opt (best improvement)
        return self.two_opt_best_improvement(solution)

    def solve_grasp(self):
        for iteration in range(self.max_iter):
            # Fase Construtiva
            solution = self.greedy_randomized_construction()
            # Fase Busca Local
            solution, cost = self.local_search(solution)

            if cost < self.objective_function:
                self.path = solution
                self.objective_function = cost
