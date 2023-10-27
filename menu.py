""" File containing all GUI related settings for the application.

:author: Ben Hickman
:date: 2023/10/26
:version: v1.0.0
"""
from artifacts import Artifacts as art
import enums

class Menu():
    """ A static class containing information related to the settings of the game.
        Audio, resolution, and fps limit reside here.
    """
    mute = False #Mute bool
    fullscreen = False #Fullscreen bool
    settingsPage = False #bool to show settings page
    res = enums.Resolution.RES_1920_1080.value
    resIndex = -1
    fpsLimit = 144


def toggle_mute() -> None:
    """ Setter to mute/unmute.
    """
    Menu.mute = not Menu.mute


def toggle_fullscreen() -> None:
    """ Setter to fullscreen/unfullscreen.
    """
    Menu.fullscreen = not Menu.fullscreen


def toggle_settings_page() -> None:
    """ Setter to switch to settings menu or main screen.
    """
    Menu.settingsPage = not Menu.settingsPage


def set_res(index) -> None:
    """ Setter to select a resolution for the application.
        Selected from settings page.

    :param index: The value associated to a resolution. 
    """
    match index:
        case enums.ResolutionIndex.IND_1280_720.value:
            Menu.res = enums.Resolution.RES_1280_720.value

        case enums.ResolutionIndex.IND_1920_1080.value:
            Menu.res = enums.Resolution.RES_1920_1080.value

        case enums.ResolutionIndex.IND_2560_1440.value:
            Menu.res = enums.Resolution.RES_2560_1440.value

        case enums.ResolutionIndex.IND_3840_2160.value:
            Menu.res = enums.Resolution.RES_3840_2160.value

    Menu.resIndex = index


def play_sound(soundName: str) -> None:
    """ Plays an mp3 file mapped to soundName.

    :param soundName: The sound map key.
    :raises KeyError: If the sound file is not present in /sounds.
    """
    if not Menu.mute:
        try:
            art.sounds[soundName].play()
        except KeyError:
            print("No sound corresponding to `", soundName, "` exists")