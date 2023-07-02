import numpy as np
from sklearn.metrics import accuracy_score
from AI import create_weights

def create_first_generation(num_population):
    print("Criando População. Quantidade: ", num_population)
    population = np.empty(num_population, dtype=object)

    for i in range(num_population):
        weights = create_weights(3)
        initial_score = 0
        population[i] = [i, initial_score, weights]
        
    return population
   
def crossover(weights_parents_1, weights_parents_2):
    
    num_params_1 = len(weights_parents_1)
    num_params_2 = len(weights_parents_2)
    verification = num_params_1 == num_params_2
    assert verification, f"A quantidade de parametros não é igual. O modelo 1 tem {num_params_1} e o modelo 2 tem {num_params_2}"

    offspring_1 = []
    offspring_2 = []

    for i in range(num_params_1):
        parent_1 = weights_parents_1[i]
        parent_2 = weights_parents_2[i]

        mask = np.random.randint(0, 2, parent_1.shape)

        offspring_1.append((parent_1*mask) + (parent_2*(1-mask)))
        offspring_2.append((parent_2*mask) + (parent_1*(1-mask)))

    return offspring_1, offspring_2

def mutation(weights, mutation_rate = 0.1):
    for i in range(len(weights)):

        if len(weights[i].shape) == 1:
            for j in range(weights[i].shape[0]):
                if np.random.random() <= mutation_rate:
                    new_bias = np.random.random()
                    weights[i][j] = new_bias

        else:
            for j in range(weights[i].shape[0]):
                for k in range(weights[i].shape[1]):
                    if np.random.random() <= mutation_rate:
                        new_bias = np.random.random()
                        weights[i][j][k] = new_bias
                        
    return weights

def new_generation(scores):
    population_sorted = sorted(scores, key=lambda column: column[1], reverse=True)
    
    parents = population_sorted[:2]
    
    weights_parent_1 = parents[0][2]
    weights_parent_2 = parents[1][2]
    num_par_offsprings = int((len(scores)-2)/2)
    
    for i in range(num_par_offsprings):
    
        offspring_1, offspring_2 = crossover(weights_parent_1, weights_parent_2)
        
        offspring_1_mutation = mutation(offspring_1)
        offspring_2_mutation = mutation(offspring_2)
        
        population_sorted[i+2][2] = offspring_1_mutation
        population_sorted[i+2+num_par_offsprings][2] = offspring_2_mutation
        
    offsprings = population_sorted[2:]
    
    new_generation = parents + offsprings
    return new_generation