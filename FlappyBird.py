import os
import pygame
from constructors import Passaro, Cano, Chao, desenhar_tela
from AI import create_new_population, new_generation, create_model

# Definições gerais do jogo como tamanho da tela e imagens usadas
tela_altura = 800
tela_largura = 500

#Configuração da Rede neural e Algoritimo genético
num_population = 100
num_geracoes = 300
geracao = 0
learning_threshold = 1000

input_shape = 3

def main(model):
    passaros = [Passaro(230, 350) for p in range(num_population)]

    chao = Chao(730)
    canos = [Cano(550)]
    tela = pygame.display.set_mode((tela_largura, tela_altura))
    pontos = 0
    relogio = pygame.time.Clock()

    global geracao
    geracao += 1
    rodando = True
    while rodando:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            #if evento.type == pygame.KEYDOWN:
             #   if evento.key == pygame.K_SPACE:
              #      for passaro in passaros:
               #         passaro.pular()

        indice_cano = 0                
        if len(passaros) > 0:
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].cano_topo.get_width()):
                '''Este índice é usado quando a dois canos na tela, sendo este índice utilizado
                para passar as informações do segundo cano para a Rede neural'''
                indice_cano = 1
        else:
            rodando = False
        
        for i, passaro in enumerate(passaros):
            passaro.mover()

            #aumentando score do passaro
            fitness = 0.1
            population[i][1] += fitness

            #calculo_decisao = ((passaro.y - canos[indice_cano].pos_base) / tela_altura) + ((passaro.y - canos[indice_cano].altura) / tela_altura)

            #Realizando previsão com a rede neural do passaro
            dados = [passaro.y, (passaro.y - canos[indice_cano].altura), (passaro.y - canos[indice_cano].pos_base)]
            
            weights = population[i][2]
            model.set_weights(weights)
            prediction = model.predict(dados)

            if prediction[0] > 0.75:
                passaro.pular()

            #if x3 > 0:
            #    passaro.pular()

        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    population[i][1] -= 1
                elif (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                    passaros.pop(i)
                    population[i][1] -= 10

                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
                    #Adicionar o score
                    fitness = 20
                    population[i][1] += fitness
                    if population[i][1] >= learning_threshold:
                        weights = population[i][2]
                        model.set_weights(weights)
                        model.save_params()
                        rodando = False
                        pygame.quit()
                        quit()

            cano.mover()
            if cano.x + cano.cano_topo.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))

        for cano in remover_canos:
            canos.remove(cano)

        desenhar_tela(tela, tela_largura, passaros, canos, chao, pontos, geracao)


def print_results(geracao, population, show_individuos = 2):
    print(f"\nGeração: {geracao}")
    print("Melhores Individuos: ")

    population_sorted = sorted(population, key=lambda x: x[1], reverse=True)

    print("Parâmetros melhor Individuo: \n", population_sorted[0][2])

    print(f"{'Id':^5} | {'Age':^5} | {'fitness':^5}")
    print(f"{'-'*5} | {'-'*5} | {'-'*5}")

    for i in range(show_individuos):
        id = population_sorted[i][0]
        fitness = population_sorted[i][1]
        age = population_sorted[i][3]
        print(f"{id:^5} | {age:^5} | {fitness:^5.4f}")

    print("\n")


def calcula_geracoes():

    global population
    global num_population
    global learning_threshold

    use_trained_model = False

    if use_trained_model:
        num_population = 1
        population = create_new_population(num_population, input_shape)

        model = create_model(input_shape)
        model.load_params()

        population[0][2] = model.get_weights()
        learning_threshold = 100000

    else:
        model = create_model(input_shape)
        population = create_new_population(num_population, input_shape)

    for g in range(num_geracoes):
        main(model)

        print_results(geracao, population)

        population = new_generation(population, input_shape)

if __name__ == '__main__':
    calcula_geracoes()
