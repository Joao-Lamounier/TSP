import matplotlib.pyplot as plt
import numpy as np
import os
from time import perf_counter

from src.entities.graph import Graph
from src.heuristics.NearestNeighbor import NearestNeighbor


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
        bar_width = graphic_1.largura  # Assumindo que todas as larguras de barra são iguais

        # Ajustar as posições para garantir que as barras fiquem alinhadas e com o mesmo espaçamento
        ax.bar(ind - bar_width, graphic_1.run_time, bar_width, label='LS N1', color='b')
        ax.bar(ind, graphic_2.run_time, bar_width, label='LS N2', color='g')
        ax.bar(ind + bar_width, graphic_3.run_time, bar_width, label='LS N3', color='r')

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
        graph.load_optimal_solution('optimal_solutions.txt')
        graph.start_node = 0

        nn = NearestNeighbor(graph)
        inicio = perf_counter()
        nn.solve_nearest_neighbor()
        fim = perf_counter()
        nn.run_time = fim - inicio

        run_time.append(nn.run_time)

        print(
            f'NAME: {graph.name: <10} NN: {nn.total_cost: <20} BEST: {graph.optimal_solution: <10}'
            f' RUN_TIME: {nn.run_time: <25} GAP: {Graph.gap_calc(graph.optimal_solution, nn.total_cost)}'
        )

    graphic = Graphic('Gráfico de Barras', run_time)

    Graphic.plot_graphic(graphic, graphic, graphic)



