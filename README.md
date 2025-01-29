## Task
A traveling salesperson needs to visit multiple cities. Their goal is to minimize travel costs, where the cost of transportation is proportional to the travel distance. Therefore, they aim to find the shortest possible route while visiting each city exactly once. Since they must return to the starting city, the route forms a closed loop.

## Assignment
A set of at least 20 cities (ranging from 20 to 40) is given, each with coordinates defined as integer values X and Y. These coordinates are randomly generated (e.g., within a map of 200 × 200 km). The travel cost between two cities corresponds to the Euclidean distance, calculated using the Pythagorean theorem. The total route length is determined by a permutation (order) of the cities. The goal is to find a permutation that results in the shortest possible total distance.

## Solutions
### Genetic algorithm

#### Implementation

1. **Initialization**: A random population of genes (routes) is generated, where each gene represents a different order of cities.
2. **Fitness Calculation**: The fitness of each gene is inversely proportional to the total distance of the route (shorter distances yield higher fitness values).
3. **Selection**: Two selection methods are provided:
   - **Roulette Wheel Selection**: Genes are chosen probabilistically based on their fitness.
   - **Tournament Selection**: A subset of genes competes, and the best among them is selected as a parent.
4. **Crossover (Mating)**: A permutation-based crossover method is used to create offspring from two parent solutions.
5. **Mutation**: Several mutation strategies can be applied with a small probability to introduce diversity and prevent premature convergence:
   - **Reverse Segment Mutation**: A random segment of the route is reversed.
   - **Neighbor Swap Mutation**: Adjacent cities are randomly swapped.
   - **Random Swap Mutation**: Two random cities in the route are swapped.
6. **Elitism**: A portion of the best-performing genes is carried over to the next generation to retain high-quality solutions.
7. **Iteration**: The process repeats for a set number of generations, refining the routes over time.

#### Visualization

The algorithm tracks progress over generations by plotting:
- The best route found by the algorithm.
- Fitness progression over generations.
- Distance progression over generations.


### Tabu search algorithm

#### Implementation 

1. **Path Representation**: A path represents a specific sequence of cities to be visited.
2. **Neighborhood Generation**: A set of neighboring solutions is created by selecting two random indices and reversing the segment between them.
3. **Tabu List**: Recently visited solutions are stored in a tabu list to prevent cycling back to them. The list maintains a limited number of entries.
4. **Best Neighbor Selection**: Among non-tabu neighbors, the one with the shortest path is chosen.
5. **Stopping Criteria**: The algorithm runs for a fixed number of iterations, updating the best solution whenever an improvement is found.

Visualization
The algorithm provides graphical outputs to demonstrate:
- Initial path visualization.
- Best path found after iterations.
- Fitness progression over the iterations.
