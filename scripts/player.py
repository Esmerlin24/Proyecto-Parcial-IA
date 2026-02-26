# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033
import pygame 
# Creamos la clase Player
class Player: 
  # EL Constructor que se ejecuta cuando se crea el jugador 
    def __init__(self, Mapa): 

        self.Mapa = Mapa  # Guardamos el mapa dentro del jugador para poder revisar colisiones.

        self.Fila = 1.0  # Posición inicial vertical en la cuadricula 
        self.Columna = 1.0  # Posición inicial horizontal en el cuadricula

        self.Color = (0, 255, 0)  # Color De mi jugador 

        self.Velocidad = 4.0  # Velocidad en píxeles por segundo, que va a tener el jugador. 

       # Función que mueve el jugador
    
    def Mover(self, Teclas, DeltaTiempo):   

        NuevaFila = self.Fila # Para calcular la nueva funsion vertical del jugador 
        NuevaColumna = self.Columna # Para calcular la nueva funsion horizontal del jugador

        if Teclas[pygame.K_UP]:  # si se presiona la flecha hacia arriba, se mueve hacia arriba 
            NuevaFila -= self.Velocidad * DeltaTiempo 
        if Teclas[pygame.K_DOWN]:  # si se presiona la flecha hacia abajo, se mueve hacia abajo
            NuevaFila += self.Velocidad * DeltaTiempo
        if Teclas[pygame.K_LEFT]:  #si se presiona la flecha hacia la izquierda, se mueve hacia la izquierda
            NuevaColumna -= self.Velocidad * DeltaTiempo
        if Teclas[pygame.K_RIGHT]:  # si se presiona la flecha hacia la derecha, se mueve hacia la derecha
            NuevaColumna += self.Velocidad * DeltaTiempo

       
        # Añadimos un margen (0.2) para que el "cuadrado" del jugador no entre en la pared
        margen = 0.3

        # Revisar colisión en Columna (Eje X)
        # Evaluamos el lado izquierdo y derecho del jugador
        if self.Mapa.Cuadricula[int(self.Fila + margen)][int(NuevaColumna + margen)] != 1 and \
           self.Mapa.Cuadricula[int(self.Fila + 1 - margen)][int(NuevaColumna + margen)] != 1 and \
           self.Mapa.Cuadricula[int(self.Fila + margen)][int(NuevaColumna + 1 - margen)] != 1 and \
           self.Mapa.Cuadricula[int(self.Fila + 1 - margen)][int(NuevaColumna + 1 - margen)] != 1:
            self.Columna = NuevaColumna

        # Revisar colisión en Fila (Eje Y)
        # Evaluamos el lado superior e inferior del jugador
        if self.Mapa.Cuadricula[int(NuevaFila + margen)][int(self.Columna + margen)] != 1 and \
           self.Mapa.Cuadricula[int(NuevaFila + 1 - margen)][int(self.Columna + margen)] != 1 and \
           self.Mapa.Cuadricula[int(NuevaFila + margen)][int(self.Columna + 1 - margen)] != 1 and \
           self.Mapa.Cuadricula[int(NuevaFila + 1 - margen)][int(self.Columna + 1 - margen)] != 1:
            self.Fila = NuevaFila
         
      # Función para dibujar el jugador 
    def Dibujar(self, Pantalla): 

        AnchoPantalla = Pantalla.get_width()  # Para devolver cuantos pixeles mide el ancho
        AltoPantalla = Pantalla.get_height()  # Para devolver cuantos pixeles mide el alto

        Filas = len(self.Mapa.Cuadricula)   # Para devolver cuantas filas tiene el mapa 
        Columnas = len(self.Mapa.Cuadricula[0]) # Para devolver cuantas columnas tiene el mapa 

        TamañoCeldaX = AnchoPantalla // Columnas  # Para dividir el ancho de la pantalla entre el numero de la columna del mapa
        TamañoCeldaY = AltoPantalla // Filas  # Para dividir el alto de la pantalla entre el numero de fila del mapa

        PosicionX = int(self.Columna * TamañoCeldaX)  # Para calcular la posicion horizontal del jugador multiplicando su columna por el tamaño de cada celda 
        PosicionY = int(self.Fila * TamañoCeldaY)  # Para calcular la posicion vertical del jugador multiplicando su fila por el tamaño de cada celda 

        Rectangulo = pygame.Rect(PosicionX, PosicionY, TamañoCeldaX, TamañoCeldaY)  # para crear un rectangulocon la posicion y el tamaño el jugador

        pygame.draw.rect(Pantalla, self.Color, Rectangulo) # para dibujar el rectangulo del jugador en la pantalla con su color 