# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033
import pygame 
# Cree la clase Timer
class Timer:  

    def __init__(self, TiempoInicial):  # Constructor que recibe el tiempo inicial

        self.TiempoRestante = TiempoInicial  #  Para Guardar el tiempo que irá bajando

        self.Fuente = pygame.font.SysFont("Arial", 40)  # Para Crear la fuente del texto 

    def Actualizar(self, DeltaTiempo):  # Función para que reste el tiempo cada frame 

        self.TiempoRestante -= DeltaTiempo  # Para restar el tiempo transcurrido 

        if self.TiempoRestante < 0:  # Si el tiempo baja de 0
            self.TiempoRestante = 0  # Lo fija en 0 para que no sea negativo

    def Dibujar(self, Pantalla):  # Función para dibujar el tiempo en pantalla

        Texto = f"Tiempo: {int(self.TiempoRestante)}"  # Convierte el tiempo a entero para mostrarlo limpio

        SuperficieTexto = self.Fuente.render(Texto, True, (255, 255, 255))  # Para visualizar texto blanco

        Pantalla.blit(SuperficieTexto, (20, 20))  # Dibuja el texto en la esquina superior izquierda

    def TiempoTerminado(self):  # Función que indica si el tiempo llegó a 0

        return self.TiempoRestante <= 0  # Devuelve True si terminó, False si no