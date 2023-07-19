import numpy as np
from sklearn.metrics import accuracy_score
from AI import create_weights
from math import floor
from copy import deepcopy

def create_new_population(num_population, input_shape):
    population = []

    for i in range(num_population):
        weights = create_weights(input_shape)
        initial_score = 0
        age = 0
        population.append([i, initial_score, weights, age])
        
    return population
   
def crossover(weights_parents_1, weights_parents_2):
    
    num_params_1 = len(weights_parents_1)
    num_params_2 = len(weights_parents_2)
    verification = num_params_1 == num_params_2
    assert verification, f"A quantidade de parametros não é igual. O modelo 1 tem {num_params_1} e o modelo 2 tem {num_params_2}"

    offspring_1 = []

    for i in range(num_params_1):
        parent_1 = weights_parents_1[i]
        parent_2 = weights_parents_2[i]

        mask = np.random.randint(0, 2, parent_1.shape)

        offspring_1.append((parent_1*mask) + (parent_2*(1-mask)))

    return offspring_1

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
        population[i][0] = i
        population[i][1] = 0
        population[i][3] += 1

    return population

def make_parents(population, elitism):

    verification = (len(population) >= elitism)
    msg = f"A quantidade da população ({len(population)}) deve ser maior ou igual a quantidade do elitsmo ({elitism})"
    assert verification, msg

    parents = population[:elitism]
    #print(parents)
    return parents

def make_survivors(population, elitism, survival_threshold, crossover_rate, mutation_rate):

    n_survival = floor(len(population)*survival_threshold)

    survivors = deepcopy(population[:n_survival])
    for i in range(n_survival):

        weights_individuo = survivors[i][2]

        if np.random.random() <= crossover_rate and n_survival > 1:
            idx1 = 0
            idx2 = np.random.randint(1, n_survival)
            weights_1 = survivors[idx1][2]
            weights_2 = survivors[idx2][2]

            weights_individuo = crossover(weights_1, weights_2)
        
        survivors[i][2] = mutation(weights_individuo, mutation_rate)

    return survivors

def make_new_individuos(input_shape, n_population, n_parents, n_survivors):

    n_new_individuos = n_population - n_parents - n_survivors

    new_individuos = create_new_population(n_new_individuos, input_shape)
    return new_individuos

def new_generation(population, input_shape, elitism=2, survival_threshold=0.2, crossover_rate=0.5, mutation_rate=0.1):
    '''
    Coisas a adicionar:
    - OK Nº de individuos que vão para a próxima geração (Elitismo ou parents)
    - OK % da especie que passa para a próxima geração (survival_threshold)
    - OK % de crossover (crossover_rate)
    - % de mutatation (mutation_rate)
    '''

    population_sorted = sorted(population, key=lambda column: column[1], reverse=True)

    #print(population_sorted[:2], '\n')

    parents = make_parents(population_sorted, elitism)

    survivors = make_survivors(population_sorted, elitism, survival_threshold, crossover_rate, mutation_rate)

    n_population = len(population)
    n_parents = len(parents)
    n_survivors = len(survivors)
    new_individuos = make_new_individuos(input_shape, n_population, n_parents, n_survivors)
    
    new_generation = parents + survivors + new_individuos

    print(f'Mantendo: {n_parents} melhores individuos \nCriando: {n_survivors} sobreviventes \nCriando: {n_population - n_parents - n_survivors} novos individuos')

    new_generation_reseted_scores = reset_scores(new_generation)

    return new_generation_reseted_scores