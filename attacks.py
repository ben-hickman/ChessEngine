""" File used to determine if a square on the board is attacked or not.

:author: Ben Hickman
:date: 2023/10/26
:version: v1.0.0
"""
import board
import data
import enums

def is_attacked(square: int, board: board.Board) -> bool:
    """ Given a 120sq index, return whether it is attacked or not by an opposing piece.
        Important to determine king moves as well as castling permissions.
    
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

    if board.turn == enums.Turn.WHITE.value:
        if board.pieces[square + 9] == enums.Piece.bP.value or board.pieces[square + 11] == enums.Piece.bP.value:
            return "Black Pawn Threat"
    
    else:
        if board.pieces[square - 9] == enums.Piece.wP.value or board.pieces[square - 11] == enums.Piece.wP.value:
            return "White Pawn Threat"
    
    for direction in data.KnightDirection:
        if board.pieces[square + direction] == (enums.Piece.wN.value + modifier):
            return "Knight Threat"
    
    for direction in data.BishopDirection:
        tile = square + direction
        piece = board.pieces[tile]

        while piece == enums.Piece.EMPTY.value:
            if piece == (enums.Piece.wB.value + modifier):
                return "Bishop Threat"

            tile += direction
            piece = board.pieces[tile]

    for direction in data.RookDirection:
        tile = square + direction
        piece = board.pieces[tile]

        while piece == enums.Piece.EMPTY.value:
            if piece == (enums.Piece.wR.value + modifier):
                return "Rook Threat"
            
            tile += direction
            piece = board.pieces[tile]

    for direction in data.BishopDirection + data.RookDirection:
        if board.pieces[square + direction] == (enums.Piece.wK.value + modifier):
            return "King Threat"
        
    for direction in data.BishopDirection + data.RookDirection:
        tile = square + direction
        piece = board.pieces[tile]

        # while piece != enums.Tiles.OFF_BOARD.value:
        while piece == enums.Piece.EMPTY.value:
            if piece == (enums.Piece.wQ.value + modifier):
                return "Queen Threat"
            
            tile += direction
            piece = board.pieces[tile]

    return False