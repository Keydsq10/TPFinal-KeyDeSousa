# gestor.py
# Lógica del sistema de turnos

import uuid
from datetime import datetime
import storage


class GestorTurnos:
    def __init__(self):
        # "Base de datos" en memoria
        self.db = {"clientes": {}, "turnos": {}}

    # ------------------------------
    # Persistencia (solo CSV)
    # ------------------------------
    def cargar_csv(self):
        self.db = storage.load_from_csv()

    def guardar_csv(self):
        storage.save_to_csv(self.db)

    # ------------------------------
    # Clientes
    # ------------------------------
    def registrar_cliente(self, nombre, telefono, email=None):
        cid = str(uuid.uuid4())[:8]
        self.db["clientes"][cid] = {
            "id": cid,
            "nombre": nombre,
            "telefono": telefono,
            "email": email or ""
        }
        return cid

    def encontrar_cliente_id(self, query):
        # Buscar por ID exacto
        if query in self.db["clientes"]:
            return query

        # Buscar por nombre (contiene)
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
            datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Formato de fecha inválido (usar YYYY-MM-DD).")

    def _parse_hora(self, s):
        try:
            datetime.strptime(s, "%H:%M")
        except ValueError:
            raise ValueError("Formato de hora inválido (usar HH:MM).")

    def _hay_solape(self, fecha, hora, estilista):
        """Chequea si ya hay un turno activo en esa fecha y hora.
           Si hay estilista, bloquea por ese estilista; si no, bloquea el horario general.
        """
        for t in self.db["turnos"].values():
            if t["estado"] != "activo":
                continue

            if t["fecha"] == fecha and t["hora"] == hora:
                # Sin estilista: bloqueo total. Con estilista: bloqueo por estilista.
                if (estilista and t["estilista"] == estilista) or (not estilista):
                    return True

        return False

    # ------------------------------
    # Turnos
    # ------------------------------
    def solicitar_turno(self, cliente_id, fecha, hora, servicio, estilista=None):
        if cliente_id not in self.db["clientes"]:
            raise ValueError("Cliente inexistente.")

        # Validar formatos
        self._parse_fecha(fecha)
        self._parse_hora(hora)

        # Chequear solapamiento
        if self._hay_solape(fecha, hora, estilista):
            raise ValueError("Ese horario ya está ocupado.")

        tid = str(uuid.uuid4())[:8]
        self.db["turnos"][tid] = {
            "id": tid,
            "cliente_id": cliente_id,
            "fecha": fecha,
            "hora": hora,
            "servicio": servicio,
            "estilista": estilista or "",
            "estado": "activo"
        }
        return tid

    def listar_turnos(self, cliente_id=None, fecha=None, estado=None):
        """Devuelve una lista de líneas de texto para mostrar en consola."""
        lista = list(self.db["turnos"].values())

        if cliente_id:
            lista = [t for t in lista if t["cliente_id"] == cliente_id]
        if fecha:
            lista = [t for t in lista if t["fecha"] == fecha]
        if estado:
            lista = [t for t in lista if t["estado"] == estado]

        # Orden por fecha y hora
        lista.sort(key=lambda x: (x["fecha"], x["hora"]))

        salida = []
        for t in lista:
            cli = self.db["clientes"].get(t["cliente_id"], {})
            nombre = cli.get("nombre", "N/D")
            linea = f"[{t['id']}] {t['fecha']} {t['hora']} - {nombre} - {t['servicio']} - Estado: {t['estado']}"
            if t.get("estilista"):
                linea += f" - Estilista: {t['estilista']}"
            salida.append(linea)

        return salida

    def reprogramar_turno(self, turno_id, nueva_fecha, nueva_hora):
        if turno_id not in self.db["turnos"]:
            raise ValueError("Turno no existe.")

        # Validar formatos
        self._parse_fecha(nueva_fecha)
        self._parse_hora(nueva_hora)

        t = self.db["turnos"][turno_id]

        # Verificar que el nuevo horario no esté ocupado
        if self._hay_solape(nueva_fecha, nueva_hora, t.get("estilista") or None):
            raise ValueError("El nuevo horario está ocupado.")

        t["fecha"] = nueva_fecha
        t["hora"] = nueva_hora

    def cancelar_turno(self, turno_id):
        if turno_id not in self.db["turnos"]:
            raise ValueError("Turno no existe.")
        self.db["turnos"][turno_id]["estado"] = "cancelado"


    def cancelar_turno(self, turno_id):
        if turno_id not in self.db["turnos"]:
            raise ValueError("Turno no existe.")
        self.db["turnos"][turno_id]["estado"] = "cancelado"

