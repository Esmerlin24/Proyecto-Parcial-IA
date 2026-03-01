# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

# Importe la libreria para hacer el juego y para que cierre bien.
import pygame
import sys 
import random # Importe random para seleccionar posisiones aleatorias para los enemigos
from scripts.game import Game # Para llamar la clase game desde game.py

# Inicie pygame para que mi juego corra y cree la funcion principal para controlar el juego.

def main():
    pygame.init()
    
    # INTEGRACION DE MUSICA Y SONIDOS 
    pygame.mixer.init() # Inicia el mezclador de sonidos
    
    # Variables de control para evitar  que los sonidos se reproduzcan multiples veces al cambiar de estado 
    estado_anterior = ""
    sonido_victoria_jugado = False
    sonido_derrota_jugado = False

    try:
        # Carga de canciones Musica de fondo y Menu
        ruta_musica_fondo = "assets/music/musica_fondo.mp3"
        ruta_musica_menu = "assets/music/musica_menu.mp3"
        
        # Carga de efectos de sonido
        sonido_victoria = pygame.mixer.Sound("assets/music/sonido_victoria.mp3")
        sonido_choque = pygame.mixer.Sound("assets/sounds/sonido_choque.wav")
        sonido_pierdo = pygame.mixer.Sound("assets/sounds/sonido_pierdo.mp3")
    except:
        print("Error: Revisa las rutas de los archivos de audio en assets/music y assets/sounds")
    

    # Obtener resolución real de la pantalla

    infoPantalla = pygame.display.Info() # Para obtener la informacion de la pantalla actual    
    anchoPantalla = infoPantalla.current_w # Para obtener el ancho de la pantalla actual 
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

    # Definir posiciones estratégicas para que los enemigos aparezcan en lugares distintos

    posiciones_estrategicas = [(200, 200), (800, 200), (200, 600), (900, 500), (500, 300)]

    Jugando = True # Variable para controlar el bucle principal del juego 
    EnPantallaCompleta = True # variable para controlar el estado de pantalla completa 

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

        #  GESTOR DE SONIDO DINÁMICO CORREGIDO 
        if JuegoPrincipal.Estado != estado_anterior:
            # Si el estado cambió, detenemos todo lo que esté sonando
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            
            if JuegoPrincipal.Estado == "MENU":
                pygame.mixer.music.load(ruta_musica_menu)
                pygame.mixer.music.play(-1)
                sonido_victoria_jugado = False
                sonido_derrota_jugado = False

            elif JuegoPrincipal.Estado == "JUGANDO":
                pygame.mixer.music.load(ruta_musica_fondo)
                pygame.mixer.music.play(-1)
                sonido_victoria_jugado = False
                sonido_derrota_jugado = False

            elif JuegoPrincipal.Estado == "VICTORIA":
                if not sonido_victoria_jugado:
                    sonido_victoria.play()
                    sonido_victoria_jugado = True

            elif JuegoPrincipal.Estado == "GAME_OVER":
                if not sonido_derrota_jugado:
                    sonido_pierdo.play()
                    sonido_derrota_jugado = True
            
            # Actualice el estado anterior para que esto solo ocurra una vez por cambio
            estado_anterior = JuegoPrincipal.Estado
        

        JuegoPrincipal.Handle_Events(Eventos) # Para manejar los eventos del juego 
        
        # Limitamos los FPS a 60 y calculamos el DeltaTiempo de forma precisa
        DeltaTiempo = Reloj.tick(Velocidad) / 1000.0
        
        # Si por alguna razón DeltaTiempo es muy grande (ej. al inicio), lo limitamos
        # para que el jugador no "salte" o se mueva demasiado rápido de golpe.
        if DeltaTiempo > 0.1:
            DeltaTiempo = 1/60

        # Lógica de reinicio 
        # Verificamos si el jugador perdió una vida o el tiempo se acabó 
        if hasattr(JuegoPrincipal, 'perdio') and JuegoPrincipal.perdio:
            
            # REPRODUCIR SONIDO CUANDO PIERDE CHOQUE O PINCHOS
            try:
                sonido_choque.play()
            except:
                pass

            # Reubicar al jugador a su posición inicial
            JuegoPrincipal.jugador.rect.topleft = (50, 50) 
            
            # Reubicar a cada enemigo en una posición estratégica aleatoria
            for enemigo in JuegoPrincipal.enemigos:
                enemigo.rect.topleft = random.choice(posiciones_estrategicas)
            
            # Resetear la variable de pérdida para que el juego continúe
            JuegoPrincipal.perdio = False
            
        # Lógica de victoria Sonido cuando llegas a la salida
        if hasattr(JuegoPrincipal, 'gano') and JuegoPrincipal.gano:
            # El sonido ya se maneja arriba por cambio de estado
            JuegoPrincipal.gano = False 

        JuegoPrincipal.Update(DeltaTiempo) # Para actualizar la logica del juego
        JuegoPrincipal.Draw() # Para dibujar el juego en la pantalla 
       
        pygame.display.flip() # Para actualizar la pantalla con lo que se ha dibujado 
        

    pygame.quit() # para cerrar pygame correctamente 
    sys.exit() # para cerrar el programa correctamente 

if __name__ == "__main__": # Para ejecutar la funsion main solo si este archivo es el que se esta ejecutando directamente. 
      main()