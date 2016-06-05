# Translation support

prepare: locale/de.po
	xgettext -L Python -c -o locale/pi-jukebox.pot *.py
	msgmerge -U locale/de.po locale/pi-jukebox.pot

translation: locale/de/LC_MESSAGES/pi-jukebox.mo
	msgfmt locale/de.po -o locale/de/LC_MESSAGES/pi-jukebox.mo
