""" Main chess driver file. Handles UI, and displays the GUI board.

:author: Ben Hickman
:date: 2023/10/26
:version: v1.0.0
"""
import enums
import board
import move
from artifacts import Artifacts as art
import artifacts
import data
import menu

import pygame
from pygame.locals import *

from typing import Tuple

def pygame_setup() -> Tuple[pygame.Surface, pygame.time.Clock, pygame.Surface]:
    """ Initalization functions used for the pygame library.

    :returns:
        The created surface object to be drawn onto.
        The clock object created to track time.
        The settings surface object to be drawn onto.
    """
    # Default pygame initialization.
    pygame.init()

    # Screen to draw onto. Open window on main display.
    screen = pygame.display.set_mode(enums.Resolution.RES_1920_1080.value, flags = pygame.RESIZABLE, display = 0)

    # Set background colour for application.
    screen.fill(data.COLOUR_CHELSEA_CUCUMBER)

    # Keep track of game time.
    clock = pygame.time.Clock()

    # Load Winston the cat into the display window icon.
    pygame.display.set_icon(pygame.image.load("images/monkey.png"))

    # Change the title of the display window.
    pygame.display.set_caption("ChessEngine v1.0.0")

    # Initialize a surface for the settings menu.
    settingsScreen = pygame.display.set_mode(enums.Resolution.RES_1920_1080.value, flags = pygame.RESIZABLE, display = 0)

    return (screen, clock, settingsScreen)


def draw_game_state(screen: pygame.Surface, gameBoard: board.Board, makeMove: move.Move, settingsScreen: pygame.Surface) -> None:
    """ Called for each frame to draw the current game state.
        Draws the board, previous mousePos marker, and then the pieces.

    :param screen: The surface area to draw onto.
    :param gameBoard: The game board object including information for each successive turn.
    :param coords: An object representing pixel values and grid mousePoss for the game.
    :param makeMove: The move object containing information for a given turn.
    :param settingsScreen: The settings surface object to be drawn onto.
    """
    # Fill the background; This should also be moved somewhere else.
    screen.fill(data.COLOUR_CHELSEA_CUCUMBER)

    # Draw the chess board onto the screen, starting from top left corner Already scaled.
    blit_source(screen, art.scaledImgs["board"], art.boardPos)

    # Highlight attack squares on the board.
    if menu.Menu.showAttacks:
        draw_attacked_tiles(screen)

    # If the User has selected a previous square, highlight it.
    if 21 <= makeMove.from120 <= 98:
        draw_rect(screen, art.fromTilePos, art.fromTileSize, data.COLOUR_CLOUDY_BLUE)

    # Draw each of the pieces on the board.
    draw_pieces(screen)

    # If a promotion is active in the game, draw the promotion menu.
    if makeMove.prom:
        draw_prom_piece(screen, makeMove)

    # Write the PGN
    render_pgn(screen, gameBoard)

    # Draw the turn indicator
    render_turn(screen, gameBoard)

    # Blits the undo button onto the screen.
    blit_source(screen, art.scaledImgs["undo"], art.undoPos)

    # Draw the side navigation bar that contains settings menu, and volume toggle.
    draw_rect(screen, art.sideNavBarPos, art.sideNavBarSize, data.COLOUR_LIGHT_TAUPE)

    # Blit the hamburger menu icon for the settings button.
    blit_source(screen, art.scaledImgs["hamburger"], art.hamburgerPos)

    # Blit the mute button onto the navigation bar.
    if menu.Menu.mute:
        blit_source(screen, art.scaledImgs["mute"], art.mutePos)
    # Blit the speaker icon onto the navigation bar.
    else:
        blit_source(screen, art.scaledImgs["speaker"], art.speakerPos)

    # Blit the show moves button onto the navigation bar.
    if menu.Menu.showAttacks:
        blit_source(screen, art.scaledImgs["showAttacks"], art.showAttacksPos)
    else:
        blit_source(screen, art.scaledImgs["showAttacks"], art.showAttacksPos)
        blit_source(screen, art.scaledImgs["slash"], art.slashPos)

    # If user selected settingsPage, display it.
    if menu.Menu.settingsPage:
        draw_settings(screen, settingsScreen)


def draw_settings(screen: pygame.Surface, settingsScreen: pygame.Surface) -> None:
    """ Render all objects for the settings screen.

    :param screen: The surface area to draw onto.
    :param settingsScreen: The settings surface object to be drawn onto.
    """
    # Fill the settings screen background.
    settingsScreen.fill(data.COLOUR_CHELSEA_CUCUMBER)

    # Draw the side navigation bar that contains settings menu, and volume toggle.
    draw_rect(settingsScreen, art.sideNavBarPos, art.sideNavBarSize, data.COLOUR_LIGHT_TAUPE)
    # Blit the home button on the settings screen.
    blit_source(settingsScreen, art.scaledImgs["home"], art.homePos)

    # Render the save button in the settings menu.
    render_settings_save(settingsScreen)
    # Render the fullscreen options in the settings menu.
    render_settings_fullscreen(settingsScreen)
    # Render the resolutions options in the settings menu.
    render_settings_res(settingsScreen)

    # Blit the settings menu.
    blit_source(screen, settingsScreen, (0, 0))


def draw_pieces(screen: pygame.Surface) -> None:
    """ Draw each of the chess pieces from artifacts. Already scaled to correct size.

    :param screen: The surface to be drawn onto.
    """
    for key in art.pieceImgsPos.keys():
        blit_source(screen, *art.pieceImgsPos[key])


def draw_attacked_tiles(screen: pygame.Surface) -> None:
    """ Draw each of the tiles attacked by opponents piece.

    :param screen: The surface to be drawn onto.
    """
    for tilePos in art.attackedTiles:
        rectSurface = pygame.Surface(art.fromTileSize, pygame.SRCALPHA)
        rectSurface.fill(data.COLOUR_RED_CLEAR)
        screen.blit(rectSurface, tilePos)


def render_settings_save(screen: pygame.Surface) -> None:
    """ Draw the save button in the settings menu.
    
    :param screen: The surface to be drawn onto.
    """
    draw_rect(screen, art.savePos, art.saveSize, data.COLOUR_BONE_RED, 3)
    blit_source(screen, render_font(art.saveTextFont, "SAVE"), art.savePos)


def render_settings_fullscreen(screen: pygame.Surface) -> None:
    """ Draw the fullscreen option in the settings menu.

    :param screen: The surface to be drawn onto.
    """
    draw_rect(screen, art.fsPos[0], art.fsSize[0], data.COLOUR_LIGHT_TAUPE)
    draw_rect(screen, art.fsPos[1], art.fsSize[1], data.COLOUR_BONE_RED)

    blit_source(screen, render_font(art.fsTextFont, "FULLSCREEN"), art.fsPos[0])
    text = "ON" if menu.Menu.fullscreen else "OFF"
    blit_source(screen, render_font(art.fsTextFont, text), art.fsPos[1])


def render_settings_res(screen: pygame.Surface) -> None:
    """ Draw the resolution options in the settings menu.

    :param screen: The surface to be drawn onto.
    """
    # For each resolution option, draw the rectangle with appropriate colour and blit it.
    for i in range(5):
        colour = data.COLOUR_BONE_RED if i % 2 == 0 else data.COLOUR_LIGHT_TAUPE

        if i == menu.Menu.resIndex:
            colour = data.COLOUR_CLOUDY_BLUE

        draw_rect(screen, art.resPos[i], art.resSize[i], colour)
        blit_source(screen, render_font(art.fsTextFont, data.res[i]), art.resPos[i])


def render_turn(screen: pygame.Surface, gameBoard: board.Board) -> None:
    """ Draws the turn indicator.

    :param screen: The surface to be drawn onto.
    :param gameBoard: The game board object including information for each successive turn.
    """

    text = "WHITE" if gameBoard.turn == enums.Turn.WHITE.value else "BLACK"
    blit_source(screen, render_font(art.turnTextFont, text), art.turnBoxPos)
    

def render_pgn(screen: pygame.Surface, gameBoard: board.Board) -> None:
    """ Draws the pgn text box onto the screen within the PGN box.
        When a line has become filled, write below on a new line.
    
    :param screen: The surface to be drawn onto.
    :param gameBoard: The game board object including information for each successive turn.
    """
    draw_rect(screen, art.pgnBoxPos, art.pgnBoxSize, data.COLOUR_BONE_RED, 5)
    blit_source(screen, render_font(art.pgnHeaderFont, "PGN:"), art.pgnHeaderPos)

    words = gameBoard.pgn.split(' ')
    tempX, tempY = art.pgnTextPos

    # For each word in the PGN, blit it to the right if room, otherwise on a new line.
    for word in words:
        renderedWord = render_font(art.pgnTextFont, word + ' ')

        if renderedWord.get_width() + tempX > (art.pgnBoxPos[0] + art.pgnBoxSize[0] - (art.pgnTextPos[0] - art.pgnBoxPos[0])):
            tempY += renderedWord.get_height()
            tempX = art.pgnTextPos[0]

        screen.blit(renderedWord, (tempX, tempY))
        tempX += renderedWord.get_width()


def draw_prom_piece(screen: pygame.surface, makeMove: move.Move) -> None:
    """ Draw the promotion menu onto the board when a pawn advances to the 8th (or 1st) rank.
        Blits the respective images for each piece, drawn on the promotion square.

    :param screen: The surface area to draw onto.
    :param makeMove: The move object containing information for a given turn.
    """
    draw_rect(screen, art.promPos, art.promSize, data.COLOUR_RED)
    
    # imageIndices = data.whitePromotionIndices if makeMove.prom == 1 else data.blackPromotionIndices
    imgIndices = data.whitePromPieces if makeMove.prom == 1 else data.blackPromPieces
    for index, value in enumerate(imgIndices):
        # blit_source(screen, art.scaledImgs[str(value)], (art.promPos[0], art.promPos[1] + art.fromTileSize[1] * index))
        blit_source(screen, art.scaledImgs[str(value.value)], (art.promPos[0], art.promPos[1] + art.fromTileSize[1] * index))
    

def blit_source(screen: pygame.Surface, source: pygame.Surface, pos: Tuple[int, int]) -> None:
    """ Generic render function to blit artifacts onto the screen.

    :param screen: The surface area to draw onto.
    :param source: The source surface to draw onto the screen. Mostly images.
    :param pos: The coordinates to render the image.
    """
    screen.blit(source, pos)


def draw_rect(screen: pygame.Surface, pos: Tuple[int, int], size: Tuple[int, int],
               colour: Tuple[int, int, int] = data.COLOUR_BLACK, width: int = 0) -> None:
    """ Generic draw function to draw rects onto the screen.

    :param screen: The surface area to draw onto.
    :param pos: The coordiantes to draw the rectangle.
    :param size: The size of the rectangle to draw.
    :param colour: The colour to make the rectangle.
    """
    pygame.draw.rect(screen, colour, pygame.Rect(pos, size), width = width)


def render_font(font: pygame.font.Font, text: str, colour: Tuple[int, int, int] = data.COLOUR_BLACK,
                 antialias: bool = False) -> pygame.Surface:
    """ Generic render function to blit fonts onto the screen.

    :param font: The font object to render.
    :param text: The string literal to be displayed.
    :param colour: The colour of the text.
    :param antialias: Boolean to smooth text edges or not.

    :returns: A surface of the rendered font.
    """
    return font.render(text, antialias, colour)


def main():
    # Initialize pygame
    screen, clock, settingsScreen = pygame_setup()

    # Initalize gameBoard object.
    gameBoard = board.Board()

    # Initalize the move object.
    makeMove = move.Move()

    # Load in chess piece images.
    artifacts.import_img()

    # Load in all of the sounds.
    artifacts.import_sound()

    # Initalize all of the artifacts values.
    artifacts.calculate_resize(*enums.Resolution.RES_1920_1080.value, gameBoard)

    running = True
    while running:
        for event in pygame.event.get():
            # If the window has been closed by user, or program force closed from console.
            if event.type == pygame.QUIT:
                running = False

            # If the escape key is pressed, toggle the settings menu.
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                menu.toggle_settings_page()

            # If there is registered mouse input, and it's a left-click.
            if data.left_click(event):

                # Get the current mouse mousePos.
                mousePos = pygame.mouse.get_pos()

                # If on the main page.
                if not menu.Menu.settingsPage:

                    # If clicking the board.
                    if artifacts.is_clicked("board", mousePos):

                        # If promotion menu
                        if makeMove.prom:
                            promPiece = artifacts.is_clicked_prom(art.promPos, mousePos, makeMove.prom)

                            # If a promotion piece was actually selected.
                            if promPiece:
                                makeMove.handle_prom(gameBoard, promPiece)    

                        # If previous piece already selected, process the move.
                        elif 21 <= makeMove.from120 <= 98:
                            makeMove.process_move(mousePos, gameBoard)
                            
                        # Previous piece not seleted, set it.
                        else:
                            makeMove.set_from_index_120(mousePos, gameBoard)

                    # If undo button clicked, undo move and play undo sound.
                    elif artifacts.is_clicked("undo", mousePos):
                        makeMove.undo_move(gameBoard)
                        menu.play_sound('undoMove')

                    # If mute button clicked, toggle mute.
                    elif artifacts.is_clicked("mute", mousePos):
                        menu.toggle_mute()

                    # If hamburger menu selected, toggle settings vs main screen.
                    elif artifacts.is_clicked("hamburger", mousePos):
                        menu.toggle_settings_page()

                    # If showAttacks selected, toggle it.
                    elif artifacts.is_clicked("showAttacks", mousePos):
                        menu.toggle_show_attacks()
                        
                # If on the settings page.
                else:
                    # Hamburger menu selected, toggle home/settings page.
                    if artifacts.is_clicked("hamburger", mousePos):
                        menu.toggle_settings_page()

                    # Fullscreen selected, toggle it.
                    elif artifacts.is_clicked("fs", mousePos, index = 1):
                        menu.toggle_fullscreen()

                    # 1280x720 res seleted, set it.
                    elif artifacts.is_clicked("res", mousePos, index = enums.ResolutionIndex.IND_1280_720.value):
                        menu.set_res(enums.ResolutionIndex.IND_1280_720.value)

                    # 1920x1080 res selected, set it.
                    elif artifacts.is_clicked("res", mousePos, index = enums.ResolutionIndex.IND_1920_1080.value):
                        menu.set_res(enums.ResolutionIndex.IND_1920_1080.value)

                    # 2560x1440 res selected, set it.
                    elif artifacts.is_clicked("res", mousePos, index = enums.ResolutionIndex.IND_2560_1440.value):
                        menu.set_res(enums.ResolutionIndex.IND_2560_1440.value)

                    # 3840x2160 res selected, set it.
                    elif artifacts.is_clicked("res", mousePos, index = enums.ResolutionIndex.IND_3840_2160.value):
                        menu.set_res(enums.ResolutionIndex.IND_3840_2160.value)

                    # Save button selected, update screen size values.
                    elif artifacts.is_clicked("save", mousePos):
                        displayFlags = pygame.FULLSCREEN if menu.Menu.fullscreen else pygame.RESIZABLE

                        screen = settingsScreen = pygame.display.set_mode(menu.Menu.res, flags = displayFlags, display = 0)
                        artifacts.calculate_resize(screen.get_width(), screen.get_height(), gameBoard)

            # If window resized, recompute artifacts.
            elif event.type == VIDEORESIZE:
                artifacts.calculate_resize(screen.get_width(), screen.get_height(), gameBoard)

            # Draw the current game state.
            draw_game_state(screen, gameBoard, makeMove, settingsScreen)

        # Update game clock.
        clock.tick(menu.Menu.fpsLimit)

        # Updates everything on the display surface to the screen.
        pygame.display.flip()

if __name__ == '__main__':
    main()