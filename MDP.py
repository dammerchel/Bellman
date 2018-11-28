from tkinter import *
from Map_File import *

# Map data

map_types = [[1,1,1,1,1,1,1,1,1,1,1],
             [1,1,0,1,1,1,1,1,1,1,1],
             [1,1,2,1,1,1,1,1,1,1,1],
             [1,1,1,1,1,1,1,0,0,0,1],
             [1,1,1,1,1,1,1,0,0,1,1]]

# Algorithm

map = MapFile(0, map_types)

map.MDP_algorithm()
print("Mapa potencjałów pól")
for i in range(map.map_height):
    print(map.map_value[i])

print("Mapa polityki ruchów")
for i in range(map.map_height):
    print(map.map_policy[i])

print("Mapa prawdopodobieństw ruchów")
for i in range(len(map.map_moves_probabilities)):
    print("Pole:" + str(i))
    for j in range(len(map.map_moves_probabilities[i])):
        print(map.map_moves_probabilities[i][j])
print(map.iteration)










