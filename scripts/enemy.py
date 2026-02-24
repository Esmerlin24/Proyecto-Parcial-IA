# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

import pygame  

#Cree mi clase enemigo    
class Enemigo:  

    def __init__(self, Mapa, Fila, Columna, DireccionInicial=1):
        # Mapa, es para hacer referencia al mapa 
        # Fila, para la posición vertical inicial 
        # Columna,para la posición horizontal inicial 
        # DireccionInicial, 1 derecha, -1 izquierda 

        self.Mapa = Mapa  # Guarda referencia al mapa 
        self.Fila = Fila  # Guarda fila actual
        self.Columna = Columna  # Guarda columna actual
        self.Direccion = DireccionInicial  # Guarda dirección actual
        self.Velocidad = 3  # Velocidad del enemigo 

        self.TamanoCelda = 40  # Tamaño de cada celda 

    def Actualizar(self, DeltaTiempo): #tiempo entre frames 
        

        NuevaColumna = self.Columna + self.Direccion * self.Velocidad * DeltaTiempo
        # self.Columna, posición actual
        # self.Direccion, 1 o -1
        # self.Velocidad, velocidad
        # * DeltaTiempo, movimiento suave
        # NuevaColumna, nueva posición calculada

        # Para verificar límites del mapa
        if 0 <= int(NuevaColumna) < len(self.Mapa.Cuadricula[0]):
            if self.Mapa.Cuadricula[self.Fila][int(NuevaColumna)] != 1:
                self.Columna = NuevaColumna
            else:
                self.Direccion *= -1  # Cambia dirección si hay pared
        else:
            self.Direccion *= -1  # Cambia dirección si sale del mapa

    def Dibujar(self, Pantalla): # Pantalla, superficie donde se dibuja
         

        Rectangulo = pygame.Rect(  #Para crear el rectangulo del enemigo
            int(self.Columna * self.TamanoCelda),
            int(self.Fila * self.TamanoCelda),
            self.TamanoCelda,
            self.TamanoCelda
        )

        pygame.draw.rect(Pantalla, (200, 0, 0), Rectangulo) # lo voy a dibujar rojo por el momento.
       

    def ColisionaConJugador(self, Jugador):

        return int(self.Fila) == int(Jugador.Fila) and int(self.Columna) == int(Jugador.Columna)
        # Devuelve True si están en la misma celda