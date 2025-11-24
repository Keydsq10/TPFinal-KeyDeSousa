# app.py
# Menú simple por consola

from gestor import GestorTurnos

gestor = GestorTurnos()

try:
    gestor.cargar_csv()
    print("Datos cargados desde CSV (si existen).")
except:
    pass


def menu():
    print("\n--- SISTEMA DE TURNOS ---")
    print("1) Registrar cliente")
    print("2) Solicitar turno")
    print("3) Listar turnos")
    print("4) Reprogramar turno")
    print("5) Cancelar turno")
    print("6) Guardar datos")
    print("7) Cargar datos JSON")
    print("8) Salir")


while True:
    menu()
    op = input("Opción: ").strip()

    if op == "1":
        n = input("Nombre: ")
        t = input("Telefono: ")
        e = input("Email: ")
        cid = gestor.registrar_cliente(n, t, e)
        print("Cliente registrado. ID:", cid)

    elif op == "2":
        q = input("ID cliente o nombre: ")
        cid = gestor.encontrar_cliente_id(q)
        if not cid:
            print("Cliente no encontrado.")
            continue

        f = input("Fecha (YYYY-MM-DD): ")
        h = input("Hora (HH:MM): ")
        s = input("Servicio: ")
        est = input("Estilista (opcional): ") or None

        try:
            tid = gestor.solicitar_turno(cid, f, h, s, est)
            print("Turno creado. ID:", tid)
        except Exception as e:
            print("Error:", e)

    elif op == "3":
        for linea in gestor.listar_turnos():
            print(linea)

    elif op == "4":
        tid = input("ID del turno: ")
        nf = input("Nueva fecha: ")
        nh = input("Nueva hora: ")
        try:
            gestor.reprogramar_turno(tid, nf, nh)
            print("Turno reprogramado.")
        except Exception as e:
            print("Error:", e)

    elif op == "5":
        tid = input("ID del turno: ")
        try:
            gestor.cancelar_turno(tid)
            print("Turno cancelado.")
        except Exception as e:
            print("Error:", e)

    elif op == "6":
        gestor.guardar_csv()
        print("Datos guardados en CSV.")

    elif op == "7":
        gestor.cargar_dict()
        print("Datos cargados desde JSON.")

    elif op == "8":
        break

    else:
        print("Opción inválida.")
