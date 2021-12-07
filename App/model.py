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
from DISClib.Algorithms.Graphs.bellmanford import BellmanFord, hasPathTo, initSearch, pathTo
from DISClib.Algorithms.Graphs.bfs import BreadhtFisrtSearch, bfsVertex
from DISClib.Algorithms.Graphs.cycles import dfs
from DISClib.Algorithms.Graphs.dfo import DepthFirstOrder, dfsVertex
from DISClib.Algorithms.Graphs.dfs import DepthFirstSearch
from DISClib.Algorithms.Graphs.dfs import pathTo as dfsPathTo
from DISClib.Algorithms.Graphs.prim import PrimMST, edgesMST, prim, scan
from DISClib.DataStructures.arraylist import compareElements
from DISClib.DataStructures.chaininghashtable import contains
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
        'CitiesRoutes':gr.newGraph(datastructure='ADJ_LIST',directed=True, size = 5000, comparefunction=compareDistances),
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

    Newcity= lt.getElement(citiesList,pos_minor)
    lt.addLast(Newcity['airports'],airport)
    lt.deleteElement(citiesList,pos_minor)
    lt.addLast(citiesList,Newcity)
    

    key = actual_city['city_ascii']+str(actual_city['lat'])+str(actual_city['lng'])
    m.put(analyzer['cities'],key,actual_city)
    
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


#↓↓Aquí comienza el req3↓↓
def Requerimiento3(analyzer,cityDep,cityDest):


    pass
    # smallgraph=djk.Dijkstra(analyzer['CitiesRoutes'],cityDep)
    # camino = djk.pathTo(smallgraph,cityDest)
    # for i in camino:
    #     print(i)
    # return camino
    # pathTo(analyzer['CitiesRoutes'],cityDest)
    # return pathTo(analyzer['CitiesRoutes'],cityDest)

def selectAirport(analyzer, city):
    print(m.get(analyzer['citiesUser'],city)['value'])
    

##Aquí comienza el req4
def Requerimiento4(analyzer,distancia,origin):
    distancia *= 1.6
    searchStructure = PrimMST(analyzer['CompleteAirports'])
    # print(searchStructure)
    hola = (prim(analyzer['CompleteAirports'],searchStructure,origin))
    # DepthFirstOrder(searchStructure)
    # dfsVertex(analyzer,searchStructure,origin)
    # path = edgesMST(analyzer['CompleteAirports'],hola)
    # print(gr.newGraph(datastructure='ADJ_LIST',directed=True,size=2,comparefunction=None))
    # cosa = DepthFirstSearch(searchStructure,origin)
    for i in lt.iterator(gr.vertices(analyzer['CompleteAirports'])):
        if scan(analyzer['CompleteAirports'],searchStructure,i)['edgeTo']['size']!=0:
            print(scan(analyzer['CompleteAirports'],searchStructure,i)['weight'])
    # print(searchStructure)
    # for i in lt.iterator(gr.vertices(analyzer['CompleteAirports'])):   
    #     print(dfsPathTo(cosa,i))
    # total=0
    # cantidad = 0
    # for i in lt.iterator(hola):
    #     if i['key']!=None:
    #         if float(i['value']['weight'])+total<=distancia:
    #             total+=float(i['value']['weight'])
    #             cantidad+=1

    # print(total)
    # print(cantidad)
    # print(m.size(hola))
    # return hola
    # vertexMax=None
    # pesoMax=0
    # for vertex in lt.iterator(gr.vertices(analyzer['CompleteAirports'])):
    #     peso=0
    #     hola = (prim(analyzer['CompleteAirports'],searchStructure,vertex)['edgeTo']['table'])
    #     for i in lt.iterator(hola):
    #         if i['key']!=None:
    #             peso+=i['value']['weight']
    #     if peso>pesoMax:
    #         pesoMax=peso
    #         vertexMax=vertex
    # print(vertexMax)


def Requerimiento5(analyzer,IATA):
    grafo = analyzer['CompleteAirports']
    listReturn = lt.newList('SINGLE_LINKED',cmpfunction=None)


    for edge in lt.iterator(gr.edges(grafo)):
        if edge['vertexB']== IATA:
            lt.addLast(listReturn,edge['vertexA'])
    print(lt.size(listReturn))
    return listReturn

def addData(route,analyzer):

    addVertex(analyzer,route['Departure'],'CompleteAirports')
    addVertex(analyzer,route['Destination'],'CompleteAirports')

    addVertex(analyzer,route['Departure'],'FullRoutes')
    addVertex(analyzer,route['Destination'],'FullRoutes')

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
