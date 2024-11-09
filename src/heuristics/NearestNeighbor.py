from src.entities.graph import Graph


class NearestNeighbor:

    def __init__(self, graph):
        if not isinstance(graph, Graph):
            raise TypeError("O parâmetro 'graph' deve ser uma instância da classe Graph.")

        self.graph = graph
        self.path = []
        self.total_distance = 0
        self.run_time = 0.0

    def __str__(self):
        return f"Caminho: {self.path}\nDistância total: {self.total_distance}"

    def solve_nearest_neighbor(self, start=0):
        visited = [False] * self.graph.dimension
        current_node = start
        self.path = [current_node]
        visited[current_node] = True
        self.total_distance = 0.0

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
                self.total_distance += nearest_distance
                visited[nearest_node] = True
                current_node = nearest_node

        # Retorna à cidade inicial para completar o ciclo
        self.total_distance += self.graph.graph[current_node, start]
        self.path.append(start)

        return self.path, self.total_distance
