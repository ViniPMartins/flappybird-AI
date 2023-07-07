import os
import neat
import pygame
from constructors import Passaro, Cano, Chao, desenhar_tela

# Variaveis para ativar e desativar IA e contar geração
ativar_ai = True
geracao = 0

# Definições gerais do jogo como tamanho da tela e imagens usadas
tela_altura = 800
tela_largura = 500

'''main'''
def main_ai(genomas, config):
    global geracao
    geracao += 1
    lista_genomas = []
    redes = []
    passaros = []
    for _, genoma in genomas:
        rede = neat.nn.FeedForwardNetwork.create(genoma, config)
        redes.append(rede)
        genoma.fitness = 0
        lista_genomas.append(genoma)
        passaros.append(Passaro(230, 350))

    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((tela_largura, tela_altura))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

        indice_cano = 0
        if len(passaros) > 0:
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].cano_topo.get_width()):
                indice_cano = 1
        else:
            rodando = False

        for i, passaro in enumerate(passaros):
            passaro.mover()
            # aumentar o fitness
            lista_genomas[i].fitness += 0.1
            # dar informações para rede neural
            output = redes[i].activate((passaro.y,
                                        abs(passaro.y - canos[indice_cano].altura),
                                        abs(passaro.y - canos[indice_cano].pos_base)))  # Output entre -1 e 1. Se Output > 0,5, pular.
            if output[0] > 0.5:
                passaro.pular()

        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    lista_genomas[i].fitness -= 1
                    lista_genomas.pop(i)
                    redes.pop(i)

                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True

                if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                    passaros.pop(i)
                    lista_genomas.pop(i)
                    redes.pop(i)

            cano.mover()

            if cano.x + cano.cano_topo.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
            for genoma in lista_genomas:
                genoma.fitness += 5

        for cano in remover_canos:
            canos.remove(cano)

        desenhar_tela(tela, tela_largura, passaros, canos, chao, pontos, ativar_ai, geracao)

def main():  # fitness function
    passaros = [Passaro(230, 350)]

    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((tela_largura, tela_altura))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        indice_cano = 0
        if len(passaros) > 0:
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].cano_topo.get_width()):
                indice_cano = 1
        else:
            rodando = False

        for i, passaro in enumerate(passaros):
            passaro.mover()

        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)

                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True

                if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                    passaros.pop(i)

            cano.mover()
            if cano.x + cano.cano_topo.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))

        for cano in remover_canos:
            canos.remove(cano)

        desenhar_tela(tela, tela_largura, passaros, canos, chao, pontos)


def rodar(caminho_config):
    # Passar Fitness function e o número de gerações para rodar
    if ativar_ai:
        config = neat.config.Config(neat.DefaultGenome,
                                    neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation,
                                    caminho_config)

        populacao = neat.Population(config)
        populacao.add_reporter(neat.StdOutReporter(True))
        populacao.add_reporter(neat.StatisticsReporter())

        populacao.run(main_ai, 50)
    else:
        main()


if __name__ == '__main__':
    caminho_local = os.path.dirname(__file__)
    caminho_config = os.path.join(caminho_local, 'Config_rede.txt')
    rodar(caminho_config)
