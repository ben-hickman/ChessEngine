""" All commonly used enumerations.

:author: Ben Hickman
:date: 2023/10/26
:version: v1.0.0
"""
from enum import Enum

class Tiles(Enum):
    """ Chess tile mapped to 120sq index.
    """
    A1 = 21
    B1 = 22
    C1 = 23
    D1 = 24
    E1 = 25
    F1 = 26
    G1 = 27
    H1 = 28

    A2 = 31
    B2 = 32
    C2 = 33
    D2 = 34
    E2 = 35
    F2 = 36
    G2 = 37
    H2 = 38

    A3 = 41
    B3 = 42
    C3 = 43
    D3 = 44
    E3 = 45
    F3 = 46
    G3 = 47
    H3 = 48
    
    A4 = 51
    B4 = 52
    C4 = 53
    D4 = 54
    E4 = 55
    F4 = 56
    G4 = 57
    H4 = 58

    A5 = 61
    B5 = 62
    C5 = 63
    D5 = 64
    E5 = 65
    F5 = 66
    G5 = 67
    H5 = 68

    A6 = 71
    B6 = 72
    C6 = 73
    D6 = 74
    E6 = 75
    F6 = 76
    G6 = 77
    H6 = 78

    A7 = 81
    B7 = 82
    C7 = 83
    D7 = 84
    E7 = 85
    F7 = 86
    G7 = 87
    H7 = 88

    A8 = 91
    B8 = 92
    C8 = 93
    D8 = 94
    E8 = 95
    F8 = 96
    G8 = 97
    H8 = 98
    
    NO_SQUARE = 99
    OFF_BOARD = 100

class Piece(Enum):
    """ Piece name mapped to piece index.
    """
    EMPTY = 0
    wP = 1
    wN = 2
    wB = 3
    wR = 4
    wQ = 5
    wK = 6
    bP = 7
    bN = 8
    bB = 9
    bR = 10
    bQ = 11
    bK = 12

class File(Enum):
    """ File name mapped to file index.
    """
    FILE_A = 0
    FILE_B = 1
    FILE_C = 2
    FILE_D = 3
    FILE_E = 4
    FILE_F = 5
    FILE_G = 6
    FILE_H = 7

class Rank(Enum):
    """ Rank name mapped to rank index.
    """
    RANK_1 = 0
    RANK_2 = 1
    RANK_3 = 2
    RANK_4 = 3
    RANK_5 = 4
    RANK_6 = 5
    RANK_7 = 6
    RANK_8 = 7

class Turn(Enum):
    """ Player turn mapped to index.
    """
    WHITE = 0
    BLACK = 1
    BOTH = 2

class Castle(Enum):
    """ Castle permission mapped to bits.
    """
    WKCA = 1
    WQCA = 2
    BKCA = 4
    BQCA = 8

class MoveBitmasks(Enum):
    """ Bitmasks and shifts related to a move.
    """
    FROM_MASK = 0x7F
    FROM_SHIFT = 0

    TO_MASK = 0x3F80
    TO_SHIFT = 7

    CAPTURED_MASK = 0x3C000
    CAPTURED_SHIFT = 14

    EN_PASSANT_MASK = 0x40000
    EN_PASSANT_SHIFT = 18

    PAWN_START_MASK = 0x80000
    PAWN_START_SHIFT = 19

    PROMOTED_PIECE_MASK = 0xF00000
    PROMOTED_PIECE_SHIFT = 20

    PROMOTED_Q_MASK = 0x100000
    PROMOTED_N_MASK = 0x200000
    PROMOTED_R_MASK = 0x400000
    PROMOTED_B_MASK = 0x800000

    CASTLING_MASK = 0x1000000
    CASTLING_SHIFT = 24

class Resolution(Enum):
    """ Commonly used resolutions.
    """
    RES_1280_720 = (1280, 720)
    RES_1920_1080 = (1920, 1080)
    RES_2560_1440 = (2560, 1440)
    RES_3840_2160 = (3840, 2160)

class ResolutionIndex(Enum):
    """ Indices when selecting resolution in settings page.
    """
    IND_1280_720 = 1
    IND_1920_1080 = 2
    IND_2560_1440 = 3
    IND_3840_2160 = 4