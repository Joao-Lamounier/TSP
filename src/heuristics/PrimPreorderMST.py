import os
from time import perf_counter

from src.entities.graph import Graph


import heapq


class PrimPreOrderMST:

    def __init__(self, graph):
        """
        Inicializa a estrutura com o grafo fornecido.

        Args:
            graph (Graph): Objeto do grafo contendo a matriz de adjacência e a dimensão.
        """
        self.graph = graph
        self.mst = [[] for _ in range(graph.dimension)]
        self.visited = [False] * graph.dimension
        self.start_node = graph.start_node  # Nó inicial

    def _prim_mst(self):
        """
        Calcula a Árvore Geradora Mínima (MST) utilizando o algoritmo de Prim
        e armazena o resultado como uma lista de adjacências.
        """
        num_nodes = self.graph.dimension
        selected = [False] * num_nodes
        selected[self.start_node] = True  # Usa o nó inicial fornecido

        for _ in range(num_nodes - 1):
            min_edge = (None, None, float('inf'))
            for u in range(num_nodes):
                if selected[u]:
                    for v in range(num_nodes):
                        weight = self.graph.graph[u][v]
                        if not selected[v] and weight < min_edge[2]:
                            min_edge = (u, v, weight)

            u, v, weight = min_edge
            if u is not None and v is not None:
                selected[v] = True
                self.mst[u].append(v)
                self.mst[v].append(u)

    def _pre_order_dfs(self, node, path):
        """
        Realiza uma busca em profundidade (DFS) na MST para gerar a ordem pré-ordem.

        Args:
            node (int): Nó atual da DFS.
            path (list): Caminho percorrido na DFS.
        """
        self.visited[node] = True
        path.append(node)
        for neighbor in self.mst[node]:
            if not self.visited[neighbor]:
                self._pre_order_dfs(neighbor, path)

    def approximate_tsp(self):
        """
        Gera uma solução aproximada para o TSP.

        Returns:
            list: Caminho aproximado que resolve o TSP.
        """
        self._prim_mst()
        path = []
        self._pre_order_dfs(self.start_node, path)  # Usa o nó inicial fornecido
        path.append(self.start_node)  # Fechando o ciclo
        self._two_opt(path)
        return path

    def _two_opt(self, path):
        """
        Realiza a otimização 2-Opt no caminho para melhorar a solução aproximada do TSP.

        Args:
            path (list): Caminho aproximado do TSP.
        """
        improved = True
        while improved:
            improved = False
            for i in range(1, len(path) - 2):
                for j in range(i + 1, len(path) - 1):
                    if self._swap_cost_benefit(path, i, j):
                        path[i:j + 1] = reversed(path[i:j + 1])
                        improved = True

    def _swap_cost_benefit(self, path, i, j):
        """
        Verifica se a troca 2-Opt entre dois segmentos resulta em um menor custo.

        Args:
            path (list): Caminho atual do TSP.
            i (int): Índice inicial do primeiro segmento.
            j (int): Índice final do segundo segmento.

        Returns:
            bool: True se a troca reduz o custo; False caso contrário.
        """
        return (self._edge_cost(path[i - 1], path[i]) + self._edge_cost(path[j], path[j + 1]) >
                self._edge_cost(path[i - 1], path[j]) + self._edge_cost(path[i], path[j + 1]))

    def _edge_cost(self, u, v):
        """
        Retorna o custo da aresta entre dois nós.

        Args:
            u (int): Nó de origem.
            v (int): Nó de destino.

        Returns:
            float: Custo da aresta entre u e v.
        """
        return self.graph.graph[u][v]


