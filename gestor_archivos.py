import pandas as pd

class GestorArchivos:
    @staticmethod
    def cargar_datos_csv(ruta):
        df = pd.read_csv(ruta, parse_dates=['fecha'], index_col='fecha', sep=';')
        return df

    @staticmethod
    def guardar_datos_csv(df, ruta):
        df.to_csv(ruta, sep=';')
        print('Carga de datos completa')