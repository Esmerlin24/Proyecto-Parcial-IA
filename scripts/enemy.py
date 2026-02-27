# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

import pygame  
import math # Importe math para calcular distancias y vision real
from .behavior_tree import Selector, Secuencia, Accion # Importe el algoritmo del arbol de comportamiento
from .astar import Astar # Importe el algoritmo de búsqueda de caminos A* 

class Enemigo:  
   
    # Si un enemigo ve al jugador, guarda aquí la posición para que los otros lo sepan
    Alerta_Global_Pos = None 

    def __init__(self, Mapa, Fila, Columna, DireccionInicial=1):
        # Mapa, es para hacer referencia al mapa 
        # Fila, para la posición vertical inicial 
        # Columna,para la posición horizontal inicial 
        # DireccionInicial, 1 derecha, -1 izquierda 

        self.Mapa = Mapa  # Para guardar el mapa dentro del enemigo y poder revisar colisiones
        self.Fila = float(Fila)  # para guardar la posicion vertical del enemigo
        self.Columna = float(Columna)  # para guardar la posicion horizontal del enemigo
        
       
        self.OrigenFila = float(Fila) # para guardar la posicion de origen vertical del enemigo
        self.OrigenColumna = float(Columna)
        
        self.Direccion = DireccionInicial  # Para guardar la direccion del enemigo 
        self.Velocidad = 2.0  # velocidad base de los enemigos
         

        # Variables temporales para el Árbol
        self.DeltaTiempo_actual = 0 # Para guardar el delta tiempo actual y usarlo en las acciones 
        self.jugador_actual = None # Para guardar la referencia al jugador y usarlo en las acciones 
        self.estado_terminal = "" # Para no saturar la consola de prints
        self.Alerta = False #  variable para saber si el enemigo está en modo búsqueda

        # CONSTRUCCIÓN DEL ÁRBOL DE COMPORTAMIENTO
        self.comportamiento = Selector() 
        
        # Rama 1: Persecución Directa (Si yo lo veo)
        secuencia_persecucion = Secuencia()  
        secuencia_persecucion.agregar_hijo(Accion(self.ve_al_jugador)) 
        secuencia_persecucion.agregar_hijo(Accion(self.perseguir))
        
        # Rama 2: Refuerzo (Si otro lo vio, voy a ese punto)
        secuencia_refuerzo = Secuencia()
        secuencia_refuerzo.agregar_hijo(Accion(self.hay_alerta_global))
        secuencia_refuerzo.agregar_hijo(Accion(self.ir_al_refuerzo))

        # 1. Intentar perseguir si yo lo veo
        self.comportamiento.agregar_hijo(secuencia_persecucion) 
        # 2. Si no lo veo yo, ver si alguien más dio la voz de alerta
        self.comportamiento.agregar_hijo(secuencia_refuerzo)
        # 3. Si todo falla, volver a su puesto y patrullar
        self.comportamiento.agregar_hijo(Accion(self.patrullar))

    def Actualizar(self, DeltaTiempo, Jugador): # Para actualizar el comportamiento del enemigo 
        self.DeltaTiempo_actual = DeltaTiempo
        self.jugador_actual = Jugador
        self.comportamiento.ejecutar()

    def ve_al_jugador(self):
        distancia = math.sqrt((self.Fila - self.jugador_actual.Fila)**2 + (self.Columna - self.jugador_actual.Columna)**2)
        
        if distancia <= 8: # Rango de visión equilibrado
            pasos = int(distancia * 3) 
            for i in range(1, pasos):
                t = i / pasos
                check_f = self.Fila + (self.jugador_actual.Fila - self.Fila) * t
                check_c = self.Columna + (self.jugador_actual.Columna - self.Columna) * t
                if self.Mapa.Cuadricula[int(check_f)][int(check_c)] == 1:
                    self.Alerta = False
                    return False 
            
            # SI LO VEO: Activo mi alerta y aviso a los demás (Colmena)
            self.Alerta = True 
            Enemigo.Alerta_Global_Pos = (self.jugador_actual.Fila, self.jugador_actual.Columna)
            
            if self.estado_terminal != "PERSIGUIENDO":
                print("🎯 ¡Enemigo: Objetivo localizado! Avisando a la colmena.")
                self.estado_terminal = "PERSIGUIENDO"
            return True 
            
        self.Alerta = False 
        return False 

    def hay_alerta_global(self):
        # Comprobar si algún compañero vio al jugador
        if Enemigo.Alerta_Global_Pos is not None:
            dist_alerta = math.sqrt((self.Fila - Enemigo.Alerta_Global_Pos[0])**2 + (self.Columna - Enemigo.Alerta_Global_Pos[1])**2)
            # Si llega al punto y no hay nadie, se apaga la alerta
            if dist_alerta < 0.5:
                Enemigo.Alerta_Global_Pos = None
                return False
            return True
        return False

    def ir_al_refuerzo(self):
        # Velocidad de refuerzo moderada (2.4) para que el jugador pueda reaccionar
        return self.mover_con_astar(Enemigo.Alerta_Global_Pos[0], Enemigo.Alerta_Global_Pos[1], 2.4)

    def perseguir(self):
        # Persecución activa directa (2.8), lo suficientemente lento para poder huir
        return self.mover_con_astar(self.jugador_actual.Fila, self.jugador_actual.Columna, 2.8)

    def mover_con_astar(self, t_fila, t_columna, vel_base):
        # Función genérica para mover al enemigo usando A*
        if self.Mapa.Cuadricula[int(self.Fila)][int(self.Columna)] == 4:
            self.Velocidad = vel_base * 0.4 
        else:
            self.Velocidad = vel_base

        Inicio = (int(round(self.Fila)), int(round(self.Columna))) 
        Destino = (int(t_fila), int(t_columna)) 

        Ruta, _, _ = Astar(Inicio, Destino, self.Mapa.Cuadricula)

        if len(Ruta) > 1:
            SiguientePaso = Ruta[1] 
            TargetFila = float(SiguientePaso[0])
            TargetCol = float(SiguientePaso[1])

            dir_f = 1 if TargetFila > self.Fila else (-1 if TargetFila < self.Fila else 0)
            dir_c = 1 if TargetCol > self.Columna else (-1 if TargetCol < self.Columna else 0)

            self.Fila += dir_f * self.Velocidad * self.DeltaTiempo_actual
            self.Columna += dir_c * self.Velocidad * self.DeltaTiempo_actual
            
            return True
        return False

    def patrullar(self):
        # Si no hay nadie a quien perseguir, primero vuelve a su origen usando A* (Evita quedarse parado)
        dist_al_origen = math.sqrt((self.Fila - self.OrigenFila)**2 + (self.Columna - self.OrigenColumna)**2)
        
        if dist_al_origen > 0.5:
            if self.estado_terminal != "RETORNANDO":
                print("🔙 Enemigo: Perdió rastro. Volviendo a base.")
                self.estado_terminal = "RETORNANDO"
            return self.mover_con_astar(self.OrigenFila, self.OrigenColumna, 1.8)
        
        # Una vez en su origen, hace la patrulla normal horizontal que ya tenías
        if self.estado_terminal != "PATRULLANDO":
            print("🚶‍♂️ Enemigo: Patrullando zona asignada.")
            self.estado_terminal = "PATRULLANDO"
        
        self.Velocidad = 1.2 # Patrulla lenta para que el jugador pueda pasar sigiloso
        proxima_c = self.Columna + self.Direccion * self.Velocidad * self.DeltaTiempo_actual
        
        # Si choca con pared (1) o salida (2), cambia de dirección
        if self.Mapa.Cuadricula[int(self.Fila)][int(proxima_c + (0.4 * self.Direccion))] in [1, 2]:
            self.Direccion *= -1 
        else:
            self.Columna = proxima_c 
        return True

    def Dibujar(self, Pantalla):
        TX = Pantalla.get_width() // len(self.Mapa.Cuadricula[0])
        TY = Pantalla.get_height() // len(self.Mapa.Cuadricula)
        CentroX, CentroY = int((self.Columna + 0.5) * TX), int((self.Fila + 0.5) * TY)
        Radio = int(min(TX, TY) * 0.35) 
        
        if self.Alerta: Color = (255, 0, 0) # Rojo: Te vio
        elif Enemigo.Alerta_Global_Pos: Color = (255, 128, 0) # Naranja: Refuerzo
        else: Color = (130, 0, 0) # Marrón: Patrulla
            
        pygame.draw.circle(Pantalla, Color, (CentroX, CentroY), Radio) 
        pygame.draw.circle(Pantalla, (255, 255, 255), (CentroX, CentroY), int(Radio * 0.5)) 

    def ColisionaConJugador(self, Jugador):
        Distancia = math.sqrt((self.Fila - Jugador.Fila)**2 + (self.Columna - Jugador.Columna)**2)
        return Distancia < 0.7