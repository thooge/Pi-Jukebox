"""
======================================================================
**gui_themes.py**: Styling for the application
======================================================================
"""

import os
from ConfigParser import ConfigParser

BLUE = 0, 148, 255
CREAM = 206, 206, 206
BLACK = 0, 0, 0
WHITE = 255, 255, 255
YELLOW = 255, 255, 0
RED = 255, 0, 0
GREEN = 0, 255, 0

# Theme fifties (default)
FIFTIES_CHARCOAL = 124, 120, 106
FIFTIES_TEAL = 141, 205, 193
FIFTIES_GREEN = 211, 227, 151
FIFTIES_YELLOW = 255, 245, 195
FIFTIES_ORANGE = 235, 110, 68

# Theme aqua (currently not in use)
# TODO Create theme folder in filesystem
#AQUA_TEAL = 18, 151, 147
#AQUA_CHARCOAL = 80, 80, 80
#AQUA_YELLOW = 255, 245, 195
#AQUA_BLUE = 155, 215, 213
#AQUA_PINK = 255, 114, 96

class Theme(object):

    class Color(object):
        def __init__(self):

            # Main screen
            self.screen_background = BLACK
            self.screen_font = FIFTIES_YELLOW
            self.screen_caption_font = FIFTIES_TEAL
            self.backdrop = BLACK
            self.page_indicator = FIFTIES_ORANGE

            # Screens
            self.background = BLACK
            self.font = WHITE
            self.title = FIFTIES_ORANGE
            self.title_font = BLACK
            self.outline = FIFTIES_ORANGE

            # Modal
            self.modal_background = BLACK
            self.modal_title = FIFTIES_ORANGE
            self.modal_title_font = BLACK
            self.modal_outline = FIFTIES_ORANGE

            # Yes-No
            self.yn_title = FIFTIES_ORANGE
            self.yn_outline = FIFTIES_ORANGE

            # Message
            self.message_background = BLACK
            self.message_title = FIFTIES_TEAL
            self.message_title_info = FIFTIES_GREEN
            self.message_title_warn = FIFTIES_YELLOW
            self.message_title_error = FIFTIES_ORANGE
            self.message_title_question = FIFTIES_ORANGE
            self.message_title_font = BLACK
            self.message_outline = FIFTIES_ORANGE

            # Search
            self.search_title = FIFTIES_YELLOW
            self.search_font = GREEN

            # Stations
            self.stations_title = FIFTIES_YELLOW

            # Selected
            self.selected_title = FIFTIES_YELLOW
            self.selected_font = GREEN

            # Default widgets
            self.widget_background = BLACK
            self.widget_font = FIFTIES_YELLOW
            self.widget_outline = WHITE

            # Buttons
            self.button = FIFTIES_YELLOW
            self.button_ok = FIFTIES_YELLOW
            self.button_cancel = FIFTIES_YELLOW
            self.button_yes = FIFTIES_ORANGE
            self.button_no = FIFTIES_ORANGE
            self.button_outline = WHITE
            self.button_font = BLACK
            self.button_font_ok = BLACK
            self.button_font_cancel = BLACK
            self.button_title = FIFTIES_ORANGE  # Button in titlebar
            self.button_title_font = BLACK
            self.button_selected = FIFTIES_TEAL
            self.button_selected_font = BLACK

            # Memo
            self.memo_outline = FIFTIES_CHARCOAL

            # Rectangles
            self.rect = FIFTIES_CHARCOAL
            self.rect_font = FIFTIES_YELLOW
            self.rect_outline = WHITE

            # Sliders / Progress bars
            self.slider_bottom = FIFTIES_CHARCOAL
            self.slider_progress = FIFTIES_GREEN
            self.slider_progress2 = FIFTIES_ORANGE

            # Labels
            self.label_outline = FIFTIES_CHARCOAL

            # Lists
            self.item = BLACK
            self.item_font = FIFTIES_YELLOW
            self.item_outline = FIFTIES_CHARCOAL
            self.item_active = FIFTIES_ORANGE
            self.item_active_font = FIFTIES_ORANGE
            self.item_selected = BLACK
            self.item_selected_font = BLUE

            # Letter lists
            self.item_letter_font = FIFTIES_GREEN

    class Icon(object):
        def __init__(self):
            self.play = 'play'
            self.stop = 'stop'
            self.next = 'next'
            self.previous = 'previous'

    class Font(object):
        def __init__(self):
            self.default = ''

    def __init__(self, themedir = None):
        self.color = self.Color()
        self.icon = self.Icon()
        self.font = self.Font()
        if themedir:
            self.load(themedir)

    def load(self, themedir):
        parser = ConfigParser()
        themefile = os.path.join(themedir, 'theme.ini')
        parser.read(themefile)
        for color in parser.items('Colors'):
            if hasattr(self.color, color[0]):
                col = tuple(int(e.strip()) for e in color[1].split(','))
                setattr(self.color, color[0], col)
