

class PrimPreOrderMST:
    def __init__(self, graph):
        """
        Inicializa o objeto PrimPreOrderMST com um grafo fornecido.

        Argumentos:
            graph (Graph): O grafo para calcular a Árvore Geradora Mínima (MST).
        """
        self.graph = graph
        self.mst = [[] for _ in range(graph.dimension)]
        self.visited = [False] * graph.dimension
        self.path = []
        self.total_cost = 0.0
        self.run_time = 0.0

    def _find_min_edge(self, selected: list, num_nodes: int) -> tuple:
        """
        Função auxiliar para encontrar a aresta mínima que conecta um nó selecionado
        a um nó não selecionado.

        Argumentos:
            selected (list): Lista de nós selecionados.
            num_nodes (int): O número total de nós no grafo.

        Retorna:
            tuple: Uma tupla no formato (u, v, peso) representando a aresta com o
                   menor peso conectando nós selecionados a não selecionados.
        """
        min_edge = (None, None, float('inf'))
        for u in range(num_nodes):
            if selected[u]:
                for v in range(num_nodes):
                    if not selected[v] and self.graph.graph[u][v] < min_edge[2]:
                        min_edge = (u, v, self.graph.graph[u][v])
        return min_edge

    def prim_mst(self):
        """
        Calcula a Árvore Geradora Mínima (MST) usando o algoritmo de Prim.
        """
        num_nodes = self.graph.dimension
        selected = [False] * num_nodes
        selected[0] = True  # Começa a partir do nó 0

        for _ in range(num_nodes - 1):
            u, v, weight = self._find_min_edge(selected, num_nodes)
            if u is not None and v is not None:
                selected[v] = True
                self.mst[u].append(v)
                self.mst[v].append(u)

    def _dfs_pre_order(self, node: int, path: list):
        """
        Realiza uma busca em profundidade (DFS) em pré-ordem na MST.

        Argumentos:
            node (int): O nó atual para começar a busca DFS.
            path (list): A lista para armazenar os nós visitados na ordem.
        """
        self.visited[node] = True
        path.append(node)
        for neighbor in self.mst[node]:
            if not self.visited[neighbor]:
                self._dfs_pre_order(neighbor, path)

    def approximate_tsp(self) -> list:
        """
        Calcula uma aproximação do TSP usando a MST de Prim e a DFS em pré-ordem.

        Retorna:
            list: O caminho aproximado do TSP.
        """
        self.prim_mst()
        path = []
        self._dfs_pre_order(0, path)
        path.append(0)  # Fechando o ciclo
        self.path = path
        return path

    def total_cost_calc(self) -> float:
        """
        Calcula o custo total do caminho aproximado do TSP.

        Retorna:
            float: O custo total do caminho aproximado do TSP.
        """

        total_cost = 0
        for i in range(len(self.path) - 1):
            total_cost += self.graph.graph[self.path[i], self.path[i + 1]]

        return total_cost
