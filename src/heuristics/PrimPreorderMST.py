import math
import heapq
from typing import List, Tuple


class PrimPreorderMST:
    def __init__(self, graph):
        """Inicializa o problema TSP com o grafo fornecido."""
        self.graph = graph
        self.dimension = graph.dimension
        self.visited = [False] * self.dimension
        self.total_cost = 0
        self.path = []

    def _prim_algorithm(self) -> List[Tuple[int, int]]:
        """
        Executa o algoritmo de Prim para encontrar a árvore geradora mínima (MST).

        Retorna uma lista de arestas (u, v) que pertencem à MST.
        """
        key = [math.inf] * self.dimension
        parent = [-1] * self.dimension
        key[0] = self.graph.start_node  # Começa pela primeira cidade

        # Fila de prioridade com heapq
        min_heap = [(0, 0)]  # (custo, cidade)
        heapq.heapify(min_heap)

        while min_heap:
            _, u = heapq.heappop(min_heap)

            if self.visited[u]:
                continue
            self.visited[u] = True

            # Atualiza os vizinhos de u
            for v in range(self.dimension):
                edge_cost = self.graph.graph[u][v]
                if not self.visited[v] and edge_cost < key[v]:
                    key[v] = edge_cost
                    parent[v] = u
                    heapq.heappush(min_heap, (key[v], v))

        # Gera a lista de arestas da árvore geradora mínima
        mst_edges = [(parent[v], v) for v in range(1, self.dimension)]
        self.total_cost = sum(self.graph.graph[parent[v]][v] for v in range(1, self.dimension))

        return mst_edges

    def _preorder_traversal(self, node: int, mst_edges: List[Tuple[int, int]]) -> None:
        """
        Realiza uma busca em pré-ordem sobre a árvore geradora mínima e calcula o caminho TSP.

        Atualiza a lista de 'path' com a ordem dos nós visitados.
        """
        self.visited[node] = True
        self.path.append(node)

        for u, v in mst_edges:
            # Verifica as arestas adjacentes para o nó atual
            if u == node and not self.visited[v]:
                self._preorder_traversal(v, mst_edges)
            elif v == node and not self.visited[u]:
                self._preorder_traversal(u, mst_edges)

    def solve_tsp(self) -> Tuple[List[int], float]:
        """
        Resolve o problema do Caixeiro Viajante (TSP) usando o algoritmo de Prim e busca em pré-ordem.

        Retorna o caminho (sequência de cidades) e o custo total do ciclo TSP.
        """
        # Executa o algoritmo de Prim para encontrar a árvore geradora mínima
        mst_edges = self._prim_algorithm()

        # Limpa o estado para a busca em pré-ordem
        self.visited = [False] * self.dimension
        self.path = []
        self._preorder_traversal(0, mst_edges)

        # Cálculo do custo total do ciclo TSP
        tsp_cost = self.total_cost
        # Adiciona o retorno ao ponto de partida
        tsp_cost += self.graph.graph[self.path[-1]][self.path[0]]

        return self.path, tsp_cost
