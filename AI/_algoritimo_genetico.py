import numpy as np
from sklearn.metrics import accuracy_score
from AI import create_weights

def create_new_population(num_population, input_shape):
    population = []

    for i in range(num_population):
        weights = create_weights(input_shape)
        initial_score = 0
        population.append([i, initial_score, weights])
        
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

def reset_scores(population):

    for i in range(len(population)):
        population[i][1] = 0
        population[i][0] = i

    return population

def new_generation(scores, input_shape):
    population_sorted = sorted(scores, key=lambda column: column[1], reverse=True)
    
    parents = population_sorted[:4]
    new_individuos = create_new_population(2, input_shape)
    
    weights_parent_1 = parents[0][2]
    weights_parent_2 = parents[1][2]

    parents[2][2] = mutation(weights_parent_1, mutation_rate=0.3)
    parents[3][2] = mutation(weights_parent_2, mutation_rate=0.3)

    alredy_individuos = len(parents) + len(new_individuos)
    num_par_offsprings = int((len(scores)-alredy_individuos)/2)
    
    for i in range(num_par_offsprings):
    
        offspring_1, offspring_2 = crossover(weights_parent_1, weights_parent_2)
        
        offspring_1_mutation = mutation(offspring_1, mutation_rate=0.3)
        offspring_2_mutation = mutation(offspring_2, mutation_rate=0.3)
        
        population_sorted[i+alredy_individuos][2] = offspring_1_mutation
        population_sorted[i+alredy_individuos+num_par_offsprings][2] = offspring_2_mutation
            
    offsprings = population_sorted[alredy_individuos:]
    
    new_generation = parents + new_individuos + offsprings

    new_generation_reseted_scores = reset_scores(new_generation)

    return new_generation_reseted_scores