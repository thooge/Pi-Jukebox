"""
=======================================================
**pij_screen_navigation.py**: Main navigation elements
=======================================================
"""

from gui_widgets import *

__author__ = 'Mark Zwart'

class ScreenNavigation(WidgetContainer):
    
    def __init__(self, tag_name, screen_rect, button_active):
        WidgetContainer.__init__(self, tag_name, screen_rect,
            0, 0, ICO_WIDTH + 5, SCREEN_HEIGHT)
        self.__button_active = button_active
        self.__radio_mode = False
        button_offset = theme.icon_height + theme.icon_offset_y
        button_top = 5
        buttons = (
            ('btn_player',  theme.icon.player_file_active),
            ('btn_playlist', theme.icon.playlist),
            ('btn_library', theme.icon.library),
            ('btn_directory', theme.icon.directory),
            ('btn_radio', theme.icon.radio),
            ('btn_settings', theme.icon.settings) 
        )
        for button in buttons:
            self.add_component(ButtonIcon(button[0], self.screen, button[1], 3, button_top))
            button_top += button_offset
        self.button_active_set(button_active)

    def on_click(self, x, y):
        tag_name = super(ScreenNavigation, self).on_click(x, y)
        return tag_name

    def radio_mode_set(self, radio_mode_bool):
        self.__radio_mode = radio_mode_bool
        if radio_mode_bool:
            if self.__button_active == 'btn_player':
                self.components['btn_player'].icon_file_set(theme.icon.player_radio_active)
            else:
                self.components['btn_player'].icon_file_set(theme.icon.player_radio)
        else:
            if self.__button_active == 'btn_player':
                self.components['btn_player'].icon_file_set(theme.icon.player_file_active)
            else:
                self.components['btn_player'].icon_file_set(theme.icon.player_file)
        self.draw()

    def button_active_set(self, button_active):
        self.__button_active = button_active
        if self.__radio_mode:
            self.components['btn_player'].icon_file_set(theme.icon.padio)
        else:
            self.components['btn_player'].icon_file_set(theme.icon.player_file)
        self.components['btn_playlist'].icon_file_set(theme.icon.playlist)
        self.components['btn_library'].icon_file_set(theme.icon.library)
        self.components['btn_directory'].icon_file_set(theme.icon.directory)
        self.components['btn_radio'].icon_file_set(theme.icon.radio)

        if button_active == 'btn_player':
            if self.__radio_mode:
                self.components['btn_player'].icon_file_set(theme.icon.player_radio_active)
            else:
                self.components['btn_player'].icon_file_set(theme.icon.player_file_active)
        elif button_active == 'btn_playlist':
            self.components['btn_playlist'].icon_file_set(theme.icon.playlist_active)
        elif button_active == 'btn_library':
            self.components['btn_library'].icon_file_set(theme.icon.library_active)
        elif button_active == 'btn_directory':
            self.components['btn_directory'].icon_file_set(theme.icon.directory_active)
        elif button_active == 'btn_radio':
            self.components['btn_radio'].icon_file_set(theme.icon.radio_active)

        self.draw()
