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
num_population = 30
num_geracoes = 50
geracao = 0

input_shape = 3

@tf.function(reduce_retracing=True)
def predict_function(model, input_data):
    return model(input_data, training=False)

def main():
    passaros = [Passaro(230, 350) for p in range(num_population)]

    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((tela_largura, tela_altura))
    pontos = 0
    relogio = pygame.time.Clock()

    model = create_model(input_shape)

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

            x1 = passaro.y
            x2 = canos[indice_cano].pos_base
            x3 = canos[indice_cano].altura
            #calculo_decisao = ((passaro.y - canos[indice_cano].pos_base) / tela_altura) + ((passaro.y - canos[indice_cano].altura) / tela_altura)

            #Realizando previsão com a rede neural do passaro
            #dados = tf.convert_to_tensor([[passaro.y, 
            #                               abs(passaro.y - canos[indice_cano].altura), 
            #                               abs(passaro.y - canos[indice_cano].pos_base)]])


            #population[i][1] += (1 - calculo_decisao)
            dados = tf.convert_to_tensor([[x1, x2, x3]])
            
            weights = population[i][2]
            model.set_weights(weights)
            prediction = predict_function(model, dados)

            #print(x3, prediction.numpy()[0][0])
            if np.argmax(prediction) == 1:
                passaro.pular()

            #print(x3)
            #if x3 > 0:
            #    passaro.pular()

        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro) or (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                    passaros.pop(i)
                    population[i][1] -= 1

                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
                    #Adicionar o score
                    fitness = 5
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
    population = create_new_population(num_population, input_shape)

    for g in range(num_geracoes):
        main()
        print("Geração: ", g)
        print("Melhores Individuos: ")

        show_individuos = 2

        for i in range(show_individuos):
            print(sorted(population, key=lambda x: x[1], reverse=True)[i][:2])

        population = new_generation(population, input_shape)

if __name__ == '__main__':
    calcula_geracoes()
