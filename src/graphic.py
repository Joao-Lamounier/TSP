from src.entities.graph import Graph
from heuristics.NearestNeighbor import NearestNeighbor
from heuristics.PrimPreOrderMST import PrimPreOrderMST
import matplotlib.pyplot as plt
import numpy as np
import os
from time import perf_counter

from src.heuristics.Christofides import Christofides


class Graphic:

    def __init__(self, name, run_time):
        self.name = name
        self.run_time = run_time
        self.largura = 0.2
        self.instancias = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                           '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

    @staticmethod
    def plot_graphic(graphic_1, graphic_2, graphic_3):
        # Número de instâncias
        n = len(graphic_1.instancias)

        # Posições das instâncias no eixo X
        ind = np.arange(n)

        # Criação do gráfico
        fig, ax = plt.subplots(figsize=(10, 6))

        # Criando as barras para as heurísticas
        ax.bar(ind - graphic_1.largura / 2, graphic_1.run_time, graphic_1.largura, label='Heurística A', color='b')
        ax.bar(ind + graphic_2.largura / 2, graphic_2.run_time, graphic_2.largura, label='Heurística B', color='g')
        ax.bar(ind + 2 * graphic_3.largura / 2, graphic_3.run_time, graphic_3.largura, label='Heurística C', color='r')

        # Adicionando rótulos, título e legendas
        ax.set_xlabel('Instâncias')
        ax.set_ylabel('Tempo de Execução (segundos)')
        ax.set_title('Tempo de Execução por Instância e Heurística')
        ax.set_xticks(ind)
        ax.set_xticklabels(graphic_1.instancias)
        ax.legend()

        # Exibindo o gráfico
        plt.tight_layout()  # Ajusta o layout para não cortar nada
        plt.show()


if __name__ == '__main__':

    folder = 'files/benchmark'
    file_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.tsp')]

    run_time = []
    run_time_2 = []
    run_time_3 = []
    for arquivo in file_list:

        graph = Graph.load_graph(arquivo)
        graph.start_node = 0
        graph.load_optimal_solution('optimal_solutions.txt')

        nn = NearestNeighbor(graph)
        inicio = perf_counter()
        nn.solve_nearest_neighbor()
        fim = perf_counter()
        nn.run_time = fim - inicio

        mst = PrimPreOrderMST(graph)
        inicio_2 = perf_counter()
        path_mst = mst.approximate_tsp()
        fim_2 = perf_counter()

        christ = Christofides(graph)
        inicio_3 = perf_counter()
        path_c, solution_c = christ.solve_tsp()
        fim_3 = perf_counter()

        total = 0.0
        for i in range(len(path_mst) - 1):
            total += graph.graph[path_mst[i], path_mst[i + 1]]

        mst.total_cost = total

        run_time.append(nn.run_time)
        run_time_2.append(fim_2 - inicio_2)
        run_time_3.append(fim_3 - inicio_3)

        print(
            f'NAME: {graph.name: <10} NN: {nn.total_cost: <20} BEST: {graph.optimal_solution: <10}'
            f' RUN_TIME: {nn.run_time: <25} GAP: {Graph.gap_calc(graph.optimal_solution, nn.total_cost)}'
        )

        print(
            f'NAME: {graph.name: <10} MST: {mst.total_cost: <20} BEST: {graph.optimal_solution: <10}'
            f' RUN_TIME: {fim_2 - inicio_2: <25} GAP: {Graph.gap_calc(graph.optimal_solution, mst.total_cost)}'
        )

        print(
            f'NAME: {graph.name: <10} CHRIS: {solution_c: <20} BEST: {graph.optimal_solution: <10}'
            f' RUN_TIME: {fim_3 - inicio_3: <25} GAP: {Graph.gap_calc(graph.optimal_solution, solution_c)}'
        )


    nn = Graphic('NN', run_time)
    mst = Graphic('MST', run_time_2)
    christ = Graphic('CHRIST', run_time_3)
    Graphic.plot_graphic(nn, mst, christ)