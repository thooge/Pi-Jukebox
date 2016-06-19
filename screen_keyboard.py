#-*- coding: utf-8 -*-

"""
=======================================================
**screen_keyboard.py**: On-screen keyboard
=======================================================
"""
__author__ = 'Mark Zwart'

from settings import *
from gui_screens import *

class KeyboardBase(ScreenModal):
    """ The base class of a keyboard, should not be instantiated.

        :param screen_rect: The display's rectangle where the keyboard is drawn on.
        :param caption: The title displayed at the top of the screen.
        :param text: The text that will be edited with the keyboard, default = "".
    """
    def __init__(self, screen_rect, caption, text=""):
        ScreenModal.__init__(self, screen_rect, caption)
        self.text = text
        # Dialog close button
        btn = ButtonText('btn_cancel', self.screen,
            SCREEN_WIDTH - TITLE_HEIGHT, 0, TITLE_HEIGHT, TITLE_HEIGHT, 'X')
        btn.button_color = theme.color.button_title
        self.add_component(btn)
        # Edit box
        edit_box = LabelText('lbl_edit_box', screen_rect, 5, 30, 310, 25, text)
        edit_box.background_color = WHITE
        edit_box.font_color = BLACK
        edit_box.set_alignment(HOR_LEFT, VERT_MID, 5)
        self.add_component(edit_box)

    def add_row_buttons(self, list_symbols, x, y, w, h):
        """ Adds a list of symbol keys starting at x on y with width w and height h. """
        for letter in list_symbols:
            btn_name = 'btn_symbol_' + letter
            btn = ButtonText(btn_name, self.screen, x, y, w, h, letter)
            self.add_component(btn)
            x += w + KEY_SPACE

    def set_text(self, text):
        """ Sets the edit box's text.

            :param text: Text that needs to be edited using the keyboard
        """
        self.text = text
        self.components['lbl_edit_box'].caption = text


class KeyboardLetters(KeyboardBase):
    """ Displays keyboard for letters.
    """
    def __init__(self, screen_rect, caption, text=""):
        KeyboardBase.__init__(self, screen_rect, caption, text)

        self.shift_state = False

        y_row = 65
        y_row_increment = 45
        if KEYBOARD_LAYOUT == 'de':
            first_row = ['q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', 'ü']
            first_x = 1
            second_row = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä']
            second_x = 1
            third_row = ['y', 'x', 'c', 'v', 'b', 'n', 'm']
            third_x = 60
        else:
            first_row = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
            first_x = 0
            second_row = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
            second_x = 17
            third_row = ['z', 'x', 'c', 'v', 'b', 'n', 'm']
            third_x = 49
        self.add_row_buttons(first_row, first_x, y_row, KEY_LTR_WIDTH_STD, KEY_HEIGHT)
        y_row += y_row_increment
        self.add_row_buttons(second_row, second_x, y_row, KEY_LTR_WIDTH_STD, KEY_HEIGHT)
        y_row += y_row_increment
        self.add_row_buttons(third_row, third_x, y_row, KEY_LTR_WIDTH_STD, KEY_HEIGHT)
        self.add_component(ButtonIcon('btn_shift', screen_rect, ICO_SHIFT, 3, y_row))
        self.add_component(ButtonIcon('btn_backspace', screen_rect, ICO_BACKSPACE, 271, y_row))

        y_row += y_row_increment
        self.add_component(ButtonText('btn_symbol_comma', screen_rect, 50, y_row, 32, 32, ','))
        self.add_component(ButtonText('btn_symbol_space', screen_rect, 82, y_row, 159, 32, ' '))
        self.add_component(ButtonText('btn_symbol_point', screen_rect, 241, y_row, 32, 32, '.'))
        self.add_component(ButtonIcon('btn_enter', screen_rect, ICO_ENTER, 271, y_row))
        self.add_component(ButtonIcon('btn_symbols', screen_rect, ICO_SYMBOLS, 4, y_row))

    def __letters_shift(self):
        """ Sets button values to lower- or uppercase depending on the shift state. """
        for key, value in self.components.items():
            if value.tag_name[:11] == 'btn_symbol_':
                if not self.shift_state:
                    new_letter = value.caption.upper()
                else:
                    new_letter = value.caption.lower()
                value.caption = new_letter
        self.shift_state = not self.shift_state
        self.show()

    def on_click(self, x, y):
        tag_name = super(KeyboardLetters, self).on_click(x, y)

        if tag_name is None:
            return

        if tag_name == 'btn_cancel':
            self.return_object = 'cancel'
            self.close()
            return

        if tag_name == 'btn_shift':
            self.__letters_shift()
        elif tag_name[:11] == 'btn_symbol_':  # If keyboard symbol is pressed add it to the text
            self.components['lbl_edit_box'].caption += self.components[tag_name].caption
            self.components['lbl_edit_box'].draw()
            if self.shift_state:
                self.shift_state = False
                self.__letters_shift()
        elif tag_name == 'btn_backspace':  # Remove last character of the text
            current_value = self.components['lbl_edit_box'].caption
            self.components['lbl_edit_box'].caption = current_value[:len(current_value) - 1]
            self.components['lbl_edit_box'].draw()
        self.text = self.components['lbl_edit_box'].caption
        self.return_object = self.components['lbl_edit_box'].caption

        if tag_name == 'btn_symbols':
            self.return_object = 'symbols'  # Switch to numbers/symbols keyboard
            self.close()
        elif tag_name == 'btn_enter':
            self.return_object = 'enter'  # Confirms current text value
            self.close()


class KeyboardSymbols(KeyboardBase):
    """ Displays keyboard for numbers and symbols.
    """
    def __init__(self, screen_rect, caption, text=""):
        KeyboardBase.__init__(self, screen_rect, caption, text)

        y_row = 65
        y_row_increment = 45
        first_row = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.add_row_buttons(first_row, 0, y_row, KEY_WIDTH_STD, KEY_HEIGHT)

        y_row += y_row_increment
        second_row = ['-', '+', '=', '/', '(', ')', '%', '$', '#', '_']
        self.add_row_buttons(second_row, 0, y_row, KEY_WIDTH_STD, KEY_HEIGHT)

        y_row += y_row_increment
        third_row = [':', ';', '.', ',', '?', '!', '\'', '*']
        self.add_row_buttons(third_row, 5, y_row, KEY_WIDTH_STD, KEY_HEIGHT)
        self.add_component(ButtonIcon('btn_backspace', screen_rect, ICO_BACKSPACE, 271, y_row))

        y_row += y_row_increment
        self.add_component(ButtonIcon('btn_enter', screen_rect, ICO_ENTER, 271, y_row))
        self.add_component(ButtonIcon('btn_symbol_letters', screen_rect, ICO_LETTERS, 0, y_row))
        self.add_component(ButtonText('btn_symbol_ampersand', screen_rect, 50, y_row, 32, 32, '&'))
        self.add_component(ButtonText('btn_symbol_space', screen_rect, 82, y_row, 159, 32, ' '))
        self.add_component(ButtonText('btn_symbol_at', screen_rect, 241, y_row, 32, 32, '@'))

    def on_click(self, x, y):
        tag_name = super(KeyboardSymbols, self).on_click(x, y)

        if tag_name is None:
            return

        if tag_name == 'btn_cancel':
            self.return_object = 'cancel'
            self.close()
            return

        if tag_name[:11] == 'btn_symbol_':  # If keyboard symbol is pressed add it to the text
            self.components['lbl_edit_box'].caption += self.components[tag_name].caption
            self.components['lbl_edit_box'].draw()
        elif tag_name == 'btn_backspace':  # Remove last character of the text
            current_value = self.components['lbl_edit_box'].caption
            self.components['lbl_edit_box'].caption = current_value[:len(current_value) - 1]
            self.components['lbl_edit_box'].draw()
        self.return_object = self.components['lbl_edit_box'].caption
        self.text = self.components['lbl_edit_box'].caption  # Ensure text = to the edit box

        if tag_name == 'btn_symbol_letters':
            self.return_object = 'letters'  # Switch to letters keyboard
            self.close()
        if tag_name == 'btn_enter':
            self.return_object = 'enter'  # Confirms current text value
            self.close()


class Keyboard():
    """ Called keyboard class that displays a text edit field with a
        letter or symbol keyboard.

        :param screen_rect: The display's rectangle where the keyboard is drawn on.
        :param caption: The title displayed at the top of the screen.
        :param text: The text that will be edited with the keyboard, default = "".
    """
    def __init__(self, screen_rect, caption, text=""):
        self.text = text
        self.text_original = text
        self.selected = 'letters'
        self.keyboard_letters = KeyboardLetters(screen_rect, caption, text)
        self.keyboard_symbols = KeyboardSymbols(screen_rect, caption, text)

    def show(self):
        """ Loops until enter, cancel or escape on the keyboard is pressed.

            :return: The text as it was edited when return was pressed, or the original text in case of a cancellation.
        """
        value = ''
        while value != 'enter' and value != 'cancel':
            # Switch between the different keyboards (letter or number/symbol)
            if self.selected == 'letters':
                self.keyboard_letters.set_text(self.text)
                value = self.keyboard_letters.show()
                self.text = self.keyboard_letters.text
                if value == 'symbols':
                    self.selected = value
                    self.show()
            elif self.selected == 'symbols':
                self.keyboard_symbols.set_text(self.text)
                value = self.keyboard_symbols.show()
                self.text = self.keyboard_symbols.text
                if value == 'letters':
                    self.selected = value
            if value is None:
                # ESC pressed
                value = 'cancel'
        if value == 'enter':
            return self.text  # When the user pressed enter the entered text value is returned
        elif value == 'cancel':
            return self.text_original  # When the user chose to cancel the original text value is returned

