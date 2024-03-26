import pygame
from constructors import Passaro, Cano, Chao, desenhar_tela
from AI import create_new_population, new_generation, create_model

class SetupNeuralNetwork:

    def __init__(self, use_neural_net_model, use_trained_model) -> None:
        self.num_population = 100
        self.num_geracoes = 300
        self.geracao = 0
        self.learning_threshold = 1000
        self.input_shape = 3
        self.use_neural_net_model = use_neural_net_model
        self.use_trained_model = use_trained_model

    # def using_trained_model(self):
    #     self.population = create_new_population(self.num_population, self.input_shape)
    #     self.model = create_model(self.input_shape)
    #     self.model.load_params()

    #     self.population[0][2] = self.model.get_weights()
    #     self.learning_threshold = 100000

    #     self.main()
    
    # def new_training_routine(self):
    #     self.population = create_new_population(self.num_population, self.input_shape)
    #     self.model = create_model(self.input_shape)

    #     for g in range(self.num_geracoes):
    #         self.geracao += 1
    #         self.main()
    #         self.print_results(self.geracao, self.population)
    #         self.population = new_generation(self.population, self.input_shape)

    def setup_new_generation(self):
        self.geracao += 1
        self.population = new_generation(self.population, self.input_shape)
    
    def setup_population(self):
        self.population = create_new_population(self.num_population, self.input_shape)
        self.model = create_model(self.input_shape)

        if self.use_trained_model:
            self.model.load_params()
            self.population[0][2] = self.model.get_weights()
            self.learning_threshold = 100000
            
    def increase_fitness(self, idx_passaro):
        fitness = 0.1
        self.population[idx_passaro][1] += fitness
    
    def increse_fitness_passing_cano(self, idx):
        fitness = 20
        self.population[idx][1] += fitness

class Game(SetupNeuralNetwork):

    def __init__(self, use_neural_net_model = True, use_trained_model = False) -> None:
        # Definições gerais do jogo como tamanho da tela e imagens usadas
        self.tela_altura = 800
        self.tela_largura = 500
        super().__init__(use_neural_net_model, use_trained_model)

        if not use_neural_net_model or use_trained_model:
            self.num_population = 1
            self.num_geracoes = 1
        
        if not use_neural_net_model:
            self.use_trained_model = None

    def init_objects(self):
        self.passaros = [Passaro(230, 350) for p in range(self.num_population)]
        self.chao = Chao(730)
        self.canos = [Cano(550)]
        self.tela = pygame.display.set_mode((self.tela_largura, self.tela_altura))
        self.pontos = 0
        self.relogio = pygame.time.Clock()

    def listening_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
                pygame.quit()
                quit()
            
            #if evento.type == pygame.KEYDOWN:
            #   if evento.key == pygame.K_SPACE:
            #      for passaro in passaros:
            #         passaro.pular()

    def verify_if_contain_passaros(self, passaros):
        if len(passaros) > 0:
            return True
        else:
            return False
        
    def setup_index_cano(self, passaros, canos):
        '''Este índice é usado quando a dois canos na tela, sendo este índice utilizado
            para passar as informações do segundo cano para a Rede neural'''
        if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].cano_topo.get_width()):
            self.indice_cano = 1
        else:
            self.indice_cano = 0

    def verify_state_passaros(self, passaros, canos):
        contain_passaros = self.verify_if_contain_passaros(passaros)

        if contain_passaros:
            self.setup_index_cano(passaros, canos)
        else:
            self.rodando = False

    def moving_passaro(self, idx_passaro, passaro):
            passaro.mover()

            if self.use_neural_net_model:
                self.increase_fitness(idx_passaro)
                prediction = self.predict_move_with_model(idx_passaro, passaro)
            else:
                prediction = self.predict_move_with_calc(passaro)

            if prediction:
                passaro.pular()
    
    def predict_move_with_calc(self, passaro):
        calculo_decisao = ((passaro.y - self.canos[self.indice_cano].pos_base) / self.tela_altura) + ((passaro.y - self.canos[self.indice_cano].altura) / self.tela_altura)
        if calculo_decisao > 0:
           return True
        return False

    def predict_move_with_model(self, idx_passaro, passaro):
        dados = [passaro.y, (passaro.y - self.canos[self.indice_cano].altura), (passaro.y - self.canos[self.indice_cano].pos_base)]
            
        weights = self.population[idx_passaro][2]
        self.model.set_weights(weights)
        prediction = self.model.predict(dados)
        if prediction[0] > 0.75:
            return True
        return False

    def check_colision(self, i, cano, passaro):
        if cano.colidir(passaro):
            self.passaros.pop(i)
            self.population[i][1] -= 1
        elif (passaro.y + passaro.imagem.get_height()) > self.chao.y or passaro.y < 0:
            self.passaros.pop(i)
            self.population[i][1] -= 10

    def check_learning_threshold(self, idx):
        if self.population[idx][1] >= self.learning_threshold:
            weights = self.population[idx][2]
            self.model.set_weights(weights)
            self.model.save_params()
            self.rodando = False
            pygame.quit()
            quit()

    def add_cano(self):
        self.pontos += 1
        self.canos.append(Cano(600))

    def check_remove_canos(self, cano):
        if cano.x + cano.cano_topo.get_width() < 0:
            self.canos.remove(cano)

    def main(self):

        self.init_objects()
        self.rodando = True

        while self.rodando:
            self.relogio.tick(30)

            self.listening_events()
            self.verify_state_passaros(self.passaros, self.canos)
            
            self.chao.mover()

            for i, passaro in enumerate(self.passaros):
                self.moving_passaro(i, passaro)

            for cano in self.canos:
                for i, passaro in enumerate(self.passaros):
                    #self.moving_passaro(i, passaro)
                    self.check_colision(i, cano, passaro)

                    if not cano.passou and passaro.x > cano.x:
                        cano.passou = True
                        self.add_cano()

                        if self.use_neural_net_model:
                            self.increse_fitness_passing_cano(i)
                            self.check_learning_threshold(i)

                cano.mover()
                self.check_remove_canos(cano)

            desenhar_tela(self.tela, self.tela_largura, self.passaros, self.canos, self.chao, self.pontos, self.geracao)

    def print_results(self, geracao, population, show_individuos = 2):
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

    def init_game(self):

        if self.use_neural_net_model:
            self.setup_population()
        else:
            print("Using manual calculation")

        for g in range(self.num_geracoes):
            self.main()
            if not self.use_trained_model:
                self.print_results(self.geracao, self.population)
                self.population = new_generation(self.population, self.input_shape)

if __name__ == '__main__':
    use_neural_net_model = True
    use_trained_model = True
    game_app = Game(use_neural_net_model, use_trained_model,)
    game_app.init_game()
