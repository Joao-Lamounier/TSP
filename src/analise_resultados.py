import numpy as np
import matplotlib.pyplot as plt


def plot_graphic(rt_2opt, rt_rev, rt_3opt, instancias):

    # Número de instâncias
    n = len(instancias)

    # Posições das instâncias no eixo X
    ind = np.arange(n)

    # Criação do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Criando as barras para as heurísticas
    bar_width = 0.2  # Assumindo que todas as larguras de barra são iguais

    # Ajustar as posições para garantir que as barras fiquem alinhadas e com o mesmo espaçamento
    ax.bar(ind - bar_width, rt_2opt, bar_width, label='2-OPT', color='b')
    ax.bar(ind, rt_rev, bar_width, label='REVERSE', color='g')
    ax.bar(ind + bar_width, rt_3opt, bar_width, label='3-OPT', color='r')

    # Adicionando rótulos, título e legendas
    ax.set_xlabel('Instâncias')
    ax.set_ylabel('Tempo de Execução (segundos)')
    ax.set_title('Tempo de Execução - Busca Local')
    ax.set_xticks(ind)
    ax.set_xticklabels(instancias)
    ax.legend()

    # Exibindo o gráfico
    plt.tight_layout()  # Ajusta o layout para não cortar nada
    plt.show()


def calculate_ci(valores_gaps, nome):

    benchmarks = [f"Benchmark {i+1}" for i in range(20)]  # Nomes dos benchmarks
    x = np.arange(len(benchmarks))  # Índices dos benchmarks

    # Calcular média e intervalo de confiança global
    media_global = np.mean(valores_gaps)
    desvio_padrao = np.std(valores_gaps, ddof=1)  # Desvio padrão amostral
    n = len(valores_gaps)  # Tamanho da amostra
    z_critico = 1.96  # Para 95% de confiança
    intervalo_conf = z_critico * (desvio_padrao / np.sqrt(n))  # Intervalo de confiança

    # Criar gráfico
    plt.figure(figsize=(12, 6))
    plt.scatter(x, valores_gaps, color='skyblue', alpha=0.8, label='Valores dos Gaps')
    plt.axhline(float(media_global), color='red', linestyle='--', label=f"Média Global = {media_global:.2f}")
    plt.fill_between(
        [-0.5, len(benchmarks)-0.5],
        media_global - intervalo_conf,
        media_global + intervalo_conf,
        color='red', alpha=0.2, label=f"IC 95% [{media_global - intervalo_conf:.2f}, {media_global + intervalo_conf:.2f}]"
    )
    plt.xticks(x, benchmarks, rotation=45, ha='right')  # Benchmarks como rótulos no eixo X
    plt.ylabel('Valor do Gap')
    plt.xlabel('Benchmarks')
    plt.title('Intervalo de Confiança - ' + nome)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Mostrar gráfico
    plt.show()


def box_plot(dados):
    # Criando o boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot(dados, tick_labels=['2-OPT', 'REVERSE', '3-OPT'], patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='red', linewidth=1.5),
                whiskerprops=dict(color='blue'),
                capprops=dict(color='blue'),
                flierprops=dict(marker='o', color='blue', alpha=0.5))

    # Adicionando título e rótulos
    plt.title('Boxplot de Gaps dos Algoritmos de Busca Local', fontsize=14)
    plt.ylabel('Gap', fontsize=12)
    plt.xlabel('Busca Local', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Mostrando o gráfico
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':

    gaps_2opt = [8.722983530823097, 7.588890259865752, 11.06972802503398, 4.736141154662574, 2.312544858893704,
                 5.1346251883426275, 2.8404710557627237, 6.55833793011476, 9.034229601621977, 5.231027424835082,
                 6.906860953597653, 4.767194033720428, 9.788722630990936, 8.914426132015448, 1.8711530183819916,
                 4.968908599348264, 9.65109341792673, 7.280741754457084, 3.6835057031521163, 5.354833673085255]

    gaps_rev = [8.722983530823097, 7.588890259865752, 11.06972802503398, 4.737595448960528, 2.312544858893704,
                10.628054783821, 4.944427977108956, 6.55833793011476, 6.738961375063292, 5.3477472716082035,
                6.906860953597653, 4.767194033720428, 10.10146193602423, 6.563589461442189, 5.784486726769165,
                8.231796218374361, 7.879458610510441, 7.280741754457084, 4.067899527098706, 5.354833673085255]

    gaps_3opt = [5.325484925216114, 7.513544758725459, 6.886594308954089, 1.3284258769290713, 1.6116929418915757,
                 5.7005106141606365, 2.812088211291299, 3.966912415730664, 3.2131738370465763, 1.1079185782529926,
                 2.776725312779963, 3.281928562076173, 2.341076393447998, 2.6166575846300724, 0.82799396670231,
                 6.164828783444121, 7.703725390989318, 2.4711545657736216, 0.31253470738470746, 6.6714575015762385]

    dados = [gaps_2opt, gaps_rev, gaps_3opt]

    # Gráfico Box Plot
    box_plot(dados)

    # Intervalos de Confiança
    calculate_ci(gaps_2opt, '2-OPT')
    calculate_ci(gaps_rev, 'Reverse')
    calculate_ci(gaps_3opt, '3-OPT')

    # Gráfico Run Time
