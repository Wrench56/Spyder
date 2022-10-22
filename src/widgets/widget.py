class Widget():
    def __init__(self, stdscr):
        self.stdscr = stdscr

        self.lambda_x = lambda x: x
        self.lambda_y = lambda y: y

    def set_size(self, lambda_x, lambda_y, lambda_w, lambda_h):
        self.lambda_x = lambda_x
        self.lambda_y = lambda_y
        self.lambda_w = lambda_w
        self.lambda_h = lambda_h

    def getxy(self):
        return self.last_x, self.last_y

    def resize(self, x, y):
        self.last_x = x
        self.last_y = y

        self.draw()

    