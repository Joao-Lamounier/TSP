import heapq


class PrimPreorderMST:
    def __init__(self, graph):
        self.graph = graph

    def mst_heuristic(self):
        # Inicializa a MST (Arvore Geradora Mínima)
        visited = [False] * self.graph.dimension
        min_heap = [(0, 0)]  # (peso, nó), começa pelo nó 0
        mst_edges = []
        total_cost = 0

        while min_heap:
            weight, node = heapq.heappop(min_heap)
            if not visited[node]:
                visited[node] = True
                total_cost += weight
                mst_edges.append(node)

                # Adiciona os vizinhos do nó à fila de prioridade
                for neighbor in range(self.graph.dimension):
                    if not visited[neighbor] and self.graph.graph[node][neighbor] > 0:
                        heapq.heappush(min_heap, (self.graph.graph[node][neighbor], neighbor))

        # Após a construção da MST, realizamos uma travessia pré-ordem (DFS)
        return self.preorder_traversal(mst_edges)

    def preorder_traversal(self, mst_edges):
        # Usaremos uma travessia em pré-ordem (DFS) para gerar uma solução do TSP
        # A solução do TSP será a ordem dos nós na árvore geradora mínima.
        tsp_solution = []
        visited = [False] * self.graph.dimension

        def dfs(node):
            visited[node] = True
            tsp_solution.append(node)
            for neighbor in range(self.graph.dimension):
                if self.graph.graph[node][neighbor] > 0 and not visited[neighbor]:
                    dfs(neighbor)

        # Começa o DFS a partir do primeiro nó da MST
        dfs(mst_edges[0])

        return tsp_solution

    def show_solution(self, solution):
        """
        Exibe a solução gerada para o TSP: caminho dos nós e custo total.
        """
        total_cost = 0
        print("Caminho do TSP:", solution)
        print("Custo total:", end=" ")

        # Calculando o custo total da solução
        for i in range(len(solution) - 1):
            u = solution[i]
            v = solution[i + 1]
            total_cost += self.graph.graph[u][v]

        # Para fechar o circuito, adicionamos o custo da aresta final ao primeiro nó
        total_cost += self.graph.graph[solution[-1]][solution[0]]

        print(total_cost)
