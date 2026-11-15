import json
import os

ARCHIVO_DATOS = "expedientes.json"

def cargar_expedientes():
    if not os.path.exists(ARCHIVO_DATOS):
        return []
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return []

def guardar_expedientes(expedientes):
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(expedientes, archivo, ensure_ascii=False, indent=4)

def generar_codigo(expedientes):
    mayor = 0
    for expediente in expedientes:
        try:
            mayor = max(mayor, int(expediente["codigo"].replace("EXP-", "")))
        except (ValueError, KeyError):
            continue
    return f"EXP-{mayor + 1:04d}"
