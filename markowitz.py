import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')

#1º PARTE: Análise de Portfólio

acoes = ['ITUB4.SA', 'BBDC4.SA', 'DIRR3.SA', 'JBSS3.SA','GUAR3.SA', 'PSSA3.SA']

ydata = yf.download(acoes, '2015-01-01', '2023-12-31', '1d');
dados = ydata["Adj Close"]

dados = dados *100 / dados.iloc[0]
display(dados)

dados.plot(figsize = (15,5));

dados_chg = dados.pct_change()
dados_chg = dados_chg.fillna(0)

ret_acc = (dados.iloc[-1] / dados.iloc[0])-1
print("Retorno acumulado:\n", ret_acc)

ret_aa = ((dados.iloc[-1]/dados.iloc[0])**(1/5))-1
print("Retorno anualizado:\n", ret_aa)

vol_aa = dados_chg.std()*np.sqrt(252)
print("Vol anualizada:\n", vol_aa)

#Calculo da correlação dos dados
dados_chg.corr()

dados[['GUAR3.SA', 'JBSS3.SA']].plot(figsize = (15,5));

dados_chg[['GUAR3.SA', 'JBSS3.SA']].iloc[200:220].plot(figsize = (15,5));

port_pesos = [0, 0, 0.5, 0, 0.5, 0]
dados['PORT1'] = dados.dot(port_pesos)

display(dados)

dados[['GUAR3.SA', 'JBSS3.SA', 'PORT1']].plot(figsize = (15,5));

dados_chg = dados.pct_change()
dados_chg = dados_chg.fillna(0)

ret_acc = (dados.iloc[dados.count()[0]-1] / dados.iloc[0])-1
print("Retorno acumulado:\n", ret_acc)
ret_aa = ((dados.iloc[-1]/dados.iloc[0])**(1/5))-1
print("Ret aa:\n", ret_aa)

vol_aa = dados_chg.std()*np.sqrt(252)
print("Vol aa:\n", vol_aa)

#Calcular drawdown
ddown = pd.DataFrame()

for ativo in dados.columns:
  list = []
  for ind in range(dados.count()[0]):
    list.append((dados[ativo].iloc[ind]/dados[ativo].iloc[:ind+1].max()-1)*100)
  ddown[ativo]=list

ddown['Data']=dados.index.values
ddown.set_index(keys = 'Data', inplace = True)

#display(ddown)
print(ddown.min())

ddown[['GUAR3.SA', 'JBSS3.SA', 'PORT1']].plot(figsize = (15,5));

# 2º PARTE: Fronteira Eficiente de Markowitz

dados=dados.drop(['PORT1'], axis=1)
dados_chg=dados_chg.drop(['PORT1'], axis=1)

dados

def calc_ret_vol(ativos, ativos_chg, port_pesos):
  port = ativos.dot(port_pesos)
  port_chg =port.pct_change()
  port_chg = port_chg.fillna(0)
  ret = ((port.iloc[-1]/port.iloc[0])**(1/5))-1
  vol = port_chg.std()*np.sqrt(252)
  return ret, vol

#Portfolio com 2 ativos: JBSS3 e GUAR3
points = []
min_vol_ret = [100, 0] #[vol, ret]
port_pesos = [0, 0, 0, 0, 0, 0]
for w in range(0, 101, 5):
  ret, vol = calc_ret_vol(dados, dados_chg, [0, 0,  w/100, 0, (1-w/100), 0])
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
plt.scatter(lp[[1][:]],lp[[0][:]]);
plt.ylabel("Retorno");
plt.xlabel("Volatilidade");

plt.scatter(vol_aa['GUAR3.SA'], ret_aa['GUAR3.SA'], color='red');
plt.text(vol_aa['GUAR3.SA'], ret_aa['GUAR3.SA'], 'GUAR3');

plt.scatter(vol_aa['JBSS3.SA'], ret_aa['JBSS3.SA'], color='red');
plt.text(vol_aa['JBSS3.SA'], ret_aa['JBSS3.SA'], 'JBSS3');

plt.scatter(min_vol_ret[0], min_vol_ret[1], color='green');
plt.text(min_vol_ret[0], min_vol_ret[1], 'Min. Vol.');

dados['PORT1'] = dados.dot(port_pesos)
dados_chg = dados.pct_change()
dados_chg = dados_chg.fillna(0)

ret_aa = ((dados.iloc[-1]/dados.iloc[0])**(1/5))-1
print("Ret aa:\n", ret_aa)
vol_aa = dados_chg.std()*np.sqrt(252)
print("Vol aa:\n", vol_aa)

#Calcular drawdown
ddown = pd.DataFrame()

for ativo in dados.columns:
  list = []
  for ind in range(dados.count()[0]):
    list.append((dados[ativo].iloc[ind]/dados[ativo].iloc[:ind+1].max()-1)*100)
  ddown[ativo]=list

ddown['Data']=dados.index.values
ddown.set_index(keys = 'Data', inplace = True)

#display(ddown)
print(ddown.min())

dados=dados.drop(['PORT1'], axis=1)
dados_chg=dados_chg.drop(['PORT1'], axis=1)

#Portfolio com 3 ativos: JBSS3, GUAR3 e PSSA3
points = []
min_vol_ret = [100, 0]
port_pesos = [0, 0, 0, 0, 0, 0]
for w1 in range(0, 101, 5):
  for w2 in range(0, 101-w1, 5):
    ret, vol = calc_ret_vol(dados, dados_chg, [0, 0, w1/100, 0, w2/100, (1-w1/100-w2/100)])
    #print("Aloc:", round(w1/100, 2), round(w2/100, 2), round(1-w1/100-w2/100, 2), "Ret:", round(ret, 3), "Vol:", round(vol, 3))
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

lp = np.array(points).T
plt.scatter(lp[[1][:]],lp[[0][:]]);
plt.ylabel("Retorno");
plt.xlabel("Volatilidade");

plt.scatter(vol_aa['GUAR3.SA'], ret_aa['GUAR3.SA'], color='red');
plt.text(vol_aa['GUAR3.SA'], ret_aa['GUAR3.SA'], 'GUAR3');

plt.scatter(vol_aa['JBSS3.SA'], ret_aa['JBSS3.SA'], color='red');
plt.text(vol_aa['JBSS3.SA'], ret_aa['JBSS3.SA'], 'JBSS3');

plt.scatter(vol_aa['PSSA3.SA'], ret_aa['PSSA3.SA'], color='red');
plt.text(vol_aa['PSSA3.SA'], ret_aa['PSSA3.SA'], 'PSSA3');

plt.scatter(min_vol_ret[0], min_vol_ret[1], color='green');
plt.text(min_vol_ret[0], min_vol_ret[1], 'Min. Vol.');

dados['PORT1'] = dados.dot(port_pesos)
dados_chg = (dados - dados.shift(1)) / dados.shift(1)
dados_chg = dados_chg.fillna(0)

ret_aa = ((dados.iloc[-1]/dados.iloc[0])**(1/5))-1
print("Ret aa:\n", ret_aa)
vol_aa = dados_chg.std()*np.sqrt(252)
print("Vol aa:\n", vol_aa)

#Calcular drawdown (valor de queda de um ativo em comparação ao valor máximo de cotação anterior)
ddown = pd.DataFrame()

for ativo in dados.columns:
  list = []
  for ind in range(dados.count()[0]):
    list.append((dados[ativo].iloc[ind]/dados[ativo].iloc[:ind+1].max()-1)*100)
  ddown[ativo]=list

ddown['Data']=dados.index.values
ddown.set_index(keys = 'Data', inplace = True)

#display(ddown)
print(ddown.min())

ddown[['JBSS3.SA', 'GUAR3.SA', 'PSSA3.SA', 'PORT1']].plot(figsize = (15,5));

dados[['JBSS3.SA', 'GUAR3.SA', 'PSSA3.SA', 'PORT1']].plot(figsize = (15,5));