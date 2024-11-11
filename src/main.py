import argparse
import os
from time import perf_counter
from heuristics.PrimPreOrderMST import PrimPreOrderMST
from heuristics.NearestNeighbor import NearestNeighbor
from heuristics.Insertion import Insertion
from entities.graph import Graph


def main():
    # Configuração dos argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Solucionador TSP usando heurísticas")
    parser.add_argument("input_file", type=str, help="Caminho para o arquivo de entrada .tsp")
    parser.add_argument("output_file", type=str, help="Caminho para o arquivo de saída dos resultados")
    parser.add_argument("best_known_solution", type=float, help="Melhor solução conhecida para a instância")
    parser.add_argument("heuristic", type=str, choices=["MST", "NN", "INS"],
                        help="Heurística a ser usada (MST, NN, INS)")
    parser.add_argument("start_node", type=int, help="Nó de início")

    args = parser.parse_args()

    # Carregamento do grafo a partir do arquivo de entrada
    folder = 'files/benchmark/'
    graph = Graph.load_graph(folder + args.input_file)
    graph.start_node = args.start_node - 1

    # Escolha e execução da heurística

    tsp_solver = None
    if args.heuristic == "MST":
        tsp_solver = PrimPreOrderMST(graph)
        tsp_solver.run_time = medir_tempo_execucao(tsp_solver.solve_prim_pre_order_mst)

    elif args.heuristic == "NN":
        tsp_solver = NearestNeighbor(graph)
        tsp_solver.run_time = medir_tempo_execucao(tsp_solver.solve_nearest_neighbor)

    elif args.heuristic == 'INS':
        tsp_solver = Insertion(graph)
        tsp_solver.run_time = medir_tempo_execucao(tsp_solver.solve_insertion)

    # Verificação se o arquivo está vazio ou não existe -> Para o cabeçalho
    file_exists = os.path.exists(args.output_file) and os.path.getsize(args.output_file) > 0

    # Se o arquivo não existe ou está vazio, escreve o cabeçalho
    if not file_exists:
        with open(args.output_file, 'a') as f:
            f.write(
                f"{'INSTANCE': <12}{'METHOD': <10}{'PARAM': <10}{'OBJECTIVE': <20}{'RUNTIME': <25}"
                f"{'GAP': <20}{'NODES': <10}{'ARCS': <5}\n")

    # Escrita dos dados normalmente
    with open(args.output_file, 'a') as f:
        f.write(
            f"{args.input_file: <12}{args.heuristic: <10}{args.start_node: <10}{tsp_solver.total_cost: <20}"
            f"{tsp_solver.run_time: <25}{gap(tsp_solver.total_cost, args.best_known_solution): <20}"
            f"{graph.dimension: <10}{graph.arcs: <5}\n")


# Função que calcula o gap
def gap(objective_function, optimal_solution):
    return 100 * ((objective_function - optimal_solution) / optimal_solution)


# Função que mede o tempo de execução de uma heurística
def medir_tempo_execucao(func, *args, **kwargs):
    inicio = perf_counter()
    func(*args, **kwargs)
    fim = perf_counter()
    return fim - inicio


if __name__ == '__main__':
    main()
