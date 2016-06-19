#!/usr/bin/env python
"""
**pi-jukebox.py**: Main file
"""

import time
import pygame
import locale
import gettext
from config_file import config_file
from settings import *
from gui_screens import Screens
from pij_screen_navigation import ScreenNavigation
from screen_library import ScreenMessage, ScreenLibrary
from screen_player import ScreenPlaying, ScreenPlaylist
from screen_directory import ScreenDirectory
from screen_radio import ScreenRadio
from screen_settings import ScreenSettingsMPD
from mpd_client import mpd

__author__ = 'Mark Zwart'

class PiJukeboxScreens(Screens):
    """ Manages Pi Jukebox's main screens.
            - Player screen
            - Library screen
        Handles screen switching, clicking and swiping and displaying mpd status
        updates on screen(s)
    """
    def __init__(self):
        Screens.__init__(self)
        self.screen_list.append(ScreenPlaying(SCREEN))  # Screen with now playing and cover art
        self.screen_list.append(ScreenPlaylist(SCREEN))  # Create player with playlist screen
        self.screen_list.append(ScreenLibrary(SCREEN))  # Create library browsing screen
        self.screen_list.append(ScreenDirectory(SCREEN))  # Create directory browsing screen
        self.screen_list.append(ScreenRadio(SCREEN))  # Create radio station managing screen

    def mpd_updates(self):
        """ Updates a current screen if it shows mpd relevant content. """
        self.screen_list[self.current_index].update()

def init_gettext(domain, localedir):
    locale.setlocale(locale.LC_ALL, '')
    gettext.bindtextdomain(domain, localedir)
    gettext.bind_textdomain_codeset(domain, 'UTF-8')
    gettext.textdomain(domain)
    gettext.install(domain, localedir, unicode=True)

def apply_settings():
    # Check for first time settings
    if not config_file.setting_exists('MPD Settings', 'music directory'):
        screen_message = ScreenMessage(
            SCREEN, 
            _("No music directory"),
            _("If you want to display cover art, Pi-Jukebox needs to "
              "know which directory your music collection is in. "
	          "The location can also be found in your mpd.conf entry "
	          "'music directory'."),
            'warning')
        screen_message.show()
        settings_mpd_screen = ScreenSettingsMPD(SCREEN)
        settings_mpd_screen.keyboard_setting(_("Set music directory"), 'MPD Settings', 'music directory',
                                             '/var/lib/mpd/music/')
    mpd.host = config_file.setting_get('MPD Settings', 'host')
    mpd.port = int(config_file.setting_get('MPD Settings', 'port'))
    mpd.music_directory_set(config_file.setting_get('MPD Settings', 'music directory'))
    if not config_file.section_exists('Radio stations'):
        config_file.setting_set('Radio stations', "Radio Swiss Jazz", "http://stream.srg-ssr.ch/m/rsj/mp3_128")


def main():
    """ The function where it all starts...."""
    init_gettext('pi-jukebox', 'locale')
    pygame.display.set_caption("Pi Jukebox")
    apply_settings()  # Check for first time settings and applies settings

    # Check whether mpd is running and get it's status
    if not mpd.connect():
        screen_message = ScreenMessage(
            SCREEN,
            _("Couldn't connect to the mpd server!"),
            _("Couldn't connect to the mpd server {0} on port {1:d}!".format(mpd.host, mpd.port)) +
            _("Check settings in file pi-jukebox.conf or check is server is running 'sudo service mpd status'."),
            'error')
        screen_message.show()
        sys.exit()

    mpd.status_get()  # Get mpd status
    screens = PiJukeboxScreens()  # Screens
    screens.show()  # Display the screen

    while 1:
        # Check whether mpd's status changed
        pygame.time.wait(PYGAME_EVENT_DELAY)
        if mpd.status_get():
            screens.mpd_updates()  # If so update relevant screens

        for event in pygame.event.get():  # Do for all events in pygame's event queue
            screens.process_mouse_event(event)  # Handle mouse related events
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                mpd.disconnect()
                sys.exit()

    time.sleep(0.2)
    pygame.display.update()


if __name__ == '__main__':
    main()
