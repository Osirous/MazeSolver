from graphicals import Cell
import random
import time

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._cells = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = seed

        if self.seed is not None:
            random.seed(self.seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()


    def _create_cells(self):
        for i in range(self.num_cols):
            col_cells = []
            for j in range(self.num_rows):
                col_cells.append(Cell(self.win))
            self._cells.append(col_cells)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
    
    def _draw_cell(self, i, j):
        if self.win is None:
            return
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.02)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self._draw_cell(self.num_cols -1, self.num_rows -1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            possible_directions = []
            
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                possible_directions.append((i, j - 1))

            # down
            if j < self.num_rows -1 and not self._cells[i][j + 1].visited:
                possible_directions.append((i, j + 1))

            # left
            if i > 0 and not self._cells[i -1][j].visited:
                possible_directions.append((i - 1, j))
            
            # right
            if i < self.num_cols -1 and not self._cells[i + 1][j].visited:
                possible_directions.append((i + 1, j))
            

            # return if there is nowhere to go
            if not possible_directions:
                self._draw_cell(i, j)
                return
            
            # Random selection of possible directions
            current_direction = random.randrange(len(possible_directions))
            new_direction = possible_directions[current_direction]


            # Wall-breaking logic

            # Determine which wall to remove between current cell and next cell

            if new_direction[1] == j - 1:  # moving up
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            elif new_direction[1] == j + 1:  # moving down
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            elif new_direction[0] == i - 1:  # moving left
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            elif new_direction[0] == i + 1:  # moving right
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False


            # Move to the newly chosen cell
            self._break_walls_r(new_direction[0], new_direction[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        # moving up
        if (j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j - 1].visited):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)
        # moving down
        if (j < self.num_rows - 1 and not self._cells[i][j].has_bottom_wall and not self._cells[i][j + 1].visited):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)
        # moving left
        if (i > 0 and not self._cells[i][j].has_left_wall and not self._cells[i - 1][j].visited):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)
        # moving right
        if (i < self.num_cols - 1 and not self._cells[i][j].has_right_wall and not self._cells[i + 1][j].visited):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        return False

    def solve(self):
        return self._solve_r(0, 0)