import random
import numpy as np
# L-Pieces, J-Pieces, T-Pieces, I-Pieces, Z-Pieces, S-Pieces, O-Pieces

'''
1. L-Pieces : 
    []
    []
    [][] 

2. J-Pieces : 
      []
      []
    [][]

3. T-Pieces : 
    [][][]
      []

4. I-Pieces : 
    []
    []
    []
    []

5. Z-Pieces : 
    [][]
      [][]

6. S-Pieces : 
      [][]
    [][]

7. O-Pieces : 
    [][]
    [][]

'''

class Pieces: 
    
    def generate_pieces(self, next = None):
        if next is not None: 
            return next

        random_shape = random.randint(1, 7)
        if random_shape == 1 : # L
            piece = np.array([[0, 0, 0, 0, 0], 
                                   [0, 0, 1, 0, 0], 
                                   [0, 0, 1, 0, 0], 
                                   [0, 0, 1, 1, 0], 
                                   [0, 0, 0, 0, 0]])
        elif random_shape == 2 : # J 
            piece = np.array([[0, 0, 0, 0, 0], 
                                   [0, 0, 1, 0, 0], 
                                   [0, 0, 1, 0, 0], 
                                   [0, 1, 1, 0, 0], 
                                   [0, 0, 0, 0, 0]])
        elif random_shape == 3 : # T
            piece = np.array([[0, 0, 0, 0, 0], 
                                   [0, 0, 0, 0, 0], 
                                   [0, 1, 1, 1, 0], 
                                   [0, 0, 1, 0, 0], 
                                   [0, 0, 0, 0, 0]])
        elif random_shape == 4 : # I
            piece = np.array([[0, 0, 0, 0, 0], 
                                   [0, 0, 1, 0, 0], 
                                   [0, 0, 1, 0, 0], 
                                   [0, 0, 1, 0, 0], 
                                   [0, 0, 1, 0, 0]])
        elif random_shape == 5 : # Z 
            piece = np.array([[0, 0, 0, 0, 0], 
                                   [0, 0, 0, 0, 0], 
                                   [0, 1, 1, 0, 0], 
                                   [0, 0, 1, 1, 0], 
                                   [0, 0, 0, 0, 0]])
        elif random_shape == 6 : # S
            piece = np.array([[0, 0, 0, 0, 0], 
                                   [0, 0, 0, 0, 0], 
                                   [0, 0, 1, 1, 0], 
                                   [0, 1, 1, 0, 0], 
                                   [0, 0, 0, 0, 0]])
        else : # O
            piece = np.array([[0, 0, 0, 0, 0], 
                                   [0, 0, 0, 0, 0], 
                                   [0, 0, 1, 1, 0], 
                                   [0, 0, 1, 1, 0], 
                                   [0, 0, 0, 0, 0]])
        return piece

    def rotate_clockwise(self, piece):
        # rotate right
        new_piece = np.rot90(piece, k = -1)
        old_coor = []
        new_coor = []
        for r in range(len(piece)):
            for c in range(len(piece[r])):
                if piece[r][c] == 1: 
                    old_coor.append((r, c))
                if new_piece[r][c] == 1: 
                    new_coor.append((r, c))
        dif = [(new_r - old_r, new_c - old_c) for (new_r, new_c), (old_r, old_c) in zip(new_coor, old_coor)]   
        return new_piece, dif

    def rotate_counterclockwise(self, piece):
        # rotate left
        new_piece = np.rot90(piece, k = 1)
        old_coor = []
        new_coor = []
        for r in range(len(piece)):
            for c in range(len(piece[r])):
                if piece[r][c] == 1: 
                    old_coor.append((r, c))
                if new_piece[r][c] == 1: 
                    new_coor.append((r, c))
        dif = [(new_r - old_r, new_c - old_c) for (new_r, new_c), (old_r, old_c) in zip(new_coor, old_coor)]   
        return new_piece, dif

