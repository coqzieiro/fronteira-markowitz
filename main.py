import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from portfolioAnalysis import calculate_drawdown, calc_ret_vol

# Configurações para o estilo do seaborn
sns.set(style='whitegrid')

def main():
    # 1ª PARTE: Análise de Portfólio
    # Definição dos tickers das ações a serem analisadas
    acoes = ['ITUB4.SA', 'BBDC4.SA', 'DIRR3.SA', 'PETR4.SA', 'VALE3.SA', 'ABEV3.SA']
    
    # Baixa os dados históricos de fechamento ajustado das ações selecionadas
    ydata = yf.download(acoes, '2015-01-01', '2024-06-30', '1d')
    dados = ydata["Adj Close"]

    # Normaliza os dados para 100 no início do período
    dados = dados * 100 / dados.iloc[0]
    print(dados)

    # Plota os dados normalizados
    dados.plot(figsize=(15, 5))
    plt.show()

    # Calcula a variação percentual diária dos dados
    dados_chg = dados.pct_change().fillna(0)

    # Calcula o retorno acumulado
    ret_acc = (dados.iloc[-1] / dados.iloc[0]) - 1
    print("Retorno acumulado:\n", ret_acc)

    # Calcula o retorno anualizado
    ret_aa = ((dados.iloc[-1] / dados.iloc[0]) ** (1 / 5)) - 1
    print("Retorno anualizado:\n", ret_aa)

    # Calcula a volatilidade anualizada
    vol_aa = dados_chg.std() * np.sqrt(252)
    print("Volatilidade anualizada:\n", vol_aa)

    # Calcula a matriz de correlação dos retornos diários
    corr_matrix = dados_chg.corr()
    print("Correlação:\n", corr_matrix)

    # Plota os dados de VALE3 e PETR4
    dados[['PETR4.SA', 'VALE3.SA']].plot(figsize=(15, 5))
    plt.show()

    # Plota uma janela de 20 dias dos retornos diários de VALE3 e PETR4
    dados_chg[['PETR4.SA', 'VALE3.SA']].iloc[200:220].plot(figsize=(15, 5))
    plt.show()

    # Define pesos para um portfólio com 50% em VALE3 e 50% em PETR4
    port_pesos = [0, 0, 0.5, 0, 0.5, 0]
    dados['PORT1'] = dados.dot(port_pesos)

    print(dados)

    # Plota o portfólio juntamente com VALE3 e PETR4
    dados[['PETR4.SA', 'VALE3.SA', 'PORT1']].plot(figsize=(15, 5))
    plt.show()

    # Recalcula a variação percentual diária incluindo o portfólio
    dados_chg = dados.pct_change().fillna(0)

    # Calcula o retorno acumulado do portfólio
    ret_acc = (dados.iloc[-1] / dados.iloc[0]) - 1
    print("Retorno acumulado:\n", ret_acc)

    # Calcula o retorno anualizado do portfólio
    ret_aa = ((dados.iloc[-1] / dados.iloc[0]) ** (1 / 5)) - 1
    print("Retorno anualizado:\n", ret_aa)

    # Calcula a volatilidade anualizada do portfólio
    vol_aa = dados_chg.std() * np.sqrt(252)
    print("Volatilidade anualizada:\n", vol_aa)

    # Calcula o drawdown do portfólio
    ddown = calculate_drawdown(dados)
    print(ddown.min())

    # Plota o drawdown do portfólio juntamente com VALE3 e PETR4
    ddown[['PETR4.SA', 'VALE3.SA', 'PORT1']].plot(figsize=(15, 5))
    plt.show()

    # 2ª PARTE: Fronteira Eficiente de Markowitz
    # Remove o portfólio dos dados para iniciar a análise de fronteira eficiente
    dados = dados.drop(['PORT1'], axis=1)
    dados_chg = dados_chg.drop(['PORT1'], axis=1)

    # Portfolio com 2 ativos: PETR4 e VALE3
    points = []  # Lista para armazenar os pontos da fronteira eficiente
    min_vol_ret = [100, 0]  # [volatilidade, retorno] do portfólio com menor volatilidade
    port_pesos = [0, 0, 0, 0, 0, 0]  # Inicializa pesos do portfólio

    for w in range(0, 101, 5):  # Itera sobre possíveis alocações em incrementos de 5%
        ret, vol = calc_ret_vol(dados[['PETR4.SA', 'VALE3.SA']], dados_chg[['PETR4.SA', 'VALE3.SA']], [w/100, 1-w/100])
        print(f"Aloc:{round(w/100, 2):.2f} {round(1-(w/100),2):.2f} Ret:{round(ret, 3):.3f} Vol:{round(vol, 3):.3f}")
        points.append([ret, vol])
        if vol < min_vol_ret[0]:
            min_vol_ret[0] = vol
            min_vol_ret[1] = ret
            port_pesos[2] = w/100
            port_pesos[4] = 1-w/100

    print(min_vol_ret)
    print(port_pesos)

    # Converte os pontos para numpy array e plota a fronteira eficiente
    lp = np.array(points).T
    plt.scatter(lp[1], lp[0])
    plt.ylabel("Retorno")
    plt.xlabel("Volatilidade")

    # Plota os pontos individuais de PETR4 e VALE3 no gráfico da fronteira eficiente
    plt.scatter(vol_aa['PETR4.SA'], ret_aa['PETR4.SA'], color='red')
    plt.text(vol_aa['PETR4.SA'], ret_aa['PETR4.SA'], 'PETR4')

    plt.scatter(vol_aa['VALE3.SA'], ret_aa['VALE3.SA'], color='red')
    plt.text(vol_aa['VALE3.SA'], ret_aa['VALE3.SA'], 'VALE3')

    # Plota o ponto de mínima volatilidade
    plt.scatter(min_vol_ret[0], min_vol_ret[1], color='green')
    plt.text(min_vol_ret[0], min_vol_ret[1], 'Min. Vol.')
    plt.show()

    # Calcula os dados do portfólio com os pesos encontrados
    dados['PORT1'] = dados.dot(port_pesos)
    dados_chg = dados.pct_change().fillna(0)

    # Calcula o retorno anualizado e a volatilidade anualizada do portfólio
    ret_aa = ((dados.iloc[-1] / dados.iloc[0]) ** (1 / 5)) - 1
    print("Ret aa:\n", ret_aa)
    vol_aa = dados_chg.std() * np.sqrt(252)
    print("Vol aa:\n", vol_aa)

    # Calcula o drawdown do portfólio
    ddown = calculate_drawdown(dados)
    print(ddown.min())

    # Plota o drawdown do portfólio juntamente com VALE3 e PETR4
    ddown[['PETR4.SA', 'VALE3.SA', 'PORT1']].plot(figsize=(15, 5))
    plt.show()

    # Remove o portfólio dos dados para a próxima análise
    dados = dados.drop(['PORT1'], axis=1)
    dados_chg = dados_chg.drop(['PORT1'], axis=1)

    # Portfolio com 3 ativos: PETR4, VALE3 e ABEV3
    points = []  # Lista para armazenar os pontos da fronteira eficiente
    min_vol_ret = [100, 0]  # [volatilidade, retorno] do portfólio com menor volatilidade
    port_pesos = [0, 0, 0, 0, 0, 0]  # Inicializa pesos do portfólio

    # Itera sobre possíveis alocações em incrementos de 5% para cada par de ativos
    for w1 in range(0, 101, 5):
        for w2 in range(0, 101 - w1, 5):
            ret, vol = calc_ret_vol(dados[['PETR4.SA', 'VALE3.SA', 'ABEV3.SA']], dados_chg[['PETR4.SA', 'VALE3.SA', 'ABEV3.SA']], [w1/100, w2/100, 1-w1/100-w2/100])
            print(f"Aloc:{round(w1/100, 2):.2f} {round(w2/100, 2):.2f} {round(1-w1/100-w2/100, 2):.2f} Ret:{round(ret, 3):.3f} Vol:{round(vol, 3):.3f}")
            points.append([ret, vol])
            if vol < min_vol_ret[0]:
                min_vol_ret[0] = vol
                min_vol_ret[1] = ret
                port_pesos[2] = w1/100
                port_pesos[4] = w2/100
                port_pesos[5] = 1-w1/100-w2/100
    
    print(min_vol_ret)
    print(port_pesos)

    # Converte os pontos para numpy array e plota a fronteira eficiente
    lp = np.array(points).T
    plt.scatter(lp[1], lp[0])
    plt.ylabel("Retorno")
    plt.xlabel("Volatilidade")

    # Plota os pontos individuais de PETR4, VALE3 e ABEV3 no gráfico da fronteira eficiente
    plt.scatter(vol_aa['PETR4.SA'], ret_aa['PETR4.SA'], color='red')
    plt.text(vol_aa['PETR4.SA'], ret_aa['PETR4.SA'], 'PETR4')

    plt.scatter(vol_aa['VALE3.SA'], ret_aa['VALE3.SA'], color='red')
    plt.text(vol_aa['VALE3.SA'], ret_aa['VALE3.SA'], 'VALE3')

    plt.scatter(vol_aa['ABEV3.SA'], ret_aa['ABEV3.SA'], color='red')
    plt.text(vol_aa['ABEV3.SA'], ret_aa['ABEV3.SA'], 'ABEV3')

    # Plota o ponto de mínima volatilidade
    plt.scatter(min_vol_ret[0], min_vol_ret[1], color='green')
    plt.text(min_vol_ret[0], min_vol_ret[1], 'Min. Vol.')
    plt.show()

    # Calcula os dados do portfólio com os pesos encontrados
    dados['PORT1'] = dados.dot(port_pesos)
    dados_chg = dados.pct_change().fillna(0)

    # Calcula o retorno anualizado e a volatilidade anualizada do portfólio
    ret_aa = ((dados.iloc[-1] / dados.iloc[0]) ** (1 / 5)) - 1
    print("Ret aa:\n", ret_aa)
    vol_aa = dados_chg.std() * np.sqrt(252)
    print("Vol aa:\n", vol_aa)

    # Calcula o drawdown do portfólio
    ddown = calculate_drawdown(dados)
    print(ddown.min())

    # Plota o drawdown do portfólio juntamente com VALE3, PETR4 e ABEV3
    ddown[['PETR4.SA', 'VALE3.SA', 'ABEV3.SA', 'PORT1']].plot(figsize=(15, 5))
    plt.show()

if __name__ == "__main__":
    main()
