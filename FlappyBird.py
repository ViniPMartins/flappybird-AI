import os
import random
import neat
import pygame
from constructors import Passaro, Cano, Chao

# Variaveis para ativar e desativar IA e contar geração
ativar_ai = True
geracao = 0

IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
# Inicia textos
pygame.font.init()
fonte_principal = pygame.font.SysFont('arial', 50)

# Definições gerais do jogo como tamanho da tela e imagens usadas
tela_largura = 500
tela_altura = 800

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto1 = fonte_principal.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto1, ((tela_largura - 10 - texto1.get_width()), 10))

    if ativar_ai:
        texto2 = fonte_principal.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit(texto2, ((tela_largura - 10 - texto2.get_width()), (texto1.get_height() + 10)))

    chao.desenhar(tela)
    pygame.display.update()

'''main'''

def main(genomas, config):  # fitness function

    if ativar_ai:
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
    else:
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
            if not ativar_ai:
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
            # aumentar o fitness
            if ativar_ai:
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
                    if ativar_ai:
                        lista_genomas[i].fitness -= 1
                        lista_genomas.pop(i)
                        redes.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True

            cano.mover()
            if cano.x + cano.cano_topo.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
            if ativar_ai:
                for genoma in lista_genomas:
                    genoma.fitness += 5

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
                if ativar_ai:
                    lista_genomas.pop(i)
                    redes.pop(i)

        '''if len(passaros) == 0:
            rodando = False
            main()'''

        desenhar_tela(tela, passaros, canos, chao, pontos)


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

        populacao.run(main, 50)
    else:
        main(None, None)


if __name__ == '__main__':
    caminho_local = os.path.dirname(__file__)
    caminho_config = os.path.join(caminho_local, 'Config_rede.txt')
    rodar(caminho_config)
