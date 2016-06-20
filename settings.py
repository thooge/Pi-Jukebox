"""

================================================
**settings.py**: Contains project wide variables
================================================

"""
__author__ = 'Mark Zwart'

import os
import sys
import pygame
from pygame.locals import *
import time
from config_file import config_file
from gui_themes import Theme

VERSION = (1, 1, 0)

# TODO move this to configuration file
DEBUG = False # In production set to false

# Default gui dimensions
# WIP

#BORDER_NAV = 5

FONT_SIZE = 14
TITLE_HEIGHT = 20
SPACE = 2

ICO_WIDTH= 48
ICO_HEIGHT= 32

SWITCH_WIDTH = 48
SWITCH_HEIGHT = 32

LIST_WIDTH = 52
LIST_INDICATOR_WIDTH = 3

# Support for international keyboard layouts
# Possible values: en, de
KEYBOARD_LAYOUT = config_file.setting_get('Global', 'keyboard')

KEY_SPACE = 0
KEY_WIDTH_STD = 32
KEY_HEIGHT = 32
if KEYBOARD_LAYOUT == 'de':
    KEY_LTR_WIDTH_STD = 29
else:
    KEY_LTR_WIDTH_STD = 32

#: The display dimensions, change this if you have a bigger touch screen.
#: adafruit 2.8" -> 320x200
#: adafruit 3.5" -> 480x320
#: raspberry 7" -> 800x480
DISPLAY = config_file.setting_get('Hardware', 'display')
if DISPLAY == 'adafruit2.8':
    DISPLAY_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 320, 240
elif DISPLAY == 'adafruit3.5':
    DISPLAY_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 480, 320
elif DISPLAY == 'raspberry7':
    DISPLAY_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480
else:
    DISPLAY_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 320, 240

#: Switches between development/debugging on your desktop/laptop versus running on your Raspberry Pi
RUN_ON_RASPBERRY_PI = os.uname()[4][:3] == 'arm'

# Setting up touch screen, set if statement to true on Raspberry Pi
if RUN_ON_RASPBERRY_PI:
    os.environ['SDL_FBDEV'] = '/dev/fb1'
    if DISPLAY == 'raspberry7':
        os.environ['SDL_MOUSEDEV'] = '/dev/input/mouse1'
        os.environ['SDL_MOUSEDRV'] = 'FT5406'
    else:
        os.environ['SDL_MOUSEDEV'] = '/dev/input/touchscreen'
        os.environ['SDL_MOUSEDRV'] = 'TSLIB'

# Display settings
pygame.init() 	# Pygame initialization

PYGAME_EVENT_DELAY = 25


if RUN_ON_RASPBERRY_PI:  # If started on Raspberry Pi
    display_flags = FULLSCREEN | DOUBLEBUF | ANYFORMAT  # Turn on video acceleration
    #: Points to the display.
    SCREEN = pygame.display.set_mode(DISPLAY_SIZE, display_flags)
    pygame.mouse.set_visible(False)                                 # Hide mouse cursor
else:
    SCREEN = pygame.display.set_mode(DISPLAY_SIZE)

#: The directory where resources like button icons or font files are stored.
RESOURCES = os.path.dirname(__file__) + '/resources/'

THEMEBASE = config_file.setting_get('Global', 'theme')
THEME = RESOURCES + 'themes/' + THEMEBASE + '/'
theme = Theme(THEME)


#: Standard font type
FONT = pygame.font.Font(RESOURCES + 'DroidSans.ttf', FONT_SIZE)


""" Mouse related variables """
GESTURE_MOVE_MIN = 50  # Minimum movement in pixels to call it a move
GESTURE_CLICK_MAX = 15  # Maximum movement in pixels to call it a click
GESTURE_PRESS_MIN = 500  # Minimum time to call a click a long press
# Gesture enumeration
GESTURE_NONE = -1
GESTURE_CLICK = 0
GESTURE_SWIPE_LEFT = 1
GESTURE_SWIPE_RIGHT = 2
GESTURE_SWIPE_UP = 3
GESTURE_SWIPE_DOWN = 4
GESTURE_LONG_PRESS = 5
GESTURE_DRAG_VERTICAL = 6
GESTURE_DRAG_HORIZONTAL = 7

""" Used icons """
# Switch icons
ICO_SWITCH_ON = THEME + 'switch_on_48x32.png'
ICO_SWITCH_OFF = THEME + 'switch_off_48x32.png'
ICO_MODAL_CANCEL = THEME + 'back_22x18.png'

# General icons
ICO_PLAYER_FILE = THEME + 'playing_file_48x32.png'
ICO_PLAYER_FILE_ACTIVE = THEME + 'playing_file_active_48x32.png'
ICO_PLAYER_RADIO = THEME + 'playing_radio_48x32.png'
ICO_PLAYER_RADIO_ACTIVE = THEME + 'playing_radio_active_48x32.png'
ICO_PLAYLIST = THEME + 'playlist_48x32.png'
ICO_PLAYLIST_ACTIVE = THEME + 'playlist_active_48x32.png'
ICO_LIBRARY = THEME + 'library_48x32.png'
ICO_LIBRARY_ACTIVE = THEME + 'library_active_48x32.png'
ICO_DIRECTORY = THEME + 'directory_48x32.png'
ICO_DIRECTORY_ACTIVE = THEME + 'directory_active_48x32.png'
ICO_RADIO = THEME + 'radio_48x32.png'
ICO_RADIO_ACTIVE = THEME + 'radio_active_48x32.png'
ICO_SETTINGS = THEME + 'settings_48x32.png'
ICO_SETTINGS_ACTIVE = THEME + 'settings_active_48x32.png'
ICO_BACK = THEME + 'back_48x32.png'

# Player icons
ICO_PLAY = THEME + 'play_48x32.png'
ICO_PAUSE = THEME + 'pause_48x32.png'
ICO_STOP = THEME + 'stop_48x32.png'
ICO_NEXT = THEME + 'next_48x32.png'
ICO_PREVIOUS = THEME + 'prev_48x32.png'
ICO_VOLUME = THEME + 'vol_48x32.png'

# Volume icons
ICO_VOLUME_UP = THEME + 'vol_up_48x32.png'
ICO_VOLUME_DOWN = THEME + 'vol_down_48x32.png'
ICO_VOLUME_MUTE = THEME + 'vol_mute_48x32.png'
ICO_VOLUME_MUTE_ACTIVE = THEME + 'vol_mute_active_48x32.png'

# Library icons
ICO_SEARCH = THEME + 'search_48x32.png'
ICO_SEARCH_ACTIVE = THEME + 'search_active_48x32.png'
ICO_SEARCH_ARTIST = THEME + 'artists_48x32.png'
ICO_SEARCH_ARTIST_ACTIVE = THEME + 'artists_active_48x32.png'
ICO_SEARCH_ALBUM = THEME + 'albums_48x32.png'
ICO_SEARCH_ALBUM_ACTIVE = THEME + 'albums_active_48x32.png'
ICO_SEARCH_SONG = THEME + 'songs_48x32.png'
ICO_SEARCH_SONG_ACTIVE = THEME + 'songs_active_48x32.png'
ICO_PLAYLISTS = THEME + 'playlists_48x32.png'
ICO_PLAYLISTS_ACTIVE = THEME + 'playlists_active_48x32.png'

# Directory icons
ICO_FOLDER_ROOT = THEME + 'folder_root_48x32.png'
ICO_FOLDER_UP = THEME + 'folder_up_48x32.png'

# Standard info icons
ICO_INFO = THEME + 'icon_info.png'
ICO_WARNING = THEME + 'icon_warning.png'
ICO_ERROR = THEME + 'icon_error.png'
ICO_QUESTION = THEME + 'icon_warning.png'

# Radio icons
ICO_STATION_ADD = THEME + 'station_add_48x32.png'
COVER_ART_RADIO = THEME + 'radio_cover_art.png'

# Special keyboard icons
ICO_SHIFT = THEME + 'shift_48x32.png'
ICO_BACKSPACE = THEME + 'backspace_48x32.png'
ICO_ENTER = THEME + 'enter_48x32.png'
ICO_LETTERS = THEME + 'letters_48x32.png'
ICO_SYMBOLS = THEME + 'symbols_48x32.png'
