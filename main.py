from graphicals import Window
from maze import Maze
import sys

def main():
    num_rows = 24
    num_cols = 32
    margin = 50
    screen_x = 1280
    screen_y = 1024
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    sys.setrecursionlimit(10000)
    win = Window(screen_x, screen_y)
    
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed=None)

    print("maze created")
    is_solveable = maze.solve()
    if not is_solveable:
        print("maze can't be solved...")
    else:
        print("maze solved!")

    win.wait_for_close()

if __name__ == "__main__":
    main()