class Game:
    
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.turn = player1
        self.waiting = player2
        self.board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.WIN_PERMUTATIONS = [(0, 1, 2),(3, 4, 5),(6, 7, 8),(0, 3, 6),(1, 4, 7),(2, 5, 8),(0, 4, 8),(2, 4, 6)]

    def display_board(self):
        '''returns the string representation of the current game board'''
        string_board = "\n" + "Current board:" + "\n"
        for i in range(0, len(self.board), 3):
            string_board += (f'{self.board[i]} | {self.board[i+1]} | {self.board[i+2]}') + "\n"
            if i != 6:
                string_board += (f'--+---+--') + "\n"

        return string_board

    def valid_move(self, move):
        """checks if the move is not a number, if it is out of bounds of the board, and if the move has already been made, returns eror code if invalid move and 200 valid if valid move"""
        if not move.isnumeric(): # if input is not numeric
            return False
        
        if int(move) < 0 or int(move) > 8: # checks if entry is out of range of board
            return False
        
        elif self.board[int(move)] == 'X' or self.board[int(move)] == 'O': # checks if move is taken
            return False
        
        else:
            return True
        
    def changeTurn(self):
        """Automatically switches turn. Used in main game loop to go back and forth between players"""
        if self.turn == self.player2:
            self.turn = self.player1
            self.waiting = self.player2

        else:
            self.turn = self.player2
            self.waiting = self.player1

    def make_move(self, move):
        """updates board"""
        if self.turn == self.player1:
            self.board[move] = 'X'

        if self.turn == self.player2:
            self.board[move] = 'O'
    
    def checkWinDraw(self):
        spots_filled = 0
        """checks if there was a winning move made and returns True or False"""
        for a,b,c in self.WIN_PERMUTATIONS: # check if there is a winner, returns true to end game
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != ' ' and self.board[b] != ' ' and self.board[c] != ' ':
                return "300 WIN"
            
        for i in self.board: # check if draw, returns 100 DRAW message
            if i == 'X' or i == 'O':
                spots_filled += 1

        if spots_filled == 9:
            return "300 DRAW"
        
        else:
            return "301 NEXT"

    # reference this in the server for gameloop