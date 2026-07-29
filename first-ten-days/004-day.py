# okay la micion es un juego
# dos jugadores
# humano vs maquina
# reglas: 9 convinacioes 3 * 3 cada 1 opcion = a 3 convinaciones y son 3 opciones "matriz"
    # Piedra vence a Tijera
    # Tijera vence a Papel
    # Papel vence a Piedra

# unit_steate_by_ronda cada usuario tiene un stado y cada ronda tiene un stado doble 
    # ganado
    # perdido
    # empate

# pienso en jugador , partida, gamehelper, y talvez polimorfismo de el jugador pensandolo como computadora jugador

class Jugador:
    def __init__(self, nombre, )