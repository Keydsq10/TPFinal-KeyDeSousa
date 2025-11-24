# storage.py
# Maneja guardado y lectura de archivos

import csv
import os

CLIENTES_CSV = "clientes.csv"
TURNOS_CSV = "turnos.csv"


def load_from_csv():
    db = {"clientes": {}, "turnos": {}}

    # Leer clientes
    if os.path.exists(CLIENTES_CSV):
        with open(CLIENTES_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                db["clientes"][row["id"]] = row

    # Leer turnos
    if os.path.exists(TURNOS_CSV):
        with open(TURNOS_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                db["turnos"][row["id"]] = row

    return db


def save_to_csv(db):
    # Guardar clientes
    with open(CLIENTES_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "nombre", "telefono", "email"])
        writer.writeheader()
        for c in db["clientes"].values():
            writer.writerow(c)

    # Guardar turnos
    with open(TURNOS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "cliente_id", "fecha", "hora", "servicio", "estilista", "estado"]
        )
        writer.writeheader()
        for t in db["turnos"].values():
            writer.writerow(t)
