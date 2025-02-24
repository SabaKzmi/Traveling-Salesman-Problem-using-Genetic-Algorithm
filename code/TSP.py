import math
import random

def find_distance(city1, city2, TSP_data):
    distance = math.sqrt((TSP_data[city2 - 1][0] - TSP_data[city1 - 1][0]) ** 2 + (TSP_data[city2 - 1][1] - TSP_data[city1 - 1][1]) ** 2)
    return distance

def fitness(path, TSP_data):
    total_distance = 0
    for c in range(len(path) - 1):
        total_distance += find_distance(path[c], path[c + 1], TSP_data)
    total_distance += find_distance(path[len(path) - 1], path[0], TSP_data)
    return total_distance

def make_population(n):
    cities = [i for i in range(1, 52)]
    pop = []

    for i in range(n):
        new_member = random.sample(cities, len(cities))
        pop.append(new_member)

    return pop

def choose_parents(pop, TSP_data):
    best_path = None
    min_value = float('+inf')
    second_best_path = None
    second_min_value = float('+inf')

    tournament_list = random.sample(pop, 3)
    for s in tournament_list:
        if fitness(s, TSP_data) < min_value:
            second_best_path, second_min_value = best_path, min_value
            best_path = s
            min_value = fitness(s, TSP_data)
        elif second_min_value > fitness(s, TSP_data) >= min_value:
            second_best_path = s
            second_min_value = fitness(s, TSP_data)
    return best_path, second_best_path

def find_multiple_elite(pop, num, TSP_data):
    pop_copy = pop.copy()
    elite = [None] * num
    for n in range(num):
        elite[n] = pop_copy[0]
        for c in pop_copy:
            if fitness(c, TSP_data) < fitness(elite[n], TSP_data):
                elite[n] = c
        pop_copy.remove(elite[n])
    return elite

def find_elite(pop, TSP_data):
    elite = pop[0]
    for c in pop:
        if fitness(c, TSP_data) < fitness(elite, TSP_data):
            elite = c
    return elite

#ox crossover
def crossover(parent1, parent2):
    child1 = [None] * len(parent2)
    child2 = [None] * len(parent1)

    #choose points
    startPoint, endPoint = random.sample(range(len(parent1)), 2)
    if endPoint < startPoint: startPoint, endPoint = endPoint, startPoint

    #copying the part in between two points to the child
    for i in range(startPoint, endPoint + 1):
        child1[i] = parent1[i]
        child2[i] = parent2[i]

    #completing the children
    #list of indexes that should be visited in parents
    index_list = list(range(endPoint + 1, len(parent1)))
    index_list += list(range(endPoint + 1))

    ch1_index , ch2_index = index_list, index_list
    i1, i2 = 0, 0
    #going through indexes
    for i in index_list:
        if parent2[i] not in child1:
            child1[ch1_index[i1]] = parent2[i]
            i1 += 1
        if parent1[i] not in child2:
            child2[ch2_index[i2]] = parent1[i]
            i2 += 1

    return child1, child2

def mutation(path):
    firstPoint, secondPoint = random.sample(range(51), 2)
    path[firstPoint], path[secondPoint] = path[secondPoint], path[firstPoint]
    return path

#---------- main ----------

#read data
TSP_file = open("TSP51.txt", "r")
data = []
for l in range(51):
    current_line = TSP_file.readlines(1)[0][:-1]
    line_num, x, y = current_line.split()
    data.append([int(x), int(y)])

population = make_population(30)
generation_num = 1

while generation_num < 400:
    e = find_multiple_elite(population, 2 * (len(population) // 10), data)
    newPopulation = [e[i] for i in range(len(e))]
    for i in range(8 * (len(population) // 10) // 2):
        p1, p2 = choose_parents(population, data)
        ch1, ch2 = crossover(p1, p2)
        newPopulation.append(mutation(ch1))
        newPopulation.append(mutation(ch2))
    generation_num += 1
    print("new generation ", generation_num)
    print("best fit: ", fitness(find_elite(newPopulation, data), data))
    population = newPopulation

print("best fit: ", find_elite(population, data), "   fitness: ", fitness(find_elite(population, data), data))
