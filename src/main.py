import argparse
import os
from time import perf_counter
from heuristics.PrimPreOrderMST import PrimPreOrderMST
from heuristics.NearestNeighbor import NearestNeighbor
from heuristics.Insertion import Insertion
from entities.graph import Graph
from local_search.TwoOpt import TwoOpt
from local_search.Reverse import Reverse
from local_search.ThreeOpt import ThreeOpt


def main():
    # Configuração dos argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Solucionador TSP usando heurísticas")
    parser.add_argument("input_file", type=str, help="Caminho para o arquivo de entrada .tsp")
    parser.add_argument("output_file", type=str, help="Caminho para o arquivo de saída dos resultados")
    parser.add_argument("best_known_solution", type=float, help="Melhor solução conhecida para a instância")
    parser.add_argument("heuristic", type=str,
                        choices=["MST", "NN", "INS", "LS-NN-2Opt", "LS-NN-3Opt", "LS-MST-2Opt", "LS-MST-3Opt",
                                 "LS-INS-2Opt",
                                 "LS-INS-3Opt"
                                 "LS-NN-2DnI", "LS-MST-DnI", "LS-INS-DnI", "LS-NN-Rev", "LS-MST-Rev", "LS-INS-Rev"],
                        help="Heurística a ser usada (MST, NN, INS)")
    parser.add_argument("start_node", type=int, help="Nó de início")

    args = parser.parse_args()
    local_search, constructive_heuristic, neighbor_struct = argument_process(args.heuristic)

    # Carregamento do grafo a partir do arquivo de entrada
    folder = 'files/benchmark/'
    graph = Graph.load_graph(folder + args.input_file)

    # Escolha e execução da heurística construtiva
    tsp_solver = define_constructive_heuristic(constructive_heuristic, graph, args)

    # Escolha e execução da heurística -> buscal local
    if local_search is not None:
        tsp_local_search = define_local_search(neighbor_struct, graph, tsp_solver)
        objective_function = tsp_local_search.objective_function
        run_time = tsp_local_search.run_time
    else:
        objective_function = tsp_solver.total_cost
        run_time = tsp_solver.run_time

    # Verificação se o arquivo está vazio ou não existe -> Para o cabeçalho
    file_exists = os.path.exists(args.output_file) and os.path.getsize(args.output_file) > 0

    # Se o arquivo não existe ou está vazio, escreve o cabeçalho
    if not file_exists:
        with open(args.output_file, 'a') as f:
            f.write(
                f"{'INSTANCE': <15}{'METHOD': <15}{'PARAM': <10}{'OBJECTIVE': <20}{'RUNTIME': <25}"
                f"{'GAP': <20}{'NODES': <10}{'ARCS': <5}\n")

    # Escrita dos dados normalmente
    with open(args.output_file, 'a') as f:
        f.write(
            f"{args.input_file: <15}{args.heuristic: <15}{args.start_node: <10}{objective_function: <20}"
            f"{run_time: <25}{gap(objective_function, args.best_known_solution): <20}"
            f"{graph.dimension: <10}{graph.arcs: <5}\n")


def argument_process(command_string):
    # Dividindo a string em partes com base no separador "-"
    parts = command_string.split('-')

    if len(parts) == 1:
        return None, parts[0], None
    elif len(parts) == 3:
        return parts[0], parts[1], parts[2]


def define_constructive_heuristic(constructive_heuristic, graph, args):
    tsp_solver = None

    if constructive_heuristic == "MST":
        tsp_solver = PrimPreOrderMST(graph, args.start_node - 1)
        tsp_solver.run_time = measure_execution_time(tsp_solver.solve_prim_pre_order_mst)

    elif constructive_heuristic == "NN":
        tsp_solver = NearestNeighbor(graph, args.start_node - 1)
        tsp_solver.run_time = measure_execution_time(tsp_solver.solve_nearest_neighbor)

    elif constructive_heuristic == 'INS':
        tsp_solver = Insertion(graph, args.start_node - 1)
        tsp_solver.run_time = measure_execution_time(tsp_solver.solve_insertion)

    return tsp_solver


def define_local_search(neighbor_struct, graph, tsp_solver):
    tsp_local_search = None

    if neighbor_struct == "2Opt":
        tsp_local_search = TwoOpt(graph.graph, tsp_solver.run_time, tsp_solver.path, tsp_solver.total_cost)
        tsp_local_search.run_time += measure_execution_time(tsp_local_search.solve_two_opt)

    elif neighbor_struct == "Rev":
        tsp_local_search = Reverse(graph.graph, tsp_solver.run_time, tsp_solver.path, tsp_solver.total_cost)
        tsp_local_search.run_time += measure_execution_time(tsp_local_search.solve_reverse)

    elif neighbor_struct == "3Opt":
        tsp_local_search = ThreeOpt(graph.graph, tsp_solver.run_time, tsp_solver.path, tsp_solver.total_cost)
        tsp_local_search.run_time += measure_execution_time(tsp_local_search.solve_three_opt)

    return tsp_local_search


# Função que calcula o gap
def gap(objective_function, optimal_solution):
    return 100 * ((objective_function - optimal_solution) / optimal_solution)


# Função que mede o tempo de execução de uma heurística
def measure_execution_time(func, *args, **kwargs):
    begin = perf_counter()
    func(*args, **kwargs)
    end = perf_counter()
    return end - begin


if __name__ == '__main__':
    main()
