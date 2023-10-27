""" Holds all of the bitboard logic used for storing game data.

:author: Ben Hickman
:date: 2023/10/26
:version: v1.0.0
"""
from __future__ import annotations
import board

import enums
import data

from ctypes import c_ulonglong as ull
from ctypes import c_uint as uint
import ctypes

from typing import Tuple, Union



square120ToSquare64 = (ull * 120)()
square64ToSquare120 = (ull * 64)()

setMask = (ull * 64)()
clearMask = (ull * 64)()

def init_bitmasks() -> None:
    """ Initialize the bitmasks that are used to set and clear bits.
        clearMask is the inverse of setMask.
    """
    for i in range(64):
        setMask[i] |= ull(1 << i).value
        clearMask[i] = ~setMask[i]


def set_bit(bitboard: ull, sq: int) -> ull:
    """ Set a bitboard bit given a 120sq.
    
    :param bitboard: The bitboard containing piece location information.
    :param sq: The 64sq to set.
    :returns: The bitboard with the set bit.
    """
    bitboard.value |= int(setMask[sq])
    return bitboard


def clear_bit(bitboard: ull, sq: int):
    """ Clear a bitboard bit given a 120sq.
    
    :param bitboard: The bitboard to store.
    :param sq: The 64sq to set.
    :returns: The bitboard with the removed bit.
    """
    bitboard.value &= clearMask[sq]
    return bitboard


def init_sq_arrs() -> None:
    """ Initialize the board maps with their respective values.
        Note, these arrays are flipped over the horizontal axis.
        '0' and '21' represent the bottom left hand corner.

        square120ToSquare64:

        65 65 65 65 65 65 65 65 65 65 
        65 65 65 65 65 65 65 65 65 65 
        65 0  1  2  3  4  5  6  7  65
        65 8  9  10 11 12 13 14 15 65
        65 16 17 18 19 20 21 22 23 65
        65 24 25 26 27 28 29 30 31 65
        65 32 33 34 35 36 37 38 39 65
        65 40 41 42 43 44 45 46 47 65
        65 48 49 50 51 52 53 54 55 65
        65 56 57 58 59 60 61 62 63 65
        65 65 65 65 65 65 65 65 65 65
        65 65 65 65 65 65 65 65 65 65

        square64ToSquare120:
                                White
                A    B    C    D    E    F    G    H
            +----+----+----+----+----+----+----+----+
            1 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 1
            +----+----+----+----+----+----+----+----+
            2 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 2
            +----+----+----+----+----+----+----+----+
            3 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 3
        R     +----+----+----+----+----+----+----+----+
        A   4 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 4
        N     +----+----+----+----+----+----+----+----+
        K   5 | 61 | 62 | 63 | 64 | 65 | 66 | 67 | 68 | 5
            +----+----+----+----+----+----+----+----+
            6 | 71 | 72 | 73 | 74 | 75 | 76 | 77 | 78 | 6
            +----+----+----+----+----+----+----+----+
            7 | 81 | 82 | 83 | 84 | 85 | 86 | 87 | 88 | 7
            +----+----+----+----+----+----+----+----+
            8 | 91 | 92 | 93 | 94 | 95 | 96 | 97 | 98 | 8
            +----+----+----+----+----+----+----+----+
        FILE  A    B    C    D    E    F    G    H
                                Black
    """
    sq = 21
    sq64 = 0
    for i in range (8): # Iterate up each file. (Board is printed flipped on horizontal axis.)
        for j in range(8): # Iterate across each rank.
            sq = data.file_rank_to_index(i * 8 + j)
            square64ToSquare120[sq64] = sq
            square120ToSquare64[sq] = sq64
            sq64 += 1


def print_bitboard(bitboard: ull) -> None:
    """ Prints the current bitboard positions to the console.
    
        Sample:
        - - - - - - - - 8
        - - - - - - - - 7
        - - - - - - - - 6
        - - - - - - - - 5
        - - - X - - - - 4
        - - - X - - - - 3
        - - - X - - - - 2
        - - - - - - - - 1
        A B C D E F G H

    :param bitboard: The Unsigned 64 bit integer bitboard.
    """
    shiftMe = ull(1) # Unsigned 64 bit int to be shifted.
    sq = ull(0) # 120sq index.
    sq64 = ull(0) # sq64 value to bitshift.

    for i in range(7, -1, -1): # Loop from top to bottom.
        for j in range(8): # Loop left to right.
            sq = data.file_rank_to_index(i * 8 + j)
            sq64 = square120ToSquare64[sq]

            if ((shiftMe.value << sq64) & bitboard.value):
                print("X", end = " ")
            else:
                print("-", end = " ")

        print(i + 1)
    print("A B C D E F G H")


def pop_bit(bitboard: ull) -> Tuple[int, ull] :
    """ Used to pop the most recent bit off of a bitboard. Used when undoing moves on the board.

    :param bitboard: The bitboard containing piece location information.
    :returns: A tuple containing the 64sq index and the bitboard.
    """
    b = ull(bitboard.value ^ (bitboard.value - 1))
    fold = uint((b.value & 0xffffffff) ^ (b.value >> 32))
    bitboard = ull(bitboard.value & (bitboard.value - 1))

    return data.BitTable[uint(uint(fold.value * 0x783a9b23).value >> 26).value], bitboard 


def CountBits(bitboard: ull) -> int:
    """ Counts the number of bits in a bitboard, and returns them as an integer.

    :param bitboard: The bitboard to count the number of pieces contained.
    :returns: The number of pieces stored in the bitboard.
    """
    count = 0
    while bitboard.value:
        count += 1
        bitboard.value &= bitboard.value - 1

    return count


def print_bin(num: Union[int, ctypes.c_ulonglong], binaryDigits = 64) -> None:
    """ A basic function to print a binary representation of a number up to a max
        of 64 digits (unsigned long long.)

    :param num: The decimal based number to be printed in binary.
    :param binaryDigits: The number of digits to include in the output. 64 default.
    """
    if isinstance(num, int):
        num = ull(num)
        
    denominator = ull(2 ** (binaryDigits - 1))

    def recursive(a):
        if a.value == ull(1).value:
            return True
        elif a.value < ull(1).value:
            return False
        else:
            return recursive(ull(int(a.value / 16)))

    while denominator.value >= ull(1).value:

        if num.value >= denominator.value:
            print('1', end = "")
        else:
            print('0', end = "")

        if recursive(denominator):
            print(" ", end = "")

        num = ull(num.value % denominator.value)
        denominator = ull(int(denominator.value / 2))

    print("")


def print_undo_object(undo: board.Undo()) -> None:
    """ Print the contents of the move in an undo object.
        Used for debugging.
    """
    move = undo.move
    print("\nUndo Contents:")
    print("From: ", enums.Tiles(move & enums.MoveBitmasks.FROM_MASK.value).name)
    print("To: ", enums.Tiles((move & enums.MoveBitmasks.TO_MASK.value) >> enums.MoveBitmasks.TO_SHIFT.value).name)
    print("Captured: ", (move & enums.MoveBitmasks.CAPTURED_MASK.value) >> enums.MoveBitmasks.CAPTURED_SHIFT.value)
    print("Pawn Start: ", (move & enums.MoveBitmasks.PAWN_START_MASK.value) >> enums.MoveBitmasks.PAWN_START_SHIFT.value)
    print("Promoted: ", (move & enums.MoveBitmasks.PROMOTED_PIECE_MASK.value) >> enums.MoveBitmasks.PROMOTED_PIECE_SHIFT.value)
    print("Castling: ", (move & enums.MoveBitmasks.CASTLING_MASK.value) >> enums.MoveBitmasks.CASTLING_SHIFT.value, "\n")

# INITIALIZE
init_bitmasks()
init_sq_arrs()