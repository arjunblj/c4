
from game import *
from players import *

if __name__ == "__main__":

    p1 = MinimaxAI(1, 2, 4)
    # p2 = RandomAI(2, 1)

    p2 = Human(1, 2)

    game = Connect4Game(p1, p2)
    game.play()