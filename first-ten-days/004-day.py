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
            # 0: piedra - 1: papel - 2: tijera
            # 0: Derrota - 1: Victoria
# pienso en jugador , partida, gamehelper, y talvez polimorfismo de el jugador pensandolo como computadora jugador

import random

class Jugador:
    def __init__(self):
        self.nombre = None
        self.mano: int = None
        self.victorias: int = 0

    def jugar(self, select):
        self.mano = select
    
    def quien_soy(self, entry):
        self.nombre = entry

class IA(Jugador):
    def __init__(self):
        super().__init__()
        self.quien_soy("playi")

    def jugar(self):
        self.mano = random.choice((0,1,2))

class Round:
    def __init__(self, player_one: Jugador, player_too: Jugador):
        self.winner: Jugador = None
        self.player_one = player_one
        self.player_too = player_too
      
class GameHelper:
    def __init__(self, run: bool):
        self.run: bool = run
        self.rounds: list[Round] = []
        self.empates: int = 0

    def definir_ganador(self, round: Round):
        opt = {
            0: { 
                1: 0, 
                2: 1 
            },
            1: { 
                2: 0, 
                0: 1 
            },
            2: { 
                0: 0, 
                1: 1 
            }
        }
        if round.player_one.mano == round.player_too.mano:
            self.empates += 1
        else:
            round.winner = round.player_one if opt[round.player_one.mano][round.player_too.mano] == 1 else round.player_too
            round.winner.victorias += 1
            
class ValidatorHelper:

    def __init__(self):
        pass

    # 0: piedra - 1: papel - 2: tijera 
    def validate_entry(self, entry):
        return entry in (0,1,2)

class ConsoleShowHelper:
    def __init__(self):
        self.ActualRound: Round = None

    def mano_to_string(self, mano):
        opciones = {
            0: "Piedra",
            1: "Papel",
            2: "Tijera"
        }

        return opciones[mano]

    def bienvenida(self):
        print("""
        ==========================================================
                PIEDRA - PAPEL - TIJERA
        ==========================================================

                Humano VS Playi

        Primero en conseguir más victorias gana.

        Opciones:
            0 -> Piedra
            1 -> Papel
            2 -> Tijera

        ==========================================================
        """)
    
    def solicitar_datos(self):
        print("""
        ---------------- NUEVA RONDA ----------------

        Precione "Enter" si desea volver \n o ingrese su eleccion a jugar:
        """)

    def confirmacion_de_datos(self):
        print(f"""
            Jugador : {self.ActualRound.player_one.nombre}
            Playi   : {self.ActualRound.player_too.nombre}

            Jugador eligió : {self.mano_to_string(self.ActualRound.player_one.mano)}
            Playi eligió   : {self.mano_to_string(self.ActualRound.player_too.mano)}
        """)
    
    def show_result(self):
        print("\n--------------- RESULTADO ----------------")

        if self.ActualRound.winner is None:
            print("Empate")
        else:
            print(f"Victoria para: {self.ActualRound.winner.nombre}")

        print("------------------------------------------\n")
    
    def show_round_nunber(self, entry: int):
        print("Ronda: " , entry)

# que empiece el juego
def main():
    # definimos integrantes de la estrucutructura
    # juego
    game = GameHelper(True)

    # jugadores
    jugador1 = Jugador()
    jugador2 = IA()

    # helpers
    validator_helper = ValidatorHelper()
    console_show_helper = ConsoleShowHelper()

    while game.run:

        varible_de_conprobacion = len(game.rounds)

        if len(game.rounds) <= 0:
            console_show_helper.bienvenida()
            print("\nsi decea salir precione 'enter'")
            jugador1.quien_soy(input("\n Name: "))
            if jugador1.nombre == "":
                game.run = False
                continue
            ronda = Round(jugador1, jugador2)
            console_show_helper.ActualRound = ronda
            game.rounds.append(round)
            continue
        else:
            console_show_helper.solicitar_datos()
            entry = input()
            if entry == '':
                game.rounds.clear()
                continue
            jugador1.jugar(int(entry))
            jugador2.jugar()

        if not validator_helper.validate_entry(jugador1.mano):
            print("Error de entrada Retry.... \n")
            continue

        console_show_helper.confirmacion_de_datos()

        game.definir_ganador(ronda)

        console_show_helper.show_round_nunber(len(game.rounds))

        console_show_helper.show_result()

        if input("si desea salir al menu principal precione 'enter' en caso de querere continuar escriba si: ") == "si":
            continue
        else:
            game.rounds.clear()

# CERTIFICADO POR FCASTRO
main()