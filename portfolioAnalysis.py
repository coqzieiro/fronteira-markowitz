import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_drawdown(data):
    """
    Calcula o drawdown (queda em relação ao pico anterior) para cada ativo em um DataFrame.

    Parâmetros:
    data (DataFrame): DataFrame contendo os preços dos ativos.

    Retorna:
    DataFrame: DataFrame contendo o drawdown percentual de cada ativo.
    """
    ddown = pd.DataFrame()  # DataFrame para armazenar os drawdowns
    for ativo in data.columns:
        list = []
        for ind in range(data.shape[0]):
            max_val = data[ativo].iloc[:ind+1].max()  # Encontra o valor máximo até o ponto atual
            if max_val == 0:
                list.append(0)  # Evita divisão por zero
            else:
                list.append((data[ativo].iloc[ind] / max_val - 1) * 100)  # Calcula o drawdown percentual
        ddown[ativo] = list

    ddown['Data'] = data.index.values  # Adiciona as datas como uma coluna
    ddown.set_index(keys='Data', inplace=True)  # Define a coluna de datas como índice
    return ddown

def calc_ret_vol(ativos, ativos_chg, port_pesos):
    """
    Calcula o retorno anualizado e a volatilidade anualizada de um portfólio.

    Parâmetros:
    ativos (DataFrame): DataFrame contendo os preços dos ativos do portfólio.
    ativos_chg (DataFrame): DataFrame contendo as variações percentuais diárias dos ativos do portfólio.
    port_pesos (list): Lista de pesos dos ativos no portfólio.

    Retorna:
    tuple: Retorno anualizado e volatilidade anualizada do portfólio.
    """
    port = ativos.dot(port_pesos)  # Calcula o valor do portfólio com base nos pesos dos ativos
    port_chg = port.pct_change().fillna(0)  # Calcula as variações percentuais diárias do portfólio e preenche valores NaN com zero
    initial_value = port.iloc[0]  # Valor inicial do portfólio
    final_value = port.iloc[-1]  # Valor final do portfólio
    
    # Verifica se os valores inicial e final são válidos para calcular o retorno
    if initial_value == 0 or final_value == 0 or np.isnan(initial_value) or np.isnan(final_value):
        ret = np.nan  # Retorno não calculável
    else:
        ret = ((final_value / initial_value) ** (1 / 5)) - 1  # Calcula o retorno anualizado
    
    vol = port_chg.std() * np.sqrt(252)  # Calcula a volatilidade anualizada
    return ret, vol  # Retorna o retorno anualizado e a volatilidade anualizada
