from FlappyBird import Game
import os
import sys

class MockModel:
    def __init__(self) -> None:
        pass

    def load_params(self):
        return "load_params"
    
    def get_weights(self):
        return "get_weights"

def test_init_using_trained_neural_network():
    use_neural_net_model = True
    use_trained_model = True
    newGame = Game(use_neural_net_model, use_trained_model)

    assert newGame.num_population == 1
    assert newGame.num_geracoes == 1
    assert newGame.geracao == 0
    assert newGame.learning_threshold == 1000
    assert newGame.input_shape == 3
    assert newGame.use_neural_net_model == True
    assert newGame.use_trained_model == True

    use_neural_net_model = False
    use_trained_model = True
    newGame = Game(use_neural_net_model, use_trained_model)
    assert newGame.use_neural_net_model == False
    assert newGame.use_trained_model == None
    assert newGame.num_population == 1
    assert newGame.num_geracoes == 1


def test_init_new_training_neural_network():
    use_neural_net_model = True
    use_trained_model = False
    newGame = Game(use_neural_net_model, use_trained_model)

    assert newGame.num_population == 100
    assert newGame.num_geracoes == 300
    assert newGame.geracao == 0
    assert newGame.learning_threshold == 1000
    assert newGame.input_shape == 3
    assert newGame.use_neural_net_model == True
    assert newGame.use_trained_model == False

def test_init_with_manual_calculus():
    use_neural_net_model = False
    newGame = Game(use_neural_net_model)

    assert newGame.num_population == 1
    assert newGame.num_geracoes == 1
    assert newGame.geracao == 0
    assert newGame.learning_threshold == 1000
    assert newGame.input_shape == 3
    assert newGame.use_neural_net_model == False
    assert newGame.use_trained_model == None

def test_init_game(mocker):
    mockPopulation = [[999, 999, 999, 999]]
    mocker.patch('FlappyBird.Game.setup_population', return_value="setup_population")
    mocker.patch('FlappyBird.Game.main', return_value=True)
    mocker.patch('FlappyBird.Game.print_results', return_value=True)
    mocker.patch('FlappyBird.new_generation', return_value=mockPopulation)

    newGame = Game(use_trained_model=False)
    assert newGame.use_trained_model == False

    newGame = Game(use_trained_model=True)
    assert newGame.use_trained_model == True

def test_increase_fitness():
    mockPopulation = [[999, 0, 999, 999]]
    newGame = Game()
    newGame.population = mockPopulation
    newGame.increase_fitness(0)
    assert newGame.population == [[999,0.1,999,999]]

def test_increse_fitness_passing_cano():
    mockPopulation = [[999, 0, 999, 999]]
    newGame = Game()
    newGame.population = mockPopulation
    newGame.increse_fitness_passing_cano(0)
    assert newGame.population == [[999,20,999,999]]