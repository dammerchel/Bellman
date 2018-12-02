from copy import deepcopy


class MapFile:                                      #Klasa zawierające dane pliku mapy oraz metody umożliwiajace
                                                    # ustalenie polityki ruchu aktora

    iteration = 0                                   #Zmienna przechowująca liczbę iteracji pętli głównej algorytmu MDP
    gamma = 0.5
    moves=[[[-1, 0], [0, 1], [0, -1]],
           [[0, 1], [1, 0], [-1, 0]],
           [[1, 0], [0, 1], [0, -1]],
           [[0, -1], [1, 0], [-1, 0]]]              # Tablica możliwych ruchów aktora w osiach X i Y, o współrzędnych
                                                    # i, j, k, gdzie i oznacza kolejne kierunki UP, RIGHT, DOWN, LEFT,
                                                    # j reprezentuje ruch główny oraz możliwe ruchy w kierunkach
                                                    # prostopadłych do kierunku ruchu głównego, a k reprezentuje ruchy
                                                    # w osi x i y


    def __init__(self, map_hot_floor, map_types):   #Inicjalizacja pliku mapy

        self.map_types = map_types
        self.map_height=len(map_types)
        self.map_width=len(map_types[0])
        self.map_policy=[[0 for x in range(self.map_width)] for y in range(self.map_height)]
        self.map_moves_probabilities = [[[0 for x in range(self.map_height * self.map_width)] for y in range(4)]
                                        for z in range(self.map_height * self.map_width)]
        self.map_rewards = [[0 for x in range(self.map_width)] for y in range(self.map_height)]

        for i in range(self.map_height):            # Automatyczne przydzielanie wartości nagród na podstawie  typu pola
            for j in range(self.map_width):
                if map_hot_floor == 0:
                    if self.map_types[i][j] == 0:
                        self.map_rewards[i][j] = 0
                    elif self.map_types[i][j] == 1:
                        self.map_rewards[i][j] = -1
                    elif self.map_types[i][j] == 2:
                        self.map_rewards[i][j] = 100
                    else:
                        self.map_types[i][j] = -2
                        self.map_rewards[i][j] = -10
                elif map_hot_floor == 1:
                    if self.map_types[i][j] == 0:
                        self.map_rewards[i][j] = 0
                    elif self.map_types[i][j] == 1:
                        self.map_rewards[i][j] = -50
                    elif self.map_types[i][j] == 2:
                        self.map_rewards[i][j] = 100
                    else:
                        self.map_types[i][j] = -2
                        self.map_rewards[i][j] = -100

    def MDP_algorithm(self):                        # Algorytm wyznaczania polityki ruchu

        self.map_value = deepcopy(self.map_rewards)

        k = 0
        while k < 1000:
            difference = 0
            k += 1
            self.map_value_old = deepcopy(self.map_value)
            for i in range(self.map_height):
                for j in range(self.map_width):
                    if self.map_types[i][j] != 2 and self.map_types[i][j] != 0 and self.map_types[i][j] != -2:
                        self.map_value[i][j] = self.map_rewards[i][j] + self.gamma * self.best_action(i, j)

                        if abs(self.map_value[i][j] - self.map_value_old[i][j]) > difference:
                            difference = abs(self.map_value[i][j] - self.map_value_old[i][j])

            self.iteration += 1

            if difference < 10e-4:
                break

    def best_action(self, x, y):    # Wybór najlepszej akcji dla danego pola
        field_value = [0, 0, 0, 0]
        for i in range(4):
            for j in range(len(self.map_moves_probabilities[0][0])):
                self.map_moves_probabilities[x * self.map_width + y][i][j] = 0
        for i in range(4):
            for j in range(3):
                if j == 0:
                    probability = 0.8
                else:
                    probability = 0.1
                try:
                    if (self.map_value_old[x + self.moves[i][j][0]][y + self.moves[i][j][1]] != 0 and x +
                            self.moves[i][j][0] >= 0 and y + self.moves[i][j][1] >= 0):
                        field_value[i] += probability * self.map_value_old[x + self.moves[i][j][0]][y +
                                                                                                    self.moves[i][j][1]]
                        self.map_moves_probabilities[x * self.map_width + y][i][(x + self.moves[i][j][0])
                                                                                * self.map_width + y
                                                                                + self.moves[i][j][1]] += probability

                    else:
                        field_value[i] += probability * self.map_value_old[x][y]
                        self.map_moves_probabilities[x * self.map_width + y][i][x * self.map_width + y] += probability
                except IndexError:
                    field_value[i] += probability * self.map_value_old[x][y]
                    self.map_moves_probabilities[x * self.map_width + y][i][x * self.map_width + y] += probability

        self.map_policy[x][y] = field_value.index(max(field_value)) + 1
        return max(field_value)