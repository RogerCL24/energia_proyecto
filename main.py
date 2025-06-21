import pdfplumber
import pandas as pd
import re
import os

# Ruta al folder con los archivos a leer
FACTURAS_DIR = "./data/facturas_pdf/"
OUTPUT_FILE = "./output/consumos_limpios.csv"

# Funcion para extraer datos de las facturas (PDF)
def procesar_factura(pdf_path):
    print(f"Procesando: {pdf_path}")

    with pdfplumber.open(pdf_path) as pdf:
        texto = ""
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"

    # Regex múltiples, adaptadas a ElectroSur y LuzPlus
    fecha_factura = re.search(r"(?:Fecha de Factura|Fecha de Emisión):\s*(\d{2}/\d{2}/\d{4})", texto)
    periodo = re.search(r"(?:Periodo facturado|Periodo de consumo):\s*(\d{2}/\d{2}/\d{4})\s*(?:al|-)\s*(\d{2}/\d{2}/\d{4})", texto)
    cups = re.search(r"CUPS:\s*([A-Z0-9]+)", texto)

    # Consumo total
    consumo_total = re.search(r"(?:Energía consumida|Consumo Total)\s*:?[\n\r\s]*([\d\.,]+)\s*kWh", texto)

    # Precio de energía por kWh
    precio_energia = re.search(r"(?:Precio energía|Precio por kWh)\s*:?[\n\r\s]*([\d\.,]+)\s*€", texto)

    # Potencia contratada
    potencia_contratada = re.search(r"Potencia contratada\s*:?[\n\r\s]*([\d\.,]+)\s*kW", texto)

    # Total factura
    total_factura = re.search(r"(?:TOTAL A PAGAR|Total Factura)\s*:?[\n\r\s]*([\d\.,]+)\s*€", texto)

    # Impuestos
    impuestos_electricos = re.search(r"(?:Impuesto electricidad|Impuestos eléctricos)\s*:?[\n\r\s]*([\d\.,]+)\s*€", texto)
    iva = re.search(r"IVA.*?\s*([\d\.,]+)\s*€", texto)

    return {
        "archivo": os.path.basename(pdf_path),
        "fecha_factura": fecha_factura.group(1) if fecha_factura else None,
        "periodo_inicio": periodo.group(1) if periodo else None,
        "periodo_fin": periodo.group(2) if periodo else None,
        "cups": cups.group(1) if cups else None,
        "potencia_contratada_kW": float(potencia_contratada.group(1).replace(",", ".")) if potencia_contratada else None,
        "consumo_total_kWh": float(consumo_total.group(1).replace(",", ".")) if consumo_total else None,
        "precio_energia_eur_kWh": float(precio_energia.group(1).replace(",", ".")) if precio_energia else None,
        "coste_total_euros": float(total_factura.group(1).replace(",", ".")) if total_factura else None,
        "impuestos_electricos_euros": float(impuestos_electricos.group(1).replace(",", ".")) if impuestos_electricos else None,
        "iva_euros": float(iva.group(1).replace(",", ".")) if iva else None
    }

# Leer facturas
def procesar_todas_las_facturas():
    filas = []

    for filename in os.listdir(FACTURAS_DIR):
        if filename.endswith(".pdf"):
            ruta_pdf = os.path.join(FACTURAS_DIR, filename)
            datos = procesar_factura(ruta_pdf)
            filas.append(datos)
    
    # Guardamos los datos en CSV
    df = pd.DataFrame(filas)

    # Normalizar
    df["fecha_factura"] = pd.to_datetime(df["fecha_factura"], dayfirst=True, errors="coerce").dt.date
    df["periodo_inicio"] = pd.to_datetime(df["periodo_inicio"], dayfirst=True, errors="coerce").dt.date
    df["periodo_fin"] = pd.to_datetime(df["periodo_fin"], dayfirst=True, errors="coerce").dt.date

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Datos guardados en: {OUTPUT_FILE}")

if __name__ == "__main__":
    procesar_todas_las_facturas()