# Nombre: Esmerlin Severino Paredes
# Matrícula: 24-EISN-2-033

import heapq
import time

class Nodo:
    def __init__(self, dato, padre, costo):
        self.dato = dato  # Posición (fila, columna)
        self.padre = padre
        self.costo = costo # f = g + h
        # Para que heapq pueda comparar los nodos por su costo
        self.g = padre.g + 1 if padre else 0

    def __lt__(self, otro):
        return self.costo < otro.costo

    def __eq__(self, otro):
        return self.dato == otro.dato

    def __hash__(self):
        return hash(self.dato)

    def GenerarSucesores(self, mapa):
        sucesores = []
        fila, col = self.dato
        # Movimientos: Arriba, Abajo, Izquierda, Derecha
        movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for df, dc in movimientos:
            nf, nc = fila + df, col + dc
            # Verificar si está dentro del mapa y no es pared (1)
            if 0 <= nf < len(mapa) and 0 <= nc < len(mapa[0]):
                if mapa[nf][nc] != 1:
                    sucesores.append((nf, nc))
        return sucesores

    def Costo(self, destino):
        # Heurística: Distancia Manhattan
        return self.g + abs(self.dato[0] - destino[0]) + abs(self.dato[1] - destino[1])

def Astar(estado_inicial, estado_final, mapa_cuadricula):
    totalnodos = 1
    
    inicio_nodo = Nodo(estado_inicial, None, 0)
    inicio_nodo.costo = inicio_nodo.Costo(estado_final)
    
    nodoactual = inicio_nodo
    nodosgenerado = []
    nodosvisitados = set()
    heapq.heappush(nodosgenerado, nodoactual)

    inicio_tiempo = time.perf_counter()

    while nodoactual.dato != estado_final:
        if not nodosgenerado: return [], 0, 0 # Si no hay camino
        
        nodoactual = heapq.heappop(nodosgenerado)
        
        if nodoactual.dato in nodosvisitados:
            continue
            
        sucesores = nodoactual.GenerarSucesores(mapa_cuadricula)
        totalnodos += len(sucesores)

        for sucesor_pos in sucesores:
            # Calculamos costo del sucesor
            temp = Nodo(sucesor_pos, nodoactual, 0)
            temp.costo = temp.Costo(estado_final)

            if temp.dato not in nodosvisitados:
                heapq.heappush(nodosgenerado, temp)
        
        nodosvisitados.add(nodoactual.dato)

    camino = []
    while nodoactual:
        camino.append(nodoactual.dato)
        nodoactual = nodoactual.padre
    
    camino.reverse()
    fin = time.perf_counter()
    return camino, totalnodos, fin - inicio_tiempo