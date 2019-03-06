# -*- coding: utf-8 -*-
import numpy as np
import itertools


def solve(board, pents):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is
    the coordinate of the upper left corner of pi in the board (lowest row and column index
    that the tile covers).
    -Use np.flip and np.rot90 to manipulate pentominos.
    -You can assume there will always be a solution.
    """
    # make list of all flips/rotations of pents
    all_pents = []
    for idx, pent in enumerate(pents):
        temp_pent = pent
        for i in range(0, 4):
            temp_pent = np.rot90(temp_pent)
            all_pents.append(temp_pent)
            temp_pent = np.flip(temp_pent, 0)
            all_pents.append(temp_pent)
            temp_pent = np.flip(temp_pent, 1)
            all_pents.append(temp_pent)

    # https://stackoverflow.com/questions/27751072/removing-duplicates-from-a-list-of-numpy-arrays
    # How to remove duplicates from a list of numpy arrays, retrieved from stack-overflow
    # make list of only unique pents
    unique_pents = []
    for pent in all_pents:
        if not any(np.array_equal(pent, unique_arr) for unique_arr in unique_pents):
            unique_pents.append(pent)

    sol_list = []
    sol_board = np.zeros(board.shape)
    solve_helper(sol_board, unique_pents, [], sol_list)
    return sol_list


def solve_helper(board, pents, used_pents, sol_list):
    # base case  - True if board is full
    if 0 not in board:
        return True
    for pent in pents:
        if used_pent(pent, used_pents):
            continue
        location_added = add_pentomino(board, pent)
        if location_added != [-1, -1]:
            used_pents.append(get_pent_number(pent))
            sol_list.append((pent, (location_added[0], location_added[1])))
            # recursively loop through
            if solve_helper(board, pents, used_pents, sol_list):
                return True
            else:
                remove_pentomino(board, pent, location_added)
                used_pents.pop(used_pents.index(get_pent_number(pent)))
                for pent_idx, sol_entry in enumerate(sol_list):
                    if np.array_equal(sol_entry[0], pent):
                        sol_list.pop(pent_idx)
                        break

    return False


def add_pentomino(board, pent):
    '''
    adds pentomino to board
    return [-1,-1] if failed
    will loop through board and try to fit piece onto empty square first
    '''
    h, w = board.shape  # rows, columns
    if w < h:
        for board_row in range(h):
            for board_col in range(w):
                # if piece does not fit into first empty square found return failure
                if board[board_row][board_col] == 0:
                    if not pent_will_fit(board, pent, [board_row, board_col]):
                        return [-1, -1]
                if pent_will_fit(board, pent, [board_row, board_col]):
                    for pent_row in range(pent.shape[0]):
                        for pent_col in range(pent.shape[1]):
                            if pent[pent_row][pent_col] != 0:
                                board[board_row + pent_row][board_col
                                                            + pent_col] = pent[pent_row][pent_col]
                    return [board_row, board_col]
    else:
        for board_col in range(w):
            for board_row in range(h):
                # if piece does not fit into first empty square found return failure
                if board[board_row][board_col] == 0:
                    if not pent_will_fit(board, pent, [board_row, board_col]):
                        return [-1, -1]
                if pent_will_fit(board, pent, [board_row, board_col]):
                    for pent_row in range(pent.shape[0]):
                        for pent_col in range(pent.shape[1]):
                            if pent[pent_row][pent_col] != 0:
                                board[board_row + pent_row][board_col
                                                            + pent_col] = pent[pent_row][pent_col]
                    return [board_row, board_col]

    return [-1, -1]


def pent_will_fit(board, pent, coord):
    # check to see if piece will fit
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                try:
                    if board[coord[0] + row][coord[1] + col] != 0:  # Overlap
                        return False
                except IndexError:  # sticks out of board
                    return False
    return is_good_fit(board, pent, coord)


def is_good_fit(board, pent, coord):
    # put optmizations here for whether or not a piece at coord will cause inevitable failure
    h, w = board.shape
    try:
        if len(pent[0]) == 1 or len(pent[1]) == 1:
            return True
    except IndexError:
        return True
    # check if trapping corner
    if coord == [0, 0]:
        if pent[0][0] == 0 and pent[0][1] != 0 and pent[1][0] != 0:
            return False
    if coord == [0, w - len(pent[0])]:
        if pent[0][-1] == 0 and pent[0][-2] != 0 and pent[1][-1] != 0:
            return False
    if coord == [h - len(pent[1]), 0]:
        if pent[-1][0] == 0 and pent[-2][0] != 0 and pent[-1][1] != 0:
            return False
    if coord == [h - len(pent[1]), w - len(pent[0])]:
        if pent[-1][-1] == 0 and pent[-2][-1] != 0 and pent[-1][-2] != 0:
            return False

    # check if creating "empty pocket"

    return True


def get_pent_number(pent):
    # get pent index by looking for nonzero values in board
    for row in pent:
        for val in row:
            if val != 0:
                return val
    return -1


def used_pent(pent, used_pents):
    if get_pent_number(pent) in used_pents:
        return True
    return False


def remove_pentomino(board, pent, coord):
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                board[coord[0] + row][coord[1] + col] = 0
    return True
