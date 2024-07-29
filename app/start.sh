#!/bin/bash

# Ejecutar el script de entrenamiento
python train_vanna.py

# Iniciar la aplicación Streamlit
streamlit run main.py --server.port 8080 --server.address 0.0.0.0