# Sistema de Turnos para Peluquería  
Trabajo Práctico Final – Programación Orientada a Objetos (Python)

## Cómo ejecutar
1. Tener instalado **Python**
2. Ubicar la consola dentro de la carpeta del proyecto
3. Ejecutar:

```
python app.py
```

---

## Estructura del proyecto
Este proyecto implementa un sistema de turnos para una peluquería usando Programación Orientada a Objetos y archivos CSV como almacenamiento.

Archivos principales:

- **app.py** → Menú por consola e interacción del usuario  
- **gestor.py** → Lógica principal del sistema (GestorTurnos)  
- **models.py** → Clases base: `Cliente` y `Turno`  
- **storage.py** → Guardado y carga usando archivos CSV  

Archivos generados automáticamente:
- **clientes.csv**
- **turnos.csv**

---

## Funcionalidades principales
✔ Registrar clientes (IDs tipo 'C001', 'C002', 'C003', …)  
✔ Crear turnos (IDs tipo 'T001', 'T002', 'T003', …)  
✔ Validación de fecha y hora  
✔ Evitar solapamiento de horarios  
✔ Búsqueda de clientes por nombre o por ID  
✔ Listar turnos (todos, por cliente o por estado)  
✔ Reprogramar turnos (y vuelven a quedar como *activos*)  
✔ Cancelar turnos  
✔ Guardar datos automáticamente en CSV  

---

## Persistencia (CSV)
El sistema guarda los datos en:

- 'clientes.csv' → lista de clientes  
- 'turnos.csv' → lista de turnos  

El formato es simple y permite revisar los datos manualmente si es necesario.

---

## Descripción técnica
La clase **GestorTurnos** administra:

- Clientes ('self.db["clientes"]')
- Turnos ('self.db["turnos"]')

Se incluyen validadores para:

- Formato de fecha ('YYYY-MM-DD')
- Formato de hora ('HH:MM')
- Evitar turnos duplicados en el mismo horario
- Mantener estados de turno: **activo** o **cancelado**

Los IDs se generan automáticamente con formato legible:

- Clientes → 'C001' 
- Turnos → 'T001'  

---



