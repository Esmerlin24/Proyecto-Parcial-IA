# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

import pygame 
import random # Importe random para las posiciones aleatorias de los enemigos

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
        self.joystick = None # Variable para almacenar el control conectado

        #  Para cargar los sonidos del juego
        try:
            self.sonido_victoria = pygame.mixer.Sound("assets/music/sonido_victoria.mp3")
            self.sonido_choque = pygame.mixer.Sound("assets/sounds/sonido_choque.wav")
            self.sonido_pierdo = pygame.mixer.Sound("assets/sounds/sonido_pierdo.mp3")
        except:
            print("Error cargando sonidos en Game")
        # 

        # Lista de posiciones estratégicas (Fila, Columna) donde pueden aparecer los enemigos
        self.Posiciones_Estrategicas = [
            (13, 10), (9, 5), (7, 15), (5, 5), (12, 18), (3, 10), (10, 2)
        ]

        self.Enemigos = [ # Lista de enemigos con sus posiciones iniciales
            Enemigo(self.Mapa, 13, 10), # Enemigo 1 bloqueando el pasillo de la salida
            Enemigo(self.Mapa, 9, 5),   # Enemigo 2 vigilando la entrada al lodo
            Enemigo(self.Mapa, 7, 14),   # Enemigo 3 patrullando el pasillo central derecho
        ] 
        
    # Función para reposicionar enemigos de forma aleatoria
    def Reposicionar_Enemigos_Aleatorio(self):
        for e in self.Enemigos:
            nueva_pos = random.choice(self.Posiciones_Estrategicas)
            e.Fila = float(nueva_pos[0])
            e.Columna = float(nueva_pos[1])

    # la funsion para los eventos del teclado y mouse
    def Handle_Events(self, Eventos):
        for Evento in Eventos: # Para recorrer cada evento
            # -Para los botones del control
            boton_x_presionado = False
            if Evento.type == pygame.JOYBUTTONDOWN:
                if Evento.button == 0: # Botón X en control de PS3
                    boton_x_presionado = True

            if Evento.type == pygame.KEYDOWN or boton_x_presionado: # para detectar si se presiona una tecla o botón.
                # Verificamos si fue ENTER o el botón X del mando
                if (Evento.type == pygame.KEYDOWN and Evento.key == pygame.K_RETURN) or boton_x_presionado: 
                    # Para reintentar Si presionas ENTER o X en Menu, Game Over o Victoria, el juego inicia
                    if self.Estado == "MENU" or self.Estado == "GAME_OVER" or self.Estado == "VICTORIA": # si el estado es menu, game over o victoria al presionar enter 
                        self.Estado = "JUGANDO" # Cambia el estado a jugando para iniciar el juego 
                        self.Vidas = 3  # reinicia las vidas 
                        self.Temporizador = Timer(60) # reinicia el temporizador 
                        self.Jugador = Player(self.Mapa) # reinicia el jugador a su posicion inicial 
                        
                        # Limpiar alerta global para que no te persigan al reaparecer
                        Enemigo.Alerta_Global_Pos = None
                        
                        self.Enemigos = [  # Reinicia los enemigos a sus posisiones estrategicas
                            Enemigo(self.Mapa, 13, 10), # Guardia de la salida
                            Enemigo(self.Mapa, 9, 5),   # Centinela del lodo
                            Enemigo(self.Mapa, 7, 14)   # Interceptor central
                        ]
                        # Al empezar de cero, reposicionamos los enemigos de forma aleatoria 
                        self.Reposicionar_Enemigos_Aleatorio()

    # El metodo para actualizar la logica del juego
    def Update(self, DeltaTiempo):

        if self.Estado == "JUGANDO": # Para actualizar las cosas solo si se esta jugando.
           
            self.Temporizador.Actualizar(DeltaTiempo) # para actualizar el temporizador.

            if self.Temporizador.TiempoTerminado(): # Para detectar si el tiempo se ha terminado
                self.Estado = "GAME_OVER"
                try: self.sonido_pierdo.play() # Sonido al acabar el tiempo
                except: pass

        
            # Usamos round para que detecte el bloque donde está el centro del jugador
            f_idx = int(round(self.Jugador.Fila))
            c_idx = int(round(self.Jugador.Columna))
            
            # Asegurar que los índices no se salgan del mapa por el redondeo
            f_idx = max(0, min(f_idx, len(self.Mapa.Cuadricula) - 1))
            c_idx = max(0, min(c_idx, len(self.Mapa.Cuadricula[0]) - 1))

            CeldaActual = self.Mapa.Cuadricula[f_idx][c_idx] # Para saber que pisa el jugador
            
            # LOGICA DE VELOCIDAD SEGUN EL TERRENO (LODO)
            if CeldaActual == 4: # Si el jugador esta pisando lodo (4)
                self.Jugador.Velocidad = 2.0 # Baja la velocidad del jugador 
            else:
                self.Jugador.Velocidad = 4.0 # Velocidad normal fuera del lodo

            # LOGICA DE DAÑO POR TRAMPAS
            if CeldaActual == 3: # Si el jugador pisa los pinchos rojos (3)
                self.Vidas -= 1 # Resta una vida por el daño
                try: self.sonido_choque.play() # Sonido al pisar trampa
                except: pass
                
                if self.Vidas <= 0: # Para revisar si murio
                    self.Estado = "GAME_OVER" # Cambia a pantalla de derrota
                    try: self.sonido_pierdo.play()
                    except: pass
                else:
                    # Limpiar alerta al morir por trampa
                    Enemigo.Alerta_Global_Pos = None # Para que los enemigos no te sigan al reaparecer 
                    self.Jugador.Fila = 1.0 # Lo devuelve al inicio por seguridad
                    self.Jugador.Columna = 1.0 
                    # Reposicionar enemigos al morir por trampa
                    self.Reposicionar_Enemigos_Aleatorio()

            
            Teclas = pygame.key.get_pressed() # Para obtener las teclas que se estan presionando en ese momento.
            
            # Diccionario para enviar inputs al jugador (Joysticks + D-Pad)
            inputs_control = {'x': 0, 'y': 0, 'x_der': 0, 'y_der': 0, 'dpad_x': 0, 'dpad_y': 0}
            
            # Leer todos los ejes si el control está conectado
            if self.joystick:
                # Joystick Izquierdo Ejes 0 y 1
                inputs_control['x'] = self.joystick.get_axis(0)
                inputs_control['y'] = self.joystick.get_axis(1)
                
                # Joystick Derecho Ejes 2 y 3 
                inputs_control['x_der'] = self.joystick.get_axis(2)
                inputs_control['y_der'] = self.joystick.get_axis(3)
                
                # Crucecita  D-Pad Hat 0
                dpad = self.joystick.get_hat(0)
                inputs_control['dpad_x'] = dpad[0]
                inputs_control['dpad_y'] = -dpad[1] # Invertimos Y porque el Hat es positivo hacia arriba

            #  las teclas como los inputs del joystick al jugador
            self.Jugador.Mover(Teclas, DeltaTiempo, inputs_control)

            
            if CeldaActual == 2: # si el jugador llega a la salida gana
                self.Estado = "VICTORIA"
                try: self.sonido_victoria.play() # Sonido al ganar
                except: pass

            for EnemigoActual in self.Enemigos: # Para actualizar cada enemigo en la lista de enemigos 
                EnemigoActual.Actualizar(DeltaTiempo, self.Jugador) 

                if EnemigoActual.ColisionaConJugador(self.Jugador): # para detectar si el enemigo choca con el jugador 
                    self.Vidas -= 1 
                    try: self.sonido_choque.play() # Sonido al chocar con enemigo
                    except: pass
                    
                    if self.Vidas <= 0:
                        self.Estado = "GAME_OVER"
                        try: self.sonido_pierdo.play()
                        except: pass
                    else:
                        # Reaparecer al inicio si pierde una vida
                        Enemigo.Alerta_Global_Pos = None # Resetear alerta de colmena al morir
                        self.Jugador.Fila = 1.0
                        self.Jugador.Columna = 1.0
                        #  Reposicionar enemigos al ser atrapado
                        self.Reposicionar_Enemigos_Aleatorio()

    # Para dibujar todo en mi pantalla 
    def Draw(self):

        if self.Estado == "MENU": # Para dibujar el menu 
            self.Pantalla.fill((0, 120, 252)) # color del menu 
            Fuente = pygame.font.SysFont("timesnewroman", 50, bold=True) # Para crear una fuente times new roman en negrita
            Texto = Fuente.render("LA ULTIMA SALIDA", True, (255, 255, 255)) # para creal el texto del titulo del juego 
            self.Pantalla.blit(Texto, (self.Pantalla.get_width()//2 - Texto.get_width()//2, 200)) 
            
            FuenteSub = pygame.font.SysFont("Arial", 30) # Para crear la fuente del subtitulo
            TextoSub = FuenteSub.render("Presiona ENTER o (X) para Empezar", True, (255, 255, 255))
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
            TextoR = FuenteR.render("Presiona ENTER o (X) para Reintentar", True, (255, 255, 255))
            self.Pantalla.blit(TextoR, (self.Pantalla.get_width() // 2 - TextoR.get_width() // 2, 350))

        elif self.Estado == "VICTORIA": # Pantalla de ganar
            self.Pantalla.fill((0, 125, 0)) # Verde para la victoria
            Fuente = pygame.font.SysFont("Arial", 60) 
            Texto = Fuente.render("¡NIVEL COMPLETADO!", True, (255, 255, 255))  
            self.Pantalla.blit(Texto, (self.Pantalla.get_width() // 2 - Texto.get_width() // 2, 250))
            
            # Mensaje de reintento
            FuenteR = pygame.font.SysFont("Arial", 30)
            TextoR = FuenteR.render("Presiona ENTER o (X) para jugar de nuevo", True, (255, 255, 255))
            self.Pantalla.blit(TextoR, (self.Pantalla.get_width() // 2 - TextoR.get_width() // 2, 350))