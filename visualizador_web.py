
import pandas as pd
import streamlit as st
import plotly.express as px

class Visualuzador:

    def __init__(self, df, filtro, indice, columnas):
            
            self.df = df
            self.indice = indice
            self.filtro = filtro
            self.columnas = columnas


    def graficoLineas(self):
    # Crear un filtro para seleccionar la empresa
    
        empresa_seleccionada = st.selectbox('Selecciona una empresa:', self.filtro)

        # Filtrar el DataFrame por la empresa seleccionada
        df_filtrado = self.df[self.df['Empresa'] == empresa_seleccionada]

        # Crear el gráfico de líneas utilizando Plotly
        fig = px.line(
            df_filtrado,
            x=df_filtrado.index,
            y=self.columnas,
            labels={'x': self.indice, 'value': 'COP'},
            title=f'Tendencias Mensuales para {empresa_seleccionada}'
        )

        # Mostrar el gráfico en Streamlit
        return st.plotly_chart(fig, use_container_width=True)