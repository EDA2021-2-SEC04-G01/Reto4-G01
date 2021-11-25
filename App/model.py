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
import folium as f
from datetime import datetime
from App.controller import load
from DISClib.DataStructures.arraylist import compareElements
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

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
        'airports':m.newMap(numelements=800,maptype='CHAINING',loadfactor=0.7)
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
    m.put(mapcity,cityName,city)

def addAirport(analyzer,airport):
    mapAirports = analyzer['airports']
    airportCode = airport['IATA']
    m.put(mapAirports,airportCode,airport)


def addData(route,analyzer):
    city_departure = m.get(analyzer['airports'],route['Departure'])['key']
    city_destination = m.get(analyzer['airports'],route['Destination'])['key']


    addVertex(analyzer,city_departure,'CitiesRoutes')
    addVertex(analyzer,city_destination,'CitiesRoutes')

    addVertex(analyzer,route['Departure'],'CompleteAirports')
    addVertex(analyzer,route['Destination'],'CompleteAirports')

    addVertex(analyzer,route['Departure'],'FullRoutes')
    addVertex(analyzer,route['Destination'],'FullRoutes')

    addConnection(analyzer,city_destination,city_departure,0,'CitiesRoutes')
    addConnection(analyzer,route['Departure'],route['Destination'],route['distance_km'],'CompleteAirports')
    addConnection(analyzer,route['Departure'],route['Destination'],route['distance_km'],'FullRoutes')


# Funciones de ordenamiento
