
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from pandas.tseries.offsets import DateOffset
import statsmodels.api as sm
from pmdarima import auto_arima
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt

import time

start_time = time.time()


#Conexión a base de datos SQL




mesesPredc = 60 


######################## Extraer Datos SQL ####################################################

#Credenciales para acceso a base de datos
servidor = 'servidor'
nombreBD = 'nombreBD'
Usuario = 'Usuario'
Pass = 'Pass'

engine = create_engine("mssql+pyodbc://"+Usuario+":"+Pass+"@"+servidor+"/"+nombreBD+"?driver=ODBC+Driver+17+for+SQL+Server")

#Se Extrae datos de archivos csv
def ExtraerDatosCSV ():
   dt = pd.read_csv('QrySQLPruebaEntrada.csv', parse_dates=['fecha'], index_col='fecha',sep=';')
   print('Carga de datos csv completa')
   return dt
#Se Extrae datos de consulta Base de datos SQL
def ExtractorDatosSQL ():
    con = engine.connect()
    qry = "SELECT * FROM [Stage].[dbo].[VIEW_APORTETOTAL_PREDICTIVO] ORDER BY fecha ASC"
    dt = pd.read_sql(qry, con, parse_dates=['fecha'], index_col='fecha')
    con.close()

    return dt

######################## Cargar Datos SQL ####################################################

servidor = 'servidor'
nombreBD = 'nombreBD'
Usuario = 'Usuario'
Pass = 'Pass'

engine = create_engine("mssql+pyodbc://"+Usuario+":"+Pass+"@"+servidor+"/"+nombreBD+"?driver=ODBC+Driver+17+for+SQL+Server")
#Se Cargan datos a archivos csv
def CargarDatosCSV(dfPred):
    
  ResultadoCsv = pd.DataFrame(dfPred)
  ResultadoCsv.to_csv('QrySQLPruebaSalidaV3.csv',sep=';')

  return print('Carga de datos completa')

#Se Carga datos a Base de datos SQL
def CargarDatosSQL(dfPred):

  con = engine.connect()
  dfPred.to_sql('TablaDemoPredictivoTotal',con=engine, if_exists= 'replace')
  con.close()

  return print('Carga de datos completa')

######################## Limpieza y transformacion de Datos ####################################################
#Depuración de Datos: Reemplaza 0 y datos vacios

def DepurarCerosyNull(dfDep):

  ListColumName = list(dfDep.columns.values)
  meses = 6
  for j in ListColumName:

    for i in range(len(dfDep)):

      if dfDep.iloc[i][j] == 0 or pd.isnull(dfDep.iloc[i][j]):
        valores = dfDep.iloc[i-meses:i][j]
        mediaMovil = np.round(valores.mean()) if not valores.empty else 0
        dfDep.iloc[i] = dfDep.iloc[i].replace([0],mediaMovil)
  
  return dfDep

def MediasMoviles(dfPred):
   
  ListColumName = list(dfPred.columns.values)

  count = 0
  df = dfPred
  for i in ListColumName:

    MediaMovilQ = np.round(dfPred[i].rolling(3).mean())
    MediaMovilS = np.round(dfPred[i].rolling(6).mean())
    MediaMovilA = np.round(dfPred[i].rolling(12).mean())

    columna = dfPred.columns.values[count] + 'MediaMovilQ'
    columna1 = dfPred.columns.values[count] + 'MediaMovilS'
    columna2 = dfPred.columns.values[count] + 'MediaMovilA'
    df[columna] = MediaMovilQ
    df[columna1] = MediaMovilS
    df[columna2] = MediaMovilA
    count += 1

  return df

######################## Modelo predictivo ARIMA ####################################################
def ModeloPredictivo(dfIn):

  ListColumName = list(dfIn.columns.values)

  for i in ListColumName:
    dfIn[i] = dfIn[i].astype('float64')

  pred_date=[dfIn.index[-1] + DateOffset(months=x)for x in range(0,mesesPredc)]
  pred_date=pd.DataFrame(index=pred_date[1:],columns=dfIn.columns)

  
  count = 0
  df = dfIn
  df=pd.concat([df,pred_date])
  for i in ListColumName:

    model = auto_arima(dfIn[i],start_P=1,start_q=1,max_P=6,max_q=6,m=12,start_p=0,d=1,D=1,trace=True,error_action='ignore',suppress_warnings=True,stepwise=True)
    results = model.fit(dfIn[i])
    
    parametrosModelo = str(model)

    p = int(parametrosModelo[7])
    d = int(parametrosModelo[9])
    q = int(parametrosModelo[11])

    ModeloAutoArima = np.round(results.predict(n_periods = mesesPredc))

    model= sm.tsa.arima.ARIMA(dfIn[i],order=(p,d,q))
    results=model.fit()
    ModeloArima = np.round(results.predict())

    valorPred = pd.concat([ModeloArima,ModeloAutoArima])

    columna = dfIn.columns.values[count] + 'Pred'
    
    df[columna] = valorPred.astype('int64')
    count += 1

  return df


##################################### implementación de formulas #########################################
df = ExtraerDatosCSV()
#df = ExtractorDatosSQL ()
categoria = df.columns.values[0]
ls = list(df[categoria].unique())

dfCarga = pd.DataFrame()
categoriaLS = []

for i in ls:

  df1 = df[df[categoria] == i]
  df1.drop([categoria], axis=1, inplace=True)

  categoriaLS = []

  df1 = DepurarCerosyNull(df1)
  df1 = ModeloPredictivo(df1)
  df1 = MediasMoviles(df1)

  categoriaLS = [i for k in range(len(df1))]
  df1[categoria] = categoriaLS
  dfCarga = pd.concat([dfCarga,df1])
 

  
CargarDatosCSV(dfCarga)
#CargarDatosSQL(dfCarga)

elapsed_time = time.time() - start_time

print(elapsed_time)






