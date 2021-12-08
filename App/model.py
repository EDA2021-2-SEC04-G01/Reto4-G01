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
from sys import call_tracing, maxsize
import folium as f
from datetime import datetime
from App.controller import load
from DISClib.Algorithms.Graphs.bellmanford import BellmanFord, hasPathTo, initSearch, pathTo
from DISClib.Algorithms.Graphs.bfs import BreadhtFisrtSearch, bfsVertex
from DISClib.Algorithms.Graphs.cycles import dfs
from DISClib.Algorithms.Graphs.dfo import DepthFirstOrder, dfsVertex
from DISClib.Algorithms.Graphs.dfs import DepthFirstSearch
from DISClib.Algorithms.Graphs.dfs import pathTo as dfsPathTo
from DISClib.Algorithms.Graphs.prim import PrimMST, edgesMST, prim, scan
from DISClib.DataStructures.arraylist import compareElements
from DISClib.DataStructures.chaininghashtable import contains
from DISClib.DataStructures.edge import weight
import config
from DISClib.ADT.graph import adjacentEdges, adjacents, getEdge, gr, vertices
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk

from DISClib.Utils import error as error
from DISClib.Algorithms.Sorting import shellsort as sa
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
        'CompleteAirports':gr.newGraph(datastructure='ADJ_LIST',directed=True,size=5000, comparefunction=compareDistances),
        'FullRoutes':gr.newGraph(datastructure='ADJ_LIST',directed=False, size = 5000, comparefunction=compareDistances),
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

def cmpAirportdistance(airport1,airport2):
    return airport1['distanceToCity']>airport2['distanceToCity']

def sortAirports(listAirports):
    return sa.sort(listAirports,cmpAirportdistance)

#Carga de data
#++--------------------------------------------------------------------------------------------------------------------------++
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

    cityName = city['city_ascii']   

    if m.contains(analyzer['citiesUser'],cityName):
        list_cities = m.get(analyzer['citiesUser'],cityName)['value']
    else:
        list_cities=lt.newList(datastructure='ARRAY_LIST',cmpfunction=None)

    city['airports']=lt.newList(datastructure='ARRAY_LIST',cmpfunction=None)
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
        city = {'city_ascii':airport['City'],'lat':airport['Latitude'],'lng':airport['Longitude'],'airports':lt.newList(datastructure='ARRAY_LIST',cmpfunction=None)}
        lt.addLast(citiesList,city)
        m.put(analyzer['citiesUser'],airport['City'],citiesList)
    dist_menor = inf
    pos = 0
    for city in lt.iterator(citiesList):
        distancia = calc_distancia(airport,city)
        if distancia<dist_menor:
            actual_city = city
            dist_menor = distancia
            pos_minor=pos
        pos+=1

    airport['distanceToCity']=calc_distancia(airport,actual_city)
    Newcity= lt.getElement(citiesList,pos_minor)
    lt.addLast(Newcity['airports'],airport)
    sortAirports(Newcity['airports'])

def addData(route,analyzer):

    addVertex(analyzer,route['Departure'],'CompleteAirports')
    addVertex(analyzer,route['Destination'],'CompleteAirports')

    addVertex(analyzer,route['Departure'],'FullRoutes')
    addVertex(analyzer,route['Destination'],'FullRoutes')

    addConnection(analyzer,route['Departure'],route['Destination'],float(route['distance_km']),'CompleteAirports')
    addConnection(analyzer,route['Departure'],route['Destination'],float(route['distance_km']),'FullRoutes')

#++--------------------------------------------------------------------------------------------------------------------------++

#↓↓Aquí comienza el req1
def Requerimiento1(analyzer):
    airportsMap = analyzer['airports']
    vertices = gr.vertices(analyzer['CompleteAirports'])
    listaVertices = lt.newList(datastructure='SINGLE_LINKED',cmpfunction=None)
    for vertex in lt.iterator(vertices):
        
        airportInfo = m.get(airportsMap,vertex)['value']
        entra = gr.indegree(analyzer['CompleteAirports'],vertex)
        sale = gr.outdegree(analyzer['CompleteAirports'],vertex)
        total = entra + sale
        vertexAdd = {'entrada':entra,'salida':sale,'total':total}
        airportInfo.update(vertexAdd)

        lt.addLast(listaVertices, airportInfo)
    sortbyEdges(listaVertices)
    return listaVertices

def compareEdges(lista1, lista2):
    cant1 = lista1['total']
    cant2 = lista2['total']
    return cant1>cant2

def sortbyEdges(lista):
    sa.sort(lista,compareEdges)

#↑↑Aquí termina el req1


#↓↓Aquí comienza el req2
def clusters(analyzer, IATA1,IATA2):
    a = scc.KosarajuSCC(analyzer['CompleteAirports'])
    return (scc.stronglyConnected(a,IATA1,IATA2))

#↑↑Aquí termina el req2

#++--------------------------------------------------------------------------------------------------------------------------++

#↓↓Aquí comienza el req3↓↓
def Requerimiento3(analyzer,origin,Destiny, infOrigin,infDest):

    airportsMap = analyzer['airports']

    OrgAirportInfo = m.get(airportsMap,origin)['value']

    DestArprtInfo = m.get(airportsMap,Destiny)['value']

    dist_total=calc_distancia(OrgAirportInfo,infOrigin)+calc_distancia(DestArprtInfo,infDest)

    smallgraph = djk.Dijkstra(analyzer['CompleteAirports'],origin)
    camino = djk.pathTo(smallgraph,Destiny)

    for paso in lt.iterator(camino):
        print("{} a {}, Distancia: {}".format(paso['vertexA'],paso['vertexB'],round(paso['weight']),2))
        dist_total+=paso['weight']
    
    return str(round(dist_total,2))

#Funciones auxiliares para el req3
def selectCity(analyzer, city):
    lista_cities = (m.get(analyzer['citiesUser'],city)['value'])
    pos=0
    for i in lt.iterator(lista_cities):

        infoPrint = "Nombre: {}, País: {}, Departamento: {}, Latitud: {}, Longitud: {}, Cantidad de aeropuertos: {}".format(i['city_ascii'],i['country'],
        i['admin_name'],i['lat'],i['lng'],lt.size(i['airports']))
        print(str(pos+1)+'. ',infoPrint,'\n')
        pos+=1
    return lista_cities

def showAirports(citiesList,posCity):
    infoCity = lt.getElement(citiesList,posCity)
    list_airports = infoCity['airports']
    pos = 0

    for i in lt.iterator(list_airports):
        infoPrint = "id: {}, Nombre: {}, IATA: {}, Latitud: {},Longitud: {}, Distancia a la ciudad: {} km".format(i['id'], 
        i['Name'],i['IATA'],i['Latitude'],i['Longitude'],round(calc_distancia(i, infoCity),2))
        print(str(pos+1)+'. ',infoPrint,'\n')
        pos+=1
        
    return list_airports

def infoCity(list_cities,pos):
    return lt.getElement(list_cities,pos)

def selectAirport(list_airports,pos):
    
    return lt.getElement(list_airports,pos)['IATA']
#Fin del req 3

#++--------------------------------------------------------------------------------------------------------------------------++


##Aquí comienza el req4
def Requerimiento4(analyzer,distancia,origin):
    distancia *= 1.6
    list_airports = origin['airports']
    airport = lt.firstElement(list_airports)
    airportCode = airport['IATA']
    searchStructure = djk.Dijkstra(analyzer['CompleteAirports'],airportCode)
    mst = PrimMST(analyzer['CompleteAirports'])

    maxRoute = None
    maxSize = 0
    totalWeight = 0
    spentDistance = 0

    for vertex in lt.iterator(gr.vertices(analyzer['CompleteAirports'])):

        route = (djk.pathTo(searchStructure,vertex))
        if route['size']>maxSize:
            maxsize=route['size']
            maxRoute=route
    
    for step in lt.iterator(maxRoute):
        if distancia>0:
            distancia-=step['weight']
            spentDistance+=step['weight']

        totalWeight +=step['weight']



#++--------------------------------------------------------------------------------------------------------------------------++

def Requerimiento5(analyzer,IATA):
    grafo = analyzer['CompleteAirports']
    modifiedGraph = gr.removeVertex(grafo,IATA)
    listReturn = lt.newList('SINGLE_LINKED',cmpfunction=None)

    before = (gr.numVertices(modifiedGraph),gr.numEdges(grafo))
    after = (gr.numVertices(modifiedGraph),gr.numEdges(modifiedGraph))

    for edge in lt.iterator(gr.edges(grafo)):
        if edge['vertexB']== IATA:
            lt.addLast(listReturn,edge['vertexA'])
    print(lt.size(listReturn))
    return listReturn

#++--------------------------------------------------------------------------------------------------------------------------++


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
