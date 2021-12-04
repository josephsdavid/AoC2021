import numpy as np
from rich import print

class Bingo(object):
    def __init__(self, commands: str):
        bingo = commands.splitlines()
        bingo = [b for b in bingo if len(b) > 0]
        self.input = bingo.pop(0)
        self.input = [int(b) for b in self.input.strip().split(',')]
        boards = [np.array(list(map(int, x.split()))) for x in bingo]
        self.boards = [np.row_stack(boards[i:i+5]) for i in range(0, len(boards), 5)]
        self.markers = [np.zeros_like(b) for b in self.boards]
        self.winner = [0 for m in self.markers]
        self.play_bingo()


    def play_bingo(self):
        i = 0
        while sum(self.winner)  == 0:
            callout = self.input[i]
            for j, (b, m) in enumerate(zip(self.boards, self.markers)):
                m[np.where(b == callout)] = 1
                if m.sum(0).max() == m.shape[0] or m.sum(1).max() == m.shape[1]:
                    self.winner[j] = 1
                    break
            i += 1
        self.winning_number = callout
        self.winning_board = j

    def __call__(self):
        winning_score = self.winning_number
        winning_marker = self.markers[self.winning_board]
        winning_board = self.boards[self.winning_board]
        winning_board[np.where(winning_marker != 0)] = 0
        return winning_score * winning_board.sum()

class LoseBingo(Bingo):
    def __init__(self, commands: str):
        super().__init__(commands)
        self.lose_at_bingo()

    def lose_at_bingo(self):
        while len(self.boards) > 1:
            self.boards.pop(self.winning_board)
            self.markers.pop(self.winning_board)
            self.winner.pop(self.winning_board)
            self.play_bingo()





if __name__ == "__main__":
    test = """
    7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

    22 13 17 11  0
     8  2 23  4 24
    21  9 14 16  7
     6 10  3 18  5
     1 12 20 15 19

     3 15  0  2 22
     9 18 13 17  5
    19  8  7 25 23
    20 11 10 24  4
    14 21 16 12  6

    14 21 17 24  4
    10 16 15  9 19
    18  8 23 26 20
    22 11 13  6  5
     2  0 12  3  7"""

    print(Bingo(test)())

    from data import game
    print(Bingo(game)())

    print(LoseBingo(test)())
    print(LoseBingo(game)())
