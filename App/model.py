"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """
from sys import call_tracing
import folium as f
from datetime import datetime
from App.controller import load
from DISClib.Algorithms.Graphs.bellmanford import BellmanFord, hasPathTo, pathTo
from DISClib.DataStructures.arraylist import compareElements
from DISClib.DataStructures.chaininghashtable import contains
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config
import math as mt
from math import inf
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
#Meta: 180 o menos, máximo y siendo amable, 200
def newAnalyzer():
    analyzer = {
        'CompleteAirports':gr.newGraph(datastructure='ADJ_LIST',directed=True,size=14000, comparefunction=compareDistances),
        'FullRoutes':gr.newGraph(datastructure='ADJ_LIST',directed=False, size = 14000, comparefunction=compareDistances),
        'CitiesRoutes':gr.newGraph(datastructure='ADJ_LIST',directed=True, size = 14000, comparefunction=compareDistances),
        'cities':m.newMap(numelements=200,maptype='CHAINING',loadfactor=0.7),
        'airports':m.newMap(numelements=800,maptype='CHAINING',loadfactor=0.7),
        'citiesUser':m.newMap(numelements=500,maptype='CHAINING',loadfactor=0.7)
    }
    return analyzer


# Funciones utilizadas para comparar elementos dentro de una lista
def compareDistances(value,keyairport):
    airport = keyairport['key']
    if airport==value:
        return 0
    elif airport>value:
        return 1
    else: return -1

    
def addVertex(analyzer,airportId,graphName):
    try:
        if not gr.containsVertex(analyzer[graphName],airportId):
            gr.insertVertex(analyzer[graphName],airportId)
            return analyzer
    except Exception as exp:
        error.reraise(exp,'model:addVertex')

def addConnection(analyzer, origin, destination, distance,graphName):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer[graphName], origin, destination)
    if edge is None:
        gr.addEdge(analyzer[graphName], origin, destination, distance)
    return analyzer

def addCity(analyzer,city):

    mapcity = analyzer['cities']
    cityName = city['city_ascii']   

    lat = city['lat']
    infoCity = cityName+str(city['lat'])+str(city['lng'])

    if m.contains(analyzer['citiesUser'],cityName):
        list_cities = m.get(analyzer['citiesUser'],cityName)['value']
    else:
        list_cities=lt.newList(datastructure='ARRAY_LIST',cmpfunction=None)

    lt.addLast(list_cities,city)
    m.put(analyzer['citiesUser'],cityName,list_cities)
    

def addAirport(analyzer,airport):
    mapAirports = analyzer['airports']
    airportCode = airport['IATA']
    m.put(mapAirports,airportCode,airport)

    if m.contains(analyzer['citiesUser'],airport['City']):
        citiesList =m.get(analyzer['citiesUser'],airport['City'])['value']

    else:
        citiesList=lt.newList(datastructure='ARRAY_LIST',cmpfunction=None)
        city = {'city_ascii':airport['City'],'lat':airport['Latitude'],'lng':airport['Longitude']}
        lt.addLast(citiesList,city)
        m.put(analyzer['citiesUser'],airport['City'],citiesList)
        m.put(analyzer['cities'],airport['City'],city)

    dist_menor = inf
    for city in lt.iterator(citiesList):
        distancia = calc_distancia(airport,city)
        if distancia<dist_menor:
            actual_city = city
            dist_menor = distancia

    key = actual_city['city_ascii']+str(actual_city['lat'])+str(actual_city['lng'])
    m.put(analyzer['cities'],key,actual_city)
    

def clusters(analyzer, IATA1,IATA2):
    a = scc.KosarajuSCC(analyzer['CompleteAirports'])
    return (scc.stronglyConnected(a,IATA1,IATA2))


#↓↓Aquí comienza el req3↓↓
def Requerimiento3(analyzer,cityDep,cityDest):
    simplegraph=djk.Dijkstra(analyzer['CitiesRoutes'],cityDep)
    BellmanFord(simplegraph,cityDep)

    return None


def addMissingStuff(analyzer,city_departure,ruta_departure):
###↓↓Esto es para añadir ciudades con recorridos↓↓
    if m.contains(analyzer['citiesUser'],city_departure):
        citiesList =m.get(analyzer['citiesUser'],city_departure)['value']

    else:
        citiesList=lt.newList(datastructure='ARRAY_LIST',cmpfunction=None)
        city = {'city_ascii':ruta_departure['City'],'lat':ruta_departure['Latitude'],'lng':ruta_departure['Longitude']}
        lt.addLast(citiesList,city)
        m.put(analyzer['citiesUser'],ruta_departure['City'],citiesList)
        key = city['city_ascii']+'--'+str(city['lat'])+'--'+str(city['lng'])
        m.put(analyzer['cities'],key,city)

    dist_menor = inf
    for city in lt.iterator(citiesList):
        distancia = calc_distancia(ruta_departure,city)
        if distancia<dist_menor:
            actual_city = city
            dist_menor = distancia

    key = actual_city['city_ascii']+'--'+str(actual_city['lat'])+'--'+str(actual_city['lng'])
    m.put(analyzer['cities'],key,actual_city)
    return (key,actual_city)

def addData(route,analyzer):

    ruta_departure = m.get(analyzer['airports'],route['Departure'])['value']
    city_destination = m.get(analyzer['airports'],route['Destination'])['value']['City']
    city_departure = m.get(analyzer['airports'],route['Departure'])['value']['City']
    ruta_destination = m.get(analyzer['airports'],route['Destination'])['value']
    

###↑↑Termina lo de arriba ↑↑

    city_departure=addMissingStuff(analyzer,city_departure,ruta_departure)

    city_destination=addMissingStuff(analyzer,city_destination,ruta_destination)

    cityDep = city_departure[1]
    cityDest = city_destination[1]

    city_departure=city_departure[0]

    city_destination=city_destination[0]

    distcities=dist_cities(cityDep,cityDest)

    addVertex(analyzer,city_departure,'CitiesRoutes')
    addVertex(analyzer,city_destination,'CitiesRoutes')

    addVertex(analyzer,route['Departure'],'CompleteAirports')
    addVertex(analyzer,route['Destination'],'CompleteAirports')

    addVertex(analyzer,route['Departure'],'FullRoutes')
    addVertex(analyzer,route['Destination'],'FullRoutes')

    addConnection(analyzer,city_destination,city_departure,distcities,'CitiesRoutes')
    addConnection(analyzer,route['Departure'],route['Destination'],float(route['distance_km']),'CompleteAirports')
    addConnection(analyzer,route['Departure'],route['Destination'],float(route['distance_km']),'FullRoutes')


def calc_distancia(airport,city):

    r=6371
    lat1=float(airport['Latitude'])
    lat2 = float(city['lat'])
    long1=float(airport['Longitude'])
    long2=float(city['lng'])
    a = (mt.sin((lat2-lat1)/2)**2)+mt.cos(lat1)*mt.cos(lat2)*(mt.sin((long2-long1/2))**2)
    c=2*mt.atan2(mt.sqrt(a),mt.sqrt(1-a))
    d= r*c
    return d
def dist_cities(city1,city2):
    r=6371
    lat1=float(city1['lat'])
    lat2 = float(city2['lat'])
    long1=float(city1['lng'])
    long2=float(city2['lng'])
    a = (mt.sin((lat2-lat1)/2)**2)+mt.cos(lat1)*mt.cos(lat2)*(mt.sin((long2-long1/2))**2)
    c=2*mt.atan2(mt.sqrt(a),mt.sqrt(1-a))
    d= r*c
    return d
# Funciones de ordenamiento
