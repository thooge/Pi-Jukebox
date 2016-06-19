"""
======================================================================
**gui_themes.py**: Styling for the appliaction
======================================================================
"""

import os
from ConfigParser import ConfigParser

class Theme(object):

#FIFTIES_CHARCOAL = 124, 120, 106
#FIFTIES_TEAL = 141, 205, 193
#FIFTIES_GREEN = 211, 227, 151
#FIFTIES_YELLOW = 255, 245, 195
#FIFTIES_ORANGE = 235, 110, 68


    class Color(object):
        def __init__(self):

            # Main screen
            self.screen_background = (0, 0, 0)
            self.screen_font = (0, 0, 0)
            self.backdrop = (0, 0, 0)

            # Screens
            self.background = (0, 0, 0)
            self.font = (255, 255, 255)
            self.title = (235, 110, 68)
            #self.title_background = (235, 110, 68) # replace with 'title'
            self.title_font = (0, 0, 0)
            self.outline = (235, 110, 68)

            # Modal
            self.modal_background = (0, 0, 0)
            self.modal_title = (235, 110, 68)
            self.modal_title_font = (0, 0, 0)
            self.modal_outline = (235, 110, 68)

            # Message
            self.message_background = (0, 0, 0)
            self.message_title = (141, 205, 193)
            self.message_title_info = (211, 227, 151)
            self.message_title_warn = (255, 245, 195)
            self.message_title_error = (235, 110, 68)
            self.message_title_font = (0, 0, 0)
            self.message_outline = (235, 110, 68)

            # Search
            self.search_title = (255, 245, 195)
            self.search_font = (0, 255, 0)

            # Stations
            self.stations_title = (255, 245, 195)

            # Selected
            self.selected_title = (255, 245, 195)
            self.selected_font = (0, 255, 0)

            # Default widgets
            self.widget_background = (0, 0, 0)
            self.widget_font = (255, 245, 195)
            self.widget_outline = (255, 255, 255)

            # Widgets
            self.button = (255, 245, 195)
            self.button_ok = (255, 245, 195)
            self.button_cancel = (255, 245, 195)
            self.button_outline = (255, 255, 255)
            self.button_font = (0, 0, 0)
            self.button_font_ok = (0, 0, 0)
            self.button_font_cancel = (0, 0, 0)
            self.button_title = (235, 110, 68)  # Button in titlebar
            self.button_title_font = (0, 0, 0)
            self.button_selected = (141, 205, 193)
            self.button_selected_font = (0, 0, 0)

            self.rect = (124, 120, 106)
            self.rect_font = (255, 245, 195)
            self.rect_outline = (255, 255, 255)

            self.slider_bottom = (124, 120, 106)
            self.slider_progress = (211, 227, 151)
            self.slider_progress2 = (235, 110, 68)

            self.label_outline = (124, 120, 106)

            self.item = (0, 0, 0)
            self.item_font = (255, 245, 195)
            self.item_outline = (124, 120, 106)
            self.item_active = (0, 0, 0)
            self.item_active_font = (235, 110, 68)
            self.item_selected = (0, 0, 0)
            self.item_selected_font = (0, 0, 255)

            self.item_letter_font = (211, 227, 151)

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
