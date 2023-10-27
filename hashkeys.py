""" An algorithm to hashkey a game state used to check repetition.

:author: Ben Hickman
:date: 2023/10/26
:version: v1.0.0
"""
from __future__ import annotations
import board

import enums
from ctypes import c_ulonglong as ull
import numpy as np

pieceKeys = np.random.randint(low = 0, high = 18446744073709551615, size = (13, 120), dtype = ull)
turnKey = np.random.randint(low = 0, high = 18446744073709551615, dtype = ull)
castleKeys = np.random.randint(low = 0, high = 18446744073709551615, size = 16, dtype = ull)

def generate_pos_key(gameBoard: board.Board()) -> ull:
    """ A function to create a hashkey given the pieces on the board.

    :param gameBoard: The game board object including information for each successive turn.
    :returns: An unsigned long long representation of the hashkey.
    """
    finalKey = ull(0)

    for sq in range(120):
        piece = gameBoard.pieces[sq]

        if piece != enums.Tiles.NO_SQUARE.value and piece != enums.Piece.EMPTY.value and piece != enums.Tiles.OFF_BOARD.value:
            finalKey ^= pieceKeys[piece][sq]

    if gameBoard.turn == enums.Turn.WHITE.value:
        finalKey ^= turnKey

    if gameBoard.enPassant != enums.Tiles.NO_SQUARE.value:
        finalKey ^= pieceKeys[enums.Piece.EMPTY.value][gameBoard.enPassant]

    finalKey ^= castleKeys[gameBoard.castle]

    return finalKey