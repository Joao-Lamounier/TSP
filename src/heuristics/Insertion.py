import os
from time import perf_counter
from src.entities.graph import Graph


class HeuristicaInsercao:

    def __init__(self, graph):
        self.graph = graph
        self.solution = []
        self.total_distance = 0

    def solve(self):
        # Começamos a partir do nó inicial (start_node)
        start_node = self.graph.start_node - 1  # Ajustando para índice zero
        self.solution = [start_node]
        nodes = list(range(self.graph.dimension))
        nodes.remove(start_node)  # Removemos o nó inicial da lista de nós

        # Passo 1: Encontrar o nó mais próximo do nó inicial para formar o primeiro caminho
        closest_node = min(nodes, key=lambda x: self.graph.graph[start_node, x])
        self.solution.append(closest_node)
        self.total_distance += 2 * self.graph.graph[start_node, closest_node]  # Ida e volta para começar o ciclo
        nodes.remove(closest_node)

        # Passo 2: Inserir nós que minimizem o aumento da distância total
        while nodes:
            best_increase = float('inf')
            best_position = None
            best_node = None

            # Avaliamos todos os nós restantes para a inserção
            for node in nodes:
                for i in range(len(self.solution)):
                    # Calcula o aumento de custo para inserir o nó na posição i
                    next_i = (i + 1) % len(self.solution)
                    increase = (self.graph.graph[self.solution[i], node] +
                                self.graph.graph[node, self.solution[next_i]] -
                                self.graph.graph[self.solution[i], self.solution[next_i]])

                    # Se o aumento for o melhor até agora, salvamos o nó e a posição
                    if increase < best_increase:
                        best_increase = increase
                        best_position = i + 1
                        best_node = node

            # Inserimos o nó na posição com o menor aumento de distância
            self.solution.insert(best_position, best_node)
            self.total_distance += best_increase
            nodes.remove(best_node)

        # Retornamos ao início para completar o ciclo
        self.total_distance += self.graph.graph[self.solution[-1], self.solution[0]]

    def get_solution(self):
        # Retorna a solução como uma lista de nós e a distância total
        return [node + 1 for node in self.solution], self.total_distance  # Ajusta para indexação 1

if __name__ == '__main__':

    folder = '../files/benchmark'
    file_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.tsp')]

    for arquivo in file_list:
        graph = Graph.load_graph(arquivo)
        graph.load_optimal_solution('../optimal_solutions.txt')
        graph.start_node = 4

        begin = perf_counter()
        tsp_solver = HeuristicaInsercao(graph)
        tsp_solver.solve()
        end = perf_counter()

        # print(tsp_solver.solution)

        # print(tsp_solver.total_distance)

        print(
            f'NAME: {graph.name: <10} IS: {tsp_solver.total_distance: <20} BEST: {graph.optimal_solution: <10}'
            f' RUN_TIME: {end - begin: <25} GAP: {Graph.gap_calc(graph.optimal_solution, tsp_solver.total_distance)}'
        )

