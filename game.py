
import numpy as np

from copy import copy

class Connect4Game(object):
    """A Connect 4 game model that contains the game states and some
       (very) simple utilities for the game.
    """

    def __init__(self, p1, p2, init_board=None):
        """The game state should be initialized with two players, which can be
           two humans or two computers. From this, a numpy array is created,
           which is how game states are tracked.
        """
        if init_board is None or \
           type(init_board) != np.ndarray:
            self.initialize_board()
        else:
            self.board = init_board
        self.turn = p1 # Player one goes first.

        ## Easily accessible player objects.
        self.players = {'1': p1, '2': p2}

        ## The logic for setting player names.
        p1_name, p2_name = None, None

        if p1.type == 'human':
            p1_name = raw_input('What is Player One\'s name? ')

        if p2.type == 'human':
            p2_name = raw_input('What is Player Two\'s name? ')

        self.player_names = {p1: p1_name if p1_name else 'Jarvis',
                             p2: p2_name if p2_name else 'Optimus Prime',}

        self.last_move = ()
        self.winner = None

    def initialize_board(self):
        """Fill the board with zeroes.
        """
        self.board = np.zeros((6, 7), dtype=np.int32)

    def play(self):
        """Evaluates the actual game movements.
        """
        while not self.game_over():
            print(self.board)
            print(self.player_names[self.turn] + '\'s turn to move.')
            print '%' * 80

            ## Use a copy of the board to avoid issues with mutation.
            column_to_move = self.turn.get_move(copy(self.board))

            print self.player_names[self.turn] + ' has moved in column ' + str(column_to_move)

            self.move(self.turn, column_to_move)

        print(self.board)

        if self.winner:
            print('Winner: %s' % self.player_names[self.winner])
        else:
            print('Unfortunate tie.')

    def move(self, player, column):
        """Execute moves for the given player and the given column.
        """
        ## An issue if we run out of possible moves -- we can check against
        ## this by matching the column to 0 values -- if none, we can't move.
        column_space_available = sum(self.board[:, column] == 0) - 1
        if column_space_available == -1:
            return False

        ## TODO: Refactor me!
        if self.turn == player == self.players['1']:
            self.board[column_space_available, column] = 1
            self.turn = self.players['2']
        else:
            self.board[column_space_available, column] = 2
            self.turn = self.players['1']

        self.last_move = (column_space_available, column)
        return True

    def game_over(self):
        """Returns whether the game is won and sets the winner.
        """
        if self.last_move == ():
            return False

        row_num, col_num = self.last_move
        row, col = self.board[row_num, :], self.board[:, col_num]

        diag1 = np.diagonal(self.board, col_num - row_num)
        diag2 = np.diagonal(np.fliplr(self.board), - (col_num +
            row_num - len(self.board)))

        for line in [row, col, diag1, diag2]:
            if line.shape[0] < 4:
                continue ## Continue iterating as there is no 4-in-a-row.

            ## A clever way to check for winners -- for all row and column
            ## combinations, filter 1 and 2 values. If the sum of the boolean
            ## representations == 4, you have four in a row! Else, not.
            for filtered_rows in [line[i:i+4] for i in range(len(line)-3)]:
                if sum(filtered_rows == 1) == 4:
                    self.winner = self.players['1']
                    return True
                elif sum(filtered_rows == 2) == 4:
                    self.winner = self.players['2']
                    return True

        ## If you can't enter anything into the first row of the game,
        ## the game is over.
        if sum(self.board[0] == 0) == 0:
            return True
        return False
