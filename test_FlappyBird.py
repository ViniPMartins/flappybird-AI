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

def test_init():
    newGame = Game(False)

    assert newGame.num_population == 100
    assert newGame.num_geracoes == 300
    assert newGame.geracao == 0
    assert newGame.learning_threshold == 1000
    assert newGame.input_shape == 3
    assert newGame.use_trained_model == False

def test_init_generations(mocker):
    mocker.patch('FlappyBird.Game.new_training_routine', return_value="new_training_routine")
    mocker.patch('FlappyBird.Game.using_trained_model', return_value="using_trained_model")
    
    newGame = Game(False)
    assert newGame.use_trained_model == False

    newGame = Game(True)
    assert newGame.use_trained_model == True


def test_using_trained_model(mocker):
    mockPopulation = [[999, 999, 999, 999]]
    mocker.patch('FlappyBird.create_new_population', return_value=mockPopulation)
    mocker.patch('FlappyBird.create_model', return_value=MockModel())
    mocker.patch('FlappyBird.Game.main', return_value=True)
    
    newGame = Game(True)
    newGame.using_trained_model()
    assert newGame.num_population == 1
    assert newGame.population == [[999,999,'get_weights',999]]
    assert isinstance(newGame.model, MockModel)
    assert newGame.learning_threshold == 100000

def test_new_training_routine(mocker):
    mockPopulation = [[999, 999, 999, 999]]
    mocker.patch('FlappyBird.create_model', return_value=MockModel())
    mocker.patch('FlappyBird.create_new_population', return_value=mockPopulation)
    mocker.patch('FlappyBird.new_generation', return_value=mockPopulation)
    mocker.patch('FlappyBird.Game.main', return_value=True)
    mocker.patch('FlappyBird.Game.print_results', return_value=True)

    newGame2 = Game()
    newGame2.new_training_routine()
    assert isinstance(newGame2.model, MockModel)
    assert newGame2.population == [[999,999,999,999]]
    assert newGame2.geracao == newGame2.num_geracoes