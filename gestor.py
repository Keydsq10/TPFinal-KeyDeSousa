# gestor.py
# Lógica del sistema de turnos

import uuid
from datetime import datetime
import storage


class GestorTurnos:
    def __init__(self):
        self.db = {"clientes": {}, "turnos": {}}

    # ------------------------------
    # Persistencia
    # ------------------------------
    def cargar_csv(self):
        self.db = storage.load_from_csv()

    def guardar_csv(self):
        storage.save_to_csv(self.db)

    def guardar_dict(self):
        storage.save_dict_json(self.db)

    def cargar_dict(self):
        self.db = storage.load_dict_json()

    # ------------------------------
    # Clientes
    # ------------------------------
    def registrar_cliente(self, nombre, telefono, email=None):
        cid = str(uuid.uuid4())[:8]
        self.db["clientes"][cid] = {
            "id": cid,
            "nombre": nombre,
            "telefono": telefono,
            "email": email
        }
        return cid

    def encontrar_cliente_id(self, query):
        # Buscar por ID
        if query in self.db["clientes"]:
            return query

        # Buscar por nombre
        q = query.lower()
        for cid, c in self.db["clientes"].items():
            if q in c["nombre"].lower():
                return cid
        return None

    # ------------------------------
    # Validadores
    # ------------------------------
    def _parse_fecha(self, s):
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except:
            raise ValueError("Formato de fecha inválido (YYYY-MM-DD).")

    def _parse_hora(self, s):
        try:
            return datetime.strptime(s, "%H:%M").time()
        except:
            raise ValueError("Formato de hora inválido (HH:MM).")

    def _hay_solape(self, fecha, hora, estilista):
        for t in self.db["turnos"].values():
            if t["estado"] != "activo":
                continue

            if t["fecha"] == fecha and t["hora"] == hora:
                if (estilista and t["estilista"] == estilista) or (not estilista):
                    return True
        return False

    # ------------------------------
    # Turnos
    # ------------------------------
    def solicitar_turno(self, cliente_id, fecha, hora, servicio, estilista=None):
        if cliente_id not in self.db["clientes"]:
            raise ValueError("Cliente inexistente.")

        f = fecha
        h = hora

        if self._hay_solape(f, h, estilista):
            raise ValueError("Ese horario ya está ocupado.")

        tid = str(uuid.uuid4())[:8]
        self.db["turnos"][tid] = {
            "id": tid,
            "cliente_id": cliente_id,
            "fecha": f,
            "hora": h,
            "servicio": servicio,
            "estilista": estilista,
            "estado": "activo"
        }
        return tid

    def listar_turnos(self, cliente_id=None, fecha=None, estado=None):
        lista = list(self.db["turnos"].values())

        if cliente_id:
            lista = [t for t in lista if t["cliente_id"] == cliente_id]
        if fecha:
            lista = [t for t in lista if t["fecha"] == fecha]
        if estado:
            lista = [t for t in lista if t["estado"] == estado]

        lista.sort(key=lambda x: (x["fecha"], x["hora"]))

        salida = []
        for t in lista:
            c = self.db["clientes"][t["cliente_id"]]["nombre"]
            salida.append(
                f"[{t['id']}] {t['fecha']} {t['hora']} - {c} - {t['servicio']} ({t['estado']})"
            )
        return salida

    def reprogramar_turno(self, turno_id, nueva_fecha, nueva_hora):
        if turno_id not in self.db["turnos"]:
            raise ValueError("Turno no existe.")

        t = self.db["turnos"][turno_id]

        if self._hay_solape(nueva_fecha, nueva_hora, t["estilista"]):
            raise ValueError("Nuevo horario ocupado.")

        t["fecha"] = nueva_fecha
        t["hora"] = nueva_hora

    def cancelar_turno(self, turno_id):
        if turno_id not in self.db["turnos"]:
            raise ValueError("Turno no existe.")
        self.db["turnos"][turno_id]["estado"] = "cancelado"
