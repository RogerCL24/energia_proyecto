# query_postgres.py
import pandas as pd
from db_config import get_engine

TABLE_NAME = "facturas_energia"
engine = get_engine()

query_consumo_mensual = f"""
SELECT
    DATE_TRUNC('month', periodo_inicio::date) AS mes,
    SUM("consumo_total_kWh") AS consumo_kWh,
    SUM(coste_total_euros) AS coste_euros
FROM {TABLE_NAME}
GROUP BY mes
ORDER BY mes;
"""

query_coste_medio = f"""
SELECT
    SUM(coste_total_euros) / SUM("consumo_total_kWh") AS coste_medio_kWh
FROM {TABLE_NAME};
"""

df_consumo = pd.read_sql(query_consumo_mensual, con=engine)
df_coste_medio = pd.read_sql(query_coste_medio, con=engine)

df_consumo["mes"] = pd.to_datetime(df_consumo["mes"]).dt.strftime("%B %Y")
df_coste_medio["coste_medio_kwh"] = df_coste_medio["coste_medio_kwh"].round(4)

print("📅 Consumo mensual:")
print(df_consumo.to_string(index=False))

print("\n💰 Coste medio por kWh:")
print(df_coste_medio.to_string(index=False))
