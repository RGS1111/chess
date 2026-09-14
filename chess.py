# Python Chess game 
import numpy as np
import itertools
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

numbers = [1, 2, -1, -2]
pairs = itertools.permutations(numbers, 2)
filtered_pairs = [rook_pos for rook_pos in pairs if abs(rook_pos[0]) != abs(rook_pos[1])]
print(filtered_pairs)