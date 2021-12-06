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
 """

import config as cf
import model
import csv
import DISClib.DataStructures.graphstructure as gr
import DISClib.DataStructures.mapstructure as mp
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def init():
    analyzer = model.newAnalyzer()
    return analyzer
    

def load(analyzer,file):
    
    file = cf.data_dir+file
    input_file = csv.DictReader(open(file,encoding='utf-8'),delimiter=',')

    city_file = cf.data_dir+'worldcities-utf8.csv'
    file_cities = csv.DictReader(open(city_file,encoding='utf-8'),delimiter=',')

    airports_file = cf.data_dir+'airports-utf8-small.csv'
    file_ariports = csv.DictReader(open(airports_file,encoding='utf-8'),delimiter=',')

    for city in file_cities:
        model.addCity(analyzer,city)
    
    for airport in file_ariports:
        model.addAirport(analyzer,airport)

    for route in input_file:
        model.addData(route,analyzer)

def req1():

    pass


def req2(analyzer,Cod1,Cod2):
    return model.clusters(analyzer,Cod1,Cod2)

def req3(ciudadOrigen,ciudadDestino):
    pass


def req4(ciudadOrigen, cantidadMillas):
    pass


def req5(codIATA):
    pass


def bono(ciudadOrigen, ciudadDestino):
    pass


