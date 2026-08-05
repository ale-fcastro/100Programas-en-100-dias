# Día 6 — Contador de palabras / analizador de texto
# Lee un string largo (puede ser pegado o desde archivo),
# cuenta palabras, palabra más repetida, promedio de longitud.
# Primer contacto real con diccionarios como contadores (dict.get o Counter).

# input
    # - Archivo Referenciado a la carpeta ../Archivos_a_leer/*
    # - Texto en Linea (Consola) la misma ya tiene la propiedad de permitir pegar codigo
# Ouput: TextResultAnalyce: class
    # - Total de palablar en el texto o archivo: total_p_text: int
    # - Palabras mas repetidas: p_more_repeat: {}
    # - Promedio de Longitud longitudes totales entre los textos ej: pepe 4 va 2 a 1 comprar 7 = 14 / total_p_text, numerador_del_promedio: int

# composicion:
    # 3 clases: ConsoleUI interfaz en consola, TextResultAnalyce Objeto de resultado, TextProcesor backen para procesar la data, extra: ( LectorArchHelper metodo o clase, sin definir )
    # input ----> procesamiento ----> respuesta
    # 1 sola intervencion humana el resto computado
    # Uso de comportamiento standar de python with() metod .open() selfmetod to with 
    # misma logica una vez octenido el texto 


import os
import re
import enum

class StatusMachine(enum):
    Pendiente = "Pendiente"
    Iniciado = "Iniciando"
    InProgres = "En proceso"
    Completado = "Completado"
    Cancelado = "Canselado"
    Error = "Error"

class ConsoleUi:
    def __init__(self):
        self.processor = TextProcesor()

    def menu(self):
        while True:
            print("""
        ========================================
            ANALIZADOR DE TEXTO
        ========================================

        1) Analizar texto pegado
        2) Analizar archivo
        ENTER) Salir
        """)

            opcion = input("Seleccione una opción: ")

            if opcion == "":
                break

            match opcion:
                case "1":
                    self.text_mode()
                case "2":
                    self.archive_mode()
                case _:
                    print("\nOpción inválida.\n")

    def text_mode(self):
        print("\nPegue el texto a analizar.\n")
        texto = input("> ")

        result = self.processor.get_entry_user(False, texto)

        if not result[0]:
            print(result[1])
            return

        self.processor.processor()
        self.show_result()

    def archive_mode(self):
        print("\nArchivos disponibles en ../Archivos_a_leer/")
        nombre = input("Nombre del archivo (sin .txt): ")

        result = self.processor.get_entry_user(True, nombre)

        if not result[0]:
            print(result[1])
            return

        self.processor.processor()
        self.show_result()

    def show_result(self):
        r = self.processor.text_result_analyce

        print("\n========================================")
        print("RESULTADO DEL ANÁLISIS")
        print("========================================")

        print(f"Total de palabras : {r.total_p_text}")
        print(f"Promedio longitud : {r.promedio_result:.2f}")

        print("\nFrecuencia de palabras\n")

        for palabra, cantidad in sorted(
            r.p_more_repeat.items(),
            key=lambda item: item[1],
            reverse=True
        ):
            print(f"{palabra:<20} {cantidad}")

        print("========================================\n")

class TextProcesor:
    def __init__(self):
        self.text: str = ""
        self.text_result_analyce: TextResultAnalyce = TextResultAnalyce()
        self.status_machine: StatusMachine = StatusMachine.Pendiente

    def get_entry_user(self, is_archive: bool, entry: str = ""):
        self.status_machine = StatusMachine.Iniciado
        if is_archive:
            result = self.text_by_archive_proccesor(entry)
            if self.status_machine == StatusMachine.Error:
                return [False, result]
            
            self.status_machine = StatusMachine.InProgres
            self.text = result
            return [True, "Todo bien"]
        else:
            try: 
                convert = str(entry)
                self.status_machine = StatusMachine.InProgres
                self.text = convert
                return [True, "Todo bien"]
            except ValueError:
                self.status_machine = StatusMachine.Error
                return [False, "Tipo de dato invalido"]

    def processor(self):
        if self.status_machine == StatusMachine.Error:
            return [False, "No se puede procesar datos con errores"]
        
        self.clean_text_full()

        self.text_result_analyce.total_p_text = len(self.text.split())

        for i in self.text.split():
            self.text_result_analyce.p_more_repeat[i] = self.text_result_analyce.p_more_repeat.get(i, 0) + 1

        texto_sin_espacios = self.text.replace(" ", "")
        self.text_result_analyce.numerador_del_promedio = len(texto_sin_espacios)

        self.text_result_analyce.promedio_result = self.text_result_analyce.numerador_del_promedio / self.text_result_analyce.total_p_text
        self.status_machine = StatusMachine.Completado

    # ZONA HELPERS
    def text_by_archive_proccesor(self, archive_name: str):
        result = ""
        try:
            with open(self.get_absolute_route(archive_name), 'r', encoding="utf-8") as archivo:
                result = archivo.read()
            
            self.status_machine = StatusMachine.Completado
            return result
        except FileNotFoundError:
            self.status_machine = StatusMachine.Error
            return "No se encontro el arvhivo en la ruta corespondiente"
        except PermissionError:
            self.status_machine = StatusMachine.Error
            return "No tienes permisos suficientes para leeer este archivo"
        except Exception as e:
            self.status_machine = StatusMachine.Error
            return f"A ocurido un error inesperado: {e}"        

    def get_absolute_route(self, archive_name):
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        absolute = os.path.join(carpeta_actual, "..", "Archivos_a_leer", f"{archive_name}.txt")
        return absolute

    def clean_text_full(self):
        self.text = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', '', self.text)

class TextResultAnalyce:
    def __init__(self):
        self.total_p_text: int = 0
        self.p_more_repeat = {}
        self.numerador_del_promedio: int = 0
        self.promedio_result: int = 0

def main():
    consola = ConsoleUi()
    consola.menu()

main()

# zona de test para documentar avanze

# primer error probando txtbyarchivproccesor
    # test = TextProcesor()

    # test.text_by_archive_proccesor('test_txt_archive')

    # print(test.text)

    # Exception has occurred: FileNotFoundError
    # [Errno 2] No such file or directory: '../Archivos_a_leer/test_txt_arvhive.txt'
    # File "/home/fcastrodev/Learning/Programacion/100Programas-en-100-dias/first-ten-days/006-day.py", line 34, in text_by_archive_proccesor
    #     with open(f"../Archivos_a_leer/{archive_name}.txt", 'r', encoding="utf-8") as archivo:
    #         ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # File "/home/fcastrodev/Learning/Programacion/100Programas-en-100-dias/first-ten-days/006-day.py", line 50, in <module>
    #     test.text_by_archive_proccesor('test_txt_arvhive')
    #     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
    # FileNotFoundError: [Errno 2] No such file or directory: '../Archivos_a_leer/test_txt_arvhive.txt'
    # PROBLEMAS CON LA RUTA DEVIDO A QUE NO ARRANCA DESDE DONDE SE ENCUENTRA ESTE ARVHIVO ASI QUE TENEMOS QUE OCTENER LA RUTA RELATIVA O ABSOLUTA USAREMOS OS PARA ESTO