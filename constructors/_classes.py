import os
import random
import pygame

img_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
img_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
img_passaros = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

class Passaro:
    # Definições gerais das imagens e parâmetros que serão usados
    # Imagens dos passaros
    imgs = img_passaros
    # Quanto será o máximo que  ele irá rotacionar para cima
    rotacao_maxima = 25
    # QUal a velocidade que ele irá rotacionar caindo
    velocidade_rotacao = 20
    # tempo de animação para definir a imagem do passaro a ser usada
    tempo_animacao = 5

    def __init__(self, x, y):
        # Parâmetros iniciais de cada passaro
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.imgs[0]

    def pular(self):
        # Função pular definine a velocidade, tempo e altura iniciais para a formula mover()
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # A cada iteração acrescenta 1 no tempo e recalcula a formula do deslocamento em parabola
        self.tempo += 1
        deslocamento = 1.6 * (self.tempo ** 2) + self.velocidade * self.tempo

        # Primeiro, coloca um limite para o deslocamento quando o passaro estiver caindo, sendo no máximo 16
        if deslocamento > 16:
            deslocamento = 16
        # Em seguida, verifica de o passaro está subindo, e acrescenta mais n unidades para subir mais um pouco
        # No código original era 2 unidades. Achei mais interessante colocar zero.
        elif deslocamento < 0:
            deslocamento -= 0

        # Definine a posição y do passaro como o seu valor de deslocamento
        # É essa linha que irá mudar a posição do passaro
        self.y += deslocamento

        # Nesse bloco será definida a rotação do passaro, sendo valores negativos rotacionar em sentido horário e
        # positivo, anti-horário. Primeiro verifica se o passaro está subindo
        if deslocamento < 0 or self.y < (self.altura + 50):
            # Em seguida, verifica se o angulo é menor do que a rotação máxima permitida. Caso True, defini-se a
            # rotação máxima como o angulo
            if self.angulo < self.rotacao_maxima:
                self.angulo = self.rotacao_maxima
        # Caso o passaro esteja descendo,ele irá diminuir o angulo pela velocidade_rotacao até que chegue a -90 graus
        else:
            if self.angulo > -90:
                self.angulo -= self.velocidade_rotacao

    def desenhar(self, tela):
        # Definir qual imagem do passaro vai usar
        # A cada frame, irá chamar o desenhar tela e acrescenta 1 na contagem imagem para verificar em qual frame está
        # O tempo_animação define quantos frames cada imagem irá ficar na tela
        # Com isso é feita uma verificação de qual frame está e define a imagem que será exibida, dando o efeito do
        # passaro batendo asas.
        self.contagem_imagem += 1

        if self.contagem_imagem < self.tempo_animacao:
            self.imagem = self.imgs[0]
        elif self.contagem_imagem < self.tempo_animacao * 2:
            self.imagem = self.imgs[1]
        elif self.contagem_imagem < self.tempo_animacao * 3:
            self.imagem = self.imgs[2]
        elif self.contagem_imagem < self.tempo_animacao * 4:
            self.imagem = self.imgs[1]
        elif self.contagem_imagem >= self.tempo_animacao * 4 + 1:
            self.imagem = self.imgs[0]
            self.contagem_imagem = 0

        # Regra para se o passaro estiver caindo, não vou bater asa. ou seja, fixa uma imagem
        if self.angulo <= -80:
            self.imagem = self.imgs[1]
            self.contagem_imagem = self.tempo_animacao * 2

        # Desenhar imagem
        # Rotacionar imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        # Achar a posição do centro da imagem original
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        # Achar a posição do centro da imagem rotacionada
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        # Desenhar imagem rotacionada na tela
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        # Função coloca um máscara na imagem para identificar a colição corretamente.
        return pygame.mask.from_surface(self.imagem)


class Cano:
    # Definições gerais da classe cano
    # Distancia entre o cano de cima e o cano de baixo
    distancia = 200
    # Velocidade horizontal do cano
    velocidade = 5
    # Velocidade vertival do cano
    vel_cano = 3

    def __init__(self, x):
        # parametros iniciais na criação do cano
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        # Como são dois canos, cria-se duas imagens, uma normal e a outra virada de cabeça para baixo.
        self.cano_topo = pygame.transform.flip(img_cano, False, True)
        self.cano_base = img_cano
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        # é definido um valor aleatório para a altura dos canos
        self.altura = random.randrange(50, 450)
        # O cano topo ficara posicionado na altura aleatória e o cano base vai ficar na altura mais a distancia de
        # separação entre os canos
        self.pos_topo = self.altura - self.cano_topo.get_height()
        self.pos_base = self.altura + self.distancia

    def mover(self):
        # Este if define se o cano vai para cima ou para baixo de acordo com a posição que ele estiver
        if self.pos_base >= 640:
            self.vel_cano = -3
        elif self.pos_base <= 300:
            self.vel_cano = 3

        # Movimetno vertical
        #self.pos_topo += self.vel_cano
        #self.pos_base += self.vel_cano
        # Movimento Horizontal
        self.x -= self.velocidade

    def desenhar(self, tela):
        # Desenha  os canos na tela
        tela.blit(self.cano_topo, (self.x, self.pos_topo))
        tela.blit(self.cano_base, (self.x, self.pos_base))

    def colidir(self, passaro):
        # Essa função verifica se o cano está colidindo com o passaro
        # Primerio busca a mascara do passaro
        passaro_mask = passaro.get_mask()
        # depois cria as mascaras dos canos
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)

        # Calcula a distancia entre o x e y  do passaro e do cano
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        # pygame já oferece uma função que verifica se ha a colisão e retorna true ou false
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        # Faz e verificação e retorna true se o pasasro está colidindo
        if topo_ponto or base_ponto:
            return True
        else:
            return False


class Chao:
    # Definições gerais da classe choa
    # Velocidade do chao
    velocidade = 5
    # Largura da imagem chao
    largura = img_chao.get_width()
    # Definição da imagem chao
    imagem = img_chao

    def __init__(self, y):
        # Parametros de inicialização do chao
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        # Movimentação horizontal do chao
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        # Verifica se o chao já saiu da tela. Se true, coloca este chão em seguida ddo outro
        if self.x1 + self.largura < 0:
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura

    def desenhar(self, tela):
        # Desenha o chao na tela
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))