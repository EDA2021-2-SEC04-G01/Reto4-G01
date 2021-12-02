"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
import folium
from DISClib.ADT import list as lt
assert cf
from DISClib.DataStructures import graphstructure as gr
import threading
import model
from DISClib.DataStructures import mapstructure as m


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido! :D")
    print("1- Cargar información en el catálogo.")
    print("2- Encontrar puntos de interconexión aérea.")
    print("3- Encontrar clústeres de tráfico aéreo.")
    print("4- Encontrar la ruta más corta entre ciudades.")
    print("5- Utilizar las millas de viajero.")
    print("6- Cuantificar el efecto de un aeropuerto cerrado.")
    print("7- Comparar con servicio WEB externo.")
    print("0- Salir")
analyzer = controller.init()

"""
Menu principal
"""



def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            print("Cargando información de los archivos ....")
            controller.load(analyzer,'routes_medium.csv')

        elif int(inputs[0]) == 2:
            rta = controller.req1()


        elif int(inputs[0]) == 3:
            Cod1    =   input("Digite el código IATA del aeropuerto 1: ")
            Cod2    =   input("Digite el código IATA del aeropuerto 2: ")
            rta     =   controller.req2(analyzer,Cod1,Cod2)
            if rta:     print("Efectivamente mi querido watsom :3")
            else:       print("No están en el mismo clúster")

        elif int(inputs[0]) == 4:
            ciudadOrigen=input("Inserte el nombre de la ciudad de origen: ")
            ciudadDestino=input("Inserte el nombre de la ciudad de destino: ")
            rta=controller.req3(ciudadOrigen,ciudadDestino)
            print(rta)


        elif int(inputs[0]) == 5:
            ciudadOrigen=input("Inserte el nombre de la ciudad de origen: ")
            cantidadMillas=input("Inserte la cantidad de millas disponibles: ")
            rta=controller.req4(ciudadOrigen,cantidadMillas)
            print(rta)


        elif int(inputs[0]) == 6:
            codigoIATA=input("Ingrese el codigo IATA del aeropuerto de funcionamiento: ")
            rta=controller.req5(codigoIATA)
            print(rta)


        elif int(inputs[0]) == 7:
            ciudadOrigen=input("Inserte el nombre de la ciudad de origen: ")
            ciudadDestino=input("Inserte el nombre de la ciudad de destino: ")
            rta = controller.bono(ciudadOrigen,ciudadDestino)

        elif int(inputs[0]) == 8:
            # print(analyzer['CitiesRoutes'])
            print(model.Requerimiento3(analyzer,'Krasnodar--45.0333--38.9833','Yerevan--40.1814--44.5144'))
            # model.prueba(analyzer)
            # print(gr.numEdges(analyzer['CitiesRoutes']))
            


        else:
            sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 30)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
