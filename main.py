import time
import pandas as pd
from conexion_sql import ConexionSQL
from gestor_archivos import GestorArchivos
from procesamiento_datos import ProcesamientoDatos
from modelo_predictivo_arima import ModeloPredictivoARIMA
from visualizador_web import Visualuzador

# Implementación
start_time = time.time()

# Inicialización de objetos
#conexion = ConexionSQL('servidor', 'nombreBD', 'Usuario', 'Pass')
gestor_archivos = GestorArchivos()

# Cargar datos
df = gestor_archivos.cargar_datos_csv('CargaDatosAportes.csv')

categoria = df.columns[0]
categorias_unicas = df[categoria].unique()

df_resultado = pd.DataFrame()

print(categoria, categorias_unicas)

# Procesamiento de datos por categoría
for cat in categorias_unicas:
    df_cat = df[df[categoria] == cat].drop(columns=[categoria])

    # Depuración y transformación de datos
    df_cat = ProcesamientoDatos.depurar_ceros_y_null(df_cat)
    modelo = ModeloPredictivoARIMA(df_cat, meses_prediccion=60)
    df_cat = modelo.entrenar_y_predecir()
    df_cat = ProcesamientoDatos.medias_moviles(df_cat)

    df_cat[categoria] = cat
    df_resultado = pd.concat([df_resultado, df_cat])

# Guardar resultado
df_resultado.index.name = 'fecha'
df_resultado['Indice'] = range(1, len(df_resultado) + 1)
gestor_archivos.guardar_datos_csv(df_resultado, 'SalidaDatosAportesPred.csv')

# Visualizar Resultados
df_resultado = df_resultado.reset_index()
df_resultado['fecha'] = pd.to_datetime(df_resultado['fecha'])
filtro = df_resultado['Empresa'].unique()
df_resultado.set_index(df_resultado['fecha'].index, inplace=True)
df_resultado['Aporte'] = pd.to_numeric(df_resultado['Aporte'])
df_resultado['AportePred'] = pd.to_numeric(df_resultado['AportePred'])
columnas = ['Aporte', 'AportePred']

parametrosVilualizar = Visualuzador(
                                    df= df_resultado,
                                    filtro= filtro,
                                    indice= 'fecha',
                                    columnas= columnas).graficoLineas()

elapsed_time = time.time() - start_time
print(f'Tiempo de ejecución: {elapsed_time} segundos')