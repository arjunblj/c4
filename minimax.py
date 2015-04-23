
import numpy as np

from game import Connect4Game

class Minimax(object):

    def __init__(self, board, max_depth=8):
        self.board = board
        self. = max_depth ## How many moves ahead will the AI think?

    def search(self, depth, state,):
        """Returns the alpha value.
        """
        legal moves = np.where(board[0] == 0)[0]

        ## If this state is a terminal state or depth == 0,
        ## return the heuristic value of node.
        if depth == 0 or len(legal_moves) == 0:
            return self.value(state, player)

        # # determine opponent's color
        # if curr_player == self.colors[0]:
        #     opp_player = self.colors[1]
        # else:
        #     opp_player = self.colors[0]

        alpha = -99999999
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth-1, child, opp_player))
        return alpha

