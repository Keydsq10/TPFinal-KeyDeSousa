# gestor.py
# Lógica del sistema de turnos, IDs tipo C001 y T001

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
        """Genera id tipo C001, C002..."""
        existentes = [int(cid[1:]) for cid in self.db["clientes"].keys()] or [0]
        nuevo_num = max(existentes) + 1
        return f"C{nuevo_num:03d}"

    def _nuevo_id_turno(self):
        """Genera id tipo T001, T002..."""
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
            raise ValueError("Fecha inválida. F
