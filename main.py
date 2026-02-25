# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

# Importe la libreria para el hacer el juego y para que cierre bien.
import pygame
import sys 
from scripts.game import Game

# Inicie pygame para que mi juego corra y cree la funcion principal para controlar el juego.

def main():
    pygame.init()
    

    # Obtener resolución real de la pantalla
    infoPantalla = pygame.display.Info()
    anchoPantalla = infoPantalla.current_w
    altoPantalla = infoPantalla.current_h

    # Para que el juego se vea en pantalla completa 
    Pantalla = pygame.display.set_mode((anchoPantalla, altoPantalla), pygame.FULLSCREEN)
    pygame.display.set_caption("La Ultima Salida")

    # Para controlar el tiempo 
    Reloj = pygame.time.Clock()
    Velocidad = 60  

    # Objeto Principal del juego
    JuegoPrincipal = Game(Pantalla)

    Jugando = True
    EnPantallaCompleta = True

    while Jugando: # Bucle principal del juego, este se ejecuta mientras jugando sea verdadero
        Eventos = pygame.event.get() # para obtener los eventos del teclado y mouse 

        for Evento in Eventos: # Para recorrer cada evento
            if Evento.type == pygame.QUIT: # si se cierra la ventana, termina el juego
                Jugando = False

            if Evento.type == pygame.KEYDOWN: # para detectar si se presiona una tecla 
                if Evento.key == pygame.K_ESCAPE: # si se presiona escape cierra el juego 
                    
                    if EnPantallaCompleta: # Si esta en pantalla completa, cambia a modo ventana. 
                        Pantalla = pygame.display.set_mode((1200, 700), pygame.RESIZABLE) # 
                        EnPantallaCompleta = False
                    else:
                        Pantalla = pygame.display.set_mode((anchoPantalla, altoPantalla), pygame.FULLSCREEN)
                        EnPantallaCompleta = True

                    # Para actualizar siempre la pantalla dentro del juego
                    JuegoPrincipal.Pantalla = Pantalla

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
   