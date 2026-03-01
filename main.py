# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

# Importe la libreria para hacer el juego y para que cierre bien.
import pygame
import sys 
import random # Importe random para seleccionar posisiones aleatorias para los enemigos
from scripts.game import Game # Para llamar la clase game desde game.py
import math # Importado para efectos visuales

# Inicie pygame para que mi juego corra y cree la funcion principal para controlar el juego.

def main():
    pygame.init()
    
    # INTEGRACION DE MUSICA y SONIDOS 
    pygame.mixer.init() # Inicia el mezclador de sonidos
    
    # Variables de control para evitar que los sonidos se reproduzcan multiples veces al cambiar de estado 
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

        # CARGA DE IMAGEN DE FONDO PARA EL MENÚ 
        imagen_fondo_menu = pygame.image.load("assets/images/fondo_menu.jpg")
    except:
        print("Error: Revisa las rutas de los archivos de audio e imágenes en assets/")
    

    # Obtener resolución real de la pantalla

    infoPantalla = pygame.display.Info() # Para obtener la informacion de la pantalla actual    
    anchoPantalla = infoPantalla.current_w # Para obtener el ancho de la pantalla actual 
    altoPantalla = infoPantalla.current_h # Para obtener la altura de la pantalla actual 

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

    # FUENTES 
    fuente_botones = pygame.font.SysFont("Arial Black", 40)
    fuente_boom = pygame.font.SysFont("Arial Black", 100)
    
    # Inicializar rectángulos globales para los botones
    rect_jugar = pygame.Rect(0,0,300,80)
    rect_salir = pygame.Rect(0,0,300,80)
    rect_reintentar = pygame.Rect(0,0,350,80)
    rect_volver_menu = pygame.Rect(0,0,450,80)

    #  VARIABLES PARA EL EFECTO DE CHISPITAS 
    chispitas = []
    for _ in range(100):
        chispitas.append({
            'x': random.randint(0, anchoPantalla),
            'y': random.randint(0, altoPantalla),
            'vel_y': random.uniform(-2, -5),
            'vel_x': random.uniform(-1, 1),
            'color': random.choice([(255, 255, 255), (255, 255, 0), (255, 215, 0)]) # Blanco y Dorado
        })

    while Jugando: # Bucle principal del juego, este se ejecuta mientras jugando sea verdadero
        mouse_pos = pygame.mouse.get_pos()
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

            #  LÓGICA DE CLIC EN BOTONES 
            if Evento.type == pygame.MOUSEBUTTONDOWN:
                if Evento.button == 1: # Clic izquierdo
                    # Botones del Menú
                    if JuegoPrincipal.Estado == "MENU":
                        if rect_jugar.collidepoint(mouse_pos):
                            JuegoPrincipal.Estado = "JUGANDO"
                        elif rect_salir.collidepoint(mouse_pos):
                            Jugando = False
                    
                    # Botones de Game Over y Victoria
                    elif JuegoPrincipal.Estado == "GAME_OVER" or JuegoPrincipal.Estado == "VICTORIA":
                        if rect_reintentar.collidepoint(mouse_pos):
                            JuegoPrincipal = Game(Pantalla) 
                            JuegoPrincipal.Estado = "JUGANDO"
                            pygame.event.clear()
                            break 
                            
                        elif rect_volver_menu.collidepoint(mouse_pos):
                            JuegoPrincipal = Game(Pantalla)
                            JuegoPrincipal.Estado = "MENU"
                            pygame.event.clear()
                            break

        #  GESTOR DE SONIDO DINÁMICO CORREGIDO 
        if JuegoPrincipal.Estado != estado_anterior:
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

            elif JuegoPrincipal.Estado == "GAME_OVER":
                if not sonido_derrota_jugado:
                    sonido_pierdo.play()
                    sonido_derrota_jugado = True

            elif JuegoPrincipal.Estado == "VICTORIA":
                if not sonido_victoria_jugado:
                    sonido_victoria.play()
                    sonido_victoria_jugado = True
            
            estado_anterior = JuegoPrincipal.Estado

        # Actualización de tiempos
        DeltaTiempo = Reloj.tick(Velocidad) / 1000.0
        if DeltaTiempo > 0.1: DeltaTiempo = 1/60

        # Lógica de dibujo según el estado
        if JuegoPrincipal.Estado == "JUGANDO":
            JuegoPrincipal.Handle_Events(Eventos) 
            JuegoPrincipal.Update(DeltaTiempo)
            if hasattr(JuegoPrincipal, 'perdio') and JuegoPrincipal.perdio:
                JuegoPrincipal.Estado = "GAME_OVER"
            JuegoPrincipal.Draw()

        elif JuegoPrincipal.Estado == "MENU":
            fondo_esc = pygame.transform.scale(imagen_fondo_menu, (anchoPantalla, altoPantalla))
            Pantalla.blit(fondo_esc, (0,0))
            
            tiempo_anim = pygame.time.get_ticks()
            brillo = int(80 * math.sin(tiempo_anim * 0.005) + 80)
            
            rect_jugar.center = (anchoPantalla//2, altoPantalla//2 + 50)
            color_j = (50 + brillo, 50 + brillo, 255) if rect_jugar.collidepoint(mouse_pos) else (40, 40, 40)
            pygame.draw.rect(Pantalla, color_j, rect_jugar, border_radius=25)
            pygame.draw.rect(Pantalla, (200, 200, 255), rect_jugar, 3, border_radius=25)
            txt_j = fuente_botones.render("JUGAR", True, (255,255,255))
            Pantalla.blit(txt_j, txt_j.get_rect(center=rect_jugar.center))
            
            rect_salir.center = (anchoPantalla//2, altoPantalla//2 + 160)
            color_s = (50 + brillo, 50 + brillo, 255) if rect_salir.collidepoint(mouse_pos) else (40, 40, 40)
            pygame.draw.rect(Pantalla, color_s, rect_salir, border_radius=25)
            pygame.draw.rect(Pantalla, (200, 200, 255), rect_salir, 3, border_radius=25)
            txt_s = fuente_botones.render("SALIR", True, (255,255,255))
            Pantalla.blit(txt_s, txt_s.get_rect(center=rect_salir.center))

        elif JuegoPrincipal.Estado == "GAME_OVER":
            Pantalla.fill((15, 0, 0))
            tiempo_anim = pygame.time.get_ticks()
            brillo = int(80 * math.sin(tiempo_anim * 0.005) + 80)

            for i in range(3):
                radio = (tiempo_anim // 4 % 500) + (i * 45)
                pygame.draw.circle(Pantalla, (200, 50, 0), (anchoPantalla//2, altoPantalla//2), radio, 4)

            texto_boom = fuente_boom.render("¡BOOM! PERDISTE", True, (255, 255, 0))
            Pantalla.blit(texto_boom, texto_boom.get_rect(center=(anchoPantalla//2, altoPantalla//2 - 150)))

            rect_reintentar.center = (anchoPantalla//2, altoPantalla//2 + 50)
            color_r = (50 + brillo, 50 + brillo, 255) if rect_reintentar.collidepoint(mouse_pos) else (80, 0, 0)
            pygame.draw.rect(Pantalla, color_r, rect_reintentar, border_radius=25)
            pygame.draw.rect(Pantalla, (255,255,255), rect_reintentar, 2, border_radius=25)
            txt_r = fuente_botones.render("REINTENTAR", True, (255,255,255))
            Pantalla.blit(txt_r, txt_r.get_rect(center=rect_reintentar.center))

            rect_volver_menu.center = (anchoPantalla//2, altoPantalla//2 + 160)
            color_v = (50 + brillo, 50 + brillo, 255) if rect_volver_menu.collidepoint(mouse_pos) else (80, 0, 0)
            pygame.draw.rect(Pantalla, color_v, rect_volver_menu, border_radius=25)
            pygame.draw.rect(Pantalla, (255,255,255), rect_volver_menu, 2, border_radius=25)
            txt_v = fuente_botones.render("VOLVER AL MENÚ", True, (255,255,255))
            Pantalla.blit(txt_v, txt_v.get_rect(center=rect_volver_menu.center))

        elif JuegoPrincipal.Estado == "VICTORIA":
            Pantalla.fill((0, 80, 0)) # Fondo verde oscuro para resaltar chispitas
            tiempo_anim = pygame.time.get_ticks()
            brillo = int(80 * math.sin(tiempo_anim * 0.005) + 80)

            #  DIBUJAR EFECTO DE CHISPITAS 
            for c in chispitas:
                c['y'] += c['vel_y']
                c['x'] += c['vel_x']
                if c['y'] < -10: c['y'] = altoPantalla + 10 # Reiniciar abajo
                
                # Brillo 
                tamanio = random.randint(2, 5)
                pygame.draw.circle(Pantalla, c['color'], (int(c['x']), int(c['y'])), tamanio)

            texto_ganaste = fuente_boom.render("¡NIVEL COMPLETADO!", True, (255, 255, 255))
            Pantalla.blit(texto_ganaste, texto_ganaste.get_rect(center=(anchoPantalla//2, altoPantalla//2 - 150)))

            # Botón REINTENTAR (Victoria)
            rect_reintentar.center = (anchoPantalla//2, altoPantalla//2 + 50)
            color_r = (50 + brillo, 50 + brillo, 255) if rect_reintentar.collidepoint(mouse_pos) else (0, 120, 0)
            pygame.draw.rect(Pantalla, color_r, rect_reintentar, border_radius=25)
            pygame.draw.rect(Pantalla, (255,255,255), rect_reintentar, 2, border_radius=25)
            txt_r = fuente_botones.render("REINTENTAR", True, (255,255,255))
            Pantalla.blit(txt_r, txt_r.get_rect(center=rect_reintentar.center))

            # Botón VOLVER AL MENÚ (Victoria)
            rect_volver_menu.center = (anchoPantalla//2, altoPantalla//2 + 160)
            color_v = (50 + brillo, 50 + brillo, 255) if rect_volver_menu.collidepoint(mouse_pos) else (0, 120, 0)
            pygame.draw.rect(Pantalla, color_v, rect_volver_menu, border_radius=25)
            pygame.draw.rect(Pantalla, (255,255,255), rect_volver_menu, 2, border_radius=25)
            txt_v = fuente_botones.render("VOLVER AL MENÚ", True, (255,255,255))
            Pantalla.blit(txt_v, txt_v.get_rect(center=rect_volver_menu.center))
       
        pygame.display.flip() 

    pygame.quit()
    sys.exit()

if __name__ == "__main__": 
      main()