class BaseContainer():
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup()

    def handle_input(self, key):
        pass
    
    def rename(self, new_name: str):
        self.title_label.set_text(new_name)
        self.title_label.draw()
    
    def resize(self, x, y):
        self.win.resize(x, y)
        self.title_label.resize(x, y)
    
    def set_size(self, lambda_x, lambda_y, lambda_w, lambda_h):
        self.win.set_size(lambda_x, lambda_y, lambda_w, lambda_h)
        