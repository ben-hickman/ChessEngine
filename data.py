""" All strings, constants, literals and commonly used functions across files.

:author: Ben Hickman
:date: 2023/10/26
:version: v1.0.0
"""

import enums
import numpy as np
import pygame
from pygame.locals import *

def file_rank_to_index(index: int) -> int:
    """ Maps an index of a length 64 array (representing regular chess board), to an index of a length 120
        array (representing a chess board with out of bounds tiles.

    :param index: The 64sq index to be converted.
    :returns: The converted 120sq index.
    """
    return index // 8 * 2 + 21 + index

# Colours
COLOUR_BONE_RED = (235, 213, 199)
COLOUR_BLACK = (0, 0, 0)
COLOUR_CHELSEA_CUCUMBER = (134, 168, 98)
COLOUR_CLOUDY_BLUE = (166, 199, 222)
COLOUR_RED = (255, 0, 0)
COLOUR_LIGHT_TAUPE = (181, 136, 99)
COLOUR_RED_CLEAR = (255, 64, 64, 192)

# Fonts
COURIER_FONT = 'fonts/Courier.ttf'

# Strings
PceChar = ".PNBRQKpnbrqk"
SideChar = "wb-"
RankChar = "12345678"
FileChar = "abcdefgh"

# Piece Arrays
PieceBig = np.array([False, False, True, True, True, True, True, False, True, True, True, True, True])
PieceMaj = np.array([False, False, False, False, True, True, True, False, False, False, True, True, True])
PieceMin = np.array([False, False, True, True, False, False, False, False, True, True, False, False, False])
PieceVal = np.array([0, 100, 325, 325, 550, 1000, 50000, 100, 325, 325, 550, 1000, 50000]) 
PieceCol = np.array([2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

PiecePawn = np.array([False, True, False, False, False, False, False, True, False, False, False, False, False])
PieceKnight = np.array([False, False, True, False, False, False, False, False, True, False, False, False, False])
PieceKing = np.array([False, False, False, False, False, False, True, False, False, False, False, False, True])
PieceRookQueen = np.array([False, False, False, False, True, True, False, False, False, False, True, True, False])
PieceBishopQueen = np.array([False, False, False, True, False, True, False, False, False, True, False, True, False])
PieceSlides = np.array([False, False, False, True, True, True, False, False, False, True, True, True, False])

# Maps 120sq to corresponding ranks/files.
FilesBrd = [enums.Tiles.OFF_BOARD.value] * 120
RanksBrd = [enums.Tiles.OFF_BOARD.value] * 120

for rank in range(8):
    for file in range(8):
        sq = file_rank_to_index(rank * 8 + file)
        FilesBrd[sq] = file
        RanksBrd[sq] = rank

KingDirection = [-11, -10, -9, -1, 1, 9, 10, 11]
KnightDirection = [-21, -19, -12, -8, 8, 12, 19, 21]
BishopDirection = [-11, -9, 9, 11]
RookDirection = [-10, -1, 1, 10]

# Labels in the settings menu.
res = ["RESOLUTION", "1280x720", "1920x1080", "2560x1440", "3840x2160"]

# Indices for the promotion menu pieces. Lists: Queen, Knight, Rook, Bishop for respective colour.
whitePromPieces = [enums.Piece.wQ, enums.Piece.wN, enums.Piece.wR, enums.Piece.wB]
blackPromPieces = [enums.Piece.bQ, enums.Piece.bN, enums.Piece.bR, enums.Piece.bB]

# All of the general attributes (absolute pos relative to (0, 0))
generalAttrs = ["board", "undo",  "pgnBox", "turnBox", "prom", "fromTile", "hamburger", "home", "speaker", "mute", "showAttacks", "slash"]
# These attributes shrink with window and float right.
floatRightAttrs = {"hamburger", "home", "speaker", "mute", "showAttacks", "slash"}
# These attributes represent fonts.
fontAttrs = ["pgnHeader", "pgnText", "turnText", "saveText", "fsText"]
# These attributes are PGN specific fonts that have their own absolute positioning.
pgnAttrs = ["pgnHeader", "pgnText"]
# Image variable names for non piece images.
nonPceImgs = ["board", "undo", "hamburger", "speaker", "mute", "home", "showAttacks", "slash"]
# These attributes are specific to the settings menu and have multiple buttons.
bttnsAttrs = ["fs", "res"]

# De Bruijn Sequence
BitTable = [
  63, 30, 3, 32, 25, 41, 22, 33, 15, 50, 42, 13, 11, 53, 19, 34, 61, 29, 2,
  51, 21, 43, 45, 10, 18, 47, 1, 54, 9, 57, 0, 35, 62, 31, 40, 4, 49, 5, 52,
  26, 60, 6, 23, 44, 46, 27, 56, 16, 7, 39, 48, 24, 59, 14, 12, 55, 38, 28,
  58, 20, 37, 17, 36, 8
]

# Aliases
def left_click(event: pygame.event) -> bool:
    """ An alias to determine event left mouse button down.

    :param event: The pygame event.
    :returns: bool true if a left mouse click has occurred.
    """
    return event.type == MOUSEBUTTONDOWN and event.button == 1

def middle_click(event: pygame.event) -> bool:
    """ An alias to determine event middle mouse button down.

    :param event: The pygame event.
    :returns: bool true if a middle mouse click has occurred.
    """
    return event.type == MOUSEBUTTONDOWN and event.button == 2

def right_click(event: pygame.event) -> bool:
    """ An alias to determine event right mouse button down.

    :param event: The pygame event.
    :returns: bool true if a right mouse click has occurred.
    """
    return event.type == MOUSEBUTTONDOWN and event.button == 3