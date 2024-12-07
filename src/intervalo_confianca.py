# import numpy as np
# import matplotlib.pyplot as plt
#
#
# class ConfidenceInterval:
#
#     def __init__(self):
#         self.media = 0.0
#         self.ci = 0.0
#
#     @staticmethod
#     def calculate_ci():
#
#         # Gerar dados simulados
#         np.random.seed(42)
#         x = np.linspace(0, 10, 50)
#         y = 2.5 * x + np.random.normal(0, 2, size=len(x))
#
#         # Calcular média e intervalo de confiança
#         mean_y = np.mean(y)
#         confidence_interval = 1.96 * np.std(y) / np.sqrt(len(y))
#
#         # Plotar os dados e o intervalo de confiança
#         plt.figure(figsize=(8, 6))
#         plt.scatter(x, y, label="Dados", alpha=0.7)
#         plt.axhline(float(mean_y), color='red', linestyle='--', label=f"Média = {mean_y:.2f}")
#         plt.fill_between(
#             x, mean_y - confidence_interval, mean_y + confidence_interval,
#             color='red', alpha=0.2, label=f"Intervalo de Confiança"
#         )
#         plt.title("Gráfico com Intervalo de Confiança")
#         plt.xlabel("X")
#         plt.ylabel("Y")
#         plt.legend()
#         plt.show()
#
#
# if __name__ == '__main__':
#
#     ConfidenceInterval.calculate_ci()

import numpy as np
import matplotlib.pyplot as plt


class ConfidenceInterval:

    def __init__(self, gaps):
        self.gaps = gaps
        self.media = np.mean(self.gaps)

    @staticmethod
    def calculate_ci(valores_gaps):

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
        plt.title('Intervalo de Confiança Global dos Gaps')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Mostrar gráfico
        plt.show()


#
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Simulação de dados para 3 conjuntos
# np.random.seed(42)
# benchmarks = [f"Benchmark {i+1}" for i in range(20)]
# x = np.arange(len(benchmarks))
#
# # Conjunto 1
# valores_gaps1 = np.random.uniform(5, 10, size=20)
# media1 = np.mean(valores_gaps1)
# desvio1 = np.std(valores_gaps1, ddof=1)
# ic1 = 1.96 * (desvio1 / np.sqrt(len(valores_gaps1)))
#
# # Conjunto 2
# valores_gaps2 = np.random.uniform(4, 9, size=20)
# media2 = np.mean(valores_gaps2)
# desvio2 = np.std(valores_gaps2, ddof=1)
# ic2 = 1.96 * (desvio2 / np.sqrt(len(valores_gaps2)))
#
# # Conjunto 3
# valores_gaps3 = np.random.uniform(6, 11, size=20)
# media3 = np.mean(valores_gaps3)
# desvio3 = np.std(valores_gaps3, ddof=1)
# ic3 = 1.96 * (desvio3 / np.sqrt(len(valores_gaps3)))
#
# # Criar gráfico
# plt.figure(figsize=(12, 6))
#
# # Conjunto 1
# plt.scatter(x - 0.3, valores_gaps1, color='skyblue', alpha=0.8, label='Conjunto 1')
# plt.fill_between(
#     [-0.5, len(benchmarks)-0.5],
#     media1 - ic1, media1 + ic1,
#     color='blue', alpha=0.2, label=f"IC 95% Conjunto 1 [{media1 - ic1:.2f}, {media1 + ic1:.2f}]"
# )
#
# # Conjunto 2
# plt.scatter(x, valores_gaps2, color='lightgreen', alpha=0.8, label='Conjunto 2')
# plt.fill_between(
#     [-0.5, len(benchmarks)-0.5],
#     media2 - ic2, media2 + ic2,
#     color='green', alpha=0.2, label=f"IC 95% Conjunto 2 [{media2 - ic2:.2f}, {media2 + ic2:.2f}]"
# )
#
# # Conjunto 3
# plt.scatter(x + 0.3, valores_gaps3, color='salmon', alpha=0.8, label='Conjunto 3')
# plt.fill_between(
#     [-0.5, len(benchmarks)-0.5],
#     media3 - ic3, media3 + ic3,
#     color='red', alpha=0.2, label=f"IC 95% Conjunto 3 [{media3 - ic3:.2f}, {media3 + ic3:.2f}]"
# )
#
# # Estética
# plt.xticks(x, benchmarks, rotation=45, ha='right')
# plt.ylabel('Valor do Gap')
# plt.xlabel('Benchmarks')
# plt.title('Intervalos de Confiança de 3 Conjuntos')
# plt.legend()
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.tight_layout()
#
# # Mostrar gráfico
# plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
#
# # Simulação de dados
# np.random.seed(42)
# benchmarks = np.arange(1, 21)  # 20 benchmarks
#
# # Conjunto 1
# valores_gaps1 = np.random.uniform(5, 10, size=20)
# media1 = np.mean(valores_gaps1)
# desvio1 = np.std(valores_gaps1, ddof=1)
# ic1 = 1.96 * (desvio1 / np.sqrt(len(valores_gaps1)))
# limite_inf1 = valores_gaps1 - ic1
# limite_sup1 = valores_gaps1 + ic1
#
# # Conjunto 2
# valores_gaps2 = np.random.uniform(4, 9, size=20)
# media2 = np.mean(valores_gaps2)
# desvio2 = np.std(valores_gaps2, ddof=1)
# ic2 = 1.96 * (desvio2 / np.sqrt(len(valores_gaps2)))
# limite_inf2 = valores_gaps2 - ic2
# limite_sup2 = valores_gaps2 + ic2
#
# # Conjunto 3
# valores_gaps3 = np.random.uniform(6, 11, size=20)
# media3 = np.mean(valores_gaps3)
# desvio3 = np.std(valores_gaps3, ddof=1)
# ic3 = 1.96 * (desvio3 / np.sqrt(len(valores_gaps3)))
# limite_inf3 = valores_gaps3 - ic3
# limite_sup3 = valores_gaps3 + ic3
#
# # Criar figura com 3 subplots
# fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
#
# # Gráfico 1
# axs[0].plot(benchmarks, valores_gaps1, label='Conjunto 1', color='blue', marker='o')
# axs[0].fill_between(benchmarks, limite_inf1, limite_sup1, color='blue', alpha=0.2)
# axs[0].set_title('Conjunto 1')
# axs[0].set_ylabel('Valor do Gap')
# axs[0].grid(axis='y', linestyle='--', alpha=0.7)
# axs[0].legend()
#
# # Gráfico 2
# axs[1].plot(benchmarks, valores_gaps2, label='Conjunto 2', color='green', marker='s')
# axs[1].fill_between(benchmarks, limite_inf2, limite_sup2, color='green', alpha=0.2)
# axs[1].set_title('Conjunto 2')
# axs[1].set_ylabel('Valor do Gap')
# axs[1].grid(axis='y', linestyle='--', alpha=0.7)
# axs[1].legend()
#
# # Gráfico 3
# axs[2].plot(benchmarks, valores_gaps3, label='Conjunto 3', color='red', marker='^')
# axs[2].fill_between(benchmarks, limite_inf3, limite_sup3, color='red', alpha=0.2)
# axs[2].set_title('Conjunto 3')
# axs[2].set_xlabel('Benchmark')
# axs[2].set_ylabel('Valor do Gap')
# axs[2].grid(axis='y', linestyle='--', alpha=0.7)
# axs[2].legend()
#
# # Ajustar layout
# plt.tight_layout()
# plt.show()
