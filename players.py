
import numpy as np
import random

from copy import copy

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
        super(Human, self).__init__(p_num, opp_num, type)

    def get_move(self, board):
        """A move as inputed by a user.
        """
        column = int(raw_input('Pick a move between columns 0 through 6. '))

        ## TODO: Fix a bug here with validating inputs more than once.
        if not 0 <= column <= 6:
            column = int(raw_input('Sorry, that\'s not valid, try again. '))

        return column


class RandomAI(Player):
    """A random player.
    """

    def get_move(self, board):
        """The random player simply looks at what columns are free to be moved
           in and returns one of them at random.
        """
        free_columns = np.where(board[0] == 0)[0]
        return np.random.choice(free_columns)


class MinimaxAI(Player):
    """A basic minimax agent.
    """

    def __init__(self, p_num, opp_num, max_depth, type='AI'):
        """Initialized with much of the same arguments as the other player
           agents, the only difference is that the MinimaxAI can take a
           max_depth -- this is the ply depth of the search.
        """
        self.max_depth = max_depth
        self.player = p_num
        super(MinimaxAI, self).__init__(p_num, opp_num, type)

    def get_opp_player(self, player):
        """Simple utility that returns the opposing player's number.
        """
        if player == self.p_num:
            return self.opp_num
        else:
            return self.p_num

    def get_move(self, board):
        """Basic overview of the minimax function used -- the AI is iterating
           over the legal positions (at a depth indicated by max_depth) while
           using a heuristic (indicated by value()).
        """
        ## Set so that we can readily modify this state.
        self.board = board
        ## "Legal" columns where a move is permitted in the initial state.
        self.legal_columns = np.where(self.board[0] == 0)[0]

        ## Map each column with the expected alpha value, which is later
        ## used to influence move selection. There is a simulated move across
        ## each legal column.
        legal_moves = {}
        for column in self.legal_columns:
            temp, last_move = self.simulate_move(copy(self.board),
                column, self.player)
            legal_moves[column] = - self.search(self.max_depth - 1, temp,
                self.get_opp_player(self.player), last_move)

        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(moves)
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        return best_move

    def simulate_move(self, board, column, player):
        """Simulates a move by a player and returns the new and improved
           game state.
        """
        print board

        free_index = sum(board[:, column] == 0) - 1
        if free_index == -1:
            return False

        if player == 1:
            board[free_index, column] = 1
        else:
            board[free_index, column] = 2

        return (board, (free_index, column))

    def game_over(self, board, last_move):
        """Returns whether the game is won.

           @TODO: Refactor this -- it's just a modified version of the original
           game utility.
        """
        if last_move == ():
            return False

        row_num, col_num = last_move
        row, col = board[row_num, :], board[:, col_num]

        diag1 = np.diagonal(board, col_num - row_num)
        diag2 = np.diagonal(np.fliplr(board), - (col_num + row_num - 6))

        for line in [row, col, diag1, diag2]:
            if line.shape[0] < 4:
                continue
            for filtered_rows in [line[i:i+4] for i in range(len(line)-3)]:
                if sum(filtered_rows == 1) == 4:
                    return True
                elif sum(filtered_rows == 2) == 4:
                    return True
        if sum(board[0] == 0) == 0:
            return True
        return False

    def search(self, depth, board, player, last_move):
        """Checks out every legal move from the current state.
        """
        legal_columns = np.where(board[0] == 0)[0]
        legal_moves = []

        ## Iterate over the set of legal moves.
        for column in legal_columns:
            temp, last_move = self.simulate_move(copy(board), column, player)
            legal_moves.append([temp, last_move])

        ## If the max_depth has been exceeded or if this is the terminal node,
        ## return the heuristic value so we can pick a move already!
        if depth == 0 or len(legal_moves) == 0 or self.game_over(board, last_move):
            return self.value(board, player)

        alpha = -99999999
        for child in legal_moves:
            alpha = max(alpha, -self.search(depth-1, copy(child[0]),
                self.get_opp_player(player), child[1]))
        return alpha

    def value(self, board, player):
        """Basic heuristic used in evaluation.
        """

        my_fours = self.runs(board, player, 4)
        my_threes = self.runs(board, player, 3)
        my_twos = self.runs(board, player, 2)
        opp_fours = self.runs(board, self.get_opp_player(player), 4)
        opp_threes = self.runs(board, self.get_opp_player(player), 3)
        opp_twos = self.runs(board, self.get_opp_player(player), 2)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours*100000 + my_threes*100 + my_twos

    def runs(self, board, player, run_len):
        """Check out runs that are used to generate a four length chain.

           A bit of a naive check, it just iterates through every single (X, Y)
           coordinate on the board that belongs to the player passed and counts
           the number of horizontal, vertical, and diagonal runs created.
        """
        count = 0
        for x in xrange(len(board)):
            for y in xrange(len(board[0])):
                if board[x][y] == player:
                    count += self._horizontal_runs(x, y, board, run_len)
                    count += self._vertical_runs(x, y, board, run_len)
                    count += self._diagonal_runs(x, y, board, run_len)
        return count

    def _horizontal_runs(self, row, column, board, run_len):
        """Check horizontal runs for the specified length.
        """
        in_a_row = 0
        for y in xrange(column, len(board[0])):
            if board[row][y] == board[row][column]:
                in_a_row += 1
            else:
                break
        if in_a_row >= run_len:
            return 1
        else:
            return 0

    def _vertical_runs(self, row, column, board, run_len):
        """Check vertical runs for the specified length.
        """
        in_a_row = 0
        for x in xrange(row, len(board)):
            if board[x][column] == board[row][column]:
                in_a_row += 1
            else:
                break
        if in_a_row >= run_len:
            return 1
        else:
            return 0

    def _diagonal_runs(self, row, column, board, run_len):
        """Evaluate diagonals both ways (with a positive and negative slope).
        """
        total_runs = 0
        in_a_row = 0
        y = column

        for x in xrange(row, len(board)):
            if y > len(board):
                break
            if board[x][y] == board[row][column]:
                in_a_row += 1
            else:
                break
            y += 1

        if in_a_row >= run_len:
            total_runs += 1

        ## Now we have to check diagonals on the other end.
        in_a_row = 0
        y = column
        for x in xrange(row, -1, -1):
            if y > len(board):
                break
            elif board[x][y] == board[row][column]:
                in_a_row += 1
            else:
                break
            y += 1

        if in_a_row >= run_len:
            total_runs += 1

        return total_runs

