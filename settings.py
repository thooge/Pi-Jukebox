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

#: The directory where resources like button icons or font files are stored.
RESOURCES = os.path.dirname(__file__) + '/resources/'

THEMEBASE = config_file.setting_get('Global', 'theme')
THEME = RESOURCES + 'themes/' + THEMEBASE + '/'
theme = Theme(THEME)


# Default gui dimensions
# WIP

#BORDER_NAV = 5

FONT_SIZE = theme.font_size
TITLE_HEIGHT = theme.title_height
SPACE = 2

ICO_WIDTH = theme.icon_width
ICO_HEIGHT = theme.icon_height

SWITCH_WIDTH = theme.switch_width
SWITCH_HEIGHT = theme.switch_height

LIST_WIDTH = theme.list_width
LIST_INDICATOR_WIDTH = theme.list_indicator_width

# Support for international keyboard layouts
# Possible values: en, de
KEYBOARD_LAYOUT = config_file.setting_get('Global', 'keyboard')

KEY_SPACE = 0
KEY_WIDTH_STD = theme.key_width
KEY_HEIGHT = theme.key_height
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
RUN_ON_RASPBERRY_PI = (os.name != 'nt' and os.uname()[4][:3] == 'arm')

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

