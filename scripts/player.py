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

        self.Velocidad = 2.0  # Velocidad en píxeles por segundo, que va a tener el jugador. 

      
         
       
        self.sprite_sheet = pygame.image.load("assets/images/jugador_completo.png").convert_alpha() # Cargue la imagen del jugador para manejar transparencia y animaciones 
        
        # Diccionario para guardar las listas de frames por dirección
        # 0: Abajo, 1: Izquierda, 2: Derecha, 3: Arriba (según el orden de la imagen)
        self.animaciones = {0: [], 1: [], 2: [], 3: []}
        self.direccion_actual = 0 # Empezamos mirando hacia abajo
        self.frame_index = 0
        self.timer_animacion = 0
        self.velocidad_animacion = 0.15 # Qué tan rápido mueve las piernas
        
   
        tamano_cuadro = 1024 // 4 

        # Recortamos la imagen de 4x4
        for fila in range(4):
            for col in range(4):
                # subsurface extrae el muñequito del cuadro 
                recorte = self.sprite_sheet.subsurface(pygame.Rect(col * tamano_cuadro, fila * tamano_cuadro, tamano_cuadro, tamano_cuadro))
                
               
                
                # Tomamos el color del primer píxel (esquina superior izquierda) y lo hacemos invisible
                color_fondo = recorte.get_at((0,0))
                recorte.set_colorkey(color_fondo)
                
                
                self.animaciones[fila].append(recorte)
        

       # Función que mueve el jugador
    
    def Mover(self, Teclas, DeltaTiempo):   

        NuevaFila = self.Fila # Para calcular la nueva funsion vertical del jugador 
        NuevaColumna = self.Columna # Para calcular la nueva funsion horizontal del jugador

        se_mueve = False # Para saber si debemos animar o quedarnos quietos

        if Teclas[pygame.K_UP]:  # si se presiona la flecha hacia arriba, se mueve hacia arriba 
            NuevaFila -= self.Velocidad * DeltaTiempo 
            self.direccion_actual = 3 # Fila de Arriba
            se_mueve = True
        elif Teclas[pygame.K_DOWN]:  # si se presiona la flecha hacia abajo, se mueve hacia abajo
            NuevaFila += self.Velocidad * DeltaTiempo
            self.direccion_actual = 0 # Fila de Abajo
            se_mueve = True
        
        if Teclas[pygame.K_LEFT]:  #si se presiona la flecha hacia la izquierda, se mueve hacia la izquierda
            NuevaColumna -= self.Velocidad * DeltaTiempo
            self.direccion_actual = 1 # Fila de Izquierda
            se_mueve = True
        elif Teclas[pygame.K_RIGHT]:  # si se presiona la flecha hacia la derecha, se mueve hacia la derecha
            NuevaColumna += self.Velocidad * DeltaTiempo
            self.direccion_actual = 2 # Fila de Derecha
            se_mueve = True

       
        if se_mueve: # Si el jugador se esta moviendo, actualizamos la animacion 
            self.timer_animacion += DeltaTiempo #
            if self.timer_animacion >= self.velocidad_animacion:
                self.timer_animacion = 0
                self.frame_index = (self.frame_index + 1) % 4 # Ciclo de 4 cuadros
        else:
            self.frame_index = 0 # Si está quieto, usa el primer cuadro de la fila
        
       
        # Añadimos un margen (0.2) para que el "cuadrado" del jugador no entre en la pared
        margen = 0.2

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

       
        # 1. Obtenemos el cuadro que toca según la dirección
        sprite_actual = self.animaciones[self.direccion_actual][self.frame_index]
        
        # 2. Escalamos el sprite para que se ajuste a la celda sin perder su forma
        sprite_escalado = pygame.transform.scale(sprite_actual, (TamañoCeldaX, TamañoCeldaY))
        
        # 3. Dibujamos la imagen directamente 
        Pantalla.blit(sprite_escalado, (PosicionX, PosicionY)) # para dibujar el rectangulo del jugador en la pantalla con su color 
      