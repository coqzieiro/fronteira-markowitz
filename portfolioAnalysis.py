import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_drawdown(data):
    ddown = pd.DataFrame()

    for ativo in data.columns:
        list = []
        for ind in range(data.count()[0]):
            list.append((data[ativo].iloc[ind] / data[ativo].iloc[:ind+1].max() - 1) * 100)
        ddown[ativo] = list

    ddown['Data'] = data.index.values
    ddown.set_index(keys='Data', inplace=True)
    return ddown

def calc_ret_vol(ativos, ativos_chg, port_pesos):
    port = ativos.dot(port_pesos)
    port_chg = port.pct_change()
    port_chg = port_chg.fillna(0)
    ret = ((port.iloc[-1] / port.iloc[0]) ** (1 / 5)) - 1
    vol = port_chg.std() * np.sqrt(252)
    return ret, vol

def plot_efficient_frontier(dados, dados_chg, tickers):
    n = len(tickers)
    returns = []
    volatilities = []
    weights_list = []

    for w1 in range(0, 101, 5):
        for w2 in range(0, 101-w1, 5):
            port_pesos = [0, 0, w1/100, 0, w2/100, (1-w1/100-w2/100)]
            ret, vol = calc_ret_vol(dados[tickers], dados_chg[tickers], port_pesos[:n])
            returns.append(ret)
            volatilities.append(vol)
            weights_list.append(port_pesos)

    returns = np.array(returns)
    volatilities = np.array(volatilities)

    plt.figure(figsize=(10, 6))
    plt.scatter(volatilities, returns, c=returns / volatilities, marker='o')
    plt.grid(True)
    plt.xlabel('Volatilidade Anualizada')
    plt.ylabel('Retorno Anualizado')
    plt.colorbar(label='Sharpe ratio')
    plt.title('Fronteira Eficiente')
    plt.show()

    min_vol_idx = volatilities.argmin()
    min_vol_ret = returns[min_vol_idx]
    min_vol_vol = volatilities[min_vol_idx]
    min_vol_weights = weights_list[min_vol_idx]

    plt.scatter(min_vol_vol, min_vol_ret, color='green')
    plt.text(min_vol_vol, min_vol_ret, 'Min. Vol.')
    plt.show()

    return min_vol_weights
