import numpy as np
import matplotlib.pyplot as plt


def plot_graphic(rt_3opt, rt_grasp, instancias):

    # Número de instâncias
    n = len(instancias)

    # Posições das instâncias no eixo X
    ind = np.arange(n)

    # Criação do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Criando as barras para as heurísticas
    bar_width = 0.3  # Ajuste a largura para compensar a remoção de uma barra

    # Ajustar as posições para garantir que as barras fiquem alinhadas e com o mesmo espaçamento
    ax.bar(ind - bar_width / 2, rt_3opt, bar_width, label='3-OPT', color='#00008B')
    ax.bar(ind + bar_width / 2, rt_grasp, bar_width, label='GRASP', color='#A9A9A9')

    # Adicionando rótulos, título e legendas
    ax.set_xlabel('Instâncias')
    ax.set_ylabel('Tempo de Execução (segundos)')
    ax.set_title('Tempo de Execução')
    ax.set_xticks(ind)
    ax.set_xticklabels(instancias, rotation=45, ha='right')
    ax.legend()

    # Exibindo o gráfico
    plt.tight_layout()  # Ajusta o layout para não cortar nada
    plt.show()

def plot_graphic_log(rt_3opt, rt_grasp, instancias):
    # Número de instâncias
    n = len(instancias)

    # Posições das instâncias no eixo X
    ind = np.arange(n)

    # Criação do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Largura das barras
    bar_width = 0.3  # Ajuste a largura para compensar a remoção de uma barra

    # Ajustar as posições para garantir que as barras fiquem alinhadas e com o mesmo espaçamento
    ax.bar(ind - bar_width / 2, rt_3opt, bar_width, label='3-OPT', color='#00008B')  # Cor Tomate
    ax.bar(ind + bar_width / 2, rt_grasp, bar_width, label='GRASP', color='#A9A9A9')  # Cor LightSeaGreen

    # Definindo a escala logarítmica no eixo Y
    ax.set_yscale('log')

    # Adicionando rótulos, título e legendas
    ax.set_xlabel('Instâncias')
    ax.set_ylabel('Tempo de Execução (segundos)')
    ax.set_title('Tempo de Execução - (Escala Logarítmica)')
    ax.set_xticks(ind)
    ax.set_xticklabels(instancias, rotation=45, ha='right')
    ax.legend()

    # Exibindo o gráfico
    plt.tight_layout()  # Ajusta o layout para não cortar nada
    plt.show()

def calculate_ci(valores_gaps, nome, benchmarks):

    # benchmarks = [f"Benchmark {i+1}" for i in range(20)]  # Nomes dos benchmarks
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
    plt.boxplot(dados, tick_labels=['3-OPT', 'GRASP'], patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='red', linewidth=1.5),
                whiskerprops=dict(color='blue'),
                capprops=dict(color='blue'),
                flierprops=dict(marker='o', color='blue', alpha=0.5))

    # Adicionando título e rótulos
    plt.title('Boxplot de Gaps', fontsize=14)
    plt.ylabel('Gap', fontsize=12)
    plt.xlabel('Algoritmo', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Mostrando o gráfico
    plt.tight_layout()
    plt.show()

def box_plot_alphas(dados):
    # Criando o boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot(dados, tick_labels=['0.25', '0.5', '0.75', '1.0'], patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='red', linewidth=1.5),
                whiskerprops=dict(color='blue'),
                capprops=dict(color='blue'),
                flierprops=dict(marker='o', color='blue', alpha=0.5))

    # Adicionando título e rótulos
    plt.title('Boxplot - Avaliação Parâmetro ALPHA', fontsize=14)
    plt.ylabel('Gap', fontsize=12)
    plt.xlabel('Alpha', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Mostrando o gráfico
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':

    gaps_3opt = [5.325484925216114, 7.513544758725459, 6.886594308954089, 1.3284258769290713, 1.6116929418915757,
                 5.7005106141606365, 2.812088211291299, 3.966912415730664, 3.2131738370465763, 1.1079185782529926,
                 2.776725312779963, 3.281928562076173, 2.341076393447998, 2.6166575846300724, 0.82799396670231,
                 6.164828783444121, 7.703725390989318, 2.4711545657736216, 0.31253470738470746, 6.6714575015762385]

    rt_3opt = [18941.109269948996, 2.1880533319999813, 1535.561020235, 1557.0649181519984, 4757.821760028,
               667.6021021309971, 6.60929553099777, 254.95071903800272, 683.2204907509986, 404.98796532499546,
               54.138547012000345, 617.9474464329978, 750.5467141469999, 612.4759026199972, 412.65518922999763,
               534.0189127980011, 34.1412457760016, 43827.675052583, 162.3595915320002, 3227.1050715900055]

    gaps_grasp = [5.628071376583577, 0.03136968846576342, 2.4745169761348236, 3.298535600958567, 2.6124858050254227,
                  5.809104184930387, 0.9224464952093564, 4.089058155939852, 2.58061962922277, 1.791426027427248,
                  0.7478598091869395, 3.1842465063911742, 1.5026761533171393, 1.3213344386771417, 0.553471233061944,
                  5.621718214216966, 3.376298792547974, 5.071627817966653, 0.5199267045380582, 1.5231821284269123]

    rt_grasp = [13407.873700099997, 14.079250100068748, 990.5622559001204, 1707.8906696999911, 4416.366219900083,
                142.46091210003942, 11.124443400185555, 42.669171900022775, 147.78867419995368, 147.19550130004063,
                148.3807520000264, 143.50885370001197, 145.56756710004993, 188.10390210011974, 71.03432379988953,
                130.94476440013386, 144.6828053998761, 56058.11728559993, 44.19731059996411, 6477.7205825999845]

    nomes = ['a280.tsp', 'berlin52.tsp', 'ch130.tsp', 'ch150.tsp', 'd198.tsp', 'eil101.tsp', 'eil51.tsp',
            'eil76.tsp', 'kroA100.tsp', 'kroB100.tsp', 'kroC100.tsp', 'kroD100.tsp', 'kroE100.tsp', 'lin105.tsp',
            'pr76.tsp', 'rat99.tsp', 'rd100.tsp', 'rd400.tsp', 'st70.tsp', 'ts225.tsp']

    dados = [gaps_3opt, gaps_grasp]

    alpha_25 = ([2.5423696612679487, 3.6004479843625226, 1.5192037571582269, 0.8611567700085986, 1.022979334144066] +
                [4.0996844939989545, 2.9867485506000957, 0.731910610287666, 2.25157673191546, 1.9478883541180] +
                [4.205634323199452, 4.052688865261727, 5.181274307230675, 5.413396722947111, 5.464385527690677] +
                [1.9557485113144295, 2.109095141799088, 2.5100771787286438, 0.642217880228581, 1.1378398534338128] +
                [2.4100910858226734, 2.7769608715999246, 2.6189687856617807, 3.435672491193145, 2.4417903842489035])

    alpha_5 = ([0.03136968846576342, 1.815173073550073, 0.03136968846577549, 0.03136968846576342, 1.022979334144054] +
               [1.6211681632334138, 2.2512063175542556, 2.988103929086967, 3.018502429944232, 2.3684468132139815] +
               [4.5017232724201754, 4.701978410233537, 4.902794383439351, 5.0198260436685755, 5.2253651800268965] +
               [0.8971586569817015, 0.47819379898094905, 1.2776394630920023, 1.1653666730945325, 1.24127641066118] +
               [1.5283007052584487, 2.3414197933571916, 2.2649729890706483, 2.758813421326337, 1.9814869456593915])

    alpha_75 = ([3.517065800157336, 3.5656812471083668, 1.8905185746903783, 1.6441440569791823, 1.0229793341440419] +
                [4.023556425945699, 3.731672074362899, 3.617599501238031, 3.805947990661455, 3.5474086002712983] +
                [4.960147877881994, 4.4170602898465905,5.2963918556634635, 5.713247297216757, 5.680107535155703] +
                [2.5108036533521028, 2.377957648129276, 2.1788346829523313, 1.8609267922232582, 1.845671411263892] +
                [3.003190439413444, 3.40521832920287, 3.1975201856926607, 2.911703780637321, 2.350664489339932])

    alpha_1 = ([4.088979099567223, 4.315226190832321, 3.127056046715614, 2.6251342922580236, 2.569588772443376] +
               [5.135068919228527, 4.356308330070394, 4.127757535074396, 3.838402342246098, 3.779284790083322] +
               [5.000740902000643, 6.180375386011068, 5.164685943925088, 5.646554486442624, 5.267698231347584] +
               [1.858447785599069, 2.8414708430546476, 1.415100430347125, 1.3172148491067248, 1.272792534964389] +
               [3.9204829824468983, 2.5478772584544322, 2.536668518747185, 2.696564143623854, 2.58551771100144])

    dados_par = [alpha_25, alpha_5, alpha_75, alpha_1]

    # Gráfico Box Plot
    box_plot_alphas(dados_par)
    #
    # # Intervalos de Confiança
    # calculate_ci(gaps_3opt, '3-OPT', nomes)
    # calculate_ci(gaps_grasp, 'GRASP', nomes)

    # Gráfico Run Time
    # plot_graphic(rt_3opt, rt_grasp, nomes)

    # plot_graphic_log(rt_3opt, rt_grasp, nomes)

