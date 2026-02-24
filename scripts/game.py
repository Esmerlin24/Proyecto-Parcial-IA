# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

import pygame 

# Para llamar la clase Mapa, desde el archivo map.py
from scripts.map import Mapa  
# Importe la clase Player desde player.py dentro de scripts.
# para poder crear el jugador, moverlo y dibujarlo en pantalla.
from scripts.player import Player 
# Importe la clase Timer desde timer.py dentro de scripts.
# para crear el temporizador del juego y controlar la cuenta regresiva.
from scripts.timer import Timer

# Voy a crear mi clase llamada Game 
class Game:
    # cree mi contructor para ejecutar Game(Pantalla)

    def __init__(self, Pantalla):
        self.Pantalla = Pantalla #guardo pantalla
        self.Estado = "MENU" # utilice esta variable para controlar en que parte del juego estoy.
        self.Mapa = Mapa() # cree la el mapa para que sea un objeto real.
        self.Jugador = Player(self.Mapa)
        self.Temporizador = Timer(60)  # 60 segundos iniciales 

# la funsion para los eventos del teclado y mouse
    def Handle_Events(self, Eventos):
        for Evento in Eventos: # Para recorrer cada evento
            if Evento.type == pygame.KEYDOWN: # para detectar si se presiono una tecla.
                if Evento.key == pygame.K_RETURN: # si fue la tecla enter.
                    if self.Estado == "MENU":
                        self.Estado = "JUGANDO"
# El metodo para actualizar la logica del juego
    def Update(self, DeltaTiempo):

        if self.Estado == "JUGANDO": # Para actualizar las cosas solo si se esta jugando.
            self.Temporizador.Actualizar(DeltaTiempo)

            if self.Temporizador.TiempoTerminado():
                self.Estado = "GAME_OVER"        
            Teclas = pygame.key.get_pressed()
            self.Jugador.Mover(Teclas, DeltaTiempo)

# Para dibujar todo en mi pantalla 
    def Draw(self):

        if self.Estado == "MENU": # Si estamos en menu
            self.Pantalla.fill((0, 120, 252)) # Color de la pantalla en menu

        elif self.Estado == "JUGANDO": # si estamos jugando
            self.Pantalla.fill((0, 0, 0)) # La pantalla es negra
            self.Mapa.Dibujar(self.Pantalla) # Para dibujar mapa en pantalla S
            self.Jugador.Dibujar(self.Pantalla) # Para dibujar el jugador en pantalla 
            self.Temporizador.Dibujar(self.Pantalla) # Para dibujar el tiempo en pantalla

        elif self.Estado == "GAME_OVER":
             self.Pantalla.fill((120, 0, 0)) # Color de la pantalla en Game Over 

             Fuente = pygame.font.SysFont("Arial", 60) # Para crear la fuente de texto de Game Over 
             Texto = Fuente.render("GAME OVER", True, (255, 255, 255))  
             self.Pantalla.blit(Texto, (400, 300))   