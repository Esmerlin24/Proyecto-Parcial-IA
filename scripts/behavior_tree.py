# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

# scripts/behavior_tree.py

class Nodo:
    def __init__(self):
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def ejecutar(self):
        pass

class Selector(Nodo):
    def ejecutar(self):
        for hijo in self.hijos:
            if hijo.ejecutar():
                return True
        return False

class Secuencia(Nodo):
    def ejecutar(self):
        for hijo in self.hijos:
            if not hijo.ejecutar():
                return False
        return True

class Accion(Nodo):
    def __init__(self, accion):
        super().__init__()
        self.accion = accion

    def ejecutar(self):
        return self.accion()

class Invertir(Nodo):
    def __init__(self, accion):
        super().__init__()
        self.agregar_hijo(accion)

    def ejecutar(self):
        return not self.hijos[0].ejecutar()

class Timer(Nodo):
    def __init__(self, tiempo):
        super().__init__()
        self.tiempo = tiempo
        self.tiempo_restante = tiempo

    def ejecutar(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            return False
        else:
            self.tiempo_restante = self.tiempo
            self.hijos[0].ejecutar()
            return True