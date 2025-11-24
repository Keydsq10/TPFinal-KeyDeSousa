# models.py
# Clases simples para representar datos

class Cliente:
    def __init__(self, id, nombre, telefono, email=None):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email


class Turno:
    def __init__(self, id, cliente_id, fecha, hora, servicio, estilista=None, estado="activo"):
        self.id = id
        self.cliente_id = cliente_id
        self.fecha = fecha
        self.hora = hora
        self.servicio = servicio
        self.estilista = estilista
        self.estado = estado
