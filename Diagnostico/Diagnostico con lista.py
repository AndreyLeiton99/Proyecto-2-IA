from experta import *
from random import choice
import os


# una clase que solicite el nombre, edad y recidencia del paciente y active la clase de sintomas
class Paciente(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="Informacion_paciente")

    @Rule(Fact(action='Informacion_paciente'),
          NOT(Fact(name=W())))
    def ask_name(self):
        self.declare(Fact(name=input("Cuál es su nombre? ")))

    @Rule(Fact(action='Informacion_paciente'),
          NOT(Fact(edad=W())))
    def ask_edad(self):
        self.declare(Fact(edad=input("Cuál es su edad? ")))

    @Rule(Fact(action='Informacion_paciente'),
          NOT(Fact(residencia=W())))
    def ask_residencia(self):
        self.declare(Fact(residencia=input("Cuál es su residencia? ")))

    @Rule(Fact(action='Informacion_paciente'),
          Fact(name=MATCH.name),
          Fact(edad=MATCH.edad),
          Fact(residencia=MATCH.residencia))
    def sintomas(self, name, edad, residencia):
        print("Hola %s! Usted tiene %s años y vive en %s" %
              (name, edad, residencia))
        print("Por favor responda las siguientes preguntas con si o no")
        # llame a la clase sintomas
        engine = Sintomas()
        engine.reset()  # Prepare the engine for the execution.
        engine.run()  # Run it!


# una clase que pregunte por los sintomas y active la clase de diagnostico
class Sintomas(KnowledgeEngine):

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="preguntar_sintomas")

    def preguntar_sintoma(self, sintoma):
        respuesta = input(f"¿Tiene {sintoma}? (si/no): ").lower()
        #respuesta = choice(["si", "no"])  # Respuesta aleatoria
        #print(f"¿Tiene {sintoma}? (si/no): " + respuesta)
        while respuesta not in ["si", "no"]:
            print("Por favor, responda con 'si' o 'no'.")
            respuesta = input(f"¿Tiene {sintoma}? (si/no): ").lower()
        return respuesta == "si"


    @Rule(Fact(action='preguntar_sintomas'))
    def ask_sintomas(self):
        sintomas_ = [
            "congestión nasal", "diarrea", "dolor abdominal", "dolor al orinar", "dolor de cabeza",
            "dolor de garganta", "dolor de oído", "dolores corporales", "enrojecimiento", "estornudos",
            "fiebre", "hinchazón", "lagrimeo", "nauseas", "ojos rojos", "orina con sangre",
            "orinar con mayor frecuencia", "pérdida de audición", "pérdida del gusto y del olfato",
            "picazón", "ronquera", "sensación de presión facial", "tos", "vértigo", "vómitos"
        ]

        # se debe guardar los sintomas en una lista
        sintomas = []
        for sintoma in sintomas_:
            if self.preguntar_sintoma(sintoma):
                sintomas.append(sintoma)

        # Verifica si la lista contiene todos los síntomas necesarios para la bronquitis aguda
        if {"tos", "congestión nasal", "dolor de garganta"}.issubset(sintomas):
            print("Usted podría tener bronquitis aguda")
        else:
            print("Usted no tiene bronquitis aguda")

        # se debe verificar si el paciente tiene resfriado comun
        if {"tos", "congestión nasal", "estornudos", "dolor de garganta", "hinchazón"}.issubset(sintomas):
            print("Usted podria tener resfriado comun")
        else:
            print("Usted no tiene resfriado comun")

        # se debe verificar si el paciente tiene infeccion de oído
        if {"dolor de oído", "pérdida de audición", "fiebre", "vértigo", "nauseas"}.issubset(sintomas):
            print("Usted podria tener infeccion de oído")
        else:
            print("Usted no tiene infeccion de oído")

        # se debe verificar si el paciente tiene gripe
        if {"fiebre", "dolores coporales", "dolor de garganta", "tos", "congestión nasal"}.issubset(sintomas):
            print("Usted podria tener gripe")
        else:
            print("Usted no tiene gripe")

        # se debe verificar si el paciente tiene sinusitis
        if {"dolor de cabeza", "congestión nasal", "sensación de presión facial"}.issubset(sintomas):
            # dolor de cabeza, congestión nasal y presión facial
            print("Usted podria tener sinusitis")

        else:
            print("Usted no tiene sinusitis")

        # se debe verificar si el paciente tiene infecciones en la piel
        if {"enrojecimiento", "hinchazón", "picazón"}.issubset(sintomas):
            print("Usted podria tener infecciones en la piel")
        else:
            print("Usted no tiene infecciones en la piel")

        # se debe verificar si el paciente tiene infeccion de garganta
        if {"dolor de garganta", "ronquera", "picazón", "hinchazón"}.issubset(sintomas):
            print("Usted podria tener infeccion de garganta")
        else:
            print("Usted no tiene infeccion de garganta")

        # se debe verificar si el paciente tiene infeccion de urinaria
        if {"dolor al orinar", "orina con sangre", "orinar con mayor frecuencia"}.issubset(sintomas):
            print("Usted podria tener infeccion de urinaria")

        else:
            print("Usted no tiene infeccion de urinaria")

        # se debe verificar si el paciente tiene infeccion de ojos
        if {"ojos rojos", "picazón", "lagrimeo"}.issubset(sintomas):
            print("Usted podria tener infeccion de ojos")

        else:
            print("Usted no tiene infeccion de ojos")

        # se debe verificar si el paciente tiene coronavirus
        if {"fiebre", "tos", "dolor de garganta", "congestión nasal", "dolor de cabeza", "pérdida del gusto y del olfato"}.issubset(sintomas):
            print("Usted podria tener coronavirus")
        else:
            print("Usted no tiene coronavirus")

        # 11 Malestar estomacal tiene los sintomas de nauseas, vómitos, diarrea y dolor abdominal
        if {"nauseas", "vómitos", "diarrea", "dolor abdominal"}.issubset(sintomas):
            print("Usted podria tener malestar estomacal")
        else:
            print("Usted no tiene malestar estomacal")

        # se debe verificar si el paciente esta sano
        if sintomas == []:
            print("Usted esta sano")
            print("Gracias por usar el sistema de diagnostico de enfermedades")
            exit()
        else:
            print("Usted no tiene una enferemedad conocida para el sistema")
            print(
                "Por favor dirijase a un centro de salud para ser diagnosticado por un medico")
            exit()




engine = Paciente()
engine.reset()  # Prepare the engine for the execution.
os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
engine.run()  # Run it!

