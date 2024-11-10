

class NearestNeighbor:

    def __init__(self, graph):
        """Inicializa o problema TSP com o grafo fornecido."""

        self.graph = graph
        self.path = []
        self.total_cost = 0.0
        self.run_time = 0.0

    def __str__(self):
        return f"Caminho: {self.path}\nDistância total: {self.total_cost}"

    def solve_nearest_neighbor(self):
        """ Resolve o problema do Caixeiro Viajante (TSP) usando o Nearest Neighbor Algorithm.
            Retorna o custo total do ciclo TSP."""
        visited = [False] * self.graph.dimension
        current_node = self.graph.start_node
        self.path = [current_node]
        visited[current_node] = True
        self.total_cost = 0.0

        for _ in range(self.graph.dimension):
            nearest_distance = float('inf')
            nearest_node = None

            # Encontra o vizinho mais próximo não visitado
            for next_node in range(self.graph.dimension):
                if not visited[next_node] and self.graph.graph[current_node, next_node] < nearest_distance:
                    nearest_distance = self.graph.graph[current_node, next_node]
                    nearest_node = next_node

            # Atualiza a distância total e o caminho
            if nearest_node is not None:
                self.path.append(nearest_node)
                self.total_cost += nearest_distance
                visited[nearest_node] = True
                current_node = nearest_node

        # Retorna ao nó inicial para completar o ciclo
        self.total_cost += self.graph.graph[current_node, self.graph.start_node]
        self.path.append(self.graph.start_node)

        return self.total_cost


# if __name__ == '__main__':
#
#     folder = '../files/benchmark'
#     file_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.tsp')]
#
#     gap_list = []
#     total = 0.0
#     result = 0.0
#     for arquivo in file_list:
#
#         graph = Graph.load_graph(arquivo)
#         graph.load_optimal_solution('../optimal_solutions.txt')
#
#         for i in range(graph.dimension):
#
#             begin = perf_counter()
#             tsp_solver = NearestNeighbor(graph)
#             tsp_solver.graph.start_node = i
#             solution_weight = tsp_solver.solve_nearest_neighbor()
#             end = perf_counter()
#
#             gap_list.append(Graph.gap_calc(graph.optimal_solution, solution_weight))
#             total += Graph.gap_calc(graph.optimal_solution, solution_weight)
#
#         # print(
#         #     f'NAME: {graph.name: <10} NN: {solution_weight: <20} BEST: {graph.optimal_solution: <10}'
#         #     f' RUN_TIME: {end - begin: <25} GAP: {Graph.gap_calc(graph.optimal_solution, solution_weight)}'
#         # )
#
#         result = total/len(gap_list)
#
#     print(result)
