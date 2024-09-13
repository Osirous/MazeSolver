from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        # create the root window widget
        self.root = Tk()
        # Set the title of the root window
        self.root.title("Maze Solver")
        # creates canvas widget and assigns it to self.__canvas
        self.canvas = Canvas(self.root, width=width, height=height)
        # display's the canvas
        self.canvas.pack()
        # a bool for determining if Maze Solver is running.
        self.__isRunning = False
        # CLOSE STUFFS
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.__isRunning = True
        while self.__isRunning:
            self.redraw()
        print("application exited.")

    def close(self):
        self.__isRunning = False
        # close the program
        self.root.destroy()

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)
        
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color="black"):
        x1, y1 = self.point1.x, self.point1.y
        x2, y2 = self.point2.x, self.point2.y

        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)

class Cell:
    def __init__(self, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_top_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = window
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        # Is there a window to draw on?
        if self._win is None:
            # There isn't, we can't draw!
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        if self.has_top_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, "white")

        if self.has_bottom_wall:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, "white")

        if self.has_left_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, "white")

        if self.has_right_wall:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        self.center_x = (self._x1 + self._x2) / 2
        self.center_y = (self._y1 + self._y2) / 2
        to_cell.center_x = (to_cell._x1 + to_cell._x2) / 2
        to_cell.center_y = (to_cell._y1 + to_cell._y2) / 2

        color = "gray" if undo else "red"

        self._win.draw_line(Line(Point(self.center_x, self.center_y), Point(to_cell.center_x, to_cell.center_y)), color)