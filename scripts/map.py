# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

import pygame

# Cree mi clase Mapa
class Mapa:  

    def __init__(self): # Para ejecutar el codigo cuando cree el mapa.
        
        # 1 = Pared
        # 0 = Suelo
        # 2 = Salida

    # La estructura del mapa 

        self.Cuadricula = [  
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,2,1],
            [1,0,1,1,1,0,1,0,0,1],
            [1,0,0,0,1,0,1,0,0,1],
            [1,1,1,0,1,0,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1],
        ]
    
    # Para dibujar el mapa en la pantalla
    def Dibujar(self, Pantalla): 
        
        AnchoPantalla = Pantalla.get_width() # Para devolver cuántos píxeles mide de ancho.
        AltoPantalla = Pantalla.get_height() # Para devolver cuántos píxeles mide de alto.

       # Para dividir la pantalla tanto vertical como horizontal.
    
        Filas = len(self.Cuadricula)
        Columnas = len(self.Cuadricula[0])

        TamañoCeldaX = AnchoPantalla // Columnas
        TamañoCeldaY = AltoPantalla // Filas

        # Para recorrer la fila del mapa
        for Fila in range(Filas):  
            for Columna in range(Columnas):

                Valor = self.Cuadricula[Fila][Columna] #Para obtener el numero del mapa.

                PosicionX = Columna * TamañoCeldaX  
                PosicionY = Fila * TamañoCeldaY  

                Rectangulo = pygame.Rect(PosicionX, PosicionY, TamañoCeldaX, TamañoCeldaY)
                
                # Para dibujar bloque 
                if Valor == 1:
                    pygame.draw.rect(Pantalla, (100,100,100), Rectangulo) 

                elif Valor == 2:
                    pygame.draw.rect(Pantalla, (255,255,0), Rectangulo)

                else:
                    pygame.draw.rect(Pantalla, (30,30,30), Rectangulo)