import numpy as np
import pandas as pd

class ProcesamientoDatos:
    @staticmethod
    def depurar_ceros_y_null(df):
        columnas = df.columns
        meses = 6
        for columna in columnas:
            for i in range(len(df)):
                if df.iloc[i][columna] == 0 or pd.isnull(df.iloc[i][columna]):
                    valores = df.iloc[i-meses:i][columna]
                    media_movil = np.round(valores.mean()) if not valores.empty else 0
                    df.iloc[i] = df.iloc[i].replace([0], media_movil)
        return df

    @staticmethod
    def medias_moviles(df):
        columnas = df.columns
        for columna in columnas:
            df[f'{columna}MediaMovilQ'] = np.round(df[columna].rolling(3).mean())
            df[f'{columna}MediaMovilS'] = np.round(df[columna].rolling(6).mean())
            df[f'{columna}MediaMovilA'] = np.round(df[columna].rolling(12).mean())
        return df