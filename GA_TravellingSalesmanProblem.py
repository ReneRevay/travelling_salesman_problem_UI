import random
import math
import matplotlib.pyplot as plt

class Gene:
    def __init__(self, cities):
        self.cities = cities
        self.fitness = 0.0
        self.distance = 0.0
    
    def calculate_fitness(self):
        for i in range (0, len(self.cities)):
            x1, y1 = self.cities[i-1][0], self.cities[i-1][1]
            x2, y2 = self.cities[i][0], self.cities[i][1]
            self.distance += math.sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))

        x1, y1 = self.cities[-1][0], self.cities[-1][1]
        x2, y2 = self.cities[0][0], self.cities[0][1]
        self.distance += math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))

        self.fitness = 1 / self.distance

# PLOTTER           
# -------------------------------------------------------------------------------------------------------------------------------------------------

def show_multiple_runs(list_of_fitnesses_list):
    counter = 0
    for fitness_list in list_of_fitnesses_list:
        plt.plot(fitness_list, label = f"Run {counter}")
        counter += 1

    plt.title('5 runs of Roulette selection')
    plt.xlabel('Generation')
    plt.ylabel('Best fitness of generation')
    plt.legend()
    plt.show()

def show_results_progress(gene, fitness_progression, distance_progression):
    x = [city[0] for city in gene.cities] + [gene.cities[0][0]]
    y = [city[1] for city in gene.cities] + [gene.cities[0][1]]
    plt.figure(1,figsize=(10, 6))
    plt.title('Best gene Found by Genetic Algorithm')
    plt.plot(x, y, 'o-', label='gene')

    for i, city in enumerate(gene.cities):
        plt.annotate(str(i), (city[0], city[1]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.figure(2,figsize=(10, 6))
    plt.title('Fitness Progression')
    plt.plot(fitness_progression)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')

    plt.figure(3,figsize=(10, 6))
    plt.title('Distance Progression')
    plt.plot(distance_progression)
    plt.xlabel('Generation')
    plt.ylabel('Distance')

    plt.show()

def show_initial_city_path(gene):
    x = [city[0] for city in gene.cities] + [gene.cities[0][0]]
    y = [city[1] for city in gene.cities] + [gene.cities[0][1]]
    plt.figure(1, figsize=(10, 6))
    plt.title('Initial path')
    plt.plot(x, y, 'o-', label='path')

    for i, city in enumerate(gene.cities):
        plt.annotate(str(i), (city[0], city[1]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.show()

# INIT POPULATION
# -------------------------------------------------------------------------------------------------------------------------------------------------

def generate_random_cities(number_of_cities,maximum_lenght):
    cities = []
    while len(cities) < number_of_cities:
        x = random.randint(0,maximum_lenght)
        y = random.randint(0,maximum_lenght)
        if (x,y) not in cities:
            cities.append((x,y))
    return cities

def create_initial_population(number_of_cities, number_of_genes, maximum_lenght):
    population = []
    for _ in range(number_of_genes):
        cities = generate_random_cities(number_of_cities,maximum_lenght)
        random.shuffle(cities)
        gene = Gene(cities)
        gene.calculate_fitness()
        population.append(gene)
    return population

# SELECTION ALTERNATIVES
# -------------------------------------------------------------------------------------------------------------------------------------------------

def roulette_selection(generation):
    parents = []
    total_fitness = 0.00
    current_fitness = 0.00

    for gene in generation:
        total_fitness += gene.fitness

    for _ in range(2):
        random_fitness = random.uniform(0,total_fitness)
        for gene in generation:
            current_fitness += gene.fitness
            if current_fitness > random_fitness:
                parents.append(gene)
                break

    return parents
            

def tournament_selection(generation):
    parents = []
    for _ in range(2):
        sample_size = 2
        tournament_selection = random.sample(generation, sample_size)
        parents.append(min(tournament_selection, key=lambda fighter: fighter.distance))
    return parents

# CROSSING
# -------------------------------------------------------------------------------------------------------------------------------------------------

def mate(parent1,parent2):
# Permutational crossing
    start, end = sorted(random.sample(range(len(parent1.cities)), 2))
    child_cities = parent1.cities[start:end]

    for city in parent2.cities:
        if city not in child_cities:
            child_cities.append(city)
    
    return Gene(child_cities)

# MUTATIONS
# -------------------------------------------------------------------------------------------------------------------------------------------------

def mutation_reverse_city_segment(gene, mutation_chance):
    #reverse city segment
    if random.random() <= mutation_chance:
        start, end = sorted(random.sample(range(len(gene.cities)), 2))
        selected_cities = gene.cities[start:end]
        reversed_cities = selected_cities[::-1]
        mutated_array = gene.cities[:start] + reversed_cities + gene.cities[end:]
        gene.cities = mutated_array
    gene.calculate_fitness()


def mutation_swap_city_neighours(gene, mutation_chance):
    #neighbour city swap
    for i in range(len(gene.cities)):
        if random.random() <= mutation_chance:
            temp = gene.cities[i-1]
            gene.cities[i-1] = gene.cities[i]
            gene.cities[i] = temp
    gene.calculate_fitness()


def mutation_swap_city_random(gene, mutation_chance):
    #random city swap  
    for i in range(len(gene.cities)):
        if random.random() <= mutation_chance:
            j = random.randint(len(gene.cities))
            temp = gene.cities[i]
            gene.cities[i] = gene.cities[j]
            gene.cities[j] = temp  
    gene.calculate_fitness()

# MAIN + GENETIVE ALG
# -------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    number_of_cities = 40
    number_of_genes = 100
    number_of_elites = int(number_of_genes * 0.1)
    number_of_generations = 4000

    maximum_lenght = 200

    chance_for_mutation = 0.1
        
    distance_progress_tracker = []
    fitness_progress_tracker = []
    generation = create_initial_population(number_of_cities, number_of_genes, maximum_lenght)
    
    sample_gene = generation[random.randint(0,number_of_genes)]
    print(f'Initial Path : {sample_gene.cities} \nInitial distance : {sample_gene.distance} \nInitial fitness : {sample_gene.fitness}')
    show_initial_city_path(sample_gene)

    for _ in range(number_of_generations):
        sorted_generation = sorted(generation, key=lambda gene: gene.distance)
        distance_progress_tracker.append(sorted_generation[0].distance)
        fitness_progress_tracker.append(sorted_generation[0].fitness)

        new_generation = []
        new_generation.extend( sorted_generation[:number_of_elites] ) 

        while len(new_generation) < number_of_genes:
            first_parent , second_parent = roulette_selection(sorted_generation)
            #first_parent , second_parent = tournament_selection(sorted_generation)
            first_child = mate(first_parent, second_parent)
            second_child = mate(second_parent, first_parent)
            mutation_reverse_city_segment(first_child, chance_for_mutation)
            mutation_reverse_city_segment(second_child, chance_for_mutation)
            new_generation.extend([first_child, second_child])
        generation = new_generation
    
    sorted_generation = sorted(generation, key=lambda gene: gene.distance)
    distance_progress_tracker.append(sorted_generation[0].distance)
    fitness_progress_tracker.append(sorted_generation[0].fitness)
    print(f'\nBest Path : {sample_gene.cities} \Best distance : {sample_gene.distance} \Best fitness : {sample_gene.fitness}')
    show_results_progress(sorted_generation[0],fitness_progress_tracker,distance_progress_tracker)
    
            

if __name__ == "__main__":
    main()   


