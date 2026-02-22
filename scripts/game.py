# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

import pygame 

# Para llamar la clase Mapa, desde el archivo map.py
from scripts.map import Mapa  

# Voy a crear mi clase llamada Game 

class Game:
    # cree mi contructor para ejecutar Game(Pantalla)

    def __init__(self, Pantalla):
        self.Pantalla = Pantalla #guardo pantalla
        self.Estado = "MENU" # utilice esta variable para controlar en que parte del juego estoy.
        self.Mapa = Mapa() # cree la el mapa para que sea un objeto real.

# la funsion para los eventos del teclado y mouse
    def Handle_Events(self, Eventos):
        for Evento in Eventos: # Para recorrer cada evento
            if Evento.type == pygame.KEYDOWN: # para detectar si se presiono una tecla.
                if Evento.key == pygame.K_RETURN: # si fue la tecla enter.
                    if self.Estado == "MENU":
                        self.Estado = "JUGANDO"
# El metodo para actualizar la logica del juego
    def Update(self):
        if self.Estado == "JUGANDO": # Para actualizar las cosas solo si se esta jugando.
            pass
# Para dibujar todo en mi pantalla 
    def Draw(self):
        if self.Estado == "MENU": # Si estamos en menu
            self.Pantalla.fill((124, 252, 0)) # Color de la pantalla en menu
        elif self.Estado == "JUGANDO": # si estamos jugando
            self.Pantalla.fill((0, 0, 0)) # La pantalla es negra
            self.Mapa.Dibujar(self.Pantalla) # Para dibujar mapa en pantalla S