# storage.py
# Maneja guardado y lectura de archivos CSV.

import csv
import os

CLIENTES_CSV = "clientes.csv"
TURNOS_CSV = "turnos.csv"


def load_from_csv():
    """Carga clientes y turnos desde CSV a un diccionario db."""
    db = {"clientes": {}, "turnos": {}}

    # --- Clientes ---
    if os.path.exists(CLIENTES_CSV):
        with open(CLIENTES_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cid = row["id"]
                db["clientes"][cid] = {
                    "id": cid,
                    "nombre": row["nombre"],
                    "telefono": row["telefono"],
                    "email": row.get("email") or ""
                }

    # --- Turnos ---
    if os.path.exists(TURNOS_CSV):
        with open(TURNOS_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tid = row["id"]
                db["turnos"][tid] = {
                    "id": tid,
                    "cliente_id": row["cliente_id"],
                    "fecha": row["fecha"],
                    "hora": row["hora"],
                    "servicio": row["servicio"],
                    "estilista": row.get("estilista") or "",
                    "estado": row.get("estado") or "activo"
                }

    return db


def save_to_csv(db):
    """Guarda el contenido de db en clientes.csv y turnos.csv."""

    # --- Clientes ---
    with open(CLIENTES_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "nombre", "telefono", "email"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in db["clientes"].values():
            writer.writerow({
                "id": c["id"],
                "nombre": c["nombre"],
                "telefono": c["telefono"],
                "email": c.get("email", "")
            })

    # --- Turnos ---
    with open(TURNOS_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "cliente_id", "fecha", "hora", "servicio", "estilista", "estado"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in db["turnos"].values():
            writer.writerow({
                "id": t["id"],
                "cliente_id": t["cliente_id"],
                "fecha": t["fecha"],
                "hora": t["hora"],
                "servicio": t["servicio"],
                "estilista": t.get("estilista", ""),
                "estado": t.get("estado", "activo")
            })
