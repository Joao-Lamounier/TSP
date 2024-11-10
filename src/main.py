import argparse
from time import perf_counter

from entities.graph import Graph
from heuristics.PrimPreorderMST import PrimPreorderMST


def main():
    # Configuração dos argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Solucionador TSP usando heurísticas")
    parser.add_argument("input_file", type=str, help="Caminho para o arquivo de entrada .tsp")
    parser.add_argument("output_file", type=str, help="Caminho para o arquivo de saída dos resultados")
    parser.add_argument("best_known_solution", type=float, help="Melhor solução conhecida para a instância")
    parser.add_argument("heuristic", type=str, choices=["MST", "NN"], help="Heurística a ser usada (MST ou NN)")
    parser.add_argument("--start_node", type=int, default=0, help="Nó de início (opcional, padrão: 0)")

    args = parser.parse_args()

    # Carregar o grafo a partir do arquivo de entrada
    folder = 'files/benchmark/'
    graph = Graph.load_graph(folder + args.input_file)
    graph.start_node = args.start_node

    # Escolher e executar a heurística

    start_time = perf_counter()

    if args.heuristic == "MST":
        tsp_solver = PrimPreorderMST(graph)
        path, cost = tsp_solver.solve_tsp()
    # elif args.heuristic == "NN":
    #     path, cost = tsp_solver.nearest_neighbor()

    end_time = perf_counter()

    with open(args.output_file, 'w') as f:
        # Cabeçalho
        f.write(
            f"{'INSTANCE':<10}{'METHOD':<10}{'PARAM':<10}{'OBJECTIVE':<20}{'RUNTIME':<25}{'GAP':<20}{'NODES':<10}{'ARCS':<5}\n")

        # Dados
        f.write(
            f"{args.input_file:<10}{args.heuristic:<10}{args.start_node:<10}{cost:<20}{end_time - start_time:<25}{gap(cost, args.start_node):<20}{graph.dimension:<10}{graph.arcs:<5}\n")


def gap(fs, fs_star):
    return 100 * ((fs - fs_star) / fs_star)

if __name__ == '__main__':
    main()
