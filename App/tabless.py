from App.controller import load
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from tabulate import tabulate
import textwrap
from datetime import datetime as dt
#CREACIÓN DE TABLAS
def distribuir(elemento,cantidad):
    str_distribuido = '\n'.join((textwrap.wrap(elemento,cantidad)))
    return str_distribuido

def chkUnknown(origen,clave):
    if origen[clave]==None or origen[clave]=='': return 'Not available' #El 5000 se pone para compensar una de las funciones de comparación de años.
    else: return str(origen[clave])
def selectInfo(position,listViews,FilteredList):
#       ↓↓↓ Todo este montón de líneas se encargan de sacar la info. necesaria del diccionario grande y con textwrap lo separa en líneas de un igual tamaño.
        view = lt.getElement(listViews,position)

        name = chkUnknown(view,'Name')
        city=distribuir(chkUnknown(view,'City'),20)
        country=distribuir(chkUnknown(view,'Country'),10)
        code=distribuir(chkUnknown(view,'IATA'),20)
        total=distribuir(chkUnknown(view,'total'),20)
        entrada=distribuir(chkUnknown(view,'entrada'),15)
        salida=distribuir(chkUnknown(view,'salida'),15)

#       Se crea una lista con todo lo que pide el requerimiento.

        artwork_entrega = [name,city,country,code,total,entrada,salida]
        FilteredList.append(artwork_entrega)

def createTable(filteredList):

    listTable =[]
    for position in range(6):
        selectInfo(position,filteredList,listTable)

    headers = ['Name','City','Country','IATA','Connections','Inbound','Outbound']

    table = tabulate(listTable,headers=headers,numalign='right',tablefmt='grid') 
    return table
#↑↑↑ Termina el formatting de las tablas ↑↑↑

def simpleTable(variable,count,headerName):
    headers = [headerName,'count']
    info = [[variable,count]]
    table = tabulate(info,headers=headers,numalign='right',tablefmt='grid')
    return table

def infoTable(airport):
    headers = ['IATA','Name','City','Country']
    code = chkUnknown(airport,'IATA')
    name = chkUnknown(airport,'Name')
    city = chkUnknown(airport,'City')
    country = chkUnknown(airport,'Country')
    table = tabulate([[code,name,city,country]],headers=headers,numalign='right',tablefmt='grid')
    return table

def tripTable(route):
    headers = ['Departure','Destination','Distance_km']
    info = []
    for step in lt.iterator(route):
        dep = chkUnknown(step,'vertexA')
        dest = chkUnknown(step,'vertexB')
        distance = chkUnknown(step,'weight')
        info.append([dep,dest,distance])
    table = tabulate(info,headers=headers, numalign='right',tablefmt='grid')
    return table

def tableStops(route,analyzer):
    headers = ['IATA','Name','City','Country']
    airports = analyzer['airports']
    inserted = m.newMap(numelements=5,maptype='CHAINING',loadfactor=0.7)
    infoTable=[]
    for step in lt.iterator(route):
        if not m.contains(inserted, step['vertexA']):
                airport = m.get(airports,step['vertexA'])['value']
                code = chkUnknown(airport,'IATA')
                name = chkUnknown(airport,'Name')
                city = chkUnknown(airport,'City')
                country = chkUnknown(airport,'Country')
                infoTable.append([code,name,city,country])
                m.put(inserted,step['vertexA'], None)

        if not m.contains(inserted, step['vertexB']):
                airport = m.get(airports,step['vertexB'])['value']
                code = chkUnknown(airport,'IATA')
                name = chkUnknown(airport,'Name')
                city = chkUnknown(airport,'City')
                country = chkUnknown(airport,'Country')
                infoTable.append([code,name,city,country])
                m.put(inserted,step['vertexB'], None)
    
    table = tabulate(infoTable,headers=headers, tablefmt='grid',numalign='right')
    return table

def FirstLast3Table(listAirports,analyzer):
    headers = ['IATA','Name','City','Country']
    infoTable = []

    if lt.size(listAirports)>6:
        for pos in range(1,4):
            infoTable.append(getInfo(pos,listAirports,analyzer))  

        for pos in range(lt.size(listAirports)-2,lt.size(listAirports)+1):
            infoTable.append(getInfo(pos,listAirports,analyzer))  
    else:
        for pos in range(1,lt.size(listAirports)+1):
            infoTable.append(getInfo(pos,listAirports,analyzer))

    table = tabulate(infoTable,headers=headers, tablefmt='grid',numalign='right')

    return table

def getInfo(pos,listAirports,analyzer):
    airport = lt.getElement(listAirports,pos)
    airports = analyzer['airports']
    airport = m.get(airports,airport)['value']
    code = chkUnknown(airport,'IATA')
    name = chkUnknown(airport,'Name')
    city = chkUnknown(airport,'City')
    country = chkUnknown(airport,'Country')
    return [code,name,city,country]