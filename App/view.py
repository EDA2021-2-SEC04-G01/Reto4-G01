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

            firstAirport = lt.firstElement(analyzer['loadedAirports'])
            lastAirport = lt.lastElement(analyzer['loadedAirports'])
            firtslastAirport = lt.newList(datastructure='SINGLE_LINKED',cmpfunction=None)
            lt.addLast(firtslastAirport,firstAirport)
            lt.addLast(firtslastAirport,lastAirport)
            analyzer['loadedAirports']=None
            
            firstCity = lt.firstElement(analyzer['loadedCities'])
            lastCity = lt.lastElement(analyzer['loadedCities'])
            firtslastCity = lt.newList(datastructure='SINGLE_LINKED',cmpfunction=None)
            lt.addLast(firtslastCity,firstCity)
            lt.addLast(firtslastCity,lastCity)
            analyzer['loadedCities']=None
            

            print("=== Airports-Routes Digraph ===")
            print('Nodes: '+str(gr.numVertices(analyzer['CompleteAirports'])))
            print('Edge: '+str(gr.numEdges(analyzer['CompleteAirports'])))
            print('First & Last Airport loaded in the Digraph.')
            print(tabless.FirstLastTable(firtslastAirport,analyzer))
            print("=== Airports-Routes Graph ===")
            print('Nodes: '+str(gr.numVertices(analyzer['FullRoutes'])))
            print('Edge: '+str(gr.numEdges(analyzer['FullRoutes'])))            
            print('First & Last Airport loaded in the Digraph.')
            print(tabless.FirstLastTable(firtslastAirport,analyzer))
            print('=== City Network ===')
            print('The number of the cities are: '+str(m.size(analyzer['citiesUser'])))
            print('First & Last Airport loaded in the data structure')
            print(tabless.FirstLastCity(firtslastCity,analyzer))

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
            airport = model.showAirports(list_cities,pos)
            pos = int(input("Seleccione el aeropuerto de salida: "))
            aerSalida = model.selectAirport(airport,pos)
            

            ciudadDestino=input("Inserte el nombre de la ciudad de destino: ").strip()
            list_cities = model.selectCity(analyzer,ciudadDestino)
            pos = int(input("Seleccione a la ciudad específica: "))
            infDest = model.infoCity(list_cities,pos)
            airport = model.showAirports(list_cities,pos)
            pos = int(input("Seleccione el aeropuerto de destino: "))
            aerDestino = model.selectAirport(airport,pos)

            rta=model.Requerimiento3(analyzer,aerSalida,aerDestino,infOrigin,infDest)
            print("vamos de {} para {}".format(aerSalida,aerDestino))
            print( "+++ The departure airport in {} is: ".format(ciudadOrigen))
            print(tabless.infoTable(rta[0]))
            print("The arrival airport in {} is: ".format(ciudadDestino))
            print(tabless.infoTable(rta[1]))

            
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

            airport = (lt.firstElement(ciudadOrigen['airports']))['IATA']

            print('=============== Req No. 4 Inputs ===============')
            print('Departure IATA code: '+str(airport))
            print('Avilable Travel Miles: '+str(cantidadMillas))
            rta=controller.req4(analyzer,cantidadMillas,ciudadOrigen)
            print('=============== Req no. 5 Answer ===============')
            print('+++ Departure Airport for IATA Code: '+str(airport)+' +++\n')

            print(tabless.infoTable(rta[1]))
            print("- Number of possible airports: "+str(rta[2])+".")
            print("- Traveling distance sum between aiports: "+str(rta[3])+" (km).")
            print("- Passenger available traveling miles: "+str(round(cantidadMillas*1.6,2))+" (km).\n")
            print("+++ Longest possible route with airport "+ str(airport)+" +++")
            print("- Longests possible path distance: "+str(rta[4])+" (km)")
            print("- Longests possible path details: ")
            print(tabless.tripTable(rta[0]))
            print("-------")
            print("The passenger needs "+str(rta[5])+" miles to complete the trip.")
            print("-------")
            


        elif int(inputs[0]) == 6:
            codigoIATA=input("Ingrese el codigo IATA del aeropuerto de funcionamiento: ")
            rta=controller.req5(analyzer,codigoIATA)
            print('=============== Req No. 5 Inputs ===============')
            print('closing the airport with IATA code: '+str(codigoIATA))
            print('--- Airports-Routes DiGraph ---')
            print('Original number of Airports: '+ str(gr.numVertices(analyzer['CompleteAirports']))+' and Routes: '+str(rta[1]))
            print('--- Airports-Routes Grapf ---')
            print('Original number of Airports: '+ str(gr.numVertices(analyzer['FullRoutes']))+' and Routes: '+str(rta[2])+'\n')
            print('+++ Remocing Airport with IATA: '+str(codigoIATA)+' +++ \n')
            print('--- Airports-Routes DiGraph ---')
            print('Original number of Airports: '+ str(gr.numVertices(analyzer['CompleteAirports']))+' and Routes: '+str(rta[3]))
            print('--- Airports-Routes Grapf ---')
            print('Original number of Airports: '+ str(gr.numVertices(analyzer['FullRoutes']))+' and Routes: '+ str(rta[4])+'\n')
            print('=============== Req no. 5 Answer ===============')
                       
            print(tabless.FirstLast3Table(rta[0],analyzer))


        elif int(inputs[0]) == 7:
            ciudadOrigen=input("Inserte el nombre de la ciudad de origen: ")
            ciudadDestino=input("Inserte el nombre de la ciudad de destino: ")
            rta = controller.bono(ciudadOrigen,ciudadDestino)


        else:
            sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 30)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
