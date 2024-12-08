import matplotlib.pyplot as plt
import numpy as np

# Dados de gaps para três algoritmos (exemplo)
algoritmo1_gaps = np.random.uniform(0.5, 1.5, 30)  # Exemplo de gaps para o Algoritmo 1
algoritmo2_gaps = np.random.uniform(0.3, 1.2, 30)  # Exemplo de gaps para o Algoritmo 2
algoritmo3_gaps = np.random.uniform(0.2, 1.0, 30)  # Exemplo de gaps para o Algoritmo 3

# Consolidando os dados em uma lista
dados = [algoritmo1_gaps, algoritmo2_gaps, algoritmo3_gaps]

# Criando o boxplot
plt.figure(figsize=(8, 6))
plt.boxplot(dados, labels=['Algoritmo 1', 'Algoritmo 2', 'Algoritmo 3'], patch_artist=True,
            boxprops=dict(facecolor='lightblue', color='blue'),
            medianprops=dict(color='red', linewidth=1.5),
            whiskerprops=dict(color='blue'),
            capprops=dict(color='blue'),
            flierprops=dict(marker='o', color='blue', alpha=0.5))

# Adicionando título e rótulos
plt.title('Boxplot de Gaps dos Algoritmos de Busca Local', fontsize=14)
plt.ylabel('Gap', fontsize=12)
plt.xlabel('Algoritmos', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Mostrando o gráfico
plt.tight_layout()
plt.show()
