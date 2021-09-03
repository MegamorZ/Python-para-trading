import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

def contar_positivos_negativos_neutros(df):
  positivos = 0
  negativos = 0
  neutros = 0
  for i in range(len(df)) :
    row = df.iloc[i]
    color = row["vela"]
    if color == "verde":
      positivos += 1
    elif color == "roja":
      negativos += 1 
    else:
      neutros +=1
  return positivos, negativos, neutros

def devolver_top_n_variacion(df, n=10):
  data = df . copy()
  data["variacion"]  = data["Close"].pct_change() * 100 
  return data.sort_values("variacion", ascending=False).head(n)

def devolver_top_n_variacion(df, n=10, es_de_baja=True):
  data = df . copy() 
  data["variacion"]  = data["Close"].pct_change() * 100 
  data.dropna(inplace=True)
  return data.sort_values("variacion", ascending = es_de_baja ).head(n)

def devolver_con_percentil(df):
  data = df . copy()
  data["variacion"]  = data["Close"].pct_change() * 100 
  data.dropna(inplace=True)
  data["rank_variacion"] = data["variacion"].rank()
  data["rank_variacion_pct"] = data["variacion"].rank(pct= True)
  return data

plt.style.use('dark_background')
# fig, ax = plt.subplots(figsize=(14,7), nrows=2)

def descarga_datos(ticker, desde='2015-01-01', media_movil=200):
    try:
      data = yf.download(ticker, auto_adjust=True, start=desde)
      data['variacion_diaria'] = data["Close"].pct_change()*100
      data['volatilidad'] = data['variacion_diaria'].rolling(40).std()
      clave = 'sma_' + str(media_movil)   # "sma_50"
      data[clave] = data.Close.rolling(media_movil).mean()
      data.dropna(inplace=True)

      data['percentil'] = data.volatilidad.rank(pct=True) *100
      mediana = data.volatilidad.median()

      fig, ax = plt.subplots(figsize=(14,7), nrows=2)
      data.volatilidad.hist(bins=20, width=0.3, ax=ax[0])

    

      ax[0].set_title(f'Histograma de Volatilidad de {ticker.upper()}')
      ax[0].axvline(mediana, color='green', lw=4)
      ax[0].annotate(f'Mediana: {mediana:.2f}', xy=(mediana, 15), color='g', 
                rotation=90,  va='center', ha='right', fontsize=16)
      ax[1].plot(data['percentil'].iloc[-365:])
      ax[1].set_title(f'Percentil de Volatilidad {ticker.upper()} últimos 365 dias')
      ax[1].set_ylim(0,100)
      ax[1].grid(True)
      plt.subplots_adjust(wspace=None, hspace=0.3)
      plt.show()
      return data
    except:
      pass
      print ('me mandaste cualquiera')

# descarga_datos('XPEV', desde='2010-01-01', media_movil=50)

