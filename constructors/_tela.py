import os
import pygame

IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
# Inicia textos
pygame.font.init()
fonte_principal = pygame.font.SysFont('arial', 50)

def desenhar_tela(tela, tela_largura, passaros, canos, chao, pontos, geracao):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)

    texto1 = fonte_principal.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto1, ((tela_largura - 10 - texto1.get_width()), 10))

    texto2 = fonte_principal.render(f"Geração: {geracao}", 1, (255, 255, 255))
    tela.blit(texto2, ((tela_largura - 10 - texto2.get_width()), (texto1.get_height() + 10)))

    chao.desenhar(tela)
    pygame.display.update()