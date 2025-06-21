
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db_config import get_engine

engine = get_engine()

TABLE_NAME = "facturas_energia"

@st.cache_data
def load_data():
    query = f"SELECT * FROM {TABLE_NAME}"
    df = pd.read_sql(query, con=engine)
    df['periodo_inicio'] = pd.to_datetime(df['periodo_inicio'])
    df['periodo_fin'] = pd.to_datetime(df['periodo_fin'])
    return df

df = load_data()

st.title("Dashboard Consumo Energetico")


# Filtro periodo
min_date = df['periodo_inicio'].min()
max_date = df['periodo_fin'].max()

periodo = st.date_input("Selecciona rango de fechas", value=(min_date, max_date))

# Filtrado datos
df_filtrado = df[
    (df['periodo_inicio'] >= pd.to_datetime(periodo[0])) &
    (df['periodo_fin'] <= pd.to_datetime(periodo[1]))
]

# Metricas
total_consumo = df_filtrado['consumo_total_kWh'].sum()
total_coste = df_filtrado['coste_total_euros'].sum()
coste_medio_kWh = total_coste / total_consumo if total_consumo > 0 else 0

st.metric("Consumo total (kWh)", f"{total_consumo:.2f} kWh")
st.metric("Coste total (€)", f"{total_coste:.2f} €")
st.metric("Coste medio por kWh", f"{coste_medio_kWh:.3f} €/kWh")

# Grafico del consumo mensual
df_filtrado['mes'] = df_filtrado['periodo_inicio'].dt.to_period('M')
consumo_mes = df_filtrado.groupby('mes').agg({
    'consumo_total_kWh': 'sum',
    'coste_total_euros': 'sum'
}).reset_index()

fig, ax = plt.subplots()
ax.bar(consumo_mes['mes'].astype(str), consumo_mes['consumo_total_kWh'], color='skyblue')
ax.set_title("Consumo mensual (kWh)")
ax.set_xlabel("Mes")
ax.set_ylabel("kWh")
st.pyplot(fig)

# Mostrar tabla de facturas
st.subheader("Detalle facturas")
st.dataframe(df_filtrado)