
import pandas as pd
import streamlit as st
import plotly.express as px


# Cargar el DataFrame (asegúrate de cargar el archivo correspondiente)
df = pd.read_csv('SalidaDatosAportesPred.csv', sep=';')

# Convertir el campo 'fecha' a datetime y establecerlo como índice
df['fecha'] = pd.to_datetime(df['fecha'])
df.set_index('fecha', inplace=True)
df['Aporte'] = pd.to_numeric(df['Aporte'])
df['AportePred'] = pd.to_numeric(df['AportePred'])
 
# Crear un filtro para seleccionar la empresa
empresas = df['Empresa'].unique()
empresa_seleccionada = st.selectbox('Selecciona una empresa:', empresas)

# Filtrar el DataFrame por la empresa seleccionada
df_filtrado = df[df['Empresa'] == empresa_seleccionada]

# Seleccionar las columnas para el gráfico
columnas_a_graficar = ['Aporte', 'AportePred']

# Crear el gráfico de líneas utilizando Plotly
fig = px.line(
    df_filtrado,
    x=df_filtrado.index,
    y=columnas_a_graficar,
    labels={'x': 'fecha', 'value': 'Aporte'},
    title=f'Tendencias Mensuales para {empresa_seleccionada}'
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)