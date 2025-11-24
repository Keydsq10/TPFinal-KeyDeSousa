# gestor.py
# Lógica del sistema de turnos

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

    # ------------------------------
    # Generadores de ID
    # ------------------------------
    def _nuevo_id_cliente(self):
        existentes = [int(cid[1:]) for cid in self.db["clientes"].keys()] or [0]
        nuevo_num = max(existentes) + 1
        return f"C{nuevo_num:03d}"

    def _nuevo_id_turno(self):
        existentes = [int(tid[1:]) for tid in self.db["turnos"].keys()] or [0]
        nuevo_num = max(existentes) + 1
        return f"T{nuevo_num:03d}"

    # ------------------------------
    # Clientes
    # ------------------------------
    def registrar_cliente(self, nombre, telefono, email=None):
        cid = self._nuevo_id_cliente()
        self.db["clientes"][cid] = {
            "id": cid,
            "nombre": nombre,
            "telefono": telefono,
            "email": email or ""
        }
        return cid

    def encontrar_cliente_id(self, query):
        if query in self.db["clientes"]:
            return query

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
            raise ValueError("Fecha inválida. Formato: YYYY-MM-DD")

    def _parse_hora(self, s):
        try:
            datetime.strptime(s, "%H:%M")
        except ValueError:
            raise ValueError("Hora inválida. Formato: HH:MM")

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

        self._parse_fecha(fecha)
        self._parse_hora(hora)

        if self._hay_solape(fecha, hora, estilista):
            raise ValueError("Ese horario ya está ocupado.")

        tid = self._nuevo_id_turno()
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
            cli = self.db["clientes"][t["cliente_id"]]["nombre"]
            texto = (
                f"[{t['id']}] {t['fecha']} {t['hora']} - "
                f"{cli} - {t['servicio']} - Estado: {t['estado']}"
            )
            if t["estilista"]:
                texto += f" - Estilista: {t['estilista']}"
            salida.append(texto)

        return salida

    def reprogramar_turno(self, turno_id, nueva_fecha, nueva_hora):
        if turno_id not in self.db["turnos"]:
            raise ValueError("Turno no existe.")

        self._parse_fecha(nueva_fecha)
        self._parse_hora(nueva_hora)

        t = self.db["turnos"][turno_id]

        if self._hay_solape(nueva_fecha, nueva_hora, t["estilista"]):
            raise ValueError("Nuevo horario ocupado.")

        t["fecha"] = nueva_fecha
        t["hora"] = nueva_hora
        t["estado"] = "activo"  # <-- ¡Aquí corregimos tu problema!

    def cancelar_turno(self, turno_id):
        if turno_id not in self.db["turnos"]:
            raise ValueError("Turno no existe.")
        self.db["turnos"][turno_id]["estado"] = "cancelado"
