from src.entities.graph import Graph
from heuristics.NearestNeighbor import NearestNeighbor

import matplotlib.pyplot as plt
import numpy as np
import os
from time import perf_counter
import scipy.stats as stats

from src.heuristics.Insertion import Insertion
from src.heuristics.PrimPreOrderMST import PrimPreOrderMST


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
        ax.bar(ind - bar_width, graphic_1.run_time, bar_width, label='Nearest Neighbor', color='b')
        ax.bar(ind, graphic_2.run_time, bar_width, label='Prim + Pre Order', color='g')
        ax.bar(ind + bar_width, graphic_3.run_time, bar_width, label='Insertion', color='r')

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

    gap_list = []
    gap_list_2 = []
    gap_list_3 = []

    for arquivo in file_list:

        graph = Graph.load_graph(arquivo)
        graph.load_optimal_solution('optimal_solutions.txt')

        for i in range(graph.dimension):

            graph.start_node = i

            # nn = NearestNeighbor(graph)
            # inicio = perf_counter()
            # nn.solve_nearest_neighbor()
            # fim = perf_counter()
            # nn.run_time = fim - inicio

            # mst = PrimPreOrderMST(graph)
            # inicio_2 = perf_counter()
            # path_mst = mst.approximate_tsp()
            # fim_2 = perf_counter()
            # mst.run_time = fim_2 - inicio_2
            #
            # total = 0.0
            # for i in range(len(path_mst) - 1):
            #     total += graph.graph[path_mst[i], path_mst[i + 1]]
            #
            # mst.total_cost = total

            # inicio_3 = perf_counter()
            ins = Insertion(graph)
            ins.solve()
            cost = ins.total_cost
            # fim_3 = perf_counter()
            # ins.run_time = fim_3 - inicio_3

            # run_time.append(nn.run_time)
            # run_time_2.append(mst.run_time)
            # run_time_3.append(ins.run_time)

            # gap_list.append(Graph.gap_calc(nn.graph.optimal_solution, nn.total_cost))
            # gap_list_2.append(Graph.gap_calc(mst.graph.optimal_solution, mst.total_cost))
            gap_list_3.append(Graph.gap_calc(ins.graph.optimal_solution, ins.total_cost))

        # print(
        #     f'NAME: {graph.name: <10} NN: {nn.total_cost: <20} BEST: {graph.optimal_solution: <10}'
        #     f' RUN_TIME: {nn.run_time: <25} GAP: {Graph.gap_calc(graph.optimal_solution, nn.total_cost)}'
        # )
        #
        # print(
        #     f'NAME: {graph.name: <10} MST: {mst.total_cost: <20} BEST: {graph.optimal_solution: <10}'
        #     f' RUN_TIME: {fim_2 - inicio_2: <25} GAP: {Graph.gap_calc(graph.optimal_solution, mst.total_cost)}'
        # )
        #
        # print(
        #     f'NAME: {graph.name: <10} INS: {mst.total_cost: <20} BEST: {graph.optimal_solution: <10}'
        #     f' RUN_TIME: {fim_2 - inicio_2: <25} GAP: {Graph.gap_calc(graph.optimal_solution, mst.total_cost)}'
        # )

        # Verificar se o arquivo está vazio ou não existe
        # file_exists = os.path.exists('tabela_dados.txt') and os.path.getsize('tabela_dados.txt') > 0

        # Se o arquivo não existe ou está vazio, escreve o cabeçalho
        # if not file_exists:
        #     with open('tabela_dados.txt', 'a') as f:
        #         f.write(
        #             f"{'INSTANCE': <12}{'METHOD': <10}{'PARAM': <10}{'OBJECTIVE': <20}{'BEST SOLUTION': <25}"
        #             f"{'GAP': <20}{'NODES': <10}{'ARCS': <5}\n")

        # Escrever os dados normalmente
        # with open('tabela_dados.txt', 'a') as f:
        #     f.write(
        #         f"{nn.graph.name: <12}{'NN': <10}{nn.graph.start_node + 1: <10}{nn.total_cost: <20}{nn.graph.optimal_solution: <25}"
        #         f"{Graph.gap_calc(nn.graph.optimal_solution, nn.total_cost): <20}{nn.graph.dimension: <10}{nn.graph.arcs: <5}\n")
        #


        # file_exists = os.path.exists('tabela_dados_2.txt') and os.path.getsize('tabela_dados_2.txt') > 0
        #
        # # Se o arquivo não existe ou está vazio, escreve o cabeçalho
        # if not file_exists:
        #     with open('tabela_dados_2.txt', 'a') as f:
        #         f.write(
        #             f"{'INSTANCE': <12}{'METHOD': <10}{'PARAM': <10}{'OBJECTIVE': <20}{'BEST SOLUTION': <25}"
        #             f"{'GAP': <20}{'NODES': <10}{'ARCS': <5}\n")
        #
        # # Escrever os dados normalmente
        # with open('tabela_dados_2.txt', 'a') as f:
        #     f.write(
        #         f"{mst.graph.name: <12}{'NN': <10}{mst.graph.start_node + 1: <10}{mst.total_cost: <20}{mst.graph.optimal_solution: <25}"
        #         f"{Graph.gap_calc(mst.graph.optimal_solution, mst.total_cost): <20}{mst.graph.dimension: <10}{mst.graph.arcs: <5}\n")
        #
        # file_exists = os.path.exists('tabela_dados_3.txt') and os.path.getsize('tabela_dados_3.txt') > 0
        #
        # # Se o arquivo não existe ou está vazio, escreve o cabeçalho
        # if not file_exists:
        #     with open('tabela_dados_3.txt', 'a') as f:
        #         f.write(
        #             f"{'INSTANCE': <12}{'METHOD': <10}{'PARAM': <10}{'OBJECTIVE': <20}{'BEST SOLUTION': <25}"
        #             f"{'GAP': <20}{'NODES': <10}{'ARCS': <5}\n")
        #
        # # Escrever os dados normalmente
        # with open('tabela_dados_3.txt', 'a') as f:
        #     f.write(
        #         f"{ins.graph.name: <12}{'NN': <10}{ins.graph.start_node + 1: <10}{ins.total_cost: <20}{ins.graph.optimal_solution: <25}"
        #         f"{Graph.gap_calc(ins.graph.optimal_solution, ins.total_cost): <20}{ins.graph.dimension: <10}{ins.graph.arcs: <5}\n")
        #


    # nn = Graphic('NN', run_time)
    # mst = Graphic('MST', run_time_2)
    # ins = Graphic('INS', run_time_3)
    # Graphic.plot_graphic(nn, mst, ins)


    # print(np.mean(gap_list_2))
    # print(np.mean(gap_list_3))

    # Passo 1: Calcular a média amostral (x̄)
    mean_gap = np.mean(gap_list_3)

    # Passo 2: Calcular o desvio padrão amostral (s)
    std_gap = np.std(gap_list_3, ddof=1)  # ddof=1 para calcular o desvio padrão amostral

    # Passo 3: Calcular o número de amostras (n)
    n = len(gap_list_3)

    # Passo 4: Encontrar o valor crítico t para um intervalo de confiança de 95%
    confidence_level = 0.95
    alpha = 1 - confidence_level
    t_critical = stats.t.ppf(1 - alpha / 2, df=n - 1)  # t crítico para 95% e n-1 graus de liberdade

    # Passo 5: Calcular o erro padrão da média
    standard_error = std_gap / np.sqrt(n)

    # Passo 6: Calcular o intervalo de confiança
    margin_of_error = t_critical * standard_error
    confidence_interval = (mean_gap - margin_of_error, mean_gap + margin_of_error)

    # Exibir os resultados
    print('Insertion', n)
    print(f"Média do Gap: {mean_gap}")
    print(f"Desvio padrão amostral: {std_gap}")
    print(f"Valor crítico t (95% de confiança): {t_critical}")
    print(f"Erro padrão da média: {standard_error}")
