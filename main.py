import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from portfolioAnalysis import calculate_drawdown, calc_ret_vol

sns.set(style='whitegrid')

def main():
    # 1ª PARTE: Análise de Portfólio
    acoes = ['ITUB4.SA', 'BBDC4.SA', 'DIRR3.SA', 'PETR4.SA', 'VALE3.SA', 'ABEV3.SA']
    ydata = yf.download(acoes, '2015-01-01', '2024-06-30', '1d')
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

    # Ações da VALE e PETROBRÁS
    dados[['PETR4.SA', 'VALE3.SA']].plot(figsize=(15, 5))
    plt.show()

    dados_chg[['PETR4.SA', 'VALE3.SA']].iloc[200:220].plot(figsize=(15, 5))
    plt.show()

    port_pesos = [0, 0, 0.5, 0, 0.5, 0]
    dados['PORT1'] = dados.dot(port_pesos)

    print(dados)

    dados[['PETR4.SA', 'VALE3.SA', 'PORT1']].plot(figsize=(15, 5))
    plt.show()

    dados_chg = dados.pct_change()
    dados_chg = dados_chg.fillna(0)

    # Análise PORT 1
    ret_acc = (dados.iloc[-1] / dados.iloc[0]) - 1
    print("Retorno acumulado:\n", ret_acc)

    ret_aa = ((dados.iloc[-1] / dados.iloc[0]) ** (1 / 5)) - 1
    print("Retorno anualizado:\n", ret_aa)

    vol_aa = dados_chg.std() * np.sqrt(252)
    print("Volatilidade anualizada:\n", vol_aa)

    # Calcular drawdown
    ddown = calculate_drawdown(dados)
    print(ddown.min())

    ddown[['PETR4.SA', 'VALE3.SA', 'PORT1']].plot(figsize=(15, 5))
    plt.show()

    # 2ª PARTE: Fronteira Eficiente de Markowitz
    dados = dados.drop(['PORT1'], axis=1)
    dados_chg = dados_chg.drop(['PORT1'], axis=1)

    # Portfolio com 2 ativos: PETR4 e VALE3
    points = []
    min_vol_ret = [100, 0] #[vol, ret]
    port_pesos = [0, 0, 0, 0, 0, 0]
    for w in range(0, 101, 5):
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

    lp = np.array(points).T
    plt.scatter(lp[1], lp[0])
    plt.ylabel("Retorno")
    plt.xlabel("Volatilidade")

    plt.scatter(vol_aa['PETR4.SA'], ret_aa['PETR4.SA'], color='red')
    plt.text(vol_aa['PETR4.SA'], ret_aa['PETR4.SA'], 'PETR4')

    plt.scatter(vol_aa['VALE3.SA'], ret_aa['VALE3.SA'], color='red')
    plt.text(vol_aa['VALE3.SA'], ret_aa['VALE3.SA'], 'VALE3')

    plt.scatter(min_vol_ret[0], min_vol_ret[1], color='green')
    plt.text(min_vol_ret[0], min_vol_ret[1], 'Min. Vol.')
    plt.show()

    dados['PORT1'] = dados.dot(port_pesos)
    dados_chg = dados.pct_change()
    dados_chg = dados_chg.fillna(0)

    ret_aa = ((dados.iloc[-1] / dados.iloc[0]) ** (1 / 5)) - 1
    print("Ret aa:\n", ret_aa)
    vol_aa = dados_chg.std() * np.sqrt(252)
    print("Vol aa:\n", vol_aa)

    # Calcular drawdown
    ddown = calculate_drawdown(dados)
    print(ddown.min())

    ddown[['PETR4.SA', 'VALE3.SA', 'PORT1']].plot(figsize=(15, 5))
    plt.show()

    dados = dados.drop(['PORT1'], axis=1)
    dados_chg = dados_chg.drop(['PORT1'], axis=1)

    # Portfolio com 3 ativos: PETR4, VALE3 e ABEV3
    points = []
    min_vol_ret = [100, 0]
    port_pesos = [0, 0, 0, 0, 0, 0]
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

    # Gráfico da curva da Fronteira Eficiente de Markowitz: 3 Ações
    lp = np.array(points).T
    plt.scatter(lp[1], lp[0])
    plt.ylabel("Retorno")
    plt.xlabel("Volatilidade")

    plt.scatter(vol_aa['PETR4.SA'], ret_aa['PETR4.SA'], color='red')
    plt.text(vol_aa['PETR4.SA'], ret_aa['PETR4.SA'], 'PETR4')

    plt.scatter(vol_aa['VALE3.SA'], ret_aa['VALE3.SA'], color='red')
    plt.text(vol_aa['VALE3.SA'], ret_aa['VALE3.SA'], 'VALE3')

    plt.scatter(vol_aa['ABEV3.SA'], ret_aa['ABEV3.SA'], color='red')
    plt.text(vol_aa['ABEV3.SA'], ret_aa['ABEV3.SA'], 'ABEV3')

    plt.scatter(min_vol_ret[0], min_vol_ret[1], color='green')
    plt.text(min_vol_ret[0], min_vol_ret[1], 'Min. Vol.')
    plt.show()

    dados['PORT1'] = dados.dot(port_pesos)
    dados_chg = dados.pct_change()
    dados_chg = dados_chg.fillna(0)

    ret_aa = ((dados.iloc[-1] / dados.iloc[0]) ** (1 / 5)) - 1
    print("Ret aa:\n", ret_aa)
    vol_aa = dados_chg.std() * np.sqrt(252)
    print("Vol aa:\n", vol_aa)

    # Calcular drawdown
    ddown = calculate_drawdown(dados)
    print(ddown.min())

    ddown[['PETR4.SA', 'VALE3.SA', 'ABEV3.SA', 'PORT1']].plot(figsize=(15, 5))
    plt.show()

if __name__ == "__main__":
    main()
