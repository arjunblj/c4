
import numpy as np

class Player(object):
    """A prototype player class which all players should inherit from.
    """

    def __init__(self, p_num, opp_num, type='AI'):
        """p_num is the player's number. opp_num is the opponent's number.
        """
        self.p_num = p_num
        self.opp_num = opp_num
        self.type = type

    def get_move(self, board):
        pass


class Human(Player):
    """The rather sophisticated human player relies on input for the game.
    """

    def __init__(self, p_num, opp_num, type='human'):
        """p_num is the player's number. opp_num is the opponent's number.
        """
        super(Human, self).__init__(p_num, opp_num, type)

    def get_move(self, board):
        """A move as inputted by a user.
        """
        column = int(raw_input('Pick a move between columns 0 through 0. '))

        ## TODO: Fix a bug here with validating inputs more than once.
        if not 0 <= column <= 6:
            column = int(raw_input('Sorry, that\'s not valid, try again. '))

        return column


class RandomAI(Player):
    """A random player.
    """

    def get_move(self, board):
        """The random player simply looks at what columns are free to be moved
           in and returns one of them at random (which move() in the Game
           class uses.)
        """
        free_columns = np.where(board[0] == 0)[0]
        return np.random.choice(free_columns)
