import random
import math

# Contar el número de conflictos (ataques entre reinas)
def calcularConflictos(tablero):
    conflictos = 0
    n = len(tablero)

    for i in range(n):
        for j in range(i + 1, n):
            if tablero[i] == tablero[j] or abs(tablero[i] - tablero[j]) == j - i:
                conflictos += 1

    return conflictos

# Generar un vecino moviendo una reina a una nueva posición en la misma columna
def generarVecino(tablero):
    n = len(tablero)
    nuevo_tablero = tablero[:]
    fila = random.randint(0, n - 1)
    nueva_columna = random.randint(0, n - 1)
    while nuevo_tablero[fila] == nueva_columna:
        nueva_columna = random.randint(0, n - 1)
    nuevo_tablero[fila] = nueva_columna
    return nuevo_tablero

# Probabilidad de aceptación en el recocido simulado
def probabilidadAceptacion(delta, temperatura):
    return math.exp(-delta / temperatura) if temperatura > 0 else 0

# Mostrar el tablero en la consola
def mostrarTablero(tablero):
    for i in range(len(tablero)):
        fila = ["."] * len(tablero)
        fila[tablero[i]] = "R"
        print(" ".join(fila))
    print()

# Resolver el problema de las 8 reinas usando recocido simulado
def resolverOchoReinasRecocidoSimulado(n, temperatura_inicial, temperatura_final, tablero_inicial=None):
    if tablero_inicial is None:
        tablero = [random.randint(0, n - 1) for _ in range(n)]
    else:
        tablero = tablero_inicial
    
    print("Estado inicial:")
    mostrarTablero(tablero)
    
    conflictos_actuales = calcularConflictos(tablero)
    temperatura = temperatura_inicial
    iteraciones = 0

    while temperatura > temperatura_final:
        iteraciones += 1

        if conflictos_actuales == 0:
            print(f"Solución encontrada después de {iteraciones} iteraciones.")
            return tablero

        # Generar 4 vecinos y seleccionar el mejor
        mejores_vecinos = [generarVecino(tablero) for _ in range(4)]
        mejor_vecino = min(mejores_vecinos, key=calcularConflictos)
        conflictos_mejor_vecino = calcularConflictos(mejor_vecino)
        delta = conflictos_mejor_vecino - conflictos_actuales
        if delta < 0 or random.random() < probabilidadAceptacion(delta, temperatura):
            tablero = mejor_vecino
            conflictos_actuales = conflictos_mejor_vecino

        temperatura *= random.uniform(0.8, 0.99)  # Disminuir la temperatura de forma aleatoria en el rango establecido

    print(f"No se encontró una solución óptima después de {iteraciones} iteraciones.")
    return tablero  # Devuelve la mejor solución encontrada

# Solicitar al usuario que introduzca los parámetros
n = 8
temp_inicial = float(input("Ingrese la temperatura inicial: "))
temp_final = float(input("Ingrese la temperatura final: "))
entrada_usuario = input(f"Ingrese el estado inicial de las {n} reinas (1-{n}) separadas por comas (o presione Enter para generar aleatoriamente): ")

if entrada_usuario:
    try:
        solucion_inicial = [int(x) - 1 for x in entrada_usuario.split(',')]
        if len(solucion_inicial) != n or any(x < 0 or x >= n for x in solucion_inicial):
            raise ValueError("Entrada no válida")
    except ValueError:
        print("Entrada no válida. Se generará un estado inicial aleatorio.")
        solucion_inicial = None
else:
    solucion_inicial = None

solucion = resolverOchoReinasRecocidoSimulado(n, temp_inicial, temp_final, solucion_inicial)

# Mostrar el tablero resultante
print("Solución final:")
mostrarTablero(solucion)
