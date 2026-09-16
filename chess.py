# Python Chess game 
import numpy as np
import itertools
import math
# play=True
# while play:
#     player_in = tuple(input("Enter initial coordinates: "))
#     print("mock move made:", player_in)
#     if player_in == ('0','0'):
#         play=False
#     # only needs to handle single digit as chess coordinates are 8*8 max, so (0,0) -> (8,8)  
#     int_list = [int(char) for char in player_in if char.isdigit()]
#     print("Int only list after: ", int_list)
#     print("The validation works succesfully, and only appends int to the list: ", type(int_list[0]))
#     print(abs(2-3))

numbers = [1, -1]
pairs = list(itertools.combinations_with_replacement(numbers, 2))
filtered_pairs = [rook_pos for rook_pos in pairs if abs(rook_pos[0]) != abs(rook_pos[1])]
print(pairs)
rook_pos = (2,3)
king_position = (5,1)
y1, x1 = rook_pos
y2, x2 = king_position
# in board coordinates
generated_pos = (y2 + y1, x2 + x1)
print(generated_pos[0])
diagonal_step = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
# uses sqrt(x**2 + y**2) to get size of coordinate
bottom_right = math.sqrt(7**2 + 7**2) # diagonal_step (1, 1)
top_left = 0 # diagonal_step (-1, -1)
bottom_left = math.sqrt(7**2 + 0**2) # diagonal_step (-1, 1)
top_right = math.sqrt(0**2 + 7**2) # diagonal_step (0, 7)
x, y = diagonal_step[1]
print(x, y)
rook_pos_cpy = rook_pos
y2, x2 = rook_pos_cpy
diag = (0,0)
for i in range(8):
    y2+=1
    x2+=1
    rook_pos_cpy = (y2, x2)
    print(rook_pos_cpy)
print(rook_pos)
print(rook_pos_cpy)