# Pilas para manejar las acciones de deshacer y rehacer
undo_stack = []
redo_stack = []

def registrar_accion(accion: str, vuelo):
    """Registra una acción para poder hacer undo más tarde"""
    # Agrega la acción y el vuelo a la pila de deshacer
    undo_stack.append((accion, vuelo))
    # Limpia la pila de rehacer porque una nueva acción invalida la posibilidad de rehacer previas acciones
    redo_stack.clear()
    print(f"[REGISTRADO] Acción: {accion} sobre vuelo {vuelo.codigo}")

def undo(lista_vuelos):
    """Deshace la última acción registrada"""
    if not undo_stack:
        return "Nada para deshacer."
    
    # Saca la última acción de la pila de deshacer
    accion, vuelo = undo_stack.pop()
    # Agrega la acción a la pila de rehacer
    redo_stack.append((accion, vuelo))

    if accion == "add":
        # Deshacer un agregado implica quitar el vuelo de la lista
        for i in range(lista_vuelos.longitud()):
            if lista_vuelos.extraer_de_posicion(i).id == vuelo.id:
                break
        return f"Deshecho: agregado vuelo {vuelo.codigo}"
    
    elif accion == "remove":
        # Deshacer una eliminación implica volver a insertar el vuelo
        if vuelo.emergencia:
            lista_vuelos.insertar_al_frente(vuelo)
        else:
            lista_vuelos.insertar_al_final(vuelo)
        return f"Deshecho: eliminación de vuelo {vuelo.codigo}"

def redo(lista_vuelos):
    """Rehace la última acción deshecha"""
    if not redo_stack:
        return "Nada para rehacer."
    
    # Saca la última acción de la pila de rehacer
    accion, vuelo = redo_stack.pop()
    # Vuelve a agregar la acción a la pila de deshacer
    undo_stack.append((accion, vuelo))

    if accion == "add":
        # Rehacer un agregado implica volver a insertar el vuelo
        if vuelo.emergencia:
            lista_vuelos.insertar_al_frente(vuelo)
        else:
            lista_vuelos.insertar_al_final(vuelo)
        return f"Rehecho: agregado vuelo {vuelo.codigo}"

    elif accion == "remove":
        # Rehacer una eliminación implica quitar el vuelo de la lista
        for i in range(lista_vuelos.longitud()):
            if lista_vuelos.extraer_de_posicion(i).id == vuelo.id:
                break
        return f"Rehecho: eliminación vuelo {vuelo.codigo}"
