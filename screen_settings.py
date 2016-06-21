"""
=======================================
**screen_settings.py**: Settings screen
=======================================
"""
__author__ = 'Mark Zwart'

import socket
from config_file import *
from gui_screens import *
from mpd_client import *
from screen_keyboard import Keyboard

class ScreenSettings(ScreenModal):
    """ Screen for settings or quitting/shutting down

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """
    def __init__(self, screen_rect):
        ScreenModal.__init__(self, screen_rect, _("Settings"))
        button_top = 30
        button_left = self.window_x + 10
        button_width = self.window_width - 2 * button_left
        button_height = ICO_HEIGHT
        button_offset = ICO_HEIGHT + 10
        buttons = (
                ('btn_quit', _("Quit Pi-Jukebox")),
                ('btn_playback', _("Playback options")),
                ('btn_mpd', _("MPD related settings")),
                ('btn_system_info', _("System info")),
                ('btn_return', _("Back"))
            )
        for button in buttons:
            btn = ButtonText(button[0], self.screen,
                             button_left, button_top, button_width, button_height,
                             button[1])
            self.add_component(btn)
            button_top += button_offset

    def on_click(self, x, y):
        tag_name = super(ScreenSettings, self).on_click(x, y)
        if tag_name == 'btn_playback':
            screen_playback_options = ScreenSettingsPlayback(self.screen)
            screen_playback_options.show()
            self.show()
        elif tag_name == 'btn_quit':
            screen_quit = ScreenSettingsQuit(self.screen)
            screen_quit.show()
            self.show()
        elif tag_name == 'btn_mpd':
            screen_mpd = ScreenSettingsMPD(self.screen)
            screen_mpd.show()
            self.show()
        elif tag_name == 'btn_system_info':
            screen_system_info = ScreenSystemInfo(self.screen)
            screen_system_info.show()
            self.show()
        elif tag_name == 'btn_return':
            self.close()


class ScreenSettingsQuit(ScreenModal):
    """ Screen for quitting pi-jukebox.

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """
    def __init__(self, screen_rect):
        ScreenModal.__init__(self, screen_rect, _("Quit Pi-Jukebox"))
        if DISPLAY == 'raspberry7':
            self.window_x = 120
        else:
            self.window_x = 70
        self.window_y = TITLE_HEIGHT
        self.window_width -= 2 * self.window_x
        self.window_height -= 2 * self.window_y
        self.outline_shown = True

        button_top = self.window_y + TITLE_HEIGHT + 5
        button_left = self.window_x + 10
        button_width = self.window_width - 2 * 10
        button_height = ICO_HEIGHT
        button_offset = ICO_HEIGHT + 8
        buttons = (
                ('btn_quit', _("Quit")),
                ('btn_shutdown', _("Shutdown Pi")),
                ('btn_reboot', _("Reboot Pi")),
                ('btn_cancel', _("Cancel"))
            )
        for button in buttons:
            btn = ButtonText(button[0], screen_rect,
                            button_left, button_top, button_width, button_height,
                            button[1])
            self.add_component(btn)
            button_top += button_offset

    def on_click(self, x, y):
        tag_name = super(ScreenModal, self).on_click(x, y)
        if tag_name == 'btn_quit':
            mpd.disconnect()
            print(_("Bye!"))
            sys.exit()
        elif tag_name == 'btn_shutdown':
            if RUN_ON_RASPBERRY_PI:
                pygame.display.quit()
                os.system("sudo shutdown -h now")
            else:
                sys.exit()
        elif tag_name == 'btn_reboot':
            if RUN_ON_RASPBERRY_PI:
                pygame.display.quit()
                os.system("sudo shutdown -r now")
            else:
                sys.exit()
        elif tag_name == 'btn_cancel':
            self.close()


class ScreenSettingsPlayback(ScreenModal):
    """ Screen for settings playback options

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """
    def __init__(self, screen_rect):
        ScreenModal.__init__(self, screen_rect, _("Playback settings"))

        self.add_component(LabelText('lbl_shuffle', screen_rect,
                                     10, 30, 40, 20,
                                     _("Shuffle")))
        self.add_component(Switch('switch_shuffle', screen_rect, 60, 23))

        self.add_component(LabelText('lbl_repeat', screen_rect,
                                     120, 30, 40, 20,
                                     _("Repeat")))
        self.add_component(Switch('switch_repeat', screen_rect, 170, 23))

        self.add_component(LabelText('lbl_single', screen_rect,
                                     230, 30, 40, 20,
                                     _("Single")))
        self.add_component(Switch('switch_single', screen_rect, 280, 23))

        self.add_component(LabelText('lbl_consume', screen_rect,
                                     10, 65, 110, 20,
                                     _("Consume playlist")))
        self.add_component(Switch('switch_consume', screen_rect, 125, 58))

        button_top = 108
        button_left = 10
        button_height = ICO_HEIGHT
        button_width = self.window_width - 20
        button_offset = ICO_HEIGHT + 10

        self.add_component(ButtonText('btn_rescan', self.screen, 
                           button_left, button_top, button_width, button_height,
                           _("Re-scan library")))
        button_top += button_offset
        self.add_component(ButtonText('btn_update', self.screen,
                           button_left, button_top, button_width, button_height,
                           _("Update library")))
        button_top += button_offset
        self.add_component(ButtonText('btn_return', screen_rect,
                           button_left, button_top, button_width, button_height,
                           _("Back")))

        self.__initialize()

    def __initialize(self):
        """ Sets the screen controls according to current mpd configuration.
        """
        for key, value in self.components.items():
            if key == 'switch_shuffle':
                value.set_on(mpd.random)
            elif key == 'switch_repeat':
                value.set_on(mpd.repeat)
            elif key == 'switch_single':
                value.set_on(mpd.single)
            elif key == 'switch_consume':
                value.set_on(mpd.consume)

    def on_click(self, x, y):
        tag_name = super(ScreenModal, self).on_click(x, y)
        if tag_name == 'switch_shuffle':
            mpd.random_switch()
        elif tag_name == 'switch_repeat':
            mpd.repeat_switch()
        elif tag_name == 'switch_single':
            mpd.single_switch()
        elif tag_name == 'switch_consume':
            mpd.consume_switch()
        elif tag_name == 'btn_rescan':
            mpd.library_rescan()
        elif tag_name == 'btn_update':
            mpd.library_update()
        elif tag_name == 'btn_return':
            self.close()


class ScreenSettingsMPD(ScreenModal):
    """ Screen for settings playback options

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """
    def __init__(self, screen_rect):
        ScreenModal.__init__(self, screen_rect, _("MPD settings"))
        button_left = self.window_x + 10
        button_width = self.window_width - 2 * button_left
        label = _("Change host: {0}").format(config_file.setting_get('MPD Settings', 'host'))
        self.add_component(ButtonText('btn_host', self.screen, button_left, 30, button_width, 32, label))
        label = _("Change port: {0}").format(config_file.setting_get('MPD Settings', 'port'))
        self.add_component(ButtonText('btn_port', self.screen, button_left, 72, button_width, 32, label))
        self.add_component(
            ButtonText('btn_music_dir', self.screen, button_left, 114, button_width, 32, _("Change music directory")))
        label = _("Back")
        self.add_component(ButtonText('btn_back', self.screen, button_left, 198, button_width, 32, label))

    def on_click(self, x, y):
        tag_name = super(ScreenModal, self).on_click(x, y)
        setting_label = ""
        setting_value = None
        if tag_name == 'btn_back':
            self.close()
            return
        elif tag_name == 'btn_host':
            setting_label = _("Set mpd host")
            self.keyboard_setting(setting_label, 'MPD Settings', 'host')
            mpd.disconnect()
            mpd.host = config_file.setting_get('MPD Settings', 'host')
            mpd.connect()
        elif tag_name == 'btn_port':
            setting_label = _("Set mpd server port")
            self.keyboard_setting(setting_label, 'MPD Settings', 'port')
            mpd.disconnect()
            mpd.host = int(config_file.setting_get('MPD Settings', 'port'))
            mpd.connect()
        elif tag_name == 'btn_music_dir':
            setting_label = _("Set music directory")
            self.keyboard_setting(setting_label, 'MPD Settings', 'music directory')
            mpd.music_directory = config_file.setting_get('MPD Settings', 'music directory')
        self.update()
        self.show()

    def keyboard_setting(self, caption, section, key, value=""):
        setting_value = config_file.setting_get(section, key, value)
        keyboard = Keyboard(self.screen, caption, setting_value)
        keyboard.title_color = FIFTIES_ORANGE
        new_value = keyboard.show()  # Get entered search text
        config_file.setting_set(section, key, new_value)

    def update(self):
        label = _("Change host: {0}").format(config_file.setting_get('MPD Settings', 'host'))
        self.components['btn_host'].draw(label)
        label = _("Change port: {0}").format(config_file.setting_get('MPD Settings', 'port'))
        self.components['btn_port'].draw(label)


class ScreenSystemInfo(ScreenModal):
    """ Screen for settings playback options

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """

    def __init__(self, screen_rect):
        ScreenModal.__init__(self, screen_rect, _("System info"))
        button_left = self.window_x + 10
        button_width = self.window_width - 2 * button_left
        label = _("Back")
        self.add_component(ButtonText('btn_back', self.screen, button_left, 198, button_width, 32, label))
        info = mpd.mpd_client.stats()
        self.add_component(LabelText('lbl_database', self.screen, 
                                     button_left, 30, 200, 18,
                                     _("Music database")))
        self.components['lbl_database'].font_color = theme.color.screen_caption_font

        artist_count = _("Artists: {:,}").format(int(info['artists']))
        self.add_component(LabelText('lbl_artist_count', self.screen, 
                                     button_left, 48, 100, 18, 
                                     artist_count))

        album_count = _("Albums: {:,}").format(int(info['albums']))
        self.add_component(LabelText('lbl_album_count', self.screen,
                                    button_left + 100, 48, 100, 18,
                                    album_count))

        song_count = _("Songs: {:,}").format(int(info['songs']))
        self.add_component(LabelText('lbl_song_count', self.screen,
                                     button_left + 210, 48, 100, 18,
                                     song_count))

        play_time = _("Total time: ") + self.make_time_string(int(info['db_playtime']))
        self.add_component(LabelText('lbl_play_time', self.screen,
                                     button_left, 66, 300, 18,
                                     play_time))

        # TODO: Was ist hier gemeint? Welcher Server?
        # Was interessiert mich die IP-Adresse meines eigenen PCs?

        self.add_component(LabelText('lbl_system', self.screen,
                                     button_left, 90, 100, 18,
                                     _("Server")))
        self.components['lbl_system'].font_color = self.screen_caption_font

        self.add_component(LabelText('lbl_host_name', self.screen,
                                     button_left, 108, 1500, 18,
                                     _("Host name: {0}").format(socket.gethostname())))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('localhost', 0))
            ip_address = s.getsockname()[0]
            self.add_component(LabelText('lbl_ip_address', self.screen,
                                         button_left, 126, 1500, 18,
                                         _("IP address: {0}").format(ip_address)))

        except Exception, e:
            print e

    def on_click(self, x, y):
        tag_name = super(ScreenModal, self).on_click(x, y)
        if tag_name == 'btn_back':
            self.close()
            return

    def make_time_string(self, seconds):
        days = int(seconds / 86400)
        hours = int((seconds - (days * 86400)) / 3600)
        minutes = int((seconds - (days * 86400) - (hours * 3600)) / 60)
        seconds_left = int(round(seconds - (days * 86400) - (hours * 3600) - (minutes * 60), 0))
        time_string = ""
        if days > 0:
            time_string += str(days) + _(" days ")
        if hours > 0:
            time_string += str(hours) + _(" hrs ")
        if minutes > 0:
            time_string += str(minutes) + _(" mins ")
        if seconds_left > 0:
            time_string += str(seconds_left) + _(" secs ")

        return time_string
