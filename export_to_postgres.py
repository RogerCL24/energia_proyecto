import pandas as pd
from db_config import get_engine

TABLE_NAME="facturas_energia"
CSV_FILE = "./output/consumos_limpios.csv"

engine = get_engine()
df = pd.read_csv(CSV_FILE)

df.to_sql(TABLE_NAME,con=engine, if_exists="replace", index=False)

print(f"Datos guardados en la tabla {TABLE_NAME}")