# DockerBI

El presente micro proyecto tiene como objetivo emplear un modelo ARIMA para predecir los aportes a caja de compensación que realizan 3 empresas. Se alimenta de un dataset con aportes desde el año 2018 al 2023 y predice 60 meses posteriores a la última fecha reportada.

## Construcción de Contenedor
Con la siguiente instrucción se construye el Contenedor a partir del archivo Dockerfile.
**docker build -t streamlit .**
### Nota: Solo es necesario descargar el Dockerfile para la ejecución del proyecto. Esto se debe a que en la construcción del contenedor se descargan los archivos necesarios de este repositorio.

## Ejecución del proyecto.
Para ejecutar el proyecto se debe emplear la siguiente instrucción:
**docker run -p 8501:8501 streamlit**

## Visualización del proyecto.
En un navegador, se debe utilizar la siguiente URL:
**http://localhost:8501**
Muchas gracias.