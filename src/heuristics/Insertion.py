class Insertion:

    def __init__(self, graph):
        self.graph = graph
        self.path = []
        self.total_cost = 0.0
        self.runtime = 0.0

    def solve_insertion(self):
        # Inicia-se a partir do nó inicial (start_node)
        start_node = self.graph.start_node
        self.path = [start_node]
        nodes = list(range(self.graph.dimension))
        nodes.remove(start_node)  # Remove o nó inicial da lista de nós

        # Passo 1: Encontrar o nó mais próximo do nó inicial para formar o primeiro caminho
        closest_node = min(nodes, key=lambda x: self.graph.graph[start_node, x])
        self.path.append(closest_node)
        self.total_cost += 2 * self.graph.graph[start_node, closest_node]  # Ida e volta para começar o ciclo
        nodes.remove(closest_node)

        # Passo 2: Inserir nós que minimizem o aumento da distância total
        while nodes:
            best_increase = float('inf')
            best_position = None
            best_node = None

            # Avalia todos os nós restantes para a inserção
            for node in nodes:
                for i in range(len(self.path)):
                    # Calcula o aumento de custo para inserir o nó na posição i
                    next_i = (i + 1) % len(self.path)
                    increase = (self.graph.graph[self.path[i], node] +
                                self.graph.graph[node, self.path[next_i]] -
                                self.graph.graph[self.path[i], self.path[next_i]])

                    # Se o aumento for o melhor até agora, salva o nó e a posição
                    if increase < best_increase:
                        best_increase = increase
                        best_position = i + 1
                        best_node = node

            # Insere o nó na posição com o menor aumento de distância
            self.path.insert(best_position, best_node)
            self.total_cost += best_increase
            nodes.remove(best_node)

        # Retorna ao início para completar o ciclo
        self.total_cost += self.graph.graph[self.path[-1], self.path[0]]
        self.path.append(self.graph.start_node)
