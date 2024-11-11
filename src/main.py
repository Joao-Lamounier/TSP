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
    parser.add_argument("heuristic", type=str, choices=["MST", "NN", "INS"], help="Heurística a ser usada (MST, NN, INS)")
    parser.add_argument("--start_node", type=int, default=0, help="Nó de início (opcional, padrão: 0)")

    args = parser.parse_args()

    # Carregar o grafo a partir do arquivo de entrada
    folder = 'files/benchmark/'
    graph = Graph.load_graph(folder + args.input_file)
    graph.start_node = args.start_node - 1

    # Escolher e executar a heurística

    start_time = perf_counter()

    cost = 0.0
    if args.heuristic == "MST":
        tsp_solver = PrimPreOrderMST(graph)

        tsp_solver.approximate_tsp()

        cost = tsp_solver.calc_total_cost()

    elif args.heuristic == "NN":
        tsp_solver = NearestNeighbor(graph)

        cost = tsp_solver.solve_nearest_neighbor()

    elif args.heuristic == 'INS':
        tsp_solver = Insertion(graph)

        tsp_solver.solve()

        cost = tsp_solver.total_cost

    end_time = perf_counter()

    # Verificar se o arquivo está vazio ou não existe
    file_exists = os.path.exists(args.output_file) and os.path.getsize(args.output_file) > 0

    # Se o arquivo não existe ou está vazio, escreve o cabeçalho
    if not file_exists:
        with open(args.output_file, 'a') as f:
            f.write(
                f"{'INSTANCE': <12}{'METHOD': <10}{'PARAM': <10}{'OBJECTIVE': <20}{'RUNTIME': <25}"
                f"{'GAP': <20}{'NODES': <10}{'ARCS': <5}\n")

    # Escrever os dados normalmente
    with open(args.output_file, 'a') as f:
        f.write(
            f"{args.input_file: <12}{args.heuristic: <10}{args.start_node: <10}{cost: <20}{end_time - start_time: <25}"
            f"{gap(cost, args.best_known_solution): <20}{graph.dimension: <10}{graph.arcs: <5}\n")


def gap(fs, fs_star):
    return 100 * ((fs - fs_star) / fs_star)


if __name__ == '__main__':
    main()
