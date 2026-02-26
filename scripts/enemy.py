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

        self.Mapa = Mapa  # Para guardar el mapa dentro del enemigo y poder revisar colisiones
        self.Fila = Fila  # para guardar la posicion vertical del enemigo 
        self.Columna = Columna  # para guardar la posicion horizontal del enemigo
        self.Direccion = DireccionInicial  # Para gardar la direccion del enemigo 
        self.Velocidad = 3  # Para guardar la velocidad del enemigo 

        # Variables temporales para el Árbol
        self.DeltaTiempo_actual = 0 # Para guardar el delta tiempo actual y usarlo en las acciones 
        self.jugador_actual = None # Para guardar la referencia al jugador y usarlo en las acciones 
        self.estado_terminal = "" # Para no saturar la consola de prints

        
        # CONSTRUCCIÓN DEL ÁRBOL DE COMPORTAMIENTO
       
        self.comportamiento = Selector() # El selector va a elegir entre perseguir o patrullar dependiendo si ve o no el jugador 
        
        secuencia_persecucion = Secuencia() # Para la persecusion el enemigo tiene que ver al jugador y luego perseguirlo
        accion_patrullar = Accion(self.patrullar) # Si no ve el jugador entonces patrulla 

        # 1. Prioridad alta: Intentar perseguir
        self.comportamiento.agregar_hijo(secuencia_persecucion) 
        # 2. Prioridad baja: Si falla la persecución, patrullar
        self.comportamiento.agregar_hijo(accion_patrullar)

        # Dentro de la persecución: Condición -> Acción
        secuencia_persecucion.agregar_hijo(Accion(self.ve_al_jugador))
        secuencia_persecucion.agregar_hijo(Accion(self.perseguir))
     

    def Actualizar(self, DeltaTiempo, Jugador): 
        # Guardamos estas variables para que las Acciones puedan usarlas
        self.DeltaTiempo_actual = DeltaTiempo
        self.jugador_actual = Jugador
        
        # Ejecutamos la Inteligencia Artificial
        self.comportamiento.ejecutar()

    #  CONDICIONES Y ACCIONES DEL ÁRBOL 

    def ve_al_jugador(self):
        # Calculamos la distancia vision de 5 celdas para el nuevo mapa 
        distancia = abs(self.Fila - self.jugador_actual.Fila) + abs(self.Columna - self.jugador_actual.Columna)
        if distancia <= 5:
            if self.estado_terminal != "PERSIGUIENDO":
                print("🎯 ¡Enemigo: Ve al jugador! -> Iniciando persecución.")
                self.estado_terminal = "PERSIGUIENDO"
            return True # Retorna True para que la Secuencia pase a 'perseguir'
        return False # Retorna False, rompe la secuencia, el Selector pasa a 'patrullar'

    def perseguir(self):
        # Moverse en dirección al jugador de forma rápida
        self.Velocidad = 3.5 # Aumenta velocidad al detectar
        return self.mover_logica(self.jugador_actual.Fila, self.jugador_actual.Columna)

    def patrullar(self):
        if self.estado_terminal != "PATRULLANDO":
            print("🚶‍♂️ Enemigo: Jugador perdido -> Merodeando el área.")
            self.estado_terminal = "PATRULLANDO"

        # PATRULLA INTELIGENTE: En lugar de una línea fija, 
        # se mueve lentamente hacia la zona donde está el jugador.
        self.Velocidad = 1.8 # Velocidad de acecho lenta
        return self.mover_logica(self.jugador_actual.Fila, self.jugador_actual.Columna)

    def mover_logica(self, destino_fila, destino_col):
        # Lógica de dirección hacia un punto objetivo
        dir_x = 1 if destino_col > self.Columna else (-1 if destino_col < self.Columna else 0)
        dir_y = 1 if destino_fila > self.Fila else (-1 if destino_fila < self.Fila else 0)

        NuevaColumna = self.Columna + dir_x * self.Velocidad * self.DeltaTiempo_actual
        NuevaFila = self.Fila + dir_y * self.Velocidad * self.DeltaTiempo_actual

        # Colisión básica con la cuadrícula del mapa
        if self.Mapa.Cuadricula[int(self.Fila)][int(NuevaColumna)] != 1:
            self.Columna = NuevaColumna
        if self.Mapa.Cuadricula[int(NuevaFila)][int(self.Columna)] != 1:
            self.Fila = NuevaFila
            
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
        # Ajuste el margen de colisión a 0.6 para el nuevo tamaño de celdas
        return abs(self.Fila - Jugador.Fila) < 0.6 and abs(self.Columna - Jugador.Columna) < 0.6
        