import streamlit as st
import pandas as pd
from db_config import get_engine
import matplotlib.pyplot as plt

TABLE_FACTURAS = "facturas_energia"
TABLE_POOL = "precio_pool"

# --- Conexión
engine = get_engine()

# --- Cargar datos
@st.cache_data
def load_facturas():
    df = pd.read_sql(f"SELECT * FROM {TABLE_FACTURAS};", con=engine)
    df['periodo_inicio'] = pd.to_datetime(df['periodo_inicio'])
    df['periodo_fin'] = pd.to_datetime(df['periodo_fin'])
    return df

@st.cache_data
def load_precio_pool():
    df = pd.read_sql(f"SELECT * FROM {TABLE_POOL};", con=engine)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

df_facturas = load_facturas()
df_pool = load_precio_pool()

# --- UI
st.title("📊 Dashboard Energía - Versión 2")

# Periodo general
min_date = df_facturas['periodo_inicio'].min()
max_date = df_facturas['periodo_fin'].max()

periodo = st.date_input("Selecciona rango de fechas", value=(min_date, max_date))

# --- Filtrado de facturas
df_filtrado = df_facturas[
    (df_facturas['periodo_inicio'] >= pd.to_datetime(periodo[0])) &
    (df_facturas['periodo_fin'] <= pd.to_datetime(periodo[1]))
]

total_consumo = df_filtrado['consumo_total_kWh'].sum()
total_coste = df_filtrado['coste_total_euros'].sum()
coste_medio_kwh = total_coste / total_consumo if total_consumo > 0 else 0

# --- Filtrado de precio pool
df_pool['datetime'] = df_pool['datetime'].dt.tz_localize(None)
df_pool_filtrado = df_pool[
    (df_pool['datetime'] >= pd.to_datetime(periodo[0])) &
    (df_pool['datetime'] <= pd.to_datetime(periodo[1]))
]

precio_pool_medio_kwh = df_pool_filtrado['precio_pool_eur_kwh'].mean()

# --- Métricas
st.header("🔢 Resumen")
col1, col2, col3 = st.columns(3)
col1.metric("Consumo total (kWh)", f"{total_consumo:.2f} kWh")
col2.metric("Coste total (€)", f"{total_coste:.2f} €")
col3.metric("Coste medio facturado", f"{coste_medio_kwh:.3f} €/kWh")

st.header("⚡ Comparativa con Mercado")
col4, col5 = st.columns(2)
col4.metric("Precio pool medio", f"{precio_pool_medio_kwh:.3f} €/kWh")

# Potencial ahorro (si hubieras pagado a precio pool)
coste_teorico_pool = precio_pool_medio_kwh * total_consumo
diferencia = total_coste - coste_teorico_pool

col5.metric(
    "Potencial ahorro",
    f"{diferencia:.2f} €",
    delta=f"{diferencia/total_coste*100:.1f} %"
)

# --- Gráfico comparativo
st.subheader("📈 Evolución precio pool (€ / kWh)")

fig, ax = plt.subplots()
ax.plot(df_pool_filtrado['datetime'], df_pool_filtrado['precio_pool_eur_kwh'], label="Precio Pool", color='green')
ax.axhline(y=coste_medio_kwh, color='red', linestyle='--', label="Tarifa contratada")
ax.legend()
ax.set_xlabel("Fecha")
ax.set_ylabel("€/kWh")
st.pyplot(fig)

# --- Tabla facturas
st.subheader("📋 Facturas detalle")
st.dataframe(df_filtrado)
