class Widget():
    def __init__(self, stdscr):
        self.stdscr = stdscr

        self.lambda_x = lambda x: x
        self.lambda_y = lambda y: y

    def set_size(self, lambda_x, lambda_y):
        self.lambda_x = lambda_x
        self.lambda_y = lambda_y

    def draw(self, x, y):
        pass