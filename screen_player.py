"""
=======================================================
**screen_player.py**: Playback screen.
=======================================================
"""

from gui_screens import *
from pij_screen_navigation import *
from screen_settings import ScreenSettings
from mpd_client import mpd

class Playlist(ItemList):
    """ Displays playlist information.

        :param screen_rect: The display's rect where the library browser is drawn on.
    """
    def __init__(self, screen_rect):
        ItemList.__init__(self, 'list_playing', screen_rect,
            ICO_WIDTH + 4, 
            46,
            SCREEN_WIDTH - (ICO_WIDTH + 4) - LIST_WIDTH,
            SCREEN_HEIGHT - TITLE_HEIGHT - 3)
        self.item_height = 27
        self.item_active_color = theme.color.item_active
        self.outline_color = theme.color.item_outline
        self.font_color = theme.color.item_font
        self.outline_visible = False

    def show_playlist(self):
        """ Display the playlist. """
        updated = False
        playing_nr = mpd.playlist_current_playing_index_get()
        if self.list != mpd.playlist_current_get():
            self.list = mpd.playlist_current_get()
            updated = True
        if self.active_item_index != mpd.playlist_current_playing_index_get():
            self.active_item_index = mpd.playlist_current_playing_index_get()
            updated = True
        if updated:
            self.draw()


class ScreenPlaylist(Screen):
    """ The screen containing everything to control playback.
    """
    def __init__(self, screen_rect):
        Screen.__init__(self, screen_rect)

        # Screen navigation buttons
        self.add_component(ScreenNavigation('screen_nav', self.screen, 'btn_playlist'))

        # Playlist specific buttons
        button_x = SCREEN_WIDTH - theme.border_right - theme.icon_width
        button_y = theme.border_top + theme.icon_height + theme.icon_offset_y
        button_offset = theme.icon_height + theme.icon_offset_y
        buttons = (
                ('btn_play', theme.icon.play),
                ('btn_stop', theme.icon.stop),
                ('btn_prev', theme.icon.previous),
                ('btn_next', theme.icon.next),
                ('btn_volume', theme.icon.vol)
            )
        for button in buttons:
            self.add_component(ButtonIcon(button[0], self.screen, button[1], button_x, button_y))
            button_y += button_offset

        # Playlist specific labels
        LBL_H = FONT.get_height()
        WIDTH_A = (SCREEN_WIDTH - 2 * (theme.icon_width + theme.icon_offset_x) 
                   - theme.border_left - theme.border_right)
        labels = (
            ('lbl_track_title', 
                theme.border_left + theme.icon_width + theme.icon_offset_x,
                theme.border_top, WIDTH_A, LBL_H),
            ('lbl_track_artist', 
                theme.border_left + theme.icon_width + theme.icon_offset_x,
                theme.border_top + LBL_H + theme.line_spacing,
                WIDTH_A, LBL_H),
            ('lbl_time', SCREEN_WIDTH - 67, 5, 67, LBL_H),
            ('lbl_volume', SCREEN_WIDTH - 70, 23, 70, LBL_H)
        )
        for label in labels:
            self.add_component(LabelText(label[0], self.screen, label[1], label[2], label[3], label[4]))

        # Splits labels from playlist
        separator = Rectangle('rct_split', self.screen, 55, 43, SCREEN_WIDTH - 2 * (ICO_WIDTH + 8), 1)
        self.add_component(separator)

        # Playlist
        self.add_component(Playlist(self.screen))
        self.components['list_playing'].active_item_index = mpd.playlist_current_playing_index_get()

    def show(self):
        """ Displays the screen. """
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
        now_playing = mpd.now_playing
        self.components['lbl_time'].text_set(now_playing.time_current + '/' + now_playing.time_total)
        self.components['lbl_volume'].text_set(_('Vol: {0}%').format(mpd.volume))
        if mpd.player_control_get() == 'play':
            self.components['btn_play'].set_image_file(theme.icon.pause)
        else:
            self.components['btn_play'].set_image_file(theme.icon.play)
        self.components['btn_play'].draw()
        self.components['lbl_track_title'].text_set(now_playing.title)
        self.components['lbl_track_artist'].text_set(now_playing.artist)
        super(ScreenPlaylist, self).show()  # Draw screen
        self.components['list_playing'].show_playlist()
        self.components['list_playing'].show_item_active()  # Makes sure currently playing playlist item is on screen

    def update(self):
        now_playing = mpd.now_playing
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
        while True:
            try:
                event = mpd.events.popleft()
                if event == 'volume':
                    self.components['lbl_volume'].text_set(_('Vol: {0}%').format(mpd.volume))
                elif event == 'playing_index':
                    self.components['list_playing'].show_playlist()
                elif event == 'time_elapsed' or event == 'playing_time_total':
                    self.components['lbl_time'].text_set('{0}/{1}'.format(now_playing.time_current, now_playing.time_total))
                elif event == 'playing_file':
                    self.components['lbl_track_title'].text_set(now_playing.title)
                    self.components['lbl_track_artist'].text_set(now_playing.artist)
                elif event == 'state':
                    state = mpd.player_control_get()
                    if self.components['btn_play'].image_file != theme.icon.pause and state == 'play':
                        self.components['btn_play'].draw(theme.icon_pause)
                    elif self.components['btn_play'].image_file == theme.icon.pause and state != 'play':
                        self.components['btn_play'].draw(theme.icon.play)
            except IndexError:
                break

    def on_click(self, x, y):
        """
        :param x: The horizontal click position.
        :param y: The vertical click position.

        :return: Possibly returns a screen index number to switch to.
        """
        tag_name = super(ScreenPlaylist, self).on_click(x, y)
        if tag_name == 'btn_player':
            return 0
        elif tag_name == 'btn_playlist':
            return 1
        elif tag_name == 'btn_library':
            return 2
        elif tag_name == 'btn_directory':
            return 3
        elif tag_name == 'btn_radio':
            return 4
        elif tag_name == 'btn_settings':
            setting_screen = ScreenSettings(self.screen)
            setting_screen.show()
            self.show()
        elif tag_name == 'btn_play':
            if mpd.player_control_get() == 'play':
                mpd.player_control_set('pause')
                self.components['btn_play'].set_image_file(theme.icon.play)
            else:
                mpd.player_control_set('play')
                self.components['btn_play'].set_image_file(theme.icon.pause)
            self.components['btn_play'].draw()
        elif tag_name == 'btn_stop':
            self.components['btn_play'].set_image_file(theme.icon.play)
            mpd.player_control_set('stop')
        elif tag_name == 'btn_prev':
            mpd.player_control_set('previous')
        elif tag_name == 'btn_next':
            mpd.player_control_set('next')
        elif tag_name == 'btn_volume':
            screen_volume = ScreenVolume(self.screen)
            screen_volume.show()
            self.show()
        elif tag_name == 'list_playing':
            selected_index = self.components['list_playing'].item_selected_index
            if selected_index >= 0:
                mpd.play_playlist_item(selected_index + 1)
                self.components['list_playing'].active_item_index = selected_index
                self.components['list_playing'].draw()


class ScreenPlaying(Screen):
    """ Screen cover art

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """
    def __init__(self, screen_rect):
        Screen.__init__(self, screen_rect)

        # Screen navigation buttons
        self.add_component(ScreenNavigation('screen_nav', self.screen, 'btn_player'))

        # Player specific buttons
        button_x = SCREEN_WIDTH - ICO_WIDTH - 3
        button_y = 5
        button_offset = theme.icon_height + theme.icon_offset_y
        buttons = (
                 ('btn_play', theme.icon.play),
                 ('btn_stop', theme.icon.stop),
                 ('btn_prev', theme.icon.previous),
                 ('btn_next', theme.icon.next),
                 ('btn_volume', theme.icon.vol)
            )
        for button in buttons:
            self.add_component(ButtonIcon(button[0], self.screen, button[1], button_x, button_y))
            button_y += button_offset

        # Player specific labels
        LBL_H = FONT.get_height() + theme.line_spacing
        POS_A = theme.border_left + theme.icon_width + theme.icon_offset_x
        WIDTH_A = (SCREEN_WIDTH - 2 * (theme.icon_width + theme.icon_offset_x) 
                   - theme.border_left - theme.border_right)
        labels = (
				('lbl_track_artist', HOR_MID, VERT_MID, 
                    POS_A, 
                    theme.border_top,
                    WIDTH_A,
                    LBL_H),
				('lbl_track_album', HOR_MID, VERT_MID,
                    POS_A,
                    theme.border_top + 60,
                    WIDTH_A,
                    40),
				('lbl_track_title', HOR_MID, VERT_MID,
                    POS_A,
                    SCREEN_HEIGHT - theme.border_bottom - theme.font_size - theme.line_spacing,
                    WIDTH_A,
                    LBL_H),
				('lbl_time_current', HOR_MID, VERT_MID,
                    SCREEN_WIDTH - 51,
                    SCREEN_HEIGHT - theme.icon_height - 3,
                    theme.icon_width,
                    LBL_H),
				('lbl_time_total', HOR_MID, VERT_MID,
                    SCREEN_WIDTH - 51,
                    SCREEN_HEIGHT - theme.icon_height - 3 + theme.font_size,
                    theme.icon_width,
                    LBL_H),
			)
        for label in labels:
            lbl = LabelText(label[0], self.screen,
                            label[3], label[4], label[5], label[6])
            lbl.set_alignment(label[1], label[2])
            self.add_component(lbl)

        # TODO Document function of this object
        self.add_component(Slider2('slide_time', self.screen,
                                   theme.icon_width + theme.icon_offset_x,
                                   SCREEN_HEIGHT - 35,
                                   SCREEN_WIDTH - 2 * (theme.icon_width + theme.icon_offset_x), 
                                   3))

        # Cover art
        if mpd.radio_mode_get():
            cover_file = theme.icon.cover_radio
        else:
            cover_file = mpd.get_cover_art()
        # Original: 79, 40, 162, 162,
        cover_top = theme.border_top + theme.icon_height + theme.icon_offset_y
        cover_left = theme.border_left + theme.icon_width + theme.icon_offset_x
        pic = Picture('pic_cover_art', self.screen,
                      cover_left,
                      cover_top,
                      SCREEN_WIDTH - cover_left - theme.icon_width - theme.icon_offset_x - theme.border_right,
                      SCREEN_HEIGHT - cover_top - theme.icon_height - theme.border_bottom,
                      cover_file, True)
        pic.outline_visible = False
        self.add_component(pic)


    def show(self):
        """ Displays the screen. """
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
        self.components['lbl_time_current'].text_set(mpd.now_playing.time_current)
        self.components['lbl_time_total'].text_set(mpd.now_playing.time_total)
        if mpd.player_control_get() == 'play':
            self.components['btn_play'].set_image_file(theme.icon.pause)
        else:
            self.components['btn_play'].set_image_file(theme.icon.play)
        self.components['btn_play'].draw()
        self.components['lbl_track_title'].text_set(mpd.now_playing.title)
        self.components['lbl_track_artist'].text_set(mpd.now_playing.artist)
        self.components['lbl_track_album'].text_set(mpd.now_playing.album)
        if mpd.radio_mode_get():
            self.components['lbl_track_artist'].visible = False
            self.components['lbl_track_album'].position_set(ICO_WIDTH + 6, 3, SCREEN_WIDTH - 105, 39)
            self.components['pic_cover_art'].picture_set(theme.icon.cover_radio)
        else:
            self.components['lbl_track_artist'].visible = True
            self.components['lbl_track_artist'].text_set(mpd.now_playing.artist)
            self.components['lbl_track_album'].position_set(ICO_WIDTH + 6, 19, SCREEN_WIDTH - 105, 18)
            self.components['pic_cover_art'].picture_set(mpd.now_playing.cover_art_get())
        super(ScreenPlaying, self).show()  # Draw screen

    def update(self):
        while True:
            try:
                event = mpd.events.popleft()
                self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
                playing = mpd.now_playing
                if event == 'time_elapsed':
                    self.components['lbl_time_current'].text_set(playing.time_current)
                    self.components['slide_time'].draw(playing.time_percentage)
                elif event == 'playing_file':
                    self.components['lbl_track_title'].text_set(playing.title)
                    if mpd.radio_mode_get():
                        self.components['lbl_track_artist'].visible = False
                        self.components['lbl_track_album'].position_set(ICO_WIDTH + 6, 3, SCREEN_WIDTH - 105, 39)
                        self.components['pic_cover_art'].picture_set(theme.icon.cover_radio)
                    else:
                        self.components['lbl_track_artist'].visible = True
                        self.components['lbl_track_artist'].text_set(playing.artist)
                        self.components['lbl_track_album'].position_set(ICO_WIDTH + 6, 19, SCREEN_WIDTH - 105, 18)
                        self.components['pic_cover_art'].picture_set(mpd.now_playing.cover_art_get())
                    self.components['lbl_track_album'].text_set(playing.album)
                    self.components['lbl_time_total'].text_set(playing.time_total)
                elif event == 'state':
                    if self.components['btn_play'].image_file != theme.icon.pause and mpd.player_control_get() == 'play':
                        self.components['btn_play'].draw(theme.icon.pause)
                    elif self.components['btn_play'].image_file == theme.icon.pause and mpd.player_control_get() != 'play':
                        self.components['btn_play'].draw(theme.icon.play)
            except IndexError:
                break

    def on_click(self, x, y):
        tag_name = super(ScreenPlaying, self).on_click(x, y)
        if tag_name == 'btn_player':
            return 0
        elif tag_name == 'btn_playlist':
            return 1
        elif tag_name == 'btn_library':
            return 2
        elif tag_name == 'btn_directory':
            return 3
        elif tag_name == 'btn_radio':
            return 4
        elif tag_name == 'btn_settings':
            setting_screen = ScreenSettings(self.screen)
            setting_screen.show()
            self.show()
        elif tag_name == 'btn_play':
            print "Play pressed"
            if mpd.player_control_get() == 'play':
                mpd.player_control_set('pause')
                self.components['btn_play'].set_image_file(theme.icon.play)
            else:
                mpd.player_control_set('play')
                self.components['btn_play'].set_image_file(theme.icon.pause)
            self.components['btn_play'].draw()
        elif tag_name == 'btn_stop':
            self.components['btn_play'].set_image_file(theme.icon.play)
            mpd.player_control_set('stop')
        elif tag_name == 'btn_prev':
            mpd.player_control_set('previous')
        elif tag_name == 'btn_next':
            mpd.player_control_set('next')
        elif tag_name == 'btn_volume':
            screen_volume = ScreenVolume(self.screen)
            screen_volume.show()
            self.show()


class ScreenVolume(ScreenModal):
    """ Screen setting volume

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """

    def __init__(self, screen_rect):
        ScreenModal.__init__(self, screen_rect, _("Volume"))
        self.window_x = 15
        self.window_y = 52
        self.window_width -= 2 * self.window_x
        self.window_height -= 2 * self.window_y
        self.outline_shown = True
        self.title_color = FIFTIES_GREEN
        self.outline_color = FIFTIES_GREEN

        self.add_component(ButtonIcon('btn_mute', screen_rect, theme.icon.vol_mute,
                                      self.window_x + 5, self.window_y + 25))
        self.components['btn_mute'].x_pos = (self.window_x + self.window_width / 2
                                             - self.components['btn_mute'].width / 2)
        self.add_component(
            ButtonIcon('btn_volume_down', self.screen, theme.icon.vol_down, 
                       self.window_x + 5, self.window_y + 25))
        self.add_component(
            ButtonIcon('btn_volume_up', self.screen, theme.icon.vol_up,
                       self.window_width - 40, self.window_y + 25))
        self.add_component(
            Slider('slide_volume', self.screen,
                   self.window_x + 8, self.window_y + 63, self.window_width - 18, 30))
        self.components['slide_volume'].progress_percentage_set(mpd.volume)
        self.add_component(
            ButtonText('btn_back', self.screen,
                       self.window_x + self.window_width / 2 - 23, self.window_y + 98, 46, 32,
                       _("Back")))
        self.components['btn_back'].button_color = FIFTIES_TEAL

    def on_click(self, x, y):
        tag_name = super(ScreenModal, self).on_click(x, y)
        if tag_name == 'btn_mute':
            mpd.volume_mute_switch()
            self.components['slide_volume'].progress_percentage_set(mpd.volume)
        elif tag_name == 'btn_volume_down':
            mpd.volume_set_relative(-10)
            self.components['slide_volume'].progress_percentage_set(mpd.volume)
        elif tag_name == 'btn_volume_up':
            mpd.volume_set_relative(10)
            self.components['slide_volume'].progress_percentage_set(mpd.volume)
        elif tag_name == 'slide_volume':
            mpd.volume_set(self.components['slide_volume'].progress_percentage)
        elif tag_name == 'btn_back':
            self.close()
        if mpd.volume == 0 or mpd.volume_mute_get():
            self.components['btn_mute'].set_image_file(theme.icon.vol_mute_active)
        else:
            self.components['btn_mute'].set_image_file(theme.icon.vol_mute)
        self.components['btn_mute'].draw()
