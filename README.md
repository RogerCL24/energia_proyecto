# Dashboard Energía

Este proyecto permite visualizar y analizar el consumo energético y comparar tarifas facturadas con el precio del mercado (pool eléctrico).

## Funcionalidades

- Dashboard interactivo con Streamlit
- Ingesta automática de datos vía script programado (cron)
- Comparativa contra mercado
- Métricas clave: consumo, coste medio, potencial de ahorro

## Cómo ejecutar

1. Clonar repositorio:
```
git clone https://github.com/TU-USUARIO/energia-proyecto.git
cd energia-proyecto
```


2. Crear entorno virtual:
```
python3 -m venv venv
source venv/bin/activate
```


3. Instalar dependencias:
```
pip install -r requirements.txt
```


4. Lanzar dashboard:
```
streamlit run dashboard.py
```



## Programación con cron

El script `get_precio_pool.py` se ejecuta cada hora vía `cron` para actualizar el precio del mercado.


