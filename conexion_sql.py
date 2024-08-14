from sqlalchemy import create_engine
import pandas as pd

class ConexionSQL:
    def __init__(self, servidor, nombreBD, usuario, password):
        self.engine = create_engine(f"mssql+pyodbc://{usuario}:{password}@{servidor}/{nombreBD}?driver=ODBC+Driver+17+for+SQL+Server")

    def extraer_datos_sql(self, query):
        with self.engine.connect() as con:
            df = pd.read_sql(query, con, parse_dates=['fecha'], index_col='fecha')
        return df

    def cargar_datos_sql(self, df, tabla):
        with self.engine.connect() as con:
            df.to_sql(tabla, con=con, if_exists='replace')