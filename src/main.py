import argparse
import os
from time import perf_counter

from entities.graph import Graph
from heuristics.Insertion import Insertion
from heuristics.NearestNeighbor import NearestNeighbor
from heuristics.PrimPreOrderMST import PrimPreOrderMST
from metaheuristics.GRASP import Grasp
from local_search.TwoOpt import TwoOpt
from local_search.ThreeOpt import ThreeOpt
from local_search.Reverse import Reverse


def main():
    # Configuração dos argumentos de linha de comando
    args = parse_arguments()

    # Processa os argumentos da heurística
    local_search, constructive_heuristic, neighbor_struct, parameters = argument_process(args.heuristic)

    # Carrega o grafo do arquivo de entrada
    graph = load_graph(args.input_file)

    # Executa a heurística selecionada (construtiva ou GRASP)
    if constructive_heuristic == "GRASP":
        objective_function, run_time = run_grasp(graph, parameters, args.start_node - 1)
    else:
        # Executa a heurística construtiva
        tsp_solver = run_constructive_heuristic(constructive_heuristic, graph, args)
        # Executa a busca local se necessário
        objective_function, run_time = run_local_search(local_search, neighbor_struct, graph, tsp_solver)

    # Escreve os resultados no arquivo de saída
    write_results(args, graph, objective_function, run_time)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Solucionador TSP usando heurísticas e metaheurísticas")
    parser.add_argument("input_file", type=str, help="Caminho para o arquivo de entrada .tsp")
    parser.add_argument("output_file", type=str, help="Caminho para o arquivo de saída dos resultados")
    parser.add_argument("best_known_solution", type=float, help="Melhor solução conhecida para a instância")
    parser.add_argument("heuristic", type=str,
                        choices=["NN", "MST", "INS",
                                 "LS-NN-2Opt", "LS-NN-3Opt", "LS-NN-Rev",
                                 "LS-MST-2Opt", "LS-MST-3Opt", "LS-MST-Rev",
                                 "LS-INS-2Opt", "LS-INS-3Opt", "LS-INS-Rev",
                                 "GRASP-15-0.5", "GRASP-200-0.5", "GRASP-150-0.4"],  # Novas opções para GRASP
                        help="Heurística ou metaheurística a ser usada")
    parser.add_argument("start_node", type=int, help="Nó de início")
    return parser.parse_args()


def argument_process(command_string):
    # Dividindo a string em partes com base no separador "-"
    parts = command_string.split('-')

    if len(parts) == 1:
        return None, parts[0], None, None
    elif len(parts) == 3:
        if parts[0] == "GRASP":
            return None, "GRASP", None, (int(parts[1]), float(parts[2]))
        else:
            return parts[0], parts[1], parts[2], None
    return None, parts[0], None, None


def run_grasp(graph, parameters, start_node):
    """
    Executa o GRASP com os parâmetros especificados
    """
    max_iterations, alpha = parameters
    grasp_solver = Grasp(graph, alpha=alpha, start_node=start_node)
    begin = perf_counter()
    best_tour, best_cost = grasp_solver.run()
    end = perf_counter()
    run_time = end - begin
    return best_cost, run_time


# As outras funções permanecem iguais
def load_graph(input_file):
    folder = 'files/benchmark/'
    return Graph.load_graph(folder + input_file)


def run_constructive_heuristic(constructive_heuristic, graph, args):
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

def run_local_search(local_search, neighbor_struct, graph, tsp_solver):
    if local_search is not None:
        tsp_local_search = define_local_search(neighbor_struct, graph, tsp_solver)
        objective_function = tsp_local_search.objective_function
        run_time = tsp_local_search.run_time
    else:
        objective_function = tsp_solver.total_cost
        run_time = tsp_solver.run_time

    return objective_function, run_time


def write_results(args, graph, objective_function, run_time):
    file_exists = os.path.exists(args.output_file) and os.path.getsize(args.output_file) > 0

    if not file_exists:
        with open(args.output_file, 'a') as f:
            f.write(
                f"{'INSTANCE': <15}{'METHOD': <15}{'PARAM': <10}{'OBJECTIVE': <20}{'RUNTIME': <25}"
                f"{'GAP': <20}{'NODES': <10}{'ARCS': <5}\n")

    with open(args.output_file, 'a') as f:
        method_params = args.heuristic.split('-')
        if len(method_params) > 2:
            param = f"{method_params[1]}-{method_params[2]}"
        else:
            param = args.start_node

        f.write(
            f"{args.input_file: <15}{args.heuristic: <15}{param: <10}{objective_function: <20}"
            f"{run_time: <25}{gap(objective_function, args.best_known_solution): <20}"
            f"{graph.dimension: <10}{graph.arcs: <5}\n")


def gap(objective_function, optimal_solution):
    return 100 * ((objective_function - optimal_solution) / optimal_solution)


def measure_execution_time(func, *args, **kwargs):
    begin = perf_counter()
    func(*args, **kwargs)
    end = perf_counter()
    return end - begin


if __name__ == '__main__':
    main()