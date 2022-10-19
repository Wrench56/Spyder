from screens import screen
from widgets import textbox
import curses

class Login(screen.Screen):
    def __init__(self, stdscr, dataobj) -> None:
        super().__init__(stdscr)
        self.dataobj = dataobj

        self.show()
    
    def show(self):
        self.ms = textbox.Textbox(self.stdscr, 25, 5)
        self.ms.set_size(lambda x: 0, lambda y: 0)
        self.ms.draw(0, 0)
        while True:
            ch = self.stdscr.getch()
            if ch == curses.KEY_HOME:
                break
            else:
                self.ms.input(ch)