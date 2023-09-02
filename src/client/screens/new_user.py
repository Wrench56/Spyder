import curses

import widgets
from screens import screen
from structs.new_user_struct import NewUserData
from utils import colors, create_user, keyboard, terminal


class NewUser(screen.Screen):
    def __init__(self, stdscr: object) -> None:
        super().__init__(stdscr)
        self.focus = 0
        self.status = {
            'Valid username': 'UNKW',
            'Valid password': 'UNKW',
            'Passwords match': 'UNKW',
            'User directory created': 'UNKW',
            'Config files created': 'UNKW',
            'Login file created': 'UNKW',
            'USER READY TO USE': 'UNKW'
        }

        # Rename terminal
        terminal.rename_terminal('Spyder - Create New User')

        # Create widgets
        self.setup()

        # Start the logic part
        self.logic()

    def setup(self) -> None:
        self.set_min(68, 15)

        self.username_win = widgets.Subwindow(self.stdscr)
        self.username_win.set_size(lambda x: 5, lambda y: 2, lambda w: 20, lambda h: 3)
        self.username_label = widgets.Label(self.username_win.get(), ' Username ')
        self.username_label.set_size(lambda x: 1, lambda y: 0, None, None)
        self.username_textbox = widgets.Textbox(self.username_win.get(), width=19, height=1)
        self.username_textbox.set_size(lambda x: 1, lambda y: 1, lambda w: 17, lambda h: 0)

        self.password_win = widgets.Subwindow(self.stdscr)
        self.password_win.set_size(lambda x: 5, lambda y: 6, lambda w: 20, lambda h: 3)
        self.password_label = widgets.Label(self.password_win.get(), ' Password ')
        self.password_label.set_size(lambda x: 1, lambda y: 0, None, None)
        self.password_textbox = widgets.Textbox(self.password_win.get(), width=19, height=1, show_chars='*')
        self.password_textbox.set_size(lambda x: 1, lambda y: 1, lambda w: 17, lambda h: 0)

        self.password_conf_win = widgets.Subwindow(self.stdscr)
        self.password_conf_win.set_size(lambda x: 5, lambda y: 10, lambda w: 20, lambda h: 3)
        self.password_conf_label = widgets.Label(self.password_conf_win.get(), ' Confirm Password ')
        self.password_conf_label.set_size(lambda x: 1, lambda y: 0, None, None)
        self.password_conf_textbox = widgets.Textbox(self.password_conf_win.get(), width=19, height=1, show_chars='*')
        self.password_conf_textbox.set_size(lambda x: 1, lambda y: 1, lambda w: 17, lambda h: 0)

        self.status_win = widgets.Subwindow(self.stdscr)
        self.status_win.set_size(lambda x: 30, lambda y: 2, lambda w: 36, lambda h: 11)
        self.status_label = widgets.Label(self.status_win.get(), ' Status ')
        self.status_label.set_size(lambda x: 1, lambda y: 0, None, None)
        self.status_text_label = widgets.MultilineLabel(self.status_win.get(), self.format_status())
        self.status_text_label.set_size(lambda x: 1, lambda y: 1, None, None)

        self.help_label = widgets.Label(self.stdscr, 'Navigate with KEY_UP & KEY_DOWN, press ENTER to continue!')
        self.help_label.set_size(lambda x: 7, lambda y: 15, None, None)

        self.resize()

        self.refresh_focus(0)

    def logic(self) -> None:
        while True:
            ch = self.stdscr.getch()
            if ch == curses.KEY_RESIZE:
                self.resize()
                self.refresh_focus(self.focus)
            elif ch == curses.KEY_HOME:
                break
            elif ch == curses.KEY_UP:
                if self.focus > 0:
                    self.focus -= 1
                self.refresh_focus(self.focus)
            elif ch == curses.KEY_DOWN:
                if self.focus < 2:
                    self.focus += 1
                self.refresh_focus(self.focus)
            elif ch == keyboard.KEY_TAB:
                if self.focus < 2:
                    self.focus += 1
                else:
                    self.focus = 0
                self.refresh_focus(self.focus)
            elif ch == keyboard.KEY_ENTER:
                self.create_user()
            else:
                self.input_focused(self.focus, ch)

    def color_status_text(self) -> None:
        for i, value in enumerate(self.status.values()):
            if value == 'UNKW':
                colors.colored_addstr(self.status_win.get(), 5, i + 1, '\x1b[33mUNKW')
            elif value == 'FAIL':
                colors.colored_addstr(self.status_win.get(), 5, i + 1, '\x1b[31mFAIL')
            else:
                colors.colored_addstr(self.status_win.get(), 5, i + 1, '\x1b[32m OK ')
        self.refresh_focus(self.focus)

    def format_status(self) -> str:
        formatted_text: str = ''
        for item in self.status.items():
            formatted_text += f' > [{item[1]}] {item[0]}\n'

        return formatted_text

    def input_focused(self, focus: int, input_: int) -> None:
        if focus == 0:
            self.username_textbox.input(input_)
        elif focus == 1:
            self.password_textbox.input(input_)
        elif focus == 2:
            self.password_conf_textbox.input(input_)

    def refresh_focus(self, focus: int) -> None:
        if focus == 0:
            self.username_textbox.update_cursor()
        elif focus == 1:
            self.password_textbox.update_cursor()
        elif focus == 2:
            self.password_conf_textbox.update_cursor()

    def create_user(self) -> None:
        def cleanup() -> None:
            self.password_textbox.draw()
            self.password_conf_textbox.draw()
            self.username_textbox.draw()
            self.refresh_focus(self.focus)

        struct = NewUserData(self.username_textbox.text, self.password_textbox.text)
        if self.username_textbox.text == '':
            self.set_new_status('Valid username', 'FAIL')
            cleanup()
            return
        self.set_new_status('Valid username', ' OK ')

        if self.password_textbox.text == '':
            self.set_new_status('Valid password', 'FAIL')
            cleanup()
            return
        self.set_new_status('Valid password', ' OK ')

        if self.password_conf_textbox.text == self.password_textbox.text:
            self.set_new_status('Passwords match', ' OK ')
        else:
            self.set_new_status('Passwords match', 'FAIL')
            cleanup()
            return

        create_user.run_all(self.set_new_status, struct)
        cleanup()

    def set_new_status(self, field: str, status: str) -> None:
        self.status[field] = status
        if status == 'FAIL':
            self.status['USER READY TO USE'] = 'FAIL'
        self.status_text_label.set_text(self.format_status())
        self.resize()

    def resize(self) -> None:
        y, x = self.stdscr.getmaxyx()
        if not self.resize_check(x, y):
            return

        self.stdscr.erase()
        self.stdscr.refresh()

        self.username_win.resize(x, y)
        self.username_label.resize(x, y)
        self.username_textbox.resize(x, y)

        self.password_win.resize(x, y)
        self.password_label.resize(x, y)
        self.password_textbox.resize(x, y)

        self.password_conf_win.resize(x, y)
        self.password_conf_label.resize(x, y)
        self.password_conf_textbox.resize(x, y)

        self.status_win.resize(x, y)
        self.status_text_label.resize(x, y)
        self.color_status_text()
        self.status_win.resize(x, y)
        self.status_label.resize(x, y)

        self.help_label.resize(x, y)
