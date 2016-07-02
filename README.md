# Pi-Jukebox
A mpd front-end for playing your Raspberry Pi with touchscreen

This fork is undergoing heavy reconstruction and is currently
not intended for "production usage".

Supports different touch-displays:
  - adafruit 2.8", 320x240
  - adafruit 3.5", 480x320
  - Raspberry 7", 800x480

Configure your display in pi-jukebox.conf. The file is
created at first start of the program.

Makes use of the following libraries:
  - python-mpd2, https://github.com/Mic92/python-mpd2/
  - tinytag,  https://github.com/devsnd/tinytag/

For creating documentation debian package 'python-sphinx' is required.

Documentation of code and Raspberry Pi setup: 
http://www.hoogi.de/pi-jukebox/
