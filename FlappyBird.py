import os
import numpy as np
import tensorflow as tf
import pygame
from constructors import Passaro, Cano, Chao, desenhar_tela
from AI import create_new_population, new_generation, create_model

# Definições gerais do jogo como tamanho da tela e imagens usadas
tela_altura = 800
tela_largura = 500

#Configuração da Rede neural e Algoritimo genético
num_population = 20
num_geracoes = 300
geracao = 0

input_shape = 3

if not os.path.isdir("checkpoint"):
    os.mkdir("checkpoint")

@tf.function(reduce_retracing=True)
def predict_function(model, input_data):
    return model(input_data, training=False)

def save_model(model):
    print("Salvando modelo")
    model.save_weights('./checkpoint/my_checkpoint')

def load_model(model):
    print("Carregando modelo")
    model.load_weights('./checkpoint/my_checkpoint')
    return model

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
                save_model(model)
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

            '''x1 = passaro.y
            x2 = canos[indice_cano].pos_base
            x3 = canos[indice_cano].altura
            dados = [[x1, x2, x3]]'''
            #calculo_decisao = ((passaro.y - canos[indice_cano].pos_base) / tela_altura) + ((passaro.y - canos[indice_cano].altura) / tela_altura)

            #Realizando previsão com a rede neural do passaro
            dados = tf.convert_to_tensor([[passaro.y, 
                                           abs(passaro.y - canos[indice_cano].altura), 
                                           abs(passaro.y - canos[indice_cano].pos_base)]])


            #population[i][1] += (1 - calculo_decisao)
            dados = tf.convert_to_tensor(dados)
            
            weights = population[i][2]
            model.set_weights(weights)
            prediction = predict_function(model, dados)

            #print(x3, prediction.numpy()[0][0])

            if prediction.numpy()[0][0] > 0.7:
                passaro.pular()

            #print(x3)
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

            cano.mover()
            if cano.x + cano.cano_topo.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))

        for cano in remover_canos:
            canos.remove(cano)

        desenhar_tela(tela, tela_largura, passaros, canos, chao, pontos, geracao)

def calcula_geracoes():

    global population
    global num_population
    
    use_model_trained = False

    if use_model_trained:
        num_population = 1
        model = tf.keras.models.load_model("best_model.h5")
        population = create_new_population(num_population, input_shape)
        population[0][2] = model.get_weights()

    else:
        model = create_model(input_shape)
        load_checkpoint = True
        if len(os.listdir('./checkpoint')) > 0 and load_checkpoint:
            model = load_model(model)

        population = create_new_population(num_population, input_shape)

    for g in range(num_geracoes):
        main(model)

        print("Geração: ", g)
        print("Melhores Individuos: ")

        show_individuos = 2

        population_sorted = sorted(population, key=lambda x: x[1], reverse=True)

        for i in range(show_individuos):
            print(population_sorted[i][:2])

        population = new_generation(population, input_shape)
        #population = create_new_population(num_population, input_shape)

    model.set_weights(population_sorted[0][2])
    save_model(model)

if __name__ == '__main__':
    calcula_geracoes()
