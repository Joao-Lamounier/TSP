import math
import numpy as np


class TSP:

    def __init__(self, name, comment, problem_type, dimension, edge_weight_type, node_list):
        self.name = name
        self.comment = comment
        self.problem_type = problem_type
        self.dimension = int(dimension)
        self.edge_weight_type = edge_weight_type
        self.node_list = node_list
        self.matriz = np.zeros((self.dimension, self.dimension))

        for i in range(self.dimension):
            for j in range(self.dimension):
                self.matriz[i, j] = TSP.eucledian_2d_calc(self.node_list[i], self.node_list[j])

    def __str__(self):

        s = (f'NAME: {self.name}\nCOMMENT: {self.comment}\nTYPE: {self.problem_type}\nDIMENSION: {self.dimension}'
             f'\nEDGE_WEIGHT_TYPE: {self.edge_weight_type}\nNODE_COORD_SECTION\n')

        for node in self.node_list:
            s += f'Node {node[0]}: ({node[1]}, {node[2]})\n'

        return s

    @staticmethod
    def load_tsp(caminho_arquivo):

        name = ""
        comment = ""
        problem_type = ""
        dimension = 0
        edge_weight_type = ""
        node_list = []

        with open(caminho_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()

            # Encontrar onde começa a seção de coordenadas
            lendo_coordenadas = False
            for linha in linhas:

                linha = linha.strip()  # Remove espaços em branco

                if linha.startswith("NAME"):
                    name = linha.split(":")[1].strip()  # Nome do arquivo/problema
                elif linha.startswith("COMMENT"):
                    comment = linha.split(":")[1].strip()  # Nome do arquivo/problema
                elif linha.startswith("TYPE"):
                    problem_type = linha.split(":")[1].strip()  # Tipo de problema
                elif linha.startswith("DIMENSION"):
                    dimension = int(linha.split(":")[1].strip())  # Número de cidades (dimensão)
                elif linha.startswith("EDGE_WEIGHT_TYPE"):
                    edge_weight_type = linha.split(":")[1].strip()  # Tipo de distância (EUC_2D ou outro)

                if linha == "NODE_COORD_SECTION":
                    lendo_coordenadas = True  # Começou a seção de coordenadas
                elif linha == "EOF":
                    break  # Fim do arquivo

                if lendo_coordenadas:
                    # A linha contém as coordenadas (id, x, y)
                    partes = linha.split()
                    if len(partes) == 3:
                        node_id = int(partes[0])  # ID da cidade
                        x = float(partes[1])  # Coordenada x
                        y = float(partes[2])  # Coordenada y
                        node_list.append((node_id, x, y))  # Armazena a cidade

        tsp = TSP(name, comment, problem_type, dimension, edge_weight_type, node_list)

        return tsp

    @staticmethod
    def eucledian_2d_calc(node1, node2):
        x = node1[1] - node2[1]
        y = node1[2] - node2[2]
        return math.sqrt(x * x + y * y)


if __name__ == '__main__':

    lista_arquivo = ['Benchmark/a280.tsp', 'Benchmark/berlin52.tsp', 'Benchmark/ch130.tsp', 'Benchmark/ch150.tsp',
                     'Benchmark/d198.tsp', 'Benchmark/eil101.tsp', 'Benchmark/kroA100.tsp', 'Benchmark/kroB100.tsp',
                     'Benchmark/kroC100.tsp', 'Benchmark/kroD100.tsp', 'Benchmark/kroE100.tsp', 'Benchmark/lin105.tsp',
                     'Benchmark/pr76.tsp', 'Benchmark/rat99.tsp', 'Benchmark/rd100.tsp', 'Benchmark/rd400.tsp',
                     'Benchmark/st70.tsp', 'Benchmark/ts225.tsp']

    for arquivo in lista_arquivo:
        tsp = TSP.load_tsp(arquivo)
        print(tsp)
