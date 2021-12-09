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
import tabless


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
            controller.load(analyzer,'routes-utf8-small.csv')
            print(gr.numVertices(analyzer['CompleteAirports']))

        elif int(inputs[0]) == 2:
            print('========== Req No. 1 Inputs ========== \n')
            print('Most connected airports in network (TOP 5)')
            print('Number of airports in network: '+ str(gr.numVertices(analyzer['CompleteAirports']))+'\n')
            rta = model.Requerimiento1(analyzer)
            print('========== Req No. 1 Answer ========== \n')
            print('Connected airports inside network: '+str(lt.size(rta)))
            print('Top 5 most connected airports... \n')
            print(tabless.createTable(rta))

        elif int(inputs[0]) == 3:
            Cod1    =   input("Digite el código IATA del aeropuerto 1: ")
            Cod2    =   input("Digite el código IATA del aeropuerto 2: ")
            print('========== Req No. 2 Inputs ========== \n')
            print('Airport-1 IATA Code: ' + Cod1)
            print('Airport-2 IATA Code: ' + Cod2 +'\n')
            rta     =   controller.req2(analyzer,Cod1,Cod2)
            print('========== Req No. 2 Answer ========== \n')
            print('+++ Airport1 IATA Code: '+ Cod1+ ' +++')
            print(tabless.infoTable(rta[1]))
            print('+++ Airport2 IATA Code: '+ Cod2+ ' +++')
            print(tabless.infoTable(rta[2]))
            

        elif int(inputs[0]) == 4:

            ciudadOrigen=input("Inserte el nombre de la ciudad de origen: ").strip()
            list_cities = model.selectCity(analyzer,ciudadOrigen)
            pos = int(input("Seleccione a la ciudad específica: "))
            infOrigin = model.infoCity(list_cities,pos)
            list_airports = model.showAirports(list_cities,pos)
            pos = int(input("Seleccione el aeropuerto de salida: "))
            aerSalida = model.selectAirport(list_airports,pos)
            

            ciudadDestino=input("Inserte el nombre de la ciudad de destino: ").strip()
            list_cities = model.selectCity(analyzer,ciudadDestino)
            pos = int(input("Seleccione a la ciudad específica: "))
            infDest = model.infoCity(list_cities,pos)
            list_airports = model.showAirports(list_cities,pos)
            pos = int(input("Seleccione el aeropuerto de destino: "))
            aerDestino = model.selectAirport(list_airports,pos)

            print("vamos de {} para {}".format(aerSalida,aerDestino))
            print( "+++ The departure airport in St. Petersburg is: ")
            print(tabless.infoTable(rta[0]))
            print("The arrival airport in Lisbon is: ")
            print(tabless.infoTable(rta[1]))

            rta=model.Requerimiento3(analyzer,aerSalida,aerDestino,infOrigin,infDest)
            print(tabless.tripTable(rta[2]))
            print("\nTrip stops")
            print(tabless.tableStops(rta[2],analyzer))

            print("Distancia total de viaje: "+str(rta[3]))


        elif int(inputs[0]) == 5:
            ciudadOrigen=input("Inserte el nombre de la ciudad de origen: ")
            list_cities = model.selectCity(analyzer,ciudadOrigen)
            pos = int(input("Seleccione a la ciudad específica: "))
            ciudadOrigen = model.infoCity(list_cities,pos)
            cantidadMillas=float(input("Inserte la cantidad de millas disponibles: "))

            rta=controller.req4(analyzer,cantidadMillas,ciudadOrigen)

            print(tabless.infoTable(rta[1]))
            print(tabless.tripTable(rta[0]))
            
            # print(rta)


        elif int(inputs[0]) == 6:
            codigoIATA=input("Ingrese el codigo IATA del aeropuerto de funcionamiento: ")
            
            rta=controller.req5(analyzer,codigoIATA)
            print(tabless.FirstLast3Table(rta,analyzer))


        elif int(inputs[0]) == 7:
            ciudadOrigen=input("Inserte el nombre de la ciudad de origen: ")
            ciudadDestino=input("Inserte el nombre de la ciudad de destino: ")
            rta = controller.bono(ciudadOrigen,ciudadDestino)

        elif int(inputs[0]) == 8:
            # print(analyzer['CitiesRoutes'])
            # print(model.Requerimiento3(analyzer,'Krasnodar--45.0333--38.9833','Yerevan--40.1814--44.5144'))
            # model.prueba(analyzer)
            # print(gr.numEdges(analyzer['CitiesRoutes']))
            # print(model.Requerimiento5(analyzer,'DXB'))
            print(model.Requerimiento4(analyzer,1890,'LIS'))

        else:
            sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 30)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
