from tkinter import *
from tkinter import ttk
from Map_File import *

def button_submit_action():
    for i in range(len(map_types_entries)):
        for j in range(len(map_types_entries[i])):
            map_types[i][j] = int(map_types_entries[i][j].get())

    map = MapFile(hot_floor.get(), map_types)

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
    print("Ilość iteracji:" + str(map.iteration))

# Map data

map_types = [[0 for i in range(5)]for j in range(4)]
map_types_entries = [[0 for i in range(5)]for j in range(4)]

#GUI

root = Tk()
root.title("MDP_Bellman")
hot_floor = IntVar()            #Zmienna przechowująca dane dotyczące "Gorącej podłogi"

Label(root, text="Wprowadź rodzaje pól:").grid(row=0, column=0)
for i in range(len(map_types_entries)):
    for j in range(len(map_types_entries[i])):
        map_types_entries[i][j]=Entry(root,width=20)
        map_types_entries[i][j].grid(row=i+1, column=j)
check_button = Checkbutton(root, text="Gorąca podłoga", onvalue=1, offvalue=0, variable=hot_floor)
check_button.grid(column=0)
button_submit = Button(root, text="Potwierdź",command=button_submit_action).grid(column=len(map_types_entries[0]))

root.mainloop()










