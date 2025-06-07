import prompt_toolkit 
from prompt_toolkit.shortcuts import clear
from prompt_toolkit import print_formatted_text, HTML
import numpy as np
import time

class Board: 

    def __init__(self, row = 20, col = 10):
        self.row = row
        self.col = col
        self.board = self.init_board_grid()
        self.placed_coor = []

        self.speed = 1

    def init_board_grid(self):
        return np.zeros((self.row, self.col))

    def place_spawn_piece(self, piece, coordinate):
        block_coors = []
        first_coor = ()

        # place piece
        for i in range(piece.shape[0]):
            for j in range(piece.shape[1]):
                if piece[i][j] == 1:
                    if first_coor == ():
                        first_coor = (i, j)
                    block_coors.append((i - first_coor[0] + coordinate[0], j - first_coor[1] + coordinate[1]))
        for i in range(self.row):
            for j in range(self.col):
                if (i, j) not in block_coors: 
                    self.board[i][j] = 0
                else : 
                    self.board[i][j] = 1
        return block_coors

    def place_piece(self, coor):
        for i in range(self.row):
            for j in range(self.col):
                if (i, j) not in coor: 
                    self.board[i][j] = 0
                else : 
                    self.board[i][j] = 1

    def print_first_row(self):
        clear() # clear the terminal
        first_row = '     '
        for i in range(self.col):
            if i < 9:
                first_row += '0' + str(i + 1) + ' '
            else : 
                first_row += str(i + 1) + ' '
        first_row += ''
        print_formatted_text(HTML(
        '<ansicyan><b>┌───────────────────────────────────┐</b></ansicyan>\n'
        '<ansicyan><b>│             Tetris Game           │</b></ansicyan>\n'
        f'<ansicyan><b>│{first_row}│</b></ansicyan>'
        ))
    def print_board(self):
        content = ''
        
        for r in range(self.row):
            if r+1 < 10: 
                current_row = f'<ansicyan><b>│0{r+1} │</b></ansicyan>'
            else :
                current_row = f'<ansicyan><b>│{r+1} │</b></ansicyan>'
            for c in range(self.col):
                if self.board[r][c] == 0: 
                    current_row += '<ansicyan><b> . </b></ansicyan>'
                elif self.board[r][c] == 1: 
                    current_row += '<ansired><b> []</b></ansired>'
                elif self.board[r][c] == 2: 
                    current_row += '<ansibrightblack><b> []</b></ansibrightblack>'
            current_row += '<ansicyan><b> │</b></ansicyan>'
            content += current_row + '\n'
        print_formatted_text(HTML(
            f'{content}'
            '<ansicyan><b>└───────────────────────────────────┘</b></ansicyan>\n'
            ))

    def print_score(self, score):
        length_score = len(str(score))
        top_row = '<ansicyan><b>┌─────SCORE─────┐</b></ansicyan>\n'
        bot_row = '<ansicyan><b>└───────────────┘</b></ansicyan>'
        content = '<ansicyan><b>│ </b></ansicyan>'
        content += f'<ansired><b>{" " * (13 - length_score) + str(score)}</b></ansired>'
        content += '<ansicyan><b> │</b></ansicyan>'
        return top_row, content, bot_row
        

    def print_next_shape(self, next_shape, score):
        top_score, content_score, bot_score = self.print_score(score=score)


        top_row = f'<ansicyan><b>┌───NEXT───┐</b></ansicyan>     {top_score}'
        bot_row = f'<ansicyan><b>└──────────┘</b></ansicyan>\n'
        content = ''
        for i in range(len(next_shape)):

            current_row = '<ansicyan><b>│</b></ansicyan>'

            for j in range(len(next_shape[i])): 
                if next_shape[i][j] == 0:
                    current_row += '<ansiblue><b>  </b></ansiblue>'
                elif next_shape[i][j] == 1: 
                    current_row += '<ansiblue><b>[]</b></ansiblue>'
            current_row += '<ansicyan><b>│</b></ansicyan>'
            if i == 1: 
                current_row += f'     {bot_score}'
            elif i == 0: 
                current_row += f'     {content_score}'
                
            content += current_row
            content += '\n'

        print_formatted_text(HTML(f'{top_row}'
                                  f"{content}"
                                  f'{bot_row}'
                                  ))

    def printBoard(self):
        # time.sleep(self.speed)
        self.print_first_row()
        self.print_board()

if __name__ == "__main__":
    board = Board()
    board.printBoard()
