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
        def __init__(self, themedir):

            # Main menu
            self.player_file = themedir + '/playing_file.png'
            self.player_file_active = themedir + '/playing_file_active.png'
            self.player_radio = themedir + '/playing_radio.png'
            self.player_radio_active = themedir + '/playing_radio_active.png'
            self.playlist = themedir + '/playlist.png'
            self.playlist_active = themedir + '/playlist_active.png'
            self.library = themedir + '/library.png'
            self.library_active = themedir + '/library_active.png'
            self.directory = themedir + '/directory.png'
            self.directory_active = themedir + '/directory_active.png'
            self.radio = themedir + '/radio.png'
            self.radio_active = themedir + '/radio_active.png'
            self.settings = themedir + '/settings.png'
            self.settings_active = themedir + '/settings_active.png'

            # Player icons
            self.play = themedir + '/play.png'
            self.pause = themedir + '/pause.png'
            self.stop = themedir + '/stop.png'
            self.next = themedir + '/next.png'
            self.previous = themedir + '/previous.png'
            self.vol = themedir + '/vol.png'

            # Volume icons
            self.vol_down = themedir + '/vol_down.png'
            self.vol_mute = themedir + '/vol_mute.png'
            self.vol_mute_active = themedir + '/vol_mute_active.png'
            self.vol_up = themedir + '/vol_up.png'

            # Library icons
            self.albums = themedir + '/albums.png'
            self.albums_active = themedir + '/albums_active.png'
            self.artists = themedir + '/artists.png'
            self.artists_active = themedir + '/artists_active.png'
            self.songs = themedir + '/songs.png'
            self.songs_active = themedir + '/songs_active.png'
            self.playlists = themedir + '/playlists.png'
            self.playlists_active = themedir + '/playlists_active.png'
            self.search = themedir + '/search.png'

            # Directory icons
            self.folder_root = themedir + '/folder_root.png'
            self.folder_up = themedir + '/folder_up.png'

            # Radio icons
            self.station_add = themedir + '/station_add.png'


            # Keyboard icons
            self.key_backspace = themedir + '/backspace.png'
            self.key_clear = themedir + '/clear.png'
            self.key_enter = themedir + '/enter.png'
            self.key_symbols = themedir + '/symbols.png'
            self.key_letters = themedir + '/letters.png'
            self.key_shift = themedir + '/shift.png'

            self.cover_music = themedir + '/default_cover_art.png'
            self.cover_radio = themedir + '/radio_cover_art.png'

            # Additional 
            self.error = themedir + '/icon_error.png'
            self.info = themedir + '/icon_info.png'
            self.warning = themedir + '/icon_warning.png'
            self.question = themedir + '/icon_warning.png'

            self.switch_off = themedir + '/switch_off.png'
            self.switch_on = themedir + '/switch_on.png'

            self.back = themedir + '/back.png'
            self.exit = themedir + '/exit.png'


    class Font(object):
        def __init__(self):
            self.default = ''

    def __init__(self, themedir = None):
        self.font_size = 14
        self.line_spacing = 2
        self.icon_width = 48
        self.icon_height = 32
        self.icon_offset_x = 8
        self.icon_offset_y = 8
        self.switch_width = 48
        self.switch_height = 32
        self.border_top = 5
        self.border_bottom = 5
        self.border_left = 5
        self.border_right = 5
        self.title_height = 20
        self.list_width = 52
        self.list_indicator_width = 3
        self.key_width = 32
        self.key_height = 32
        self.color = self.Color()
        self.icon = self.Icon(themedir)
        self.font = self.Font()
        if themedir:
            self.load(themedir)

    def load(self, themedir):
        parser = ConfigParser()
        themefile = os.path.join(themedir, 'theme.ini')
        parser.read(themefile)
        for globvar in parser.items('Global'):
            if hasattr(self, globvar[0]):
                setattr(self, globvar[0], int(globvar[1]))
        for color in parser.items('Colors'):
            if hasattr(self.color, color[0]):
                col = tuple(int(e.strip()) for e in color[1].split(','))
                setattr(self.color, color[0], col)
        for icon in parser.items('Icons'):
            if hasattr(self.icon, icon[0]):
                setattr(self.icon, icon[0], themedir + icon[1])
        # parser. Fonts fontname
