"""
Prototipo de Mesa de Partes Digital
Curso: Fundamentos de Programación - CIIN1205P

Permite registrar, validar, buscar, ordenar y almacenar expedientes.
La persistencia se realiza en un archivo JSON para conservar los registros
entre ejecuciones del programa.
"""

import json
import os
from datetime import datetime

ARCHIVO_DATOS = "expedientes.json"


def cargar_expedientes():
    """Carga los expedientes guardados; si no existe el archivo, inicia una lista vacía."""
    if not os.path.exists(ARCHIVO_DATOS):
        return []
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return datos if isinstance(datos, list) else []
    except (json.JSONDecodeError, OSError):
        print("Advertencia: no se pudo leer el archivo. Se iniciará una lista vacía.")
        return []


def guardar_expedientes(expedientes):
    """Guarda la lista completa de expedientes en formato JSON."""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(expedientes, archivo, ensure_ascii=False, indent=4)


def validar_texto(texto, nombre_campo):
    """Comprueba que una cadena no esté vacía."""
    if not texto.strip():
        print(f"El campo {nombre_campo} es obligatorio.")
        return False
    return True


def generar_codigo(expedientes):
    """Genera un código correlativo para identificar cada expediente."""
    mayor = 0
    for expediente in expedientes:
        try:
            numero = int(expediente["codigo"].replace("EXP-", ""))
            mayor = max(mayor, numero)
        except (ValueError, KeyError):
            continue
    return f"EXP-{mayor + 1:04d}"


def registrar_expediente(expedientes):
    """Solicita los datos, valida los campos y registra un expediente."""
    print("\n--- REGISTRO DE EXPEDIENTE ---")
    solicitante = input("Nombre del solicitante: ").strip()
    if not validar_texto(solicitante, "solicitante"):
        return

    documento = input("DNI (8 dígitos): ").strip()
    if not (documento.isdigit() and len(documento) == 8):
        print("Error: el DNI debe contener exactamente 8 dígitos.")
        return

    asunto = input("Asunto del documento: ").strip()
    if not validar_texto(asunto, "asunto"):
        return

    tipo_documento = input("Tipo de documento: ").strip()
    if not validar_texto(tipo_documento, "tipo de documento"):
        return

    codigo = generar_codigo(expedientes)
    nuevo = {
        "codigo": codigo,
        "solicitante": solicitante,
        "dni": documento,
        "asunto": asunto,
        "tipo_documento": tipo_documento,
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    expedientes.append(nuevo)
    guardar_expedientes(expedientes)
    print(f"Expediente registrado correctamente. Código: {codigo}")


def buscar_expediente(expedientes):
    """Busca un expediente mediante su código único."""
    codigo = input("Ingrese el código del expediente: ").strip().upper()
    for expediente in expedientes:
        if expediente["codigo"].upper() == codigo:
            mostrar_expediente(expediente)
            return
    print("No se encontró un expediente con ese código.")


def mostrar_expediente(expediente):
    """Muestra los datos de un expediente."""
    print("\nCódigo:", expediente["codigo"])
    print("Solicitante:", expediente["solicitante"])
    print("DNI:", expediente["dni"])
    print("Asunto:", expediente["asunto"])
    print("Tipo de documento:", expediente["tipo_documento"])
    print("Fecha de registro:", expediente["fecha_registro"])


def ordenar_expedientes(expedientes):
    """Ordena los expedientes alfabéticamente por solicitante."""
    expedientes.sort(key=lambda item: item["solicitante"].casefold())
    guardar_expedientes(expedientes)
    print("\nExpedientes ordenados por nombre del solicitante.")
    listar_expedientes(expedientes)


def listar_expedientes(expedientes):
    """Muestra todos los expedientes registrados."""
    if not expedientes:
        print("No existen expedientes registrados.")
        return
    print("\n--- LISTADO DE EXPEDIENTES ---")
    for expediente in expedientes:
        print(f'{expediente["codigo"]} | {expediente["solicitante"]} | '
              f'{expediente["asunto"]} | {expediente["fecha_registro"]}')


def mostrar_menu():
    """Presenta las opciones principales del sistema."""
    print("\n===== MESA DE PARTES DIGITAL =====")
    print("1. Registrar expediente")
    print("2. Buscar expediente por código")
    print("3. Ordenar expedientes por solicitante")
    print("4. Listar expedientes")
    print("5. Salir")


def main():
    """Controla el flujo general del programa."""
    expedientes = cargar_expedientes()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_expediente(expedientes)
        elif opcion == "2":
            buscar_expediente(expedientes)
        elif opcion == "3":
            ordenar_expedientes(expedientes)
        elif opcion == "4":
            listar_expedientes(expedientes)
        elif opcion == "5":
            guardar_expedientes(expedientes)
            print("Datos guardados. Hasta luego.")
            break
        else:
            print("Opción no válida. Seleccione una opción del 1 al 5.")


if __name__ == "__main__":
    main()
