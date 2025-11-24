# Sistema de Turnos para Peluquería
Trabajo Práctico Final – Programación Orientada a Objetos (Python)

## Cómo ejecutar
1. Tener instalado Python 3.x  
2. Ir a la carpeta del proyecto  
3. Abrir la terminal dentro de esa carpeta  
4. Ejecutar:

```
python app.py
```

---

## Archivos del proyecto (versión simple)
- 'app.py' → Menú de consola e interacción del usuario  
- 'gestor.py' → Lógica principal del sistema (GestorTurnos)  
- 'models.py' → Clases base: Cliente y Turno  
- 'storage.py' → Guardado y carga usando archivos CSV y dict (JSON opcional)

---

## Funcionalidades principales
- Registrar cliente  
- Solicitar turno  
- Listar turnos (todos, por fecha, por cliente, activos/cancelados)  
- Reprogramar turno (cambiar fecha y hora)  
- Cancelar turno  
- Guardar datos a CSV  
- Cargar datos desde CSV o JSON  

---

## Validaciones implementadas
- Formato correcto de fecha (YYYY-MM-DD)  
- Formato correcto de hora (HH:MM)  
- Evitar solapamiento de turnos (mismo día y hora)  
- Búsqueda de clientes por ID o por nombre  
- Mantener estado de turno (activo o cancelado) sin borrar datos  

---

## Descripción técnica
El sistema usa un diccionario en memoria (`self.db`) con dos tablas:  
- 'clientes'  
- 'turnos'

La clase 'GestorTurnos' contiene toda la lógica: crear, modificar, listar y validar turnos.  
La persistencia se maneja en `storage.py`, que convierte entre diccionarios y archivos CSV/JSON.

---
