import streamlit as st
import pandas as pd

# Cargar datos
obras = pd.read_csv("clean-data/obras_clean.csv")
avisos = pd.read_csv("clean-data/avisos_clean.csv")

st.title("Dashboard")

# Métricas
st.write(f"Obras: {len(obras)}")
st.write(f"Avisos: {len(avisos)}")

# Tablas
st.dataframe(obras.head(10))
st.dataframe(avisos.head(10))
