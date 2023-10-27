""" Stores all of the information pertaining to the match.

:author: Ben Hickman
:date: 2023/10/26
:version: v1.0.0
"""
import enums
import data
import bitboards
import hashkeys
from ctypes import c_ulonglong as ull, c_uint as uint

# FEN to load the pieces onto the board.
STARTING_POS_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

class Board():
    """ Contains all of the data structures for the entire chess match.
    """
    def __init__(self):
        self.pieces = (ull * 120)()

        for i in range(120):
            self.pieces[i] = enums.Tiles.OFF_BOARD.value

        self.turn = enums.Turn.WHITE.value 
        # Int (4 bits representing all castle positions, start at 1111)
        self.castle = 15 

        # Int (Represents an index on the size 120 array for the enPassant square when a pawn was previously moved.)
        self.enPassant = enums.Tiles.NO_SQUARE.value
        # Int (Represents the number of half moves made in a game since pawn move or piece capture)
        self.fiftyMoveClock = 0 
        # Int (Represents the number of full moves that have been played in the match.)
        self.fullMoves = 0 

        self.kingSquare = (uint * 2)()
        self.hisply = 0

        self.map64To120 = (ull * 64)()
        self.map120To64 = (ull * 120)()

        # Holds the number of each of the 13 piece types. Index 0 represents NO_PIECE, and indicates empty squares.
        self.pceNum = (uint * 13)()
        # Holds the number of white big pieces, and black big pieces, respectively.
        self.bigPce = (uint * 2)()
        # Holds the number of white major pieces, and black major pieces, respectively.
        self.majPce = (uint * 2)()
        # Holds the number of white minor pieces, and black minor pieces, respectively.
        self.minPce = (uint * 2)()
        # Holds the value of white material, and black material, respectively.
        self.material = (uint * 2)()

        # Holds the square (0, 120) of each piece in a 2D array.
        self.pList = (uint * 10 * 13)()

        self.pawns = [None] * 3
        for i in range(3):
            self.pawns[i] = ull(0)

        self.posKey = 0
        self.history = [None] * 2048

        self.pgnArr = []
        self.pgn = ""

        self.historyStack = []
        self.historyStackCounts = []

        # Initialize the board maps
        self.init_board_maps()

        # Initialize the starting position on the board
        self.read_fen(STARTING_POS_FEN)

        # Initially update the materials
        self.update_materials()
        self.check_board()


    def print_object(self) -> None:
        """ Print to console all of the contents of the board object for debugging.
        """
        print("Turn: ", self.turn)
        print("Castle Permissions: ", bin(self.castle))
        print("En Passant Square: ", self.enPassant)
        print("Fifty Move Clock: ", self.fiftyMoveClock)
        print("Full Moves Count: ", self.fullMoves)

        print("pceNum: [", end ="")
        for i in range(13):
            print(self.pceNum[i], end = " ")

        print("]\nbigPce: [", end = "")
        for i in range(2):
            print(self.bigPce[i], end = " ")

        print("]\nmajPce: [", end = "")    
        for i in range(2):    
            print(self.majPce[i], end = " ")

        print("]\nminPce: [", end = "")   
        for i in range(2):    
            print(self.minPce[i], end = " ")

        print("]\nmaterial: [", end = "")  
        for i in range(2):    
            print(self.material[i], end = " ")
        print("]")
        
        print("pawns[0]: ", bitboards.print_bin(self.pawns[0]))
        print("pawns[1]: ", bitboards.print_bin(self.pawns[1]))
        print("pawns[2]: ", bitboards.print_bin(self.pawns[2]))
        print()
        print("pawns[0]: ", bitboards.printBitBoard(self.pawns[0]))
        print("pawns[1]: ", bitboards.printBitBoard(self.pawns[1]))
        print("pawns[2]: ", bitboards.printBitBoard(self.pawns[2]))


    def reset_materials(self) -> None:
        """ Reset all of the datatypes within the board object.
        """
        self.pawns = (ull * 3)()
        self.kingSquare = (uint * 2)()

        self.pceNum = (uint * 13)()
        self.bigPce = (uint * 2)()
        self.majPce = (uint * 2)()
        self.minPce = (uint * 2)()
        self.material = (uint * 2)()

        self.pList = (uint * 10 * 13)()

        self.pawns = [None] * 3
        for i in range(3):
            self.pawns[i] = ull(0)


    def update_materials(self) -> None:
        """ Updates all of the data structures. Called when a move has been made or undone.
        """
        self.reset_materials()

        for sq120 in range(0, 120):
            piece = self.pieces[sq120]

            if piece != enums.Tiles.NO_SQUARE.value and piece != enums.Tiles.OFF_BOARD.value and piece != enums.Piece.EMPTY.value:
                colour = data.PieceCol[piece]

                if piece == enums.Piece.wP.value:
                    self.pawns[enums.Turn.WHITE.value] = bitboards.set_bit(self.pawns[enums.Turn.WHITE.value], self.map120To64[sq120])
                    self.pawns[enums.Turn.BOTH.value] = bitboards.set_bit(self.pawns[enums.Turn.BOTH.value], self.map120To64[sq120])

                elif piece == enums.Piece.bP.value:
                    self.pawns[enums.Turn.BLACK.value] = bitboards.set_bit(self.pawns[enums.Turn.BLACK.value], self.map120To64[sq120])
                    self.pawns[enums.Turn.BOTH.value] = bitboards.set_bit(self.pawns[enums.Turn.BOTH.value], self.map120To64[sq120])    

                # If the piece is a king, it is also a major piece and a big piece
                elif piece == enums.Piece.wK.value or piece == enums.Piece.bK.value:
                    self.kingSquare[colour] = sq120
                    self.majPce[colour] += 1
                    self.bigPce[colour] += 1
                # If the piece is a major piece, it is also a big piece
                elif data.PieceMaj[piece]:
                    self.majPce[colour] += 1
                    self.bigPce[colour] += 1
                # Else if, the piece is a minor piece, it is also a big piece (elif prevents double counting big piece)
                elif data.PieceMin[piece]:
                    self.minPce[colour] += 1
                    self.bigPce[colour] += 1

                self.material[colour] += data.PieceVal[piece]

                self.pList[piece][self.pceNum[piece]] = sq120
                self.pceNum[piece] += 1

        self.posKey = hashkeys.generate_pos_key(self)
    

    def init_board_maps(self) -> None:
        """ Initialize the board maps with their respective values.
            Note, these arrays are flipped over the horizontal axis. '0' and '21' represent the bottom left hand corner.

            map120To64:

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

            map64To120:

                A    B    C    D    E    F    G    H
            +----+----+----+----+----+----+----+----+
            1 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 1
            +----+----+----+----+----+----+----+----+
            2 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 2
            +----+----+----+----+----+----+----+----+
            3 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 3
            +----+----+----+----+----+----+----+----+
            4 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 4
            +----+----+----+----+----+----+----+----+
            5 | 61 | 62 | 63 | 64 | 65 | 66 | 67 | 68 | 5
            +----+----+----+----+----+----+----+----+
            6 | 71 | 72 | 73 | 74 | 75 | 76 | 77 | 78 | 6
            +----+----+----+----+----+----+----+----+
            7 | 81 | 82 | 83 | 84 | 85 | 86 | 87 | 88 | 7
            +----+----+----+----+----+----+----+----+
            8 | 91 | 92 | 93 | 94 | 95 | 96 | 97 | 98 | 8
            +----+----+----+----+----+----+----+----+
                A    B    C    D    E    F    G    H
        """

        sq = 21
        sq64 = 0
        for rank in range (8): # Iterate up each file. (Board is printed flipped on horizontal axis.)
            for file in range(8): # Iterate across each rank.
                sq = data.file_rank_to_index(rank * 8 + file)
                self.map64To120[sq64] = sq
                self.map120To64[sq] = sq64
                sq64 += 1
    
    
    def read_fen(self, fen: str) -> None:
        """ Parse input FEN and setup board with pieces respective of FEN.
        
        :param fen: The string to parse.
        """
        rank = enums.Rank.RANK_8.value
        file = enums.File.FILE_A.value
        piece = 0

        # Start at rank 8 and iterate.
        while ((rank >= enums.Rank.RANK_1.value) and fen):
            char = fen[0]
            # Represents duplicates within FEN.
            count = 1

            match char:
                case 'P': piece = enums.Piece.wP.value
                case 'N': piece = enums.Piece.wN.value
                case 'B': piece = enums.Piece.wB.value
                case 'R': piece = enums.Piece.wR.value
                case 'Q': piece = enums.Piece.wQ.value
                case 'K': piece = enums.Piece.wK.value

                case 'p': piece = enums.Piece.bP.value
                case 'n': piece = enums.Piece.bN.value
                case 'b': piece = enums.Piece.bB.value
                case 'r': piece = enums.Piece.bR.value
                case 'q': piece = enums.Piece.bQ.value
                case 'k': piece = enums.Piece.bK.value

                case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8':
                    piece = enums.Piece.EMPTY.value
                    count = int(char)

                case '/' | ' ':
                    file =  enums.File.FILE_A.value
                    rank -= 1
                    fen = fen[1:]
                    continue

                case _:
                    pass

            for _ in range(count):
                sq64 = rank * 8 + file
                sq120 = self.map64To120[sq64]

                self.pieces[sq120] = piece
                file += 1

            # Set King Squares
            if char == 'K':
                self.kingSquare[0] = sq120
            elif char == 'k':
                self.kingSquare[1] = sq120

            fen = fen[1:]

        self.side = enums.Turn.WHITE.value if (fen[0] == 'w') else enums.Turn.BLACK.value
        fen = fen[2:]

        for _ in range(4):
            if fen[0] == ' ':
                break

            char = fen[0]
            match char:
                case 'K': self.castle |= enums.Castle.WKCA.value
                case 'Q': self.castle |= enums.Castle.WQCA.value
                case 'k': self.castle |= enums.Castle.BKCA.value
                case 'q': self.castle |= enums.Castle.BQCA.value
                case _: pass

            fen = fen[1:]

        fen = fen[1:]

        if fen[0] != '-':
            file = ord(fen[0]) - 97
            rank = ord(fen[1]) - 49

            self.enPassant = data.file_rank_to_index(rank * 8 + file)


    def print_board(self) -> None:
        """ Prints an ASCII representation of the board to the console.
        """
        for i in range(120):
            print(self.pieces[i], end = " ")

            if (i + 1) % 10 == 0:
                print("\n", end = "")

            if (self.pieces[i] < 10):
                print(" ", end = "")


    def check_board(self) -> None:
        """ Assert that all values within the board's data structures match.
            Close program with assertion otherwise.
        """
        tempPceNum = (uint * 13)()
        tempBigPce = (uint * 2)()
        tempMajPce = (uint * 2)()
        tempMinPce = (uint * 2)()
        tempMaterial = (uint * 2)()
        
        tempPawns = [None] * 3
        for i in range(3):
            tempPawns[i] = self.pawns[i]

        for tempPiece in range (1, 13):
            tempPieceNum = 0

            while tempPieceNum < self.pceNum[tempPiece]:
                sq120 = self.pList[tempPiece][tempPieceNum]

                assert(self.pieces[sq120] == tempPiece)

                tempPieceNum += 1

        # Set tempBig, min, MajPce and tempMaterial
        for sq120 in range(0, 120):
            tempPiece = self.pieces[sq120]

            # If not equal to no square and not equal to off board and not equal to off board.
            if tempPiece != enums.Tiles.NO_SQUARE.value and (tempPiece != enums.Tiles.OFF_BOARD.value
                ) and tempPiece != enums.Piece.EMPTY.value:
                tempColour = data.PieceCol[tempPiece]

                if data.PieceMaj[tempPiece]:
                    tempMajPce[tempColour] += 1
                    tempBigPce[tempColour] += 1
                elif data.PieceMin[tempPiece]:
                    tempMinPce[tempColour] += 1
                    tempBigPce[tempColour] += 1

                tempMaterial[tempColour] += data.PieceVal[tempPiece]

                tempPceNum[tempPiece] += 1

        # Assert tempPieceNum
        for tempPiece in range(13):
            assert(tempPceNum[tempPiece] == self.pceNum[tempPiece])

        numWP = self.pceNum[enums.Piece.wP.value]
        numBP = self.pceNum [enums.Piece.bP.value]

        # Assert bitboards counts
        assert(bitboards.CountBits(tempPawns[0]) == numWP)
        assert(bitboards.CountBits(tempPawns[1]) == numBP)
        assert(bitboards.CountBits(tempPawns[2]) == numWP + numBP)

        while (tempPawns[0]):
            sq64 = bitboards.pop_bit((tempPawns[0]))
            assert(self.pieces[self.map64To120[sq64]] == enums.Piece.wP.value)

        while (tempPawns[1]):
            sq64 = bitboards.pop_bit((tempPawns[1]))
            assert(self.pieces[self.map64To120[sq64]] == enums.Piece.bP.value)

        while (tempPawns[2]):
            sq64 = bitboards.pop_bit((tempPawns[2]))
            assert(self.pieces[self.map64To120[sq64]] == enums.Piece.wP.value or self.pieces[self.map64To120[sq64]] == enums.Piece.bP.value)

        assert(tempMaterial[0] == self.material[0])
        assert(tempMaterial[1] == self.material[1])

        assert(tempBigPce[0] == self.bigPce[0])
        assert(tempBigPce[1] == self.bigPce[1])

        assert(tempMajPce[0] == self.majPce[0])
        assert(tempMajPce[1] == self.majPce[1])

        assert(tempMinPce[0] == self.minPce[0])
        assert(tempMinPce[1] == self.minPce[1])

        assert(self.side == 0 or self.side == 1)

        assert(hashkeys.generate_pos_key(self) == self.posKey)
        
        assert(self.enPassant == enums.Tiles.NO_SQUARE.value or (data.RanksBrd[self.enPassant] == enums.Rank.RANK_6 and self.side == enums.Turn.WHITE.value) or (data.RanksBrd[self.enPassant] == enums.Rank.RANK_3 and self.side == enums.Turn.BLACK.value))

        assert(self.pieces[self.kingSquare[enums.Turn.WHITE.value]] == enums.Piece.wK.value)
        assert(self.pieces[self.kingSquare[enums.Turn.BLACK.value]] == enums.Piece.bK.value)

        assert(0 <= self.castle <= 15)

        def pce_list_assert() -> None:
            """ Assert that the pceNum values are between (1, 9) and not off the board.
            """
            for pce in range(1, 13):
                if 0 > self.pceNum[pce] >= 10:
                    return False
                
                for i in range(self.pceNum[pce]):
                    sq = self.pList[pce][i]
                    if (data.FilesBrd[sq] == enums.Tiles.OFF_BOARD.value):
                        return False
                    
            if self.pceNum[enums.Piece.wK.value] != 1 or self.pceNum[enums.Piece.bK.value] != 1:
                return False
                
        assert(pce_list_assert)

class Undo():
    def __init__(self, move: int, castle: int , fiftyMoveClock: int, enPassant: int, hashKey: int):
        """ Contains all of the information of a given move to restore it when undoing.
            0000 0000 0000 0000 0000 0111 1111: From Square [21 to 98]
            0000 0000 0000 0011 1111 1000 0000: To Square [21 to 98]
            0000 0000 0011 1100 0000 0000 0000: Captured Piece [1 to 12]
            0000 0000 0100 0000 0000 0000 0000: Is an en passant capture?
            0000 0000 1000 0000 0000 0000 0000: Pawn Start?
            0000 1111 0000 0000 0000 0000 0000: Promoted Piece? (Knight, Bishop, Rook, Queen), 1 bit for each (maybe could be done with less bits)
            0001 0000 0000 0000 0000 0000 0000: Was it a castling move? (Would you even need to set this? Couldn't you just have king move 2 squares as that is unique?)
        """
        self.move = move
        self.castle = castle
        self.fiftyMoveClock = fiftyMoveClock
        self.enPassant = enPassant
        self.hashKey = hashKey