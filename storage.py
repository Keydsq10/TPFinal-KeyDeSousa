# storage.py
# Maneja guardado y lectura de archivos CSV y dict

import csv
import json
import os

CLIENTES_CSV = "clientes.csv"
TURNOS_CSV = "turnos.csv"
DB_JSON = "db.json"


def load_from_csv():
    db = {"clientes": {}, "turnos": {}}

    # Clientes
    if os.path.exists(CLIENTES_CSV):
        with open(CLIENTES_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cid = row["id"]
                db["clientes"][cid] = row

    # Turnos
    if os.path.exists(TURNOS_CSV):
        with open(TURNOS_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tid = row["id"]
                db["turnos"][tid] = row

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


def save_dict_json(db):
    with open(DB_JSON, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)


def load_dict_json():
    with open(DB_JSON, encoding="utf-8") as f:
        return json.load(f)
