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

def validar_texto(texto, nombre_campo):
    return bool(texto.strip())

def registrar_expediente(expedientes):
    solicitante = input("Nombre del solicitante: ").strip()
    documento = input("DNI (8 digitos): ").strip()
    asunto = input("Asunto: ").strip()
    tipo_documento = input("Tipo de documento: ").strip()
    if not validar_texto(solicitante, "solicitante") or not validar_texto(asunto, "asunto") or not validar_texto(tipo_documento, "tipo"):
        print("Hay campos obligatorios vacios.")
        return
    if not (documento.isdigit() and len(documento) == 8):
        print("DNI no valido.")
        return
    expedientes.append({"codigo": generar_codigo(expedientes), "solicitante": solicitante,
                        "dni": documento, "asunto": asunto, "tipo_documento": tipo_documento})
    guardar_expedientes(expedientes)

def buscar_expediente(expedientes, codigo):
    for expediente in expedientes:
        if expediente["codigo"].upper() == codigo.strip().upper():
            return expediente
    return None

def ordenar_expedientes(expedientes):
    expedientes.sort(key=lambda item: item["solicitante"].casefold())
    guardar_expedientes(expedientes)

def listar_expedientes(expedientes):
    for expediente in expedientes:
        print(expediente)
