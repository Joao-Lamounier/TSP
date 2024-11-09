from src.entities.graph import Graph


class NearestNeighbor:

    def __init__(self, graph):
        """Inicializa o problema TSP com o grafo fornecido."""
        if not isinstance(graph, Graph):
            raise TypeError("O parâmetro 'graph' deve ser uma instância da classe Graph.")

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
