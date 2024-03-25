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
    
mockPopulation = [[999, 999, 999, 999]]

def test_init():
    newGame = Game(False)

    assert newGame.num_population == 100
    assert newGame.num_geracoes == 300
    assert newGame.geracao == 0
    assert newGame.learning_threshold == 1000
    assert newGame.input_shape == 3
    assert newGame.use_trained_model == False

# def test_init_generations(mocker):
#     newGame = Game(False)

#     mocker.patch('FlappyBird.Game.new_training_routine', return_value="new_training_routine")
#     assert newGame.init_generations() == 'new_training_routine'

def test_using_trained_model(mocker):
    mocker.patch('FlappyBird.create_new_population', return_value=mockPopulation)
    mocker.patch('FlappyBird.create_model', return_value=MockModel())
    mocker.patch('FlappyBird.Game.main', return_value=True)
    
    newGame = Game(True)
    newGame.using_trained_model()
    assert newGame.num_population == 1
    assert newGame.population == [[999,999,'get_weights',999]]
    assert isinstance(newGame.model, MockModel)
    assert newGame.learning_threshold == 100000
