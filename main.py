import time
import pandas as pd
from conexion_sql import ConexionSQL
from gestor_archivos import GestorArchivos
from procesamiento_datos import ProcesamientoDatos
from modelo_predictivo_arima import ModeloPredictivoARIMA

# Implementación
start_time = time.time()

# Inicialización de objetos
conexion = ConexionSQL('servidor', 'nombreBD', 'Usuario', 'Pass')
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
gestor_archivos.guardar_datos_csv(df_resultado, 'SalidaDatosAportesPred.csv')

elapsed_time = time.time() - start_time
print(f'Tiempo de ejecución: {elapsed_time} segundos')