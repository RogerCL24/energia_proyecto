import requests
import pandas as pd
from db_config import get_engine
from datetime import datetime, timedelta


engine = get_engine()

today = datetime.today()

# Llamada a la API
start_date = (today - timedelta(days=3)).strftime("%Y-%m-%dT00:00")
end_date = today.strftime("%Y-%m-%dT23:59")

url = f"https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real" 
params = {
    "start_date": start_date,
    "end_date": end_date,
    "time_trunc": "hour"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    values = data['included'][0]['attributes']['values']

    df_pool = pd.DataFrame(values)
    df_pool['datetime'] = pd.to_datetime(df_pool['datetime'])
    df_pool.rename(columns={'value': 'precio_pool_eur_mwh'}, inplace=True)

    # -> eur/kWh
    df_pool['precio_pool_eur_kwh'] = df_pool['precio_pool_eur_mwh'] / 1000
    
    # Guardado
    df_pool.to_sql("precio_pool", con=engine, if_exists="replace", index=False)

    print(f"Precios pool actualizados hasta {end_date}")
else: 
    print(f"Error al llamar a la API: {response.status_code}")