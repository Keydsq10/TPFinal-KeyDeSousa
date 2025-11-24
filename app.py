# app.py
# Menú de consola del sistema de turnos

from gestor import GestorTurnos

gestor = GestorTurnos()

# Intentar cargar datos desde CSV al iniciar
try:
    gestor.cargar_csv()
    print("Datos cargados desde CSV (si existían).")
except Exception as e:
    print("No se pudieron cargar datos desde CSV:", e)


def menu():
    print("\n--- SISTEMA DE TURNOS PARA PELUQUERÍA ---")
    print("1) Registrar cliente")
    print("2) Solicitar turno")
    print("3) Listar turnos")
    print("4) Reprogramar turno")
    print("5) Cancelar turno")
    print("6) Guardar datos en CSV")
    print("7) Salir")


while True:
    menu()
    op = input("Opción: ").strip()

    if op == "1":
        nombre = input("Nombre: ").strip()
        telefono = input("Teléfono: ").strip()
        email = input("Email (opcional): ").strip()

        if not nombre or not telefono:
            print("Nombre y teléfono son obligatorios.")
            continue

        cid = gestor.registrar_cliente(nombre, telefono, email)
        print(f"Cliente registrado con ID: {cid}")

    elif op == "2":
        q = input("ID de cliente o nombre: ").strip()
        cid = gestor.encontrar_cliente_id(q)
        if not cid:
            print("Cliente no encontrado.")
            continue

        fecha = input("Fecha (YYYY-MM-DD): ").strip()
        hora = input("Hora (HH:MM): ").strip()
        servicio = input("Servicio: ").strip()
        estilista = input("Estilista (opcional): ").strip() or None

        try:
            tid = gestor.solicitar_turno(cid, fecha, hora, servicio, estilista)
            print(f"Turno creado con ID: {tid}")
        except Exception as e:
            print("Error al crear turno:", e)

    elif op == "3":
        print("\n--- LISTA DE TURNOS ---")
        turnos = gestor.listar_turnos()
        if not turnos:
            print("No hay turnos cargados.")
        else:
            for linea in turnos:
                print(linea)

    elif op == "4":
        tid = input("ID del turno: ").strip()
        nueva_fecha = input("Nueva fecha (YYYY-MM-DD): ").strip()
        nueva_hora = input("Nueva hora (HH:MM): ").strip()

        try:
            gestor.reprogramar_turno(tid, nueva_fecha, nueva_hora)
            print("Turno reprogramado.")
        except Exception as e:
            print("Error al reprogramar turno:", e)

    elif op == "5":
        tid = input("ID del turno: ").strip()
        try:
            gestor.cancelar_turno(tid)
            print("Turno cancelado.")
        except Exception as e:
            print("Error al cancelar turno:", e)

    elif op == "6":
        try:
            gestor.guardar_csv()
            print("Datos guardados en CSV.")
        except Exception as e:
            print("Error al guardar CSV:", e)

    elif op == "7":
        print("Saliendo...")
        break

    else:
        print("Opción inválida.")
