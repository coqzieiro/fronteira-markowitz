import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from portfolioAnalysis import calculate_drawdown, plot_efficient_frontier

sns.set(style='whitegrid')

def main():
    # 1ª PARTE: Análise de Portfólio
    acoes = ['ITUB4.SA', 'BBDC4.SA', 'DIRR3.SA', 'JBSS3.SA', 'GUAR3.SA', 'PSSA3.SA']
    ydata = yf.download(acoes, '2015-01-01', '2023-12-31', '1d')
    dados = ydata["Adj Close"]

    dados = dados * 100 / dados.iloc[0]
    print(dados)

    dados.plot(figsize=(15, 5))
    plt.show()

    dados_chg = dados.pct_change()
    dados_chg = dados_chg.fillna(0)

    ret_acc = (dados.iloc[-1] / dados.iloc[0]) - 1
    print("Retorno acumulado:\n", ret_acc)

    ret_aa = ((dados.iloc[-1] / dados.iloc[0]) ** (1 / 5)) - 1
    print("Retorno anualizado:\n", ret_aa)

    vol_aa = dados_chg.std() * np.sqrt(252)
    print("Volatilidade anualizada:\n", vol_aa)

    # Calculo da correlação dos dados
    corr_matrix = dados_chg.corr()
    print("Correlação:\n", corr_matrix)

    dados[['GUAR3.SA', 'JBSS3.SA']].plot(figsize=(15, 5))
    plt.show()

    dados_chg[['GUAR3.SA', 'JBSS3.SA']].iloc[200:220].plot(figsize=(15, 5))
    plt.show()

    port_pesos = [0, 0, 0.5, 0, 0.5, 0]
    dados['PORT1'] = dados.dot(port_pesos)

    print(dados)

    dados[['GUAR3.SA', 'JBSS3.SA', 'PORT1']].plot(figsize=(15, 5))
    plt.show()

    dados_chg = dados.pct_change()
    dados_chg = dados_chg.fillna(0)

    ret_acc = (dados.iloc[dados.count()[0] - 1] / dados.iloc[0]) - 1
    print("Retorno acumulado:\n", ret_acc)

    ret_aa = ((dados.iloc[-1] / dados.iloc[0]) ** (1 / 5)) - 1
    print("Retorno anualizado:\n", ret_aa)

    vol_aa = dados_chg.std() * np.sqrt(252)
    print("Volatilidade anualizada:\n", vol_aa)

    # Calcular drawdown
    ddown = calculate_drawdown(dados)
    print(ddown.min())

    ddown[['GUAR3.SA', 'JBSS3.SA', 'PORT1']].plot(figsize=(15, 5))
    plt.show()

    # 2ª PARTE: Fronteira Eficiente de Markowitz
    dados = dados.drop(['PORT1'], axis=1)
    dados_chg = dados_chg.drop(['PORT1'], axis=1)

    # Portfolio com 2 ativos: JBSS3 e GUAR3
    plot_efficient_frontier(dados, dados_chg, ['JBSS3.SA', 'GUAR3.SA'])

    # Portfolio com 3 ativos: JBSS3, GUAR3 e PSSA3
    plot_efficient_frontier(dados, dados_chg, ['JBSS3.SA', 'GUAR3.SA', 'PSSA3.SA'])

if __name__ == "__main__":
    main()