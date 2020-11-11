# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 09:40:52 2020

@author: julie
"""

import numpy as np
import random

#Liste de villes
_CITIES = (("Bordeaux", (44.833333,-0.566667)), ("Paris",(48.8566969,2.3514616)),("Nice",(43.7009358,7.2683912)),
               ("Lyon",(45.7578137,4.8320114)),("Nantes",(47.2186371,-1.5541362)),("Brest",(48.4,-4.483333)),("Lille",(50.633333,3.066667)),
               ("Clermont-Ferrand",(45.783333,3.083333)),("Strasbourg",(48.583333,7.75)),("Poitiers",(46.583333,0.333333)),
               ("Angers",(47.466667,-0.55)),("Montpellier",(43.6,3.883333)),("Caen",(49.183333,-0.35)),("Rennes",(48.083333,-1.683333)),("Pau",(43.3,-0.366667)))

#Nombre de villes
nb_cities = len(_CITIES)

#Nombre de fourmis
nb_fourmis = nb_cities

nb_cycles = 100

#Liste permettant de placer au départ les fourmis
_RANDOM = list(range(0, nb_fourmis))

_PHEROMONES = np.zeros(shape=(nb_cities, nb_cities))
_DISTANCE_CITIES = np.zeros(shape=(nb_cities, nb_cities))
_FOURMIS = []
_DISTANCE_FOURMIS = []
_PHEROMONES_ARCS = np.zeros(shape=(nb_cities, nb_cities))

alpha = 1
beta = 5
Q = 100
P = 0.5 #coefficient vitesse evaporation
    
def start():
    for i in range(nb_fourmis):
        #les fourmis sont placées alétoirement sur une des nb_cities villes
        #le nombre de fourmis peut être supérieur au nombre de ville
        #_FOURMIS.append([random.randint(0, nb_cities-1)])
        #les fourmis sont réparties aléatoirement sur les nb_cities villes
        #le nombre de villes doit être égal au nombre de fourmis
        random_item = random.choice(_RANDOM)
        _FOURMIS.append([random_item])
        _RANDOM.remove(random_item)
    for i in range(nb_cities):
        for j in range(nb_cities):
            #les pheromones sont initialises avec une petite constante positive
            _PHEROMONES[i, j] = 0.1 
            _DISTANCE_CITIES[i, j] = distance(_CITIES[i][1], _CITIES[j][1])
    return _FOURMIS
        
def nextStep(_FOURMI):
    _CITIES = []
    _PROBS = []
    for city in range(nb_cities):
        if city not in _FOURMI:
            visibility = 1/_DISTANCE_CITIES[_FOURMI[-1], city]
            pheromone = _PHEROMONES[_FOURMI[-1], city]
            prob = (visibility**beta)*(pheromone**alpha)
            _CITIES.append(city)
            _PROBS.append(prob) 
    _PROBS = _PROBS/sum(_PROBS)
    return np.random.choice(_CITIES, 1, p=_PROBS)[0]

def play():
    start()
    _BESTPATH = []
    bestPath_distance = float('inf')
    for i in range(nb_cycles):
        for j in range(nb_cities):
            for _FOURMI in _FOURMIS:
                if(j == nb_cities-1):
                    _FOURMI.append(_FOURMI[0])
                else:
                    _FOURMI.append(nextStep(_FOURMI))  
        updatePheromone(_FOURMIS)
        bestPath_distance, _BESTPATH = chooseBestPath(_FOURMIS, _DISTANCE_FOURMIS, bestPath_distance, _BESTPATH)
        deleteMemory(_FOURMIS, _DISTANCE_FOURMIS, _PHEROMONES_ARCS)
        print(_PHEROMONES_ARCS)
    print(_BESTPATH)
    print(bestPath_distance)
    
def calcDistances(_FOURMIS):
    #calcule la distance totale parcourue par chaque fourmi
    for _FOURMI in _FOURMIS:
        distance = 0
        for city in range(nb_cities):
            distance = distance + _DISTANCE_CITIES[_FOURMI[city], _FOURMI[city+1]]
        _DISTANCE_FOURMIS.append(distance)
    
def calcPheromoneArcs(_FOURMIS):
    for i in range(nb_fourmis):
        for city in range(nb_cities):
            _PHEROMONES_ARCS[_FOURMIS[i][city], _FOURMIS[i][city+1]] = _PHEROMONES_ARCS[_FOURMIS[i][city], _FOURMIS[i][city+1]] + Q/_DISTANCE_FOURMIS[i] 
            
def updatePheromone(_FOURMIS):
    calcDistances(_FOURMIS)
    calcPheromoneArcs(_FOURMIS)
    for i in range(nb_cities):
        for j in range(nb_cities):
            _PHEROMONES[i,j] = P*_PHEROMONES[i,j] + _PHEROMONES_ARCS[i,j]

def chooseBestPath(_FOURMIS, _DISTANCE_FOURMIS, bestPath_distance, _BESTPATH):
    minDistance = min(_DISTANCE_FOURMIS)
    minDistance_index = _DISTANCE_FOURMIS.index(minDistance)
    minDistance_path = np.copy(_FOURMIS[minDistance_index])
    if(minDistance < bestPath_distance):
        return minDistance, minDistance_path
    else:
        return bestPath_distance, _BESTPATH
    
def deleteMemory(_FOURMIS, _DISTANCE_FOURMIS, _PHEROMONES_ARCS):
    for _FOURMI in _FOURMIS:
        while(len(_FOURMI)>1):
            _FOURMI.pop()  
    _DISTANCE_FOURMIS[:] = []
    _PHEROMONES_ARCS = np.zeros(shape=(nb_cities, nb_cities))
   
def distance(a,b):
    (x1,y1),(x2,y2) = (a,b)
    return np.sqrt((x1-x2)**2+(y1-y2)**2) 

play()