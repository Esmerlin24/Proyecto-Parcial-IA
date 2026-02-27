# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

import pygame
import math
from .behavior_tree import Selector, Secuencia, Accion 
from .astar import Astar 

class Enemigo:
    def __init__(self, Mapa, Fila, Columna, DireccionInicial=1):
        self.Mapa = Mapa  
        self.Fila = float(Fila)  
        self.Columna = float(Columna)  
        
        # Puntos de origen para el retorno y patrulla limitada
        self.OrigenFila = float(Fila)
        self.OrigenColumna = float(Columna)
        
        self.Direccion = DireccionInicial  
        self.Velocidad = 2.0  
        self.RangoPatrulla = 3.0 

        # 
        try:
            hoja = pygame.image.load("assets/images/guardia_completo.png").convert_alpha()
            ancho_r = hoja.get_width()
            alto_r = alto_r = hoja.get_height()
            self.ImagenEnemigo = hoja.subsurface(pygame.Rect(0, 0, ancho_r // 4, alto_r // 4))
        except:
            self.ImagenEnemigo = None

        self.DeltaTiempo_actual = 0 
        self.jugador_actual = None 
        self.EnAlerta = False 
        
        
        self.TiempoOlvidar = 0 # Para que no deje de perseguir al instante

        # ÁRBOL DE COMPORTAMIENTO 
        self.comportamiento = Selector() 
        
        persecucion = Secuencia()  
        persecucion.agregar_hijo(Accion(self.ve_al_jugador)) 
        persecucion.agregar_hijo(Accion(self.perseguir))
        
        self.comportamiento.agregar_hijo(persecucion) 
        self.comportamiento.agregar_hijo(Accion(self.patrullar))

    def Actualizar(self, DeltaTiempo, Jugador): 
        self.DeltaTiempo_actual = DeltaTiempo
        self.jugador_actual = Jugador
        # Reducimos el tiempo de memoria en cada frame
        if self.TiempoOlvidar > 0:
            self.TiempoOlvidar -= DeltaTiempo
        self.comportamiento.ejecutar()

    def ve_al_jugador(self):
        dist = math.sqrt((self.Fila - self.jugador_actual.Fila)**2 + (self.Columna - self.jugador_actual.Columna)**2)
        
        # 1. Si está en rango de visión (6 cuadros)
        if dist < 5:
            # 2. Raycasting flexible
            pasos = int(dist * 2) 
            obstaculo = False
            for i in range(1, pasos):
                t = i / pasos
                check_f = int(self.Fila + (self.jugador_actual.Fila - self.Fila) * t)
                check_c = int(self.Columna + (self.jugador_actual.Columna - self.Columna) * t)
                
                if self.Mapa.Cuadricula[check_f][check_c] == 1:
                    obstaculo = True
                    break
            
            # Si no hay pared, te ve y reinicia la memoria
            if not obstaculo:
                self.EnAlerta = True
                self.TiempoOlvidar = 2.5 # Te perseguirá por 2.5 segundos aunque dobles
                return True
        
        # 3. Si tienes memoria activa, sigue persiguiendo aunque no te vea directo
        if self.TiempoOlvidar > 0:
            return True

        self.EnAlerta = False
        return False 

    def perseguir(self):
        inicio = (int(round(self.Fila)), int(round(self.Columna)))
        destino = (int(round(self.jugador_actual.Fila)), int(round(self.jugador_actual.Columna)))
        
        ruta, _, _ = Astar(inicio, destino, self.Mapa.Cuadricula)
        if len(ruta) > 1:
            proximo = ruta[1] 
            df = 1 if proximo[0] > self.Fila else (-1 if proximo[0] < self.Fila else 0)
            dc = 1 if proximo[1] > self.Columna else (-1 if proximo[1] < self.Columna else 0)
            
            
            velocidad_persecucion = self.Velocidad * 2
            self.Fila += df * velocidad_persecucion * self.DeltaTiempo_actual
            self.Columna += dc * velocidad_persecucion * self.DeltaTiempo_actual
            return True
        return False

    def patrullar(self):
        dist_al_origen = math.sqrt((self.Fila - self.OrigenFila)**2 + (self.Columna - self.OrigenColumna)**2)
        
        if dist_al_origen > 0.5:
            inicio = (int(round(self.Fila)), int(round(self.Columna)))
            destino = (int(round(self.OrigenFila)), int(round(self.OrigenColumna)))
            ruta, _, _ = Astar(inicio, destino, self.Mapa.Cuadricula)
            
            if len(ruta) > 1:
                p = ruta[1]
                df = 1 if p[0] > self.Fila else (-1 if p[0] < self.Fila else 0)
                dc = 1 if p[1] > self.Columna else (-1 if p[1] < self.Columna else 0)
                self.Fila += df * 1.5 * self.DeltaTiempo_actual
                self.Columna += dc * 1.5 * self.DeltaTiempo_actual
                return True

        self.Columna += self.Direccion * 1.2 * self.DeltaTiempo_actual
        dist_desde_centro = self.Columna - self.OrigenColumna
        col_futura = int(self.Columna + (0.5 * self.Direccion))
        
        if abs(dist_desde_centro) > self.RangoPatrulla or self.Mapa.Cuadricula[int(self.Fila)][col_futura] == 1:
            self.Direccion *= -1
        return True

    def Dibujar(self, Pantalla):
        tw = Pantalla.get_width() // len(self.Mapa.Cuadricula[0])
        th = Pantalla.get_height() // len(self.Mapa.Cuadricula)
        px, py = int(self.Columna * tw), int(self.Fila * th)

        if self.ImagenEnemigo:
            img = pygame.transform.scale(self.ImagenEnemigo, (tw, th))
            Pantalla.blit(img, (px, py))
        else:
            color = (255, 0, 0) if self.EnAlerta else (130, 0, 0)
            pygame.draw.circle(Pantalla, color, (px + tw//2, py + th//2), tw//3)

    def ColisionaConJugador(self, Jugador):
        dist = math.sqrt((self.Fila - Jugador.Fila)**2 + (self.Columna - Jugador.Columna)**2)
        return dist < 0.6