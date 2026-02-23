# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033
import pygame 
# Creamos la clase Player
class Player: 
  # EL Constructor que se ejecuta cuando se crea el jugador 
    def __init__(self, Mapa): 

        self.Mapa = Mapa  # Guardamos el mapa dentro del jugador para poder revisar colisiones.

        self.Fila = 1  # Posición inicial vertical en el grid 
        self.Columna = 1  # Posición inicial horizontal en el grid 

        self.Color = (0, 255, 0)  # Color De mi jugador 

        self.Velocidad = 2  # Velocidad en píxeles por segundo, que va a tener el jugador. 

       # Función que mueve el jugador
    
    def Mover(self, Teclas, DeltaTiempo):   

        NuevaFila = self.Fila  # Variable temporal que voy a utilizar para probar movimiento vertical
        NuevaColumna = self.Columna  

        if Teclas[pygame.K_UP]:  # Si la flecha arriba está presionada 
            NuevaFila -= 1  # Restamos una fila (sube en el grid)

        if Teclas[pygame.K_DOWN]:  # Si la flecha abajo está presionada
            NuevaFila += 1 

        if Teclas[pygame.K_LEFT]:  # Si la flecha izquierda está presionada
            NuevaColumna -= 1  

        if Teclas[pygame.K_RIGHT]:  # Si la flecha derecha está presionada
            NuevaColumna += 1  

        # Verifico que la nueva posición esté dentro de los límites del mapa y que no sea una pared
        if 0 <= NuevaFila < len(self.Mapa.Cuadricula) and \
           0 <= NuevaColumna < len(self.Mapa.Cuadricula[0]) and \
          self.Mapa.Cuadricula[NuevaFila][NuevaColumna] != 1:

         self.Fila = NuevaFila
         self.Columna = NuevaColumna
         
      # Función para dibujar el jugador 
    def Dibujar(self, Pantalla): 

        AnchoPantalla = Pantalla.get_width()  # Para Obtener el ancho real de la pantalla
        AltoPantalla = Pantalla.get_height()  # Para Obtener el alto real de la pantalla

        Filas = len(self.Mapa.Cuadricula)  # Cuenta cuántas filas tiene el mapa y en la siguiente linea las columnas.
        Columnas = len(self.Mapa.Cuadricula[0]) 

        TamañoCeldaX = AnchoPantalla // Columnas  # Para Calcular el ancho de cada celda
        TamañoCeldaY = AltoPantalla // Filas  # El Alto de la celda

        PosicionX = self.Columna * TamañoCeldaX  
        PosicionY = self.Fila * TamañoCeldaY  

        Rectangulo = pygame.Rect(PosicionX, PosicionY, TamañoCeldaX, TamañoCeldaY)  # Crea el rectángulo del jugador

        pygame.draw.rect(Pantalla, self.Color, Rectangulo)  # Dibuja el jugador 