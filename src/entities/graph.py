import math
import numpy as np


class Graph:

    def __init__(self, name, comment, problem_type, dimension, edge_weight_type, node_list):
        self.name = name
        self.comment = comment
        self.problem_type = problem_type
        self.dimension = int(dimension)
        self.edge_weight_type = edge_weight_type
        self.node_list = node_list
        self.graph = np.zeros((self.dimension, self.dimension))
        self.arcs = int((dimension * dimension - dimension) / 2)
        self.optimal_solution = 0.0

        for i in range(self.dimension):
            for j in range(self.dimension):
                self.graph[i, j] = Graph.euclidean_2d_calc(self.node_list[i], self.node_list[j])

    @staticmethod
    def load_graph(file_path):

        node_list = []

        with open(file_path, 'r') as f:
            lines = f.readlines()

            # Encontrar onde começa a seção de coordenadas
            read_coord = False
            for line in lines:

                line = line.strip()  # Remove espaços em branco

                if not read_coord:
                    if line.startswith("NAME"):
                        name = line.split(":")[1].strip()  # Nome do arquivo/problema
                    elif line.startswith("COMMENT"):
                        comment = line.split(":")[1].strip()  # Nome do arquivo/problema
                    elif line.startswith("TYPE"):
                        problem_type = line.split(":")[1].strip()  # Tipo de problema
                    elif line.startswith("DIMENSION"):
                        dimension = int(line.split(":")[1].strip())  # Número de cidades (dimensão)
                    elif line.startswith("EDGE_WEIGHT_TYPE"):
                        edge_weight_type = line.split(":")[1].strip()  # Tipo de distância (EUC_2D ou outro)
                    elif line == "NODE_COORD_SECTION":
                        read_coord = True
                elif line == "EOF":
                    break  # Fim do arquivo

                if read_coord:
                    # A linha contém as coordenadas (id, x, y)
                    parts = line.split()
                    if len(parts) == 3:
                        node_id = int(parts[0])  # ID da cidade
                        x = float(parts[1])  # Coordenada x
                        y = float(parts[2])  # Coordenada y
                        node_list.append((node_id, x, y))  # Armazena a cidade

        return Graph(name, comment, problem_type, dimension, edge_weight_type, node_list)

    @staticmethod
    def euclidean_2d_calc(node1, node2):
        x = node1[1] - node2[1]
        y = node1[2] - node2[2]
        return math.sqrt(x * x + y * y)

    def load_optimal_solution(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()

            for line in lines:
                line = line.strip()
                if line.startswith(self.name):
                    self.optimal_solution = float(line.split()[1].strip())
                    return

    # def path_length(self, path):
    #     """Calculate the total length of a path."""
    #     n = len(path)
    #     length = self.graph[path[-1]][path[0]]
    #     for i in range(n - 1):
    #         length += self.graph[path[i]][path[i + 1]]
    #     return length
