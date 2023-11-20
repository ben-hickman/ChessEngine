""" File used to determine if a square on the board is attacked or not.

:author: Ben Hickman
:date: 2023/10/26
:version: v1.0.0
"""
import board
import data
import enums
from ctypes import c_ulonglong as ull
import bitboards

def is_attacked(square: int, board: board.Board) -> bool:
    """ Given a 120sq index, return whether it is attacked or not by an opposing piece.
        Important to determine king moves as well as castling permissions.
        Attacked squares can be empty, or a piece owned by either player.
    
    :param square: The 120sq index to check.
    :param gameBoard: The game board object including information for each successive turn.
    :returns: A boolean representing if the square is attacked.
    """

    # As noted in enums.Piece, each black piece value corresponds to a white piece value incremented by 6.
    # This modifier is used to reduce the number of lines of code if it is white to play.
    # If white to play, look for black pieces attacking the square.
    modifier = 0
    if board.turn == enums.Turn.WHITE.value:
        modifier = 6

    # Pawns
    if board.turn == enums.Turn.WHITE.value:
        if board.pieces[square + 9] == enums.Piece.bP.value or board.pieces[square + 11] == enums.Piece.bP.value:
            return "Black Pawn Threat"
    
    else:
        if board.pieces[square - 9] == enums.Piece.wP.value or board.pieces[square - 11] == enums.Piece.wP.value:
            return "White Pawn Threat"
    
    # Knights
    for direction in data.KnightDirection:
        if board.pieces[square + direction] == (enums.Piece.wN.value + modifier):
            return "Knight Threat"
    
    # Bishops
    for direction in data.BishopDirection:
        tile = square + direction
        piece = board.pieces[tile]

        while piece != enums.Tiles.OFF_BOARD.value:
            if piece != enums.Piece.EMPTY.value:
                if piece == (enums.Piece.wB.value + modifier):
                    return "Bishop Threat"
                break

            tile += direction
            piece = board.pieces[tile]

    # Rooks
    for direction in data.RookDirection:
        tile = square + direction
        piece = board.pieces[tile]

        while piece != enums.Tiles.OFF_BOARD.value:
            if piece != enums.Piece.EMPTY.value:
                if piece == (enums.Piece.wR.value + modifier):
                    return "Rook Threat"
                break

            tile += direction
            piece = board.pieces[tile]

    # Kings
    for direction in data.BishopDirection + data.RookDirection:
        if board.pieces[square + direction] == (enums.Piece.wK.value + modifier):
            return "King Threat"
    
    # Queens
    for direction in data.BishopDirection + data.RookDirection:
        tile = square + direction
        piece = board.pieces[tile]

        while piece != enums.Tiles.OFF_BOARD.value:
            if piece != enums.Piece.EMPTY.value:
                if piece == (enums.Piece.wQ.value + modifier):
                    return "Queen Threat"
                break
            
            tile += direction
            piece = board.pieces[tile]

    return False

def get_attacked_bitboard(board: board.Board) -> ull:
    """ Return a bitboard representation of all of the squares attacked by opponent.

    :param board: The gameBoard containing the current position.

    :returns: The ctypes.c_ulonglong representation of atatcked squares.
    """
    bitboard = ull(0)
    offBoardSet = {29, 30, 39, 40, 49, 50, 59, 60, 69, 70, 79, 80, 89, 90}

    for i in range(21, 99):
        temp = is_attacked(i, board)
        if temp and i not in offBoardSet:
            bitboards.set_bit(bitboard, bitboards.square120ToSquare64[i])

    return bitboard