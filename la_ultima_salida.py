# Importe la libreria para el hacer el juego y para que cierre bien.
import pygame
import sys 

# Inicie pygame para que mi juego corra 
pygame.init()

# Estructura basica del juego

# creo mi ventana y la velocidad que va a tener mi jugador 

Ancho = 600
Alto = 500
Titulo = "La Última Salida"
Velocidad = 60

ventana = pygame.display.set_mode((Ancho, Alto))
pygame.display.set_caption(Titulo)

# Para controlar el tiempo 

Reloj = pygame.time.Clock()

#Colores que voy a utilizar 

Blanco = (255, 255, 255)
Negro = (0, 0, 0)
Rojo = (255, 0, 0)
Verde = (0, 255, 0)

#Mi Jugador 
 
Jugador_Horizontal = 50
Jugador_Vertical = 50
Jugador_Tamaño = 40
Jugador_Velocidad = 3

#Salida (La puerta)

Puerta_Horizontal = 500
Puerta_Vertical = 400
Puerta_Tamaño = 50

#Tiempo del juego

Tiempo_Maximo = 60
Tiempo_Inicio = pygame.time.get_ticks()

# Bucle Principal
Jugando = True

while Jugando:
    Reloj.tick(Velocidad)

#Para cerrar mi ventana
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            Jugando = False
 

# Movimientos de mi jugador 
    Teclas = pygame.key.get_pressed()

    if Teclas[pygame.K_LEFT]:
        Jugador_Horizontal -= Jugador_Velocidad
    if Teclas[pygame.K_RIGHT]:
        Jugador_Horizontal += Jugador_Velocidad
    if Teclas[pygame.K_UP]:
        Jugador_Vertical-= Jugador_Velocidad
    if Teclas[pygame.K_DOWN]:
        Jugador_Vertical += Jugador_Velocidad

# Aqui voy a dibujar todo en la pantalla

    ventana.fill(Negro)

    pygame.draw.rect(ventana, Verde,
        (Jugador_Horizontal, Jugador_Vertical, Jugador_Tamaño, Jugador_Tamaño))

    pygame.draw.rect(ventana, Rojo,
        (Puerta_Horizontal, Puerta_Vertical, Puerta_Tamaño, Puerta_Tamaño))
   

    pygame.display.flip()

# Para que mi juego salga bien 
pygame.quit()
sys.exit()









