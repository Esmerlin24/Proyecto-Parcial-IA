# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

# Cree mi clase nodo para la base del arbol de comportamiento
class Nodo:  
    def __init__(self): # Para ejecutar el codigo cuando se cree un nodo 
        self.hijos = [] # para guardar los hijos de cada nodo

    def agregar_hijo(self, hijo): # Para guardar un hijo dentro del nodo
        self.hijos.append(hijo) # Para agregar el hijo a la lista de hijos del nodo 

    def ejecutar(self): # Para ejecutar el nodo
        pass

class Selector(Nodo): # Para elegir entre varias opciones, se ejecuta el primer hijoque retorne true 
    def ejecutar(self): # # Para ejecutar el selector 
        for hijo in self.hijos: # Para recorre cada hijo del selector
            if hijo.ejecutar(): # Para ejecutar el hijo y el selector retorna tru si el hijo retorna true 
                return True
        return False

class Secuencia(Nodo): # para ejecutar varias acciones en orden, se ejecuta el primer hijo que retorne false 
    def ejecutar(self):
        for hijo in self.hijos:
            if not hijo.ejecutar():
                return False
        return True

class Accion(Nodo): # para ejecutar una accion especifica. se ejecuta la funsion que se le pase al crear la accion
    def __init__(self, accion):
        super().__init__()
        self.accion = accion

    def ejecutar(self):
        return self.accion()

class Invertir(Nodo): # Para invertir el rectangulo de verdad de su hijo, si el hijo retorna true, el invertir retorna false y viceversa 
    def __init__(self, accion):
        super().__init__()
        self.agregar_hijo(accion)

    def ejecutar(self):
        return not self.hijos[0].ejecutar()

class Timer(Nodo):# para ejecutar una accion despues de un tiempo determinado,se ejecuta la accion cada vez que el tiempo se cumple, el tiempo se mide en frames 
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