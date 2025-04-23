class NodoVuelo:
    def __init__(self, vuelo):
        self.vuelo = vuelo  # Almacena el dato del vuelo en el nodo
        self.anterior = None  # Puntero al nodo anterior en la lista
        self.siguiente = None  # Puntero al nodo siguiente en la lista

class ListaDoblementeEnlazada:
    def __init__(self):
        self.primero = None  # Puntero al primer nodo de la lista
        self.ultimo = None  # Puntero al último nodo de la lista
        self._longitud = 0  # Contador del número de nodos en la lista

    def insertar_al_frente(self, vuelo):
        nuevo_nodo = NodoVuelo(vuelo)  # Crea un nuevo nodo con el vuelo dado
        if not self.primero:  # Si la lista está vacía
            self.primero = self.ultimo = nuevo_nodo  # El nuevo nodo es el primero y el último
        else:
            nuevo_nodo.siguiente = self.primero  # El siguiente del nuevo nodo es el actual primero
            self.primero.anterior = nuevo_nodo  # El anterior del actual primero es el nuevo nodo
            self.primero = nuevo_nodo  # Actualiza el puntero primero al nuevo nodo
        self._longitud += 1  # Incrementa la longitud de la lista

    def insertar_al_final(self, vuelo):
        nuevo_nodo = NodoVuelo(vuelo)  # Crea un nuevo nodo con el vuelo dado
        if not self.ultimo:  # Si la lista está vacía
            self.primero = self.ultimo = nuevo_nodo  # El nuevo nodo es el primero y el último
        else:
            nuevo_nodo.anterior = self.ultimo  # El anterior del nuevo nodo es el actual último
            self.ultimo.siguiente = nuevo_nodo  # El siguiente del actual último es el nuevo nodo
            self.ultimo = nuevo_nodo  # Actualiza el puntero último al nuevo nodo
        self._longitud += 1  # Incrementa la longitud de la lista

    def obtener_primero(self):
        return self.primero.vuelo if self.primero else None  # Devuelve el vuelo del primer nodo o None si está vacío

    def obtener_ultimo(self):
        return self.ultimo.vuelo if self.ultimo else None  # Devuelve el vuelo del último nodo o None si está vacío

    def longitud(self):
        return self._longitud  # Devuelve la longitud actual de la lista

    def insertar_en_posicion(self, vuelo, posicion):
        if posicion <= 0:
            self.insertar_al_frente(vuelo)  # Inserta al frente si la posición es menor o igual a 0
        elif posicion >= self._longitud:
            self.insertar_al_final(vuelo)  # Inserta al final si la posición es mayor o igual a la longitud
        else:
            nuevo_nodo = NodoVuelo(vuelo)  # Crea un nuevo nodo con el vuelo dado
            actual = self.primero
            for _ in range(posicion):  # Recorre la lista hasta la posición deseada
                actual = actual.siguiente
            anterior = actual.anterior  # Guarda el nodo anterior al actual
            anterior.siguiente = nuevo_nodo  # El siguiente del anterior es el nuevo nodo
            nuevo_nodo.anterior = anterior  # El anterior del nuevo nodo es el anterior
            nuevo_nodo.siguiente = actual  # El siguiente del nuevo nodo es el actual
            actual.anterior = nuevo_nodo  # El anterior del actual es el nuevo nodo
            self._longitud += 1  # Incrementa la longitud de la lista

    def extraer_de_posicion(self, posicion):
        if posicion < 0 or posicion >= self._longitud:
            return None  # Devuelve None si la posición es inválida
        actual = self.primero
        for _ in range(posicion):  # Recorre la lista hasta la posición deseada
            actual = actual.siguiente
        if actual.anterior:
            actual.anterior.siguiente = actual.siguiente  # Ajusta el siguiente del nodo anterior
        else:
            self.primero = actual.siguiente  # Si no hay anterior, actualiza el primero
        if actual.siguiente:
            actual.siguiente.anterior = actual.anterior  # Ajusta el anterior del nodo siguiente
        else:
            self.ultimo = actual.anterior  # Si no hay siguiente, actualiza el último
        self._longitud -= 1  # Decrementa la longitud de la lista
        return actual.vuelo  # Devuelve el vuelo del nodo extraído
