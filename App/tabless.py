from DISClib.ADT import list as lt
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
    table = tabulate([code,name,city,country],headers=headers,numalign='right',tablefmt='grid')
    return table
