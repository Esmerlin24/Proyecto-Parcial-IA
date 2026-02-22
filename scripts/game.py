# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

import pygame 

# Voy a crear mi clase llamada Juego 

import pygame

class Game:
    def __init__(self, Pantalla):
        self.Pantalla = Pantalla
        self.Estado = "MENU"

    def Handle_Events(self, Eventos):
        for Evento in Eventos:
            if Evento.type == pygame.KEYDOWN:
                if Evento.key == pygame.K_RETURN:
                    if self.Estado == "MENU":
                        self.Estado = "JUGANDO"

    def Update(self):
        if self.Estado == "JUGANDO":
            pass

    def Draw(self):
        if self.Estado == "MENU":
            self.Pantalla.fill((30, 30, 60))
        elif self.Estado == "JUGANDO":
            self.Pantalla.fill((0, 0, 0))