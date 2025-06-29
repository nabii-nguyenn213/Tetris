from sys import _enablelegacywindowsfsencoding, deactivate_stack_trampoline
from board import Board
from pieces import Pieces
import numpy as np

class Game : 

    def __init__(self) -> None:
        self.board = Board()
        self.piece = Pieces()

        self.point = 0
        self.point_per_line = 100
        self.level = 1
        self.total_lines_clear = 0
        self.speed = 0.5

    def spawn_pieces(self, next = None):
        if next is not None : 
            self._piece = self.piece.generate_pieces(next=next)
            self._piece_val = self.next_shape_val
        else : 
            self._piece, self._piece_val = self.piece.generate_pieces()
        row = self.board.row
        col = self.board.col
        spawn_coor = (0, col // 2 - 1)
        self.current_coor = self.board.place_spawn_piece(self._piece, self._piece_val, spawn_coor)

    def drop_piece(self):
        return [(min(r+1, self.board.row-1), c) for (r, c) in self.current_coor]

    def _check_touch(self):
        if not self.current_coor : return True
        for (r, c) in self.current_coor: 
            # We need to extract the lowest row of each col
            lowest_block_per_col = [(max(x for (x, y0) in self.current_coor if y0 == y), y)
                for y in {y for (_, y) in self.current_coor}]
        # print(lowest_block_per_col)
        for (r, c) in lowest_block_per_col: 
            if r == self.board.row - 1 : 
                if self._piece_val in self.board.placed_coor: 
                    self.board.placed_coor[self._piece_val].extend(self.current_coor)
                else : 
                    self.board.placed_coor[self._piece_val] = [*self.current_coor]
                return True
            for coors in self.board.placed_coor.values():
                for (ro, co) in coors:
                    if (r + 1, c) == (ro, co): 
                        if self._piece_val in self.board.placed_coor: 
                            self.board.placed_coor[self._piece_val].extend(self.current_coor)
                        else : 
                            self.board.placed_coor[self._piece_val] = [*self.current_coor]
                        return True
        return False

    def shadow_piece(self):
        
        self.min_dif = self.board.row 
        
        for (r, c) in self.current_coor: 
            column_slide = self.board.board[:, c].copy()
            current_dif = self.board.row - r
            for (ro, co)in self.current_coor: 
                if 0 <= ro <= self.board.row - 1: 
                    column_slide[ro] = 0
            if np.count_nonzero(column_slide != 0) == 0: # if there is no one
                self.min_dif = min(self.min_dif, current_dif)
            else : 
                first_idx_one = np.where(column_slide != 0)[0][0]
                current_dif = first_idx_one - r

            self.min_dif = min(self.min_dif, current_dif)
        return self.min_dif

    def game_over(self):

        for coors in self.board.placed_coor.values():
            for (r, c) in coors:
                if r == 0: 
                    return True
        return False

    def move_right(self):
        # move right : col + 1, keep the same row
        for (r, c) in self.current_coor: 
            if c >= self.board.col - 1: 
                return self.current_coor
        return [(r, c + 1) for (r, c) in self.current_coor]
    
    def move_left(self):
        # move left : col - 1, keep the same row
        for (r, c) in self.current_coor: 
            if c <= 0 : 
                return self.current_coor
        return [(r, c-1) for (r, c) in self.current_coor]

    def place_down(self):
        new_coor = [(r + self.min_dif - 1, c) for (r, c) in self.current_coor]
        # print('place down coor :', new_coor)
        return new_coor

    def update_board(self):

        self.board.reset_board()

        if self.current_coor is not None: 
            for i in range(self.board.row):
                for j in range(self.board.col):
                    if (i, j) in self.current_coor:
                        self.board.board[i][j] = self._piece_val
                    else:
                        self.board.board[i][j] = 0

        for piece_val, coors in self.board.placed_coor.items():
            for (r, c) in coors : 
                self.board.board[r, c] = piece_val
        
        if not self._check_touch():
            dif = self.shadow_piece()
            for i in range(self.board.row):
                for j in range(self.board.col):
                    if (i - (dif - 1), j) in self.current_coor:
                        self.board.board[i][j] = -1
                    if (i, j) in self.current_coor: 
                        self.board.board[i][j] = self._piece_val

    def rotate_left(self):
        self._piece, dif = self.piece.rotate_counterclockwise(self._piece)
        new_coor = [(current_row + dif_row, current_col + dif_col) for (current_row, current_col), (dif_row, dif_col) in zip(self.current_coor, dif)]
        return new_coor

    def rotate_right(self):
        self._piece, dif = self.piece.rotate_clockwise(self._piece)
        new_coor = [(current_row + dif_row, current_col + dif_col) for (current_row, current_col), (dif_row, dif_col) in zip(self.current_coor, dif)]
        return new_coor

    def completed_row(self):
        rows = {}
        delete_row = []
        for coors in self.board.placed_coor.values(): 
            for (r, c) in coors: 
                if r not in rows : 
                    rows[r] = [c]
                else : 
                    rows[r].append(c)
        for row, cols in rows.items():
            if len(list(set(cols))) == self.board.col:
                delete_row.append(row)
        self.total_lines_clear += len(delete_row)
        self.current_lines_clear = len(delete_row)
        return delete_row

    def delete_completed_row(self):
        delete_row = self.completed_row()
        if delete_row == []:
            droprow = False
        else :
            droprow = True
        print(f"Row {delete_row} deleted")
        new_placed_coor = {}

        for piece_val, coors in self.board.placed_coor.items():
            for (r, c) in coors:
                if r in delete_row : 
                    continue
                if piece_val not in new_placed_coor: 
                    new_placed_coor[piece_val] = [(r, c)]
                else : 
                    new_placed_coor[piece_val].append((r, c))
        # print(new_placed_coor) 
        return new_placed_coor, droprow

    def down_row(self):
        
        for r in range(self.board.row - 2, -1, -1):
            current_row = self.board.board[r, :]
            if np.all(current_row == 0):
                continue
            below_row = self.board.board[r+1, :]
            current_row = r
            while np.all(below_row == 0) and current_row < self.board.row - 1:
                # print(f"Current row ({current_row}) : {self.board.board[r, ]}")
                # print(f"Below row ({current_row + 1}) : {below_row}")
                # print(f"Swap {current_row} to {current_row + 1}")
                self.board.board[[current_row, current_row+1]] = self.board.board[[current_row+1, current_row]]
                current_row += 1
                if current_row == 19: 
                    break
                below_row = self.board.board[current_row + 1, :]

        # print("done drop")
        # print(self.board.board)
        # print()

    def point_and_level(self):
        
        '''
        Points = (Base Points for Line Clear) * (Level Multiplier) + Combo Bonus
        
        first level speed = 1s
        Level 1: Pieces fall at speed X, and you earn 100 points per line.
        Level 2: Pieces fall at speed X + 10%, and you earn 150 points per line.
        Level 3: Pieces fall at speed X + 20%, and you earn 200 points per line.
        Level 10: Pieces fall at speed X + 90%, and you earn 500 points per line.

        Level up every 10 lines clear.
        '''
        
        if self.total_lines_clear >= 10: 
            self.level += self.total_lines_clear // 10

            self.speed = self.speed - (((self.level + 1) * 10)/100)
            self.board.speed = self.speed

            self.point_per_line += 50

            self.total_lines_clear -= 10 * (self.level-1)
        
        self.point += self.point_per_line * self.current_lines_clear

    def update_placed_coor(self):
        new_placed_coor = {}
        for r in range(self.board.row):
            for c in range(self.board.col):
                cell_value = self.board.board[r, c]
                if cell_value <= 0: 
                    continue
                if cell_value not in new_placed_coor:
                    new_placed_coor[cell_value] = [(r, c)]
                else : 
                    new_placed_coor[cell_value].append((r, c))
        # print(new_placed_coor)
        return new_placed_coor
            
    def run(self):
        # game loop 
        ''' 
                             +------------------------Repeat-------------------------------+
        spawn first piece -> | spawn_next_piece -> if placed -> current piece = next piece | -> end
                             |                  -> if not placed                           |
                             +-------------------------------------------------------------+
        '''
        self.board.printBoard()
        self.spawn_pieces()
        self.shadow_piece()
        self.update_board()
        self.board.printBoard()

        next_shape, self.next_shape_val = self.piece.generate_pieces()
        self.board.print_next_shape(next_shape, self.point)

        while not self.game_over(): 
            inp = input()
            if inp == 'q':
                break
            self.update_board()
            _touch = self._check_touch()
            
            if inp == 'f': 
                self.current_coor = self.place_down()
                if self._piece_val in self.board.placed_coor: 
                    self.board.placed_coor[self._piece_val].extend(self.current_coor)
                else : 
                    self.board.placed_coor[self._piece_val] = [*self.current_coor]
                _touch = True
            if _touch == False:
                if inp == 't' : 
                    self.current_coor = self.move_right()
                if inp == 'r' : 
                    self.current_coor = self.move_left()
                if inp == 's': 
                    self.current_coor = self.drop_piece()
                if inp == 'w' : # rotate left
                    self.current_coor = self.rotate_left()
                if inp == 'p' : # rotate right
                    self.current_coor = self.rotate_right()

                self.current_coor = self.drop_piece()
            else : 
                self.current_coor = None
                self.update_board()
                self.board.placed_coor, droprow = self.delete_completed_row()
                self.update_board()
                # self.board.placed_coor = self.update_placed_coor()
                # print(self.board.placed_coor)
                self.point_and_level()
                self.update_board()
                # print(self.board.board)
                if droprow : 
                    self.down_row()
                self.board.placed_coor = self.update_placed_coor()
                self.update_board()
                self.spawn_pieces(next=next_shape)
                next_shape, self.next_shape_val = self.piece.generate_pieces()
                

            self.update_board()
            self.board.printBoard()
            self.board.print_next_shape(next_shape, self.point)
            # print(self.board.board)

if __name__ == "__main__":
    game = Game()
    game.run()
