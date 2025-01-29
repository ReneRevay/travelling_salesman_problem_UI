import random
import math
import matplotlib.pyplot as plt

class Path:
    def __init__(self, cities):
        self.cities = cities
        self.distance = self.calculate_distance()
        self.fitness = 1 / self.distance
    
    def calculate_distance(self):
        distance = 0.0
        for i in range (len(self.cities)):
            x1, y1 = self.cities[i-1][0], self.cities[i-1][1]
            x2, y2 = self.cities[i][0], self.cities[i][1]
            distance += math.sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))

        x1, y1 = self.cities[-1][0], self.cities[-1][1]
        x2, y2 = self.cities[0][0], self.cities[0][1]
        distance += math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
        return distance

# PLOTTER           
# -------------------------------------------------------------------------------------------------------------------------------------------------

def show_results(path,fitness_progression):
    x = [city[0] for city in path.cities] + [path.cities[0][0]]
    y = [city[1] for city in path.cities] + [path.cities[0][1]]
    plt.figure(1, figsize=(10, 6))
    plt.title('Best Path Found by Tabu Search Algorithm')
    plt.plot(x, y, 'o-', label='path')

    for i, city in enumerate(path.cities):
        plt.annotate(str(i), (city[0], city[1]), textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.figure(2,figsize=(10, 6))
    plt.title('Fitness Progression')
    plt.plot(fitness_progression)
    plt.xlabel('Iteration')
    plt.ylabel('Fitness')

    plt.show()

def show_initial_city_path(path):
    x = [city[0] for city in path.cities] + [path.cities[0][0]]
    y = [city[1] for city in path.cities] + [path.cities[0][1]]
    plt.figure(1, figsize=(10, 6))
    plt.title('Initial path')
    plt.plot(x, y, 'o-', label='path')

    for i, city in enumerate(path.cities):
        plt.annotate(str(i), (city[0], city[1]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.show()
    
# -------------------------------------------------------------------------------------------------------------------------------------------------

def generate_random_cities(number_of_cities, maximum_length):
    cities = []
    while len(cities) < number_of_cities:
        x = random.randint(0, maximum_length)
        y = random.randint(0, maximum_length)
        if (x, y) not in cities:
            cities.append((x, y))
    return cities

def generate_neighbours(path, number_of_neighbours):
    neighbours = []
    while len(neighbours) < number_of_neighbours:
        start, end = sorted(random.sample(range(0, len(path)), 2))
        selected_path = path[start:end]
        reversed_path = selected_path[::-1]
        new_path = path[:start] + reversed_path + path[end:]
        new_neighbour = Path(new_path)
        neighbours.append(new_neighbour)
    return neighbours

# -------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    number_of_cities = 40
    tabu_list_size = 80
    tabu_iterations = 500
    neighbourhood_size = 100

    maximum_length = 200

    fitness_progress_tracker = []

    current_solution = Path(generate_random_cities(number_of_cities, maximum_length))
    best_solution = current_solution
    show_initial_city_path(current_solution)
    print(f'Initial Path : {current_solution.cities} \nInitial distance : {current_solution.distance} \nInitial fitness : {current_solution.fitness}')
    tabu_list = []

    for _ in range(tabu_iterations):
        neighbours = generate_neighbours(current_solution.cities, neighbourhood_size)
        best_neighbour = None

        for n in neighbours:
            if n.cities not in [t.cities for t in tabu_list]:
                if best_neighbour is None or n.distance < best_neighbour.distance:
                    best_neighbour = n

        current_solution = best_neighbour
        if current_solution.distance < best_solution.distance:
            best_solution = current_solution

        fitness_progress_tracker.append(best_solution.fitness)
        tabu_list.append(current_solution)
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)

    print(f'\nBest path : {best_solution.cities}  \nBest distance : {best_solution.distance} \nBest fitness : {best_solution.fitness}')
    show_results(best_solution,fitness_progress_tracker)

if __name__ == "__main__":
    main()
