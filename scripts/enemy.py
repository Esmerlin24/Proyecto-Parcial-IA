# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

import pygame  
from .behavior_tree import Selector, Secuencia, Accion # Importamos el algoritmo del maestro

class Enemigo:  
    def __init__(self, Mapa, Fila, Columna, DireccionInicial=1):
        # Mapa, es para hacer referencia al mapa 
        # Fila, para la posición vertical inicial 
        # Columna,para la posición horizontal inicial 
        # DireccionInicial, 1 derecha, -1 izquierda 

        self.Mapa = Mapa  
        self.Fila = Fila  
        self.Columna = Columna  
        self.Direccion = DireccionInicial  
        self.Velocidad = 3  

        # Variables temporales para el Árbol
        self.DeltaTiempo_actual = 0
        self.jugador_actual = None
        self.estado_terminal = "" # Para no saturar la consola de prints

        # ==========================================
        # CONSTRUCCIÓN DEL ÁRBOL DE COMPORTAMIENTO
        # ==========================================
        self.comportamiento = Selector()
        
        secuencia_persecucion = Secuencia()
        accion_patrullar = Accion(self.patrullar)

        # 1. Prioridad alta: Intentar perseguir
        self.comportamiento.agregar_hijo(secuencia_persecucion)
        # 2. Prioridad baja: Si falla la persecución, patrullar
        self.comportamiento.agregar_hijo(accion_patrullar)

        # Dentro de la persecución: Condición -> Acción
        secuencia_persecucion.agregar_hijo(Accion(self.ve_al_jugador))
        secuencia_persecucion.agregar_hijo(Accion(self.perseguir))
        # ==========================================

    def Actualizar(self, DeltaTiempo, Jugador): 
        # Guardamos estas variables para que las Acciones puedan usarlas
        self.DeltaTiempo_actual = DeltaTiempo
        self.jugador_actual = Jugador
        
        # Ejecutamos la Inteligencia Artificial del maestro
        self.comportamiento.ejecutar()

    # --- CONDICIONES Y ACCIONES DEL ÁRBOL ---

    def ve_al_jugador(self):
        # Calculamos la distancia (vision de 4 celdas)
        distancia = abs(self.Fila - self.jugador_actual.Fila) + abs(self.Columna - self.jugador_actual.Columna)
        if distancia <= 4:
            if self.estado_terminal != "PERSIGUIENDO":
                print("🎯 ¡Enemigo: Ve al jugador! -> Iniciando persecución.")
                self.estado_terminal = "PERSIGUIENDO"
            return True # Retorna True para que la Secuencia pase a 'perseguir'
        return False # Retorna False, rompe la secuencia, el Selector pasa a 'patrullar'

    def perseguir(self):
        # Moverse en dirección al jugador
        dir_x = 1 if self.jugador_actual.Columna > self.Columna else (-1 if self.jugador_actual.Columna < self.Columna else 0)
        dir_y = 1 if self.jugador_actual.Fila > self.Fila else (-1 if self.jugador_actual.Fila < self.Fila else 0)

        NuevaColumna = self.Columna + dir_x * self.Velocidad * self.DeltaTiempo_actual
        NuevaFila = self.Fila + dir_y * self.Velocidad * self.DeltaTiempo_actual

        # Colisión básica para la persecución
        if self.Mapa.Cuadricula[int(NuevaFila)][int(NuevaColumna)] != 1:
            self.Columna = NuevaColumna
            self.Fila = NuevaFila
            
        return True

    def patrullar(self):
        if self.estado_terminal != "PATRULLANDO":
            print("🚶‍♂️ Enemigo: Jugador perdido -> Volviendo a patrullar.")
            self.estado_terminal = "PATRULLANDO"

        # El movimiento original que ya tenías
        NuevaColumna = self.Columna + self.Direccion * self.Velocidad * self.DeltaTiempo_actual
        if 0 <= int(NuevaColumna) < len(self.Mapa.Cuadricula[0]):
            if self.Mapa.Cuadricula[int(self.Fila)][int(NuevaColumna + (0.1 * self.Direccion))] != 1:
                self.Columna = NuevaColumna
            else:
                self.Direccion *= -1
        else:
            self.Direccion *= -1
            
        return True

    def Dibujar(self, Pantalla): # Pantalla, superficie donde se dibuja
        AnchoPantalla = Pantalla.get_width()
        AltoPantalla = Pantalla.get_height()
        Columnas = len(self.Mapa.Cuadricula[0])
        Filas = len(self.Mapa.Cuadricula)
        
        TX = AnchoPantalla // Columnas
        TY = AltoPantalla // Filas

        Rectangulo = pygame.Rect(int(self.Columna * TX), int(self.Fila * TY), TX, TY)
        pygame.draw.rect(Pantalla, (200, 0, 0), Rectangulo) # lo voy a dibujar rojo por el momento.

    def ColisionaConJugador(self, Jugador):
        return abs(self.Fila - Jugador.Fila) < 0.5 and abs(self.Columna - Jugador.Columna) < 0.5
        # Devuelve True si están en la misma celda