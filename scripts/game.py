# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

import pygame 

# Para llamar la clase Mapa, desde el archivo map.py
from scripts.map import Mapa  
# Importe la clase Player desde player.py dentro de scripts.
from scripts.player import Player 
# Importe la clase Timer desde timer.py dentro de scripts.
from scripts.timer import Timer
# Importe la clase enemigo desde enemy.py
from scripts.enemy import Enemigo 

# Voy a crear mi clase llamada Game 
class Game:
    # cree mi contructor para ejecutar Game(Pantalla)

    def __init__(self, Pantalla):
        self.Pantalla = Pantalla #guardo pantalla
        self.Estado = "MENU" # utilice esta variable para controlar en que parte del juego estoy.
        self.Mapa = Mapa() # cree la el mapa para que sea un objeto real.
        self.Jugador = Player(self.Mapa) # Para crear el jugador y pasarle el mapa para que pueda revisar colisiones 
        self.Temporizador = Timer(60)  # 60 segundos iniciales 
        self.Vidas = 3  # para controlar las las vidas del jugador 

        self.Enemigos = [ # Lista de enemigos con sus posiciones iniciales
            Enemigo(self.Mapa, 11, 2, 1), # Enemigo que empieza en la fila 11, columna 2 y se mueva hacia la derecha
            Enemigo(self.Mapa, 5, 15, -1) # Enemigo que empieza en la fila 5, columna 15 y se mueve hacia la izquierda 
        ] 
        
    # la funsion para los eventos del teclado y mouse
    def Handle_Events(self, Eventos):
        for Evento in Eventos: # Para recorrer cada evento
            if Evento.type == pygame.KEYDOWN: # para detectar si se presiono una tecla.
                if Evento.key == pygame.K_RETURN: # si fue la tecla enter.
                    # Para reintentar Si presionas ENTER en Menu, Game Over o Victoria, el juego inicia
                    if self.Estado == "MENU" or self.Estado == "GAME_OVER" or self.Estado == "VICTORIA": # si el estado es menu, game over o victoria al presionar enter 
                        self.Estado = "JUGANDO" # Cambia el estado a jugando para iniciar el juego 
                        self.Vidas = 3  # reinicia las vidas 
                        self.Temporizador = Timer(60) # reinicia el temporizador 
                        self.Jugador = Player(self.Mapa) # reinicia el jugador a su posicion inicial 
                        self.Enemigos = [  # Reinicia los enemigos a sus posisiones iniciales
                            Enemigo(self.Mapa, 11, 2, 1),
                            Enemigo(self.Mapa, 5, 15, -1) 
                        ]

    # El metodo para actualizar la logica del juego
    def Update(self, DeltaTiempo):

        if self.Estado == "JUGANDO": # Para actualizar las cosas solo si se esta jugando.
           
            self.Temporizador.Actualizar(DeltaTiempo) # para actualizar el temporizador.

            if self.Temporizador.TiempoTerminado(): # Para detectar si el tiempo se ha terminado
                self.Estado = "GAME_OVER"  

            Teclas = pygame.key.get_pressed() # Para obtener las teclas que se estan presionandoen ese momento.
            self.Jugador.Mover(Teclas, DeltaTiempo)

            # Para DETECTAR SI EL JUGADOR GANA 
            # Si la celda donde está el jugador es el número 2 (la salida amarilla)
            if self.Mapa.Cuadricula[int(self.Jugador.Fila)][int(self.Jugador.Columna)] == 2: # si el jugador llega a la salida gana
                self.Estado = "VICTORIA"

            for EnemigoActual in self.Enemigos: # Para actualizar cada enemigo en la lista de enemigos 
                EnemigoActual.Actualizar(DeltaTiempo, self.Jugador) 

                if EnemigoActual.ColisionaConJugador(self.Jugador): # para detectar si el enemigo choca con el jugador 
                    self.Vidas -= 1 
                    if self.Vidas <= 0:
                        self.Estado = "GAME_OVER"
                    else:
                        # Reaparecer al inicio si pierde una vida
                        self.Jugador.Fila = 1.0
                        self.Jugador.Columna = 1.0        

    # Para dibujar todo en mi pantalla 
    def Draw(self):

        if self.Estado == "MENU": # Para dibujar el menu 
            self.Pantalla.fill((0, 120, 252)) # color del menu 
            Fuente = pygame.font.SysFont("Arial", 50) # Para crear una fuente ariel 50
            Texto = Fuente.render("LA ULTIMA SALIDA", True, (255, 255, 255)) # para creal el texto del titulo del juego 
            self.Pantalla.blit(Texto, (self.Pantalla.get_width()//2 - Texto.get_width()//2, 200)) 
            
            FuenteSub = pygame.font.SysFont("Arial", 30) # Para crear la fuente del subtitulo
            TextoSub = FuenteSub.render("Presiona ENTER para Empezar", True, (255, 255, 255))
            self.Pantalla.blit(TextoSub, (self.Pantalla.get_width()//2 - TextoSub.get_width()//2, 350))

        elif self.Estado == "JUGANDO":  # para dibujar el juego solo si esta jugando 
            self.Pantalla.fill((0, 0, 0)) # Para limpiar la pantalla 
            self.Mapa.Dibujar(self.Pantalla)  # Para dibujar el mapa en la pantalla 
            self.Jugador.Dibujar(self.Pantalla) # para dibujar el jugador en la pantalla 

            for EnemigoActual in self.Enemigos: # Para dibujar enemigo 
                EnemigoActual.Dibujar(self.Pantalla) #
            self.Temporizador.Dibujar(self.Pantalla) # Para dibujar el temporizador 

            # Dibujar Vidas
            FuenteVidas = pygame.font.SysFont("Arial", 30) # Para crear la fuente para mostrar las vidas 
            TextoVidas = FuenteVidas.render(f"Vidas: {self.Vidas}", True, (255, 255, 255))
            self.Pantalla.blit(TextoVidas, (20, 50))

        elif self.Estado == "GAME_OVER":  # Pantalla de game over 
            self.Pantalla.fill((125, 0, 0)) # Rojo para la derrota
            Fuente = pygame.font.SysFont("Arial", 60) 
            Texto = Fuente.render("GAME OVER", True, (255, 255, 255))  
            self.Pantalla.blit(Texto, (self.Pantalla.get_width() // 2 - Texto.get_width() // 2, 250))
            
            # Mensaje de reintento
            FuenteR = pygame.font.SysFont("Arial", 30)
            TextoR = FuenteR.render("Presiona ENTER para Reintentar", True, (255, 255, 255))
            self.Pantalla.blit(TextoR, (self.Pantalla.get_width() // 2 - TextoR.get_width() // 2, 350))

        elif self.Estado == "VICTORIA": # Pantalla de ganar
            self.Pantalla.fill((0, 125, 0)) # Verde para la victoria
            Fuente = pygame.font.SysFont("Arial", 60) 
            Texto = Fuente.render("¡NIVEL COMPLETADO!", True, (255, 255, 255))  
            self.Pantalla.blit(Texto, (self.Pantalla.get_width() // 2 - Texto.get_width() // 2, 250))
            
            # Mensaje de reintento
            FuenteR = pygame.font.SysFont("Arial", 30)
            TextoR = FuenteR.render("Presiona ENTER para jugar de nuevo", True, (255, 255, 255))
            self.Pantalla.blit(TextoR, (self.Pantalla.get_width() // 2 - TextoR.get_width() // 2, 350))