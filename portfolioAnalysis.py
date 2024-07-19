import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_drawdown(data):
    ddown = pd.DataFrame()
    for ativo in data.columns:
        list = []
        for ind in range(data.shape[0]):
            max_val = data[ativo].iloc[:ind+1].max()
            if max_val == 0:
                list.append(0)
            else:
                list.append((data[ativo].iloc[ind] / max_val - 1) * 100)
        ddown[ativo] = list

    ddown['Data'] = data.index.values
    ddown.set_index(keys='Data', inplace=True)
    return ddown

def calc_ret_vol(ativos, ativos_chg, port_pesos):
    port = ativos.dot(port_pesos)
    port_chg = port.pct_change()
    port_chg = port_chg.fillna(0)
    initial_value = port.iloc[0]
    final_value = port.iloc[-1]
    
    if initial_value == 0 or final_value == 0 or np.isnan(initial_value) or np.isnan(final_value):
        ret = np.nan
    else:
        ret = ((final_value / initial_value) ** (1 / 5)) - 1
    
    vol = port_chg.std() * np.sqrt(252)
    return ret, vol
