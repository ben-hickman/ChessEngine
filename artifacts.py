""" Artifacts file containing positioning and size of all game artifacts.

:author: Ben Hickman
:date: 2023/10/26
:version: v1.0.0
"""
import data
import enums
import board
import attacks
import bitboards

import os
import pygame

from typing import Tuple

# Size: (width, height)
ART_SIZES = {
    # Board
    "board": (1080, 1080),
    "fromTile": (135, 135),
    "prom": (135, 540),

    # Misc
    "turnBox": (635, 195),
    "turnText": 210,
    "undo": (130, 195),

    # Nav
    "hamburger": (75, 75),
    "home": (75, 75),
    "mute": (75, 75),
    "showAttacks": (75, 75),
    "sideNavBar": (75, 1080),
    "slash": (75, 75),
    "speaker": (75, 75),
    
    # PGN
    "pgnBox": (765, 885),
    "pgnHeader": 36,
    "pgnText": 24, 

    # Settings
    "fs": [(135, 135), (135, 135)],
    "res": [(135, 135), (135, 135), (135, 135), (135, 135), (135, 135)],
    "save": (192, 108),
    "fsText": 24,
    "saveText": 72    
}


# Positions: (x, y) from top left
ART_POS = {
    # Board
    "board": (0, 0),
    "fromTile": (0, 0),
    "prom": (0, 0),

    # Misc
    "turnBox": (1210, 900),
    "undo": (1080, 885),

    # Nav
    "hamburger": (1845, 0),
    "home": (1845, 0),
    "mute": (1845, 75),
    "showAttacks": (1845, 150),
    "sideNavBar": (1845, 0),
    "slash": (1845, 150),
    "speaker": (1845, 75),
    
    # PGN
    "pgnBox": (1080, 0),
    "pgnHeader": (1090, 10),
    "pgnText": (1120, 40),

    # Settings
    "fs": [(1, 1), (135, 1)],
    "res": [(1, 135), (135, 135), (270, 135), (405, 135), (540, 135)],
    "save": (865, 486),
}


BASE_WIDTH = 1920
BASE_HEIGHT = 1080
ASPECT_RATIO = BASE_WIDTH / BASE_HEIGHT


def import_img() -> None:
    """ Map artifacts to image filenames, and appropriately scale the image.
        Sets up images to be ready to display for current display dimension.
        Separate alpha scaling for transparent images.
    """

    # Maps the name of an artifact to it's filename.
    imgMap = {
        "board": "chess_board.png",
        "undo": "uno_reverse_card.webp"
    }

    # Maps the name of a transparent artifact to it's filename.
    imgMapAlpha = {
        "9": "black_bishop.png",
        "12": "black_king.png",
        "8": "black_knight.png", 
        "7": "black_pawn.png",
        "11": "black_queen.png",
        "10": "black_rook.png",
        "3": "white_bishop.png",
        "6": "white_king.png",
        "2": "white_knight.png", 
        "1": "white_pawn.png",
        "5": "white_queen.png",
        "4": "white_rook.png",

        "hamburger": "hamburger_menu.png",
        "home": "home_icon.png",
        "showAttacks": "magnifying_glass.png",
        "slash": "slash.png",
        "mute": "mute_icon.png",
        "speaker": "speaker_icon.png",
    }

    # convert()
    for key in imgMap:
        Artifacts.imgs[key] = pygame.transform.scale(pygame.image.load("images/" + imgMap.get(key)).convert(), ART_SIZES[key])

    # convert_alpha()
    for key in imgMapAlpha: # fromTile is the size of a tile
        sizeKey = key

        if key.isnumeric():
            sizeKey = "fromTile"
            
        Artifacts.imgs[key] = pygame.transform.scale(pygame.image.load("images/" + imgMapAlpha.get(key)).convert_alpha(), ART_SIZES[sizeKey])


def import_sound() -> None:
    """ Maps sounds to sound filenames.

    :raises FileNotFoundError: If the sound file could not be located.
    :raises pygame.error: If the mixer was not initialized, usually upon running for the first time.
    """
    soundNameMapping = {
        "capturePiece": "capture_piece.mp3",
        "movePiece": "move_piece.mp3",
        "undoMove": "undo_move.mp3"
    }
    for sound in soundNameMapping:
        try:
            Artifacts.sounds[sound] = pygame.mixer.Sound("sounds/" + soundNameMapping.get(sound))
        except FileNotFoundError:
            print("Could not find file: ", soundNameMapping[sound], end = "")

            if os.name == "nt":
                print("in ChessEngine/sounds")
            else:
                print("in ChessEngine\sounds")
        except pygame.error:
            print("The mixer was not properly initialized. Unable to play sound.")


class Artifacts():
    """ A static class containing the size and positioning of attributes.
        Attributes are recomputed upon a window resize.
    
    """
    # Board
    boardSize = boardPos = None
    fromTileSize = fromTilePos = None
    promSize = promPos = None

    # Misc
    turnBoxSize = turnBoxPos = None
    turnTextFont = None
    undoSize = undoPos = None

    # Nav
    hamburgerSize = hamburgerPos = None
    homeSize = homePos = None
    muteSize = mutePos = None
    showAttacksSize = showAttacksPos = None
    sideNavBarSize = sideNavBarPos = None
    slashSize = slashPos = None
    speakerSize = speakerPos = None
    
    # PGN
    pgnBoxSize = pgnBoxPos = None
    pgnHeaderFont = pgnHeaderPos = None
    pgnTextFont = pgnTextPos = None

    # Settings
    fsSize = fsPos = None
    fsTextFont = None
    resSize = resPos = None
    saveSize = savePos = None
    saveTextFont = None

    # Maps    
    imgs = {}
    scaledImgs = {}
    pieceImgsPos = {}
    sounds = {}

    # Lists
    attackedTiles = []


def calculate_resize(screenWidth, screenHeight, gameBoard) -> None:
    """ Resize all attributes, text and scale images for a window resize event.
    
    :param screenWidth: The current screen width to scale by.
    :param screenHeight: The current screen height to scale by.
    :param gameBoard: The game board object including information for each successive turn.
    """
    # Scale by the min of current screen height and current screen width.
    if screenWidth / screenHeight < ASPECT_RATIO:
        currDim = screenWidth
        baseDim = BASE_WIDTH
    else:
        currDim = screenHeight
        baseDim = BASE_HEIGHT

    resize_general_attrs(screenWidth, currDim, baseDim)
    resize_misc_attrs(screenWidth, screenHeight, currDim, baseDim)
    resize_settings_bttns(currDim, baseDim)

    text_resize(screenWidth, screenHeight, currDim, baseDim)

    update_pieces(gameBoard)
    update_imgs()
    set_piece_imgs_positions(gameBoard)
    set_attacked_tiles(gameBoard)


def resize_misc_attrs(screenWidth, screenHeight, currDim, baseDim) -> None:
    """ Resize attributes with window size.
        These attributes have special positioning.
    
    :param screenWidth: The current screen width to scale by.
    :param screenHeight: The current screen height to scale by.
    :param currDim: Screen width if the width drops below the aspect ratio, else screen height.
    :param baseDim: BASE_WIDTH or BASE_HEIGHT, matching currDim.
    """
    # Set sideNavBar, height is screen height and floats right.
    Artifacts.sideNavBarSize = (currDim / (baseDim / ART_SIZES["sideNavBar"][0]), screenHeight)
    Artifacts.sideNavBarPos = (screenWidth - Artifacts.sideNavBarSize[0], ART_POS["sideNavBar"][1])

    # Set save button, floats bottom of screen.
    Artifacts.saveSize = (currDim / (baseDim / ART_SIZES["save"][0]),  currDim / (baseDim / ART_SIZES["save"][1]))
    Artifacts.savePos = (screenWidth / (BASE_WIDTH / ART_POS["save"][0]), screenHeight - Artifacts.saveSize[1])


def resize_general_attrs(screenWidth, currDim, baseDim) -> None:
    """ Resize attributes with window size.
        Attributes shrink with window size with absolute positioning, unless specified to float right.

    :param screenWidth: The current screen width to scale by.
    :param currDim: Screen width if the width drops below the aspect ratio, else screen height.
    :param baseDim: BASE_WIDTH or BASE_HEIGHT, matching currDim.
    """
    # Shrink attributes with window width to top left of screen.
    for attr in data.generalAttrs:
        xSize = currDim / (baseDim / ART_SIZES[attr][0]) if ART_SIZES[attr][0] != 0 else 0
        ySize = currDim / (baseDim / ART_SIZES[attr][1]) if ART_SIZES[attr][1] != 0 else 0

        # xPos absolute if not in floatRightAttrs, else xPos for attr floats right.
        xPos = screenWidth - xSize if attr in data.floatRightAttrs else currDim / (baseDim / ART_POS[attr][0]) if ART_POS[attr][0] != 0 else 0
        yPos = currDim / (baseDim / ART_POS[attr][1]) if ART_POS[attr][1] != 0 else 0

        setattr(Artifacts, attr + "Size", (xSize, ySize))
        setattr(Artifacts, attr + "Pos", (xPos, yPos))


def resize_settings_bttns(currDim, baseDim) -> None:
    """ Resize all of the buttons within the settings menu.

    :param currDim: Screen width if the width drops below the aspect ratio, else screen height.
    :param baseDim: BASE_WIDTH or BASE_HEIGHT, matching currDim.
    """
    # Settings buttons attributes
    
    for attr in data.bttnsAttrs:
        size = [(currDim / (baseDim / ART_SIZES[attr][i][0]), currDim /
                  (baseDim / ART_SIZES[attr][i][1])) for i in range(len(ART_SIZES[attr]))]
        
        pos = [(currDim / (baseDim / ART_POS[attr][i][0]), currDim /
                 (baseDim / ART_POS[attr][i][1])) for i in range(len(ART_POS[attr]))]

        setattr(Artifacts, attr + "Size", size)
        setattr(Artifacts, attr + "Pos", pos)


def text_resize(screenWidth, screenHeight, currDim, baseDim) -> None:
    """ Resize the text relative the min of screenWidth, screenHeight.
        Called whenever there is a window resize.
    
    :param screenWidth: The current screen width to scale by.
    :param screenHeight: The current screen height to scale by.
    :param currDim: Screen width if the width drops below the aspect ratio, else screen height.
    :param baseDim: BASE_WIDTH or BASE_HEIGHT, matching currDim.
    """
    ratio = min(screenWidth / BASE_WIDTH, screenHeight / BASE_HEIGHT)

    # Update font sizes
    for attr in data.fontAttrs:
        setattr(Artifacts, attr + "Font", pygame.font.Font(data.COURIER_FONT, size = int(ART_SIZES[attr] * ratio)))

    # Update pgn text positions
    for attr in data.pgnAttrs:
        pos = (currDim / (baseDim / ART_POS[attr][0]), currDim / (baseDim / ART_POS[attr][1]))
        setattr(Artifacts, attr + "Pos", pos)


def update_pieces(gameBoard: board.Board()) -> None:
    """ Updates the scaling of the pieces images and restores their values.
        Called whenever there is a window resize.

    :param gameBoard: The board object including information for each successive turn.
    """
    for i in range(8):
        for j in range(8):
            sq = data.file_rank_to_index(i * 8 + j)
            piece = gameBoard.pieces[sq]

            if piece != enums.Piece.EMPTY.value:
                Artifacts.scaledImgs[str(piece)] = pygame.transform.scale(Artifacts.imgs[str(piece)], Artifacts.fromTileSize)


def update_imgs() -> None:
    """ Updates the scaling of the images and re-stores their values.
        Called whenever there is a window resize.
    """
    for key in data.nonPceImgs:
        Artifacts.scaledImgs[key] = pygame.transform.scale(Artifacts.imgs[key], getattr(Artifacts, key + "Size"))


def is_clicked(artifact: str, mousePos: Tuple[int, int], index: int = False) -> bool:
    """ Returns true if the artifact is clicked, False otherwise.

    :param artifact: A string representing the given artifact, used for key indexing.
    :param index: An integer representing an index. False by default, for artifacts that are not list like.
    :returns: A boolean determining if an artifact was clicked by the mouse.
    """
    if index:
        tempSize = getattr(Artifacts, artifact + "Size")[index]
        tempPos = getattr(Artifacts, artifact + "Pos")[index]
    
    else:
        tempSize = getattr(Artifacts, artifact + "Size")
        tempPos = getattr(Artifacts, artifact + "Pos")

    if tempPos[0] <= mousePos[0] <= tempPos[0] + tempSize[0] and tempPos[1] <= mousePos[1] <= tempPos[1] + tempSize[1]:
        return True
    
    return False


def is_clicked_prom(promPos: Tuple[int, int], mousePos: Tuple[int, int], prom: int) -> int:
    """ Determine the promotion piece seleted from the promotion menu. 
        Returns the piece, or false (`0`) if not selected.

    :param promPos: The coordinates of the promotion menu.
    :param mousePos: The coordinates of the mouse click.
    :param prom: A tertiary value representing (no, white, black) -> (0, 1, 2) promotion.

    :returns: The promoted piece, or a false int (`0`) if not selected.
    """
    # If the horizontal position of the mouse click is within the promotion menu.
    if promPos[0] < mousePos[0] < promPos[0] + Artifacts.fromTileSize[0]:
        # The position within the promotion menu: which piece is selected. Works for both sides.
        index = int((mousePos[1] - promPos[1]) / Artifacts.fromTileSize[0] // 1)

        if 0 <= index <= 3:
            if prom == 1:
                promPiece = data.whitePromPieces[index].value
            else:
                promPiece = data.blackPromPieces[index].value

            return promPiece
        
    return 0


def set_prom_pos(gameBoard: board.Board(), to120: int, prom: int) -> None:
    """ Set the coordinates of the promotion menu, respective of which side is promoting.
    
    :param gameBoard: The board object including information for each successive turn.
    :param to120: The 120sq index representing where a piece is moving to.
    :param prom: A tertiary value representing (no, white, black) -> (0, 1, 2) promotion.
    """
    index = gameBoard.map120To64[to120]

    rank = index // 8
    file = (index / 8 - rank) * 8

    if prom == 1: # White
        Artifacts.promPos = (file * Artifacts.fromTileSize[0], (7 - rank) * Artifacts.fromTileSize[1])

    elif prom == 2: # Black
        Artifacts.promPos = (file * Artifacts.fromTileSize[0], ((7 - rank) * Artifacts.fromTileSize[1]) - Artifacts.fromTileSize[1] * 3)


def set_from_tile(gameBoard: board.Board(), from120: int) -> None:
    """ Set the coordinates of the `fromTile`, the highlighted square to move a piece from.
    
    :param gameBoard: The board object including information for each successive turn.
    :param from120: The 120sq index representing where to draw previous position.
    """
    index = gameBoard.map120To64[from120]

    rank = index // 8
    file = (index / 8 - rank) * 8

    Artifacts.fromTilePos = (file * Artifacts.fromTileSize[0], (7 - rank) * Artifacts.fromTileSize[1])


def set_piece_imgs_positions(gameBoard: board.Board()) -> None:
    """ Map the scaled piece images to their respective position on the board.

    :param gameBoard: The board object including information for each successive turn.
    """
    for i in range(8):
        for j in range(8):
            sq = data.file_rank_to_index(i * 8 + j)
            piece = gameBoard.pieces[sq]

            if piece != enums.Piece.EMPTY.value:
                dest = (j * Artifacts.fromTileSize[0], (7 - i) * Artifacts.fromTileSize[1])
                Artifacts.pieceImgsPos[sq] = (Artifacts.scaledImgs[str(piece)], dest)

            else:
                Artifacts.pieceImgsPos.pop(sq, None)


def set_attacked_tiles(gameBoard: board.Board()) -> None:
    """ Set the positions for squares currently attacked by opponent.

    :param gameBoard: The board object including information for each successive turn.
    """
    bitboard = attacks.get_attacked_bitboard(gameBoard)
    positions = bitboards.attacked_tiles_64_pos(bitboard)

    Artifacts.attackedTiles.clear()
    for position in positions:
        Artifacts.attackedTiles.append((position[0] * Artifacts.fromTileSize[0], position[1] * Artifacts.fromTileSize[1]))