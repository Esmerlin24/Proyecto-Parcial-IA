# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

# Importe la libreria para hacer el juego y para que cierre bien.
import pygame
import sys 
from scripts.game import Game

# Inicie pygame para que mi juego corra y cree la funcion principal para controlar el juego.

def main():
    pygame.init()
    

    # Obtener resolución real de la pantalla

    infoPantalla = pygame.display.Info() # Para obtener la informacion de la pantalla actual    anchoPantalla = infoPantalla.current_w
    altoPantalla = infoPantalla.current_h # Para obtener la altura de la pantalla actual 
    anchoPantalla = infoPantalla.current_w # Para obtener el ancho de la pantalla actual

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
        
        # Limitamos los FPS a 60 y calculamos el DeltaTiempo de forma precisa
        DeltaTiempo = Reloj.tick(Velocidad) / 1000.0
        
        # Si por alguna razón DeltaTiempo es muy grande (ej. al inicio), lo limitamos
        # para que el jugador no "salte" o se mueva demasiado rápido de golpe.
        if DeltaTiempo > 0.1:
            DeltaTiempo = 1/60

        JuegoPrincipal.Update(DeltaTiempo) # Para actualizar la logica del juego
        JuegoPrincipal.Draw() # Para dibujar el juego en la pantalla 
       
        pygame.display.flip() # Para actualizar la pantalla con lo que se ha dibujado 
        

    pygame.quit() # para cerrar pygame correctamente 
    sys.exit() # para cerrar el programa correctamente 

if __name__ == "__main__": # Para ejecutar la funsion main solo si este archivo es el que se esta ejecutando directamente. 
      main()