# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

import pygame

# Cree mi clase Mapa
class Mapa:  

    def __init__(self): # Para ejecutar el codigo cuando cree el mapa.
        
        # 1 = Pared
        # 0 = Suelo
        # 2 = Salida
        # 3 = Trampa de Pinchos (Peligro)
        # 4 = Zona de Lodo (Lentitud)

    # La estructura del mapa 20*15 diseñada para que sea fluida y funcional
        self.Cuadricula = [  
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], # Pasillo superior despejado para inicio
            [1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1],
            [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
            [1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1],
            [1,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0,1], # Espacio amplio alrededor de pinchos
            [1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], # Pasillo central de gran flujo para la IA
            [1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0,0,0,0,1], # Zona de lodo con escape lateral
            [1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], # Espacio de maniobra para evitar enemigos
            [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1], # Salida (2) en zona abierta para evitar bloqueos
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
        
        # Cargo la imagen del suelo con la extensión 
        try:
            self.ImagenSuelo = pygame.image.load("assets/images/suelo.jpg").convert()
            self.ImagenPared = pygame.image.load("assets/images/pared.jpg").convert()
            self.ImagenSalida = pygame.image.load("assets/images/salida.jpg").convert()
            self.ImagenPinchos = pygame.image.load("assets/images/pinchos.png").convert_alpha()
            self.ImagenSueloSinPinchos = pygame.image.load("assets/images/suelo_sin_pinchos.jpg").convert()
            self.ImagenLodo = pygame.image.load("assets/images/lodo.png").convert_alpha()
        except:
            print("Error: No se pudieron cargar las imágenes. Asegúrate de que los nombres y extensiones sean correctos.")
            self.ImagenSuelo = None
            self.ImagenPared = None
            self.ImagenSalida = None
            self.ImagenPinchos = None
            self.ImagenSueloSinPinchos = None
            self.ImagenLodo = None

        # Variables para la animación de los pinchos
        self.UltimoCambio = pygame.time.get_ticks()
        self.MostrarPinchos = True
    
    # Para dibujar el mapa en la pantalla
    def Dibujar(self, Pantalla): 
        
        # Lógica para alternar la animación 
        TiempoActual = pygame.time.get_ticks()
        if TiempoActual - self.UltimoCambio > 4000:
            self.MostrarPinchos = not self.MostrarPinchos
            self.UltimoCambio = TiempoActual

        AnchoPantalla = Pantalla.get_width() # Para devolver cuántos píxeles mide de ancho.
        AltoPantalla = Pantalla.get_height() # Para devolver cuántos píxeles mide de alto.

       # Para dividir la pantalla tanto vertical como horizontal.
    
        Filas = len(self.Cuadricula) # Para devolver cuantas filas tiene el mapa
        Columnas = len(self.Cuadricula[0]) # Para devolver cuantas columnas tiene el mapa 

        TamañoCeldaX = AnchoPantalla // Columnas # Para dividir el ancho de la pantalla entre el numero de columna 
        TamañoCeldaY = AltoPantalla // Filas # Para dividir el alto de la pantalla entre el numero de fila 

        # Para recorrer la fila del mapa
        for Fila in range(Filas):  
            for Columna in range(Columnas): # Para recorrer la columna del mapa.

                Valor = self.Cuadricula[Fila][Columna] #Para obtener el numero del mapa.

                PosicionX = Columna * TamañoCeldaX  # Para calcular la posicion horizontal del bloque a dibujar 
                PosicionY = Fila * TamañoCeldaY  # Para calcular la posicion vertical del bloque a dibujar 

                Rectangulo = pygame.Rect(PosicionX, PosicionY, TamañoCeldaX, TamañoCeldaY) # Para crear un rectangulo con la posicion y el tamaño de cada bloque a dibujar 
                
                # Para dibujar bloque 
                if Valor == 1:
                    if self.ImagenPared:
                        ImgParedEsc = pygame.transform.scale(self.ImagenPared, (TamañoCeldaX, TamañoCeldaY))
                        Pantalla.blit(ImgParedEsc, (PosicionX, PosicionY))
                    else:
                        pygame.draw.rect(Pantalla, (100,100,100), Rectangulo) # Para dibujar las paredes de color gris.

                elif Valor == 2:
                    if self.ImagenSalida:
                        ImgSalidaEsc = pygame.transform.scale(self.ImagenSalida, (TamañoCeldaX, TamañoCeldaY))
                        Pantalla.blit(ImgSalidaEsc, (PosicionX, PosicionY))
                    else:
                        pygame.draw.rect(Pantalla, (255,255,0), Rectangulo) # Para dibujar la salida de color amarillo.

                elif Valor == 3:
                    # Animación: alterna entre la imagen de pinchos y la imagen de suelo sin pinchos
                    if self.MostrarPinchos and self.ImagenPinchos:
                        ImgPinchosEsc = pygame.transform.scale(self.ImagenPinchos, (TamañoCeldaX, TamañoCeldaY))
                        Pantalla.blit(ImgPinchosEsc, (PosicionX, PosicionY))
                    elif not self.MostrarPinchos and self.ImagenSueloSinPinchos:
                        ImgSueloSinEsc = pygame.transform.scale(self.ImagenSueloSinPinchos, (TamañoCeldaX, TamañoCeldaY))
                        Pantalla.blit(ImgSueloSinEsc, (PosicionX, PosicionY))
                    else:
                        pygame.draw.rect(Pantalla, (200,0,0) if self.MostrarPinchos else (30,30,30), Rectangulo)

                elif Valor == 4:
                    if self.ImagenLodo:
                        ImgLodoEsc = pygame.transform.scale(self.ImagenLodo, (TamañoCeldaX, TamañoCeldaY))
                        Pantalla.blit(ImgLodoEsc, (PosicionX, PosicionY))
                    else:
                        pygame.draw.rect(Pantalla, (139,69,19), Rectangulo) # Para dibujar el lodo de color marrón.

                else:
                    # Aquí se dibuja la imagen solo en el valor 0 (suelo)
                    if self.ImagenSuelo:
                        SueloEscalado = pygame.transform.scale(self.ImagenSuelo, (TamañoCeldaX, TamañoCeldaY))
                        Pantalla.blit(SueloEscalado, (PosicionX, PosicionY))
                    else:
                        pygame.draw.rect(Pantalla, (30,30,30), Rectangulo) # Para dibujar el suelo de color oscuro.