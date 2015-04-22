
import numpy as np

class Connect4Game(object):

    def __init__(self, init_board=None):
        if init_board is None or \
           type(init_board) != np.ndarray:
            self.initialize_board()
        else:
            self.board = init_board
        self.turn = 1 # Player one goes first.


    def initialize_board(self):
        """
        Fill the board with zeroes
        """
        self.board = np.array([[0] * 8] * 8, np.int32)


    def move(self, player, col):
        """
        Player 1 or 2 makes a move.
        Validate the board before to make sure there are no hanging
        pucks, and then safely add a puck to the top of the given col
        Returns true iff it succeeded in making the move
        """
        if self.turn != player or not self.validate():
            return False

        for i, v in enumerate(self.board.T[col,::-1]):
            if v == 0:
                self.board.T[col][-(i+1)] = player
                self.turn = 3 - player # toggles between 1 & 2
                return True
        # There is no room in this column, can't insert!
        return False


    def validate(self):
        """
        Make sure there are no hanging pucks
        and that the board consists of [0, 1, 2]
        """
        def validate_col(col):
            seen = False
            for cell in col:
                if cell not in [0, 1, 2]:
                    return False
                if cell != 0:
                    seen = True
                elif cell == 0 and seen:
                    return False
            return True
        return all([validate_col(c) for c in self.board.T])


    def diags(self):
        """
        Return diagonals (in both directions) of the board
        """
        d = [self.board[::-1,:].diagonal(i) \
             for i in range(-self.board.shape[0]+1,
                            self.board.shape[1])]

        d.extend(self.board.diagonal(i) \
                 for i in range(self.board.shape[1]-1,
                                -self.board.shape[0],-1))
        return d


    def runs_have_four(self, runs, orientation):
        """
        Given a list of possible locations for four sequential elements
        of the same kind, returns (True, <player>) if it finds a run of
        4 anywhere in a given run
        """
        def to_actual_index(i, j):
            if orientation == 'transposed':
                return (j, i)
            if orientation == 'diagonals':
                if i < 8:    # Upper Left
                    return (i - j, j)
                elif i < 15: # Lower Right
                    return (7 - i, j%7 + i)
                elif i < 23: # Upper Right
                    return (j, 8 - i%7 + j)
                else:        # Lower Left
                    return (i%22 + j, j)
            return (i, j)

        if len(runs) < 4: return (False, None)

        for i, run in enumerate(runs):
            found = None; count = 0; indices = []
            for j, cell in enumerate(run):
                if found and cell == found:
                    count += 1
                    indices += [to_actual_index(i, j)]
                    if count == 4:
                        return (True, found, indices)
                elif cell != 0:
                    count = 1; found = cell; indices = [to_actual_index(i, j)]
                else:
                    count = 0; found = None; indices = []
        return (False, None)


    def game_over(self):
        """
        Returns whether the game is won and who won:
        (True, 1), (True, 2), (False, None)
        """
        for runs, orientation in [(self.board,   'normal'),
                                  (self.board.T, 'transposed'),
                                  (self.diags(), 'diagonals')]:
            found = self.runs_have_four(runs, orientation)
            if found[0]: return found
        return (False, None)


    def __repr__(self):
        ret_str = ''
        for row in self.board:
            for cell in row:
                if cell == 1:
                    ret_str += 'O '
                if cell == 0:
                    ret_str += '_ '
                if cell == 2:
                    ret_str += 'X '
            ret_str += '\n'
        return ret_str

if __name__ == "__main__":

    c4 = Connect4Game()
    print c4