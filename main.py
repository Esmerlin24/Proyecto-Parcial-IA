# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

# Importe la libreria para el hacer el juego y para que cierre bien.
import pygame
import sys 
from scripts.game import Game

# Inicie pygame para que mi juego corra y cree la funcion principal para controlar el juego.

def main():
    pygame.init()

    # Para que el juego se vea en pantalla completa 
    Pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("La Ultima Salida")

    # Para controlar el tiempo 
    Reloj = pygame.time.Clock()
    Velocidad = 60  

    # Objeto Principal del juego
    JuegoPrincipal = Game(Pantalla)

    Jugando = True
    EnPantallaCompleta = True

    while Jugando:
        Eventos = pygame.event.get()

        for Evento in Eventos:
            if Evento.type == pygame.QUIT:
                Jugando = False

            if Evento.type == pygame.KEYDOWN:
                if Evento.key == pygame.K_ESCAPE:

                    if EnPantallaCompleta:
                        Pantalla = pygame.display.set_mode((1200, 700), pygame.RESIZABLE)
                        EnPantallaCompleta = False
                    else:
                        Pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        EnPantallaCompleta = True

        # Para conectar con game.py
        JuegoPrincipal.Handle_Events(Eventos)
        DeltaTiempo = Reloj.tick(Velocidad) / 1000
        JuegoPrincipal.Update(DeltaTiempo)
        JuegoPrincipal.Draw()
       
        pygame.display.flip()
        

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
   
