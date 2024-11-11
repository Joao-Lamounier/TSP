import heapq
import os
from collections import defaultdict
from time import perf_counter
from src.entities.graph import Graph


class Christofides:

    def __init__(self, graph):
        self.graph = graph  # Instância da classe Graph
        self.mst = []       # Armazenará a Árvore Geradora Mínima
        self.perfect_matching = []  # Armazenará o emparelhamento mínimo
        self.eulerian_tour = []     # Armazenará o passeio euleriano
        self.hamiltonian_circuit = []  # Armazenará o circuito hamiltoniano final

    def find_mst(self):
        """Usa o algoritmo de Prim para construir a Árvore Geradora Mínima (AGM)"""
        visited = [False] * self.graph.dimension
        min_heap = [(0, 0, -1)]  # (peso, nó, pai)
        mst_edges = []

        while min_heap:
            weight, u, parent = heapq.heappop(min_heap)
            if visited[u]:
                continue
            visited[u] = True
            if parent != -1:
                mst_edges.append((parent, u, weight))

            for v in range(self.graph.dimension):
                if not visited[v]:
                    heapq.heappush(min_heap, (self.graph.graph[u][v], v, u))

        self.mst = mst_edges

    def find_odd_degree_nodes(self):
        """Encontra todos os nós de grau ímpar na AGM"""
        degree = defaultdict(int)
        for u, v, _ in self.mst:
            degree[u] += 1
            degree[v] += 1
        odd_degree_nodes = [node for node, deg in degree.items() if deg % 2 == 1]
        return odd_degree_nodes

    def minimum_weight_matching(self, odd_nodes):
        """Realiza um emparelhamento mínimo nos nós de grau ímpar"""
        while odd_nodes:
            u = odd_nodes.pop()
            closest = None
            min_dist = float('inf')
            for v in odd_nodes:
                if self.graph.graph[u][v] < min_dist:
                    min_dist = self.graph.graph[u][v]
                    closest = v
            self.perfect_matching.append((u, closest))
            odd_nodes.remove(closest)

    def eulerian_tour(self):
        """Constrói o passeio euleriano"""
        adj = defaultdict(list)
        for u, v, _ in self.mst:
            adj[u].append(v)
            adj[v].append(u)
        for u, v in self.perfect_matching:
            adj[u].append(v)
            adj[v].append(u)

        stack = [0]  # Começamos do nó 0
        tour = []
        while stack:
            u = stack[-1]
            if adj[u]:
                v = adj[u].pop()
                adj[v].remove(u)
                stack.append(v)
            else:
                tour.append(stack.pop())
        self.eulerian_tour = tour

    def hamiltonian_circuit(self):
        """Cria o circuito hamiltoniano removendo vértices repetidos no passeio euleriano"""
        visited = set()
        circuit = []
        for node in self.eulerian_tour:
            if node not in visited:
                visited.add(node)
                circuit.append(node)
        circuit.append(circuit[0])  # Retornamos ao ponto de partida
        self.hamiltonian_circuit = circuit

    def find_tsp_solution(self):
        """Aplica o algoritmo de Christofides para encontrar a solução do TSP"""
        self.find_mst()
        odd_nodes = self.find_odd_degree_nodes()
        self.minimum_weight_matching(odd_nodes)
        self.eulerian_tour()
        self.hamiltonian_circuit()
        return self.hamiltonian_circuit


if __name__ == '__main__':
    folder = '../files/benchmark'
    file_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.tsp')]

    for arquivo in file_list:
        graph = Graph.load_graph(arquivo)
        graph.load_optimal_solution('../optimal_solutions.txt')
        graph.start_node = 3

        begin = perf_counter()
        tsp_solver = Christofides(graph)
        solution_path, solution_weight = tsp_solver.find_tsp_solution()
        end = perf_counter()

        print(solution_path)

        print(
            f'NAME: {graph.name: <10} CHRIS: {solution_weight: <20} BEST: {graph.optimal_solution: <10}'
            f' RUN_TIME: {end - begin: <25} GAP: {Graph.gap_calc(graph.optimal_solution, solution_weight)}'
        )

