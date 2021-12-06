from DISClib.ADT import list as lt
from tabulate import tabulate
import textwrap
from datetime import datetime as dt
#CREACIÓN DE TABLAS
def distribuir(elemento,cantidad):
    str_distribuido = '\n'.join((textwrap.wrap(elemento,cantidad)))
    return str_distribuido

def chkUnknown(origen,clave):
    if origen[clave]==None or origen[clave]=='' or origen[clave]==5000 or origen[clave]=='2100-12-24': return 'Not available' #El 5000 se pone para compensar una de las funciones de comparación de años.
    else: return origen[clave]
def selectInfo(position,listViews,FilteredList,style):
#       ↓↓↓ Todo este montón de líneas se encargan de sacar la info. necesaria del diccionario grande y con textwrap lo separa en líneas de un igual tamaño.
        view = lt.getElement(listViews,position)

        datetime = chkUnknown(view,'datetime')
        city=distribuir(chkUnknown(view,'city'),20)
        state=distribuir(chkUnknown(view,'state'),10)
        country=distribuir(chkUnknown(view,'country'),20)
        shape=distribuir(chkUnknown(view,'shape'),20)
        duration_seconds=distribuir(chkUnknown(view,'duration (seconds)'),15)

#       Se crea una lista con todo lo que pide el requerimiento.

        artwork_entrega = [datetime,city,state,country,shape,duration_seconds]
        if style=='Location': 
            latitude = chkUnknown(view,'latitude')
            longitude = chkUnknown(view,'longitude')
            artwork_entrega.append(latitude)
            artwork_entrega.append(longitude)
        elif style == 'date':
            if datetime != 'Unknown':
                date = dt.strptime(datetime,'%Y-%m-%d %H:%M:%S').date()
            artwork_entrega = [datetime,date,city,state,country,shape,duration_seconds]
        elif style == 'time':
            if datetime != 'Unknown':
                time = dt.strptime(datetime,'%Y-%m-%d %H:%M:%S').time()
            artwork_entrega = [datetime,time,city,state,country,shape,duration_seconds]
#       Se pone un nuevo registro con la info de cada obra en la lista grande declarada al inicio.
        FilteredList.append(artwork_entrega)

def createTable(filteredList,style:str):
    listTable =[]
    for position in range(1,4):
        selectInfo(position,filteredList,listTable,style)
    for position in range(lt.size(filteredList)-2,lt.size(filteredList)+1):
        selectInfo(position,filteredList,listTable,style)

    if style=='Location': headers = ['datetime','city','state','country','shape','duration (seconds)','latitude','longitude']
    elif style == 'date' or style=='time' : headers = ['datetime',style,'city','state','country','shape','duration (seconds)']
    else:          headers = ['datetime','city','state','country','shape','duration (seconds)']

    table = tabulate(listTable,headers=headers,numalign='right',tablefmt='grid') 
    return table
#↑↑↑ Termina el formatting de las tablas ↑↑↑

def simpleTable(variable,count,headerName):
    headers = [headerName,'count']
    info = [[variable,count]]
    table = tabulate(info,headers=headers,numalign='right',tablefmt='grid')
    return table