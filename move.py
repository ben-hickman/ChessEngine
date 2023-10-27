""" Move file containing all information related to handling a move within the game.

:author: Ben Hickman
:date: 2023/10/26
:version: v1.0.0
"""
import board
import hashkeys
import enums
import data
from artifacts import Artifacts as art
import artifacts
import menu

from typing import Tuple

class Move():
    def __init__(self):
        """ A class representing a move within the game.
            Includes handling en passant, setting/storing history and promotion.
        """
        # 120sq index for tile to move from and to.
        self.from120 = -1
        self.to120 = -1

        # Piece captured, piece moving and turn indicator.
        self.capturedPiece = 0
        self.fromPiece = 0

        # Tertiary value for promotion event: false, white or black to promote.
        self.prom = 0
        self.promPiece = 0

        # The en passant square (square a pawn can move to.)
        self.enPassant = enums.Tiles.NO_SQUARE.value


    def mouse_pos_to_120(self, mousePos: Tuple[int, int]) -> int:
        """ Given mouse coordinates, convert to 120sq index.

        :param mousePos: The (x, y) values of the mouse.
        :returns: The 120sq index for the board.
        """
        file = int(mousePos[0] // (art.fromTileSize[0]))
        rank = 7 - int(mousePos[1] // (art.fromTileSize[1]))
        return data.file_rank_to_index(rank * 8 + file)


    def set_from_index_120(self, mousePos: Tuple[int, int], gameBoard: board.Board()) -> None:
        """ Set the from square to indicate a piece about to move.
            120sq based index.

        :param mousePos: The (x, y) values of the mouse.
        :param gameBoard: The game board object including information for each successive turn.
        """
        temp = self.mouse_pos_to_120(mousePos)
        # If a piece is not selected, return.
        if gameBoard.pieces[temp] == enums.Piece.EMPTY.value:
            return

        self.from120 = temp
        # Set the coordinates for the fromTile artifact.
        artifacts.set_from_tile(gameBoard, self.from120)


    def set_to_index_120(self, mousePos: Tuple[int, int]) -> None:
        """ Set the to square to indicate where to move a piece to.
            120sq based index.

        :param mousePos: The (x, y) values of the mouse.
        """
        file = int(mousePos[0] // (art.fromTileSize[0]))
        rank = 7 - int(mousePos[1] // (art.fromTileSize[1]))
        self.to120 = data.file_rank_to_index(rank * 8 + file)

    def update_history(self, gameBoard: board.Board()) -> None:
        """ Bit shift all relavent move information into a variable and store it in history array.
            Contains from, to 120sq indices, captured piece, promotion piece, castling permissions, en passant square.
            Also sets PGN.

        :param gameBoard: The game board object including information for each successive turn.
        """
        move = 0
        move |= self.from120 # 7 bits determining where the piece is moving from
        move |= (self.to120 << 7) # 7 bits determining where the piece is moving to
        move |= (self.capturedPiece << 14) # 4 bits determining which piece was captured

        # If enPassant capture.
        if self.enPassant != enums.Tiles.NO_SQUARE.value:
            move |= enums.MoveBitmasks.EN_PASSANT_MASK.value # Forcing true for now.

        # If a white pawn has moved, or a black pawn has moved.
        if (self.fromPiece == enums.Piece.wP.value and data.RanksBrd[self.from120] ==
             enums.Rank.RANK_2.value) or (self.fromPiece == enums.Piece.bP.value and
             data.RanksBrd[self.from120] == enums.Rank.RANK_7.value):
            move |= enums.MoveBitmasks.PAWN_START_MASK.value

        # If white or black is promoting.
        if (self.fromPiece == enums.Piece.wP.value and data.RanksBrd[self.to120] ==
             enums.Rank.RANK_8.value) or (self.fromPiece == enums.Piece.bP.value 
             and data.RanksBrd[self.to120] == enums.Rank.RANK_1.value):
            match self.promPiece:
                case enums.Piece.wQ.value | enums.Piece.bQ.value:
                    move |= enums.MoveBitmasks.PROMOTED_Q_MASK.value
                case enums.Piece.wN.value | enums.Piece.bN.value:
                    move |= enums.MoveBitmasks.PROMOTED_N_MASK.value
                case enums.Piece.wR.value | enums.Piece.bR.value:
                    move |= enums.MoveBitmasks.PROMOTED_R_MASK.value
                case enums.Piece.wB.value | enums.Piece.bB.value:
                    move |= enums.MoveBitmasks.PROMOTED_B_MASK.value

        # If it was a castling move.
        if (True):
            move |= enums.MoveBitmasks.CASTLING_MASK.value # Forcing true for now.

        # Handle PGN
        self.process_pgn(gameBoard)

        # Create Undo object and add to history
        currentPosHistory = board.Undo(move, gameBoard.castle, gameBoard.fiftyMoveClock,
                                        gameBoard.enPassant, hashkeys.generate_pos_key(gameBoard))
        gameBoard.history[gameBoard.hisply] = currentPosHistory
        gameBoard.hisply += 1


    def process_pgn(self, gameBoard: board.Board()) -> None:
        """ Create the PGN for the current move and add it to the board object.
        
        :param gameBoard: The game board object including information for each successive turn.
        """
        pgnInstance = ""
        if gameBoard.hisply % 2 == 0:
            pgnInstance += str(int(gameBoard.hisply / 2 + 1)) + ". "
            
        pgnInstance += enums.Tiles(self.to120).name + " "
        gameBoard.pgnArr.append(pgnInstance)

        gameBoard.pgn += pgnInstance


    def process_move(self, mousePos: Tuple[int, int], gameBoard: board.Board()):
        """ The main processing function for a move.

        :param mousePos: The (x, y) values of the mouse.
        :param gameBoard: The game board object including information for each successive turn.
        """
        # If the selected move is the same as the previous move, unselect
        if self.mouse_pos_to_120(mousePos) == self.from120:
            self.from120 = -1
            return

        self.set_to_index_120(mousePos)
        self.check_legal_move(gameBoard)

        # Update pieces array
        self.fromPiece = gameBoard.pieces[self.from120]
        gameBoard.pieces[self.from120] = 0
        self.capturedPiece = gameBoard.pieces[self.to120] # Critical

        # Play capture sound
        if self.capturedPiece != enums.Piece.EMPTY.value:
            menu.play_sound("capturePiece")
        else:
            menu.play_sound("movePiece")

        gameBoard.pieces[self.to120] = self.fromPiece

        # If white promotion
        if (self.fromPiece == enums.Piece.wP.value and data.RanksBrd[self.to120] ==
             enums.Rank.RANK_8.value and (not self.prom)):
            self.prom = 1
            artifacts.set_prom_pos(gameBoard, self.to120, self.prom)

            return
        
        # Elif black promotion
        elif (self.fromPiece == enums.Piece.bP.value and data.RanksBrd[self.to120] ==
               enums.Rank.RANK_1.value and (not self.prom)):
            self.prom = 2
            artifacts.set_prom_pos(gameBoard, self.to120, self.prom)

            return
        
        # Update board materials
        gameBoard.update_materials()

        # Update move history
        self.update_history(gameBoard)

        # Update artifact images for pieces.
        artifacts.update_pieces(gameBoard)
        artifacts.set_piece_imgs_positions(gameBoard)

        # Update 50 move clock
        if self.fromPiece == enums.Piece.wP.value or self.fromPiece == enums.Piece.bP.value: # Also need to handle piece capture
            gameBoard.fiftyMoveClock = 0

        # Change who's turn it is
        gameBoard.turn = int(not gameBoard.turn)

        self.reset_move()        
    

    def undo_move(self, gameBoard: board.Board()) -> None:
        """ Undoes the action of a move, restoring all properties to previous position.

        :param gameBoard: The game board object including information for each successive turn.
        """
        previousUndoObject = gameBoard.history[gameBoard.hisply - 1]

        # If there is a move to undo.
        if previousUndoObject:
            previousMove = previousUndoObject.move

            from120 = previousMove & enums.MoveBitmasks.FROM_MASK.value
            to120 = (previousMove & enums.MoveBitmasks.TO_MASK.value) >> enums.MoveBitmasks.TO_SHIFT.value
            capturedPiece = (previousMove & enums.MoveBitmasks.CAPTURED_MASK.value) >> enums.MoveBitmasks.CAPTURED_SHIFT.value
            piece = gameBoard.pieces[to120]

            # Set pawn to correct colour when undoing a promotion.
            if (previousMove & enums.MoveBitmasks.PROMOTED_PIECE_MASK.value and gameBoard.turn == enums.Turn.BLACK.value):
                piece = enums.Piece.wP.value
            elif (previousMove & enums.MoveBitmasks.PROMOTED_PIECE_MASK.value and gameBoard.turn == enums.Turn.WHITE.value):
                piece = enums.Piece.bP.value

            gameBoard.pieces[from120] = piece
            gameBoard.pieces[to120] = capturedPiece

            gameBoard.castle = previousUndoObject.castle
            gameBoard.fiftyMoveClock = previousUndoObject.fiftyMoveClock
            gameBoard.enPassant = previousUndoObject.enPassant
            gameBoard.posKey = previousUndoObject.hashKey

            gameBoard.hisply -= 1 if gameBoard.hisply > 0 else 0
            gameBoard.fiftyMoveClock -= 1 if gameBoard.fiftyMoveClock > 0 else 0
            gameBoard.turn = int(not gameBoard.turn)
            self.prom = False

            gameBoard.update_materials()

            # Update PGN
            gameBoard.pgn = ""
            gameBoard.pgnArr.pop()
            for i in range(gameBoard.hisply):
                gameBoard.pgn += gameBoard.pgnArr[i]

            # Update artifact images for pieces.
            artifacts.set_piece_imgs_positions(gameBoard)
    

    def handle_prom(self, gameBoard: board.Board(), promPiece: int) -> None:
        """ Set appropriate values when a promotion occurs in the game to the gameBoard.
        
        :param gameBoard: The game board object including information for each successive turn.
        :param promPiece: The piece promoted to.
        """
        self.promPiece = promPiece

        gameBoard.pieces[self.from120] = enums.Piece.EMPTY.value
        gameBoard.pieces[self.to120] = self.promPiece

        gameBoard.update_materials()
        gameBoard.turn = int(not gameBoard.turn)

        artifacts.set_piece_imgs_positions(gameBoard)

        self.update_history(gameBoard)
        self.reset_move()


    def reset_move(self) -> None:
        """ Resets all of the instance variables of the move object.
        """
        self.from120 = -1
        self.to120 = -1

        self.capturedPiece = 0
        self.fromPiece = 0

        self.prom = 0
        self.promPiece = 0


    def check_legal_move(self, gameBoard: board.Board) -> None:
        """ Incomplete function to check if an attempted move is legal.
            Will restrict if illegal.
        
        :param gameBoard: The game board object including information for each successive turn.
        """
        if gameBoard.turn == enums.Turn.WHITE.value:
            pass
        else:
            pass