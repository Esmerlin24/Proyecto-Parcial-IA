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
    
    # Para dibujar el mapa en la pantalla
    def Dibujar(self, Pantalla): 
        
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
                    pygame.draw.rect(Pantalla, (100,100,100), Rectangulo) # Para dibujar las paredes de color gris.

                elif Valor == 2:
                    pygame.draw.rect(Pantalla, (255,255,0), Rectangulo) # Para dibujar la salida de color amarillo.

                elif Valor == 3:
                    pygame.draw.rect(Pantalla, (200,0,0), Rectangulo) # Para dibujar las trampas de pinchos de color rojo.

                elif Valor == 4:
                    pygame.draw.rect(Pantalla, (139,69,19), Rectangulo) # Para dibujar el lodo de color marrón.

                else:
                    pygame.draw.rect(Pantalla, (30,30,30), Rectangulo) # Para dibujar el suelo de color oscuro.