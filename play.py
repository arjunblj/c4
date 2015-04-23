
from game import *
from players import *

if __name__ == "__main__":

    p1 = Human(1, 2)
    # p2 = RandomAI(2, 1)

    p2 = MinimaxAI(2, 1, 4)

    game = Connect4Game(p1, p2)
    game.play()