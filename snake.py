import numpy as np
import pyglet as pg
import math
import astar


class Snake(pg.window.Window):
    """
    Manages core snake game.

    Includes game window and all in-game technical and graphical behavior,
    except for pathfinding algorithm, which has its own file.
    """

    def __init__(self, play_style=1):
        """
        Declaration of class parameters.

        :param play_style: Represents type of controls.
                           1: Manual play - Player controls snake using keyboard input.
                           2: Automated play - Snake is controlled by AI.
        """
        # self.test = 100  # Number of test runs
        self.final_score = 0  # Achieved score
        self.square_size = 20  # Size of one game tile
        self.columns = 25  # Number of tiles in one row
        self.rows = 25  # Number of tiles in one column
        self.length = 1  # Length of snake (length of 1 is head without body)
        self.play_style = play_style  # 1 = manual, 2 = AI (A*)
        self.keypress = 0  # Indicates if key was pressed during last game-tick.
        self.active = 0  # Indicates if game is active (is inactive after crashing the snake or before the game.
        self.game_speed = 30.0  # Refresh rate for game-ticks
        self.green = (55, 255, 55)  # Color - Light green
        self.greenD = (25, 155, 25)  # Color - Dark green
        self.blue = (55, 55, 255)  # Color - Blue
        self.red = (255, 55, 55)  # Color - Red
        self.gray = (150, 150, 150)  # Color - Gray
        self.start_pos = (math.floor(self.columns / 2), math.floor(self.rows / 2))  # Starting position for snake
        self.direction = (0, 0)  # Direction for the next snake move (X axis, Y axis)
        self.head = self.start_pos  # Position of head of the snake
        self.apple = (np.random.randint(0, self.columns), np.random.randint(0, self.rows))  # Postion of apple
        while self.apple == self.start_pos:  # Placing apple in empty space
            self.apple = (np.random.randint(0, self.columns), np.random.randint(0, self.rows))

        """
        Numpy array representing game 

        Biggest number is apple, Biggest number-1 is head of the snake.
        Other non-zero numbers is body of the snake.
        """
        self.game_field = np.full((self.columns, self.rows), 0)  # Pre-filled array with 0
        self.game_field[self.start_pos[0], self.start_pos[1]] = self.length  # Positioning head in numpy array
        self.game_field[self.apple[0], self.apple[1]] = self.length + 1  # Positioning apple in numpy array

        self.batch = pg.graphics.Batch()  # Graphic group for snake and apple
        self.ai_lines = pg.graphics.Batch()  # Graphic group for lines (Path for automated snake)
        self.stuck = 0  # Indicates if AI found no way to apple (-> Keep same direction for snake)

        # Window for the game
        super().__init__(width=self.columns * self.square_size, height=self.rows * self.square_size, caption='0')
        super().set_visible(False)

        self.appleS = pg.shapes.Rectangle(self.apple[0] * self.square_size,
                                          self.apple[1] * self.square_size,
                                          self.square_size, self.square_size,
                                          color=self.red, batch=self.batch)  # Shape for apple
        self.dir_list = []  # List of directions to take (Last element is first direction to take)
        self.draw_list = []  # List of parts of the snake, which will be drawn
        self.draw_line = []  # List of coordinates to connect with lines (path of the automated snake)

    def run(self):
        """
        Is called, when game starts.

        :return: Nothing
        """
        self.init_game()
        self.set_visible(True)  # Show game window
        self.active = 1

    def update_graphics(self):
        """
        Updates all graphic.

        Called in update function (once per tick).

        :return: Nothing
        """
        self.draw_list = []
        for i in range(0, self.columns):
            for j in range(0, self.rows):
                if self.game_field[i, j] == self.length:
                    self.draw_list.append(pg.shapes.Rectangle(i * self.square_size,
                                                              j * self.square_size,
                                                              self.square_size,
                                                              self.square_size,
                                                              color=self.greenD, batch=self.batch))  # Head
                elif 0 < self.game_field[i, j] < self.length:
                    self.draw_list.append(pg.shapes.Rectangle(i * self.square_size,
                                                              j * self.square_size,
                                                              self.square_size,
                                                              self.square_size,
                                                              color=self.green, batch=self.batch))  # Body
        if self.dir_list:  # If there are directions, draw them
            coords = self.dir_to_coord(self.dir_list, self.head)
            self.draw_line = []
            for i in range(0, len(coords) - 1):
                self.draw_line.append(pg.shapes.Line(coords[i][0], coords[i][1], coords[i + 1][0], coords[i + 1][1], 2,
                                                     color=self.blue, batch=self.ai_lines))
        else:
            self.draw_line = []

    def on_draw(self):
        """
        Clear screen and draw prepared graphics

        :return: Nothing
        """
        self.clear()
        self.batch.draw()
        if self.draw_line:
            self.ai_lines.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Check for keyboard input.

        :param symbol: Pressed key
        :param modifiers: Pressed special key (CTRL, SHIFT...)
        :return: Nothing
        """
        if self.keypress == 0 and self.play_style == 1:
            if symbol == pg.window.key.UP or symbol == pg.window.key.W:  # Move up
                self.keypress = 1
                if self.direction != (0, -1):
                    self.direction = (0, 1)
            elif symbol == pg.window.key.DOWN or symbol == pg.window.key.S:  # Move down
                self.keypress = 1
                if self.direction != (0, 1):
                    self.direction = (0, -1)
            elif symbol == pg.window.key.LEFT or symbol == pg.window.key.A:  # Move left
                self.keypress = 1
                if self.direction != (1, 0):
                    self.direction = (-1, 0)
            elif symbol == pg.window.key.RIGHT or symbol == pg.window.key.D:  # Move right
                self.keypress = 1
                if self.direction != (-1, 0):
                    self.direction = (1, 0)
        if symbol == pg.window.key.ESCAPE:  # Quit the current game
            self.end_game()

    def get_direction(self):
        """
        Calls algorithm, which return calculated path from head to apple.

        Currently used algorithm is basic A*.
        Calculated path is saved as one of the class parameters. (dir_list)
        Path is represented as list of direction,
        which are selected one by one to direct snake for every following square.
        Directions is used for telling the snake, where to move next each frame.

        Directions:
            Go up    = ( 0,  1)
            Go down  = ( 0, -1)
            Go left  = (-1,  0)
            Go right = ( 1,  0)

        :return: Nothing
        """
        self.dir_list = astar.calculate_path(self.game_field, self.length, self.head,
                                             self.apple, self.columns, self.rows)
        if not self.dir_list:
            self.stuck = 1

    def update_direction(self):
        """
        Change direction of the head of the snake.

        Take following direction from direction list and set it as current direction.
        Remove that direction from direction list.

        :return: Nothing
        """
        if self.dir_list:
            self.direction = self.dir_list[len(self.dir_list) - 1]
            self.dir_list.pop(len(self.dir_list) - 1)

    def dir_to_coord(self, directions, start):
        """
        Calculate position for each square in the path using the direction list.

        :param directions: List of direction represented as tuple of two ints -> (int, int)
        :param start: Position of head of the snake
        :return: List of exact coordinates of each square in the path of the snake to next apple.
        """
        # noinspection PyListCreation
        coords = []
        coords.append(
            (start[0] * self.square_size + self.square_size / 2, start[1] * self.square_size + self.square_size / 2))
        for i in range(len(directions) - 1, -1, -1):
            coords.append((coords[-1][0] + (directions[i][0] * self.square_size),
                           coords[-1][1] + (directions[i][1] * self.square_size)))
        return coords

    def place_apple(self):
        """
        Place apple in free area.

        After taking the apple (Or at the start of the new game) places apple in are, where is unocuppied space.

        :return: Nothing
        """
        if self.length < self.columns*self.rows-1:
            empty = []
            for i in range(0, self.columns):
                for j in range(0, self.rows):
                    if self.game_field[i, j] == 0:
                        empty.append((i, j))
            apple_pos = np.random.randint(0, len(empty))
            self.apple = (empty[apple_pos][0], empty[apple_pos][1])
            self.appleS.x = self.apple[0] * self.square_size
            self.appleS.y = self.apple[1] * self.square_size
        else:
            self.apple = (-1, -1)
            self.appleS.x = self.apple[0] * self.square_size
            self.appleS.y = self.apple[1] * self.square_size

    def init_game(self):
        """
        Prepare new game.

        Set mandatory parameters to new or default values.

        :return: Nothing
        """
        self.direction = (0, 0)
        self.head = self.start_pos
        self.length = 1
        self.apple = (np.random.randint(0, self.columns), np.random.randint(0, self.rows))
        while self.apple == self.start_pos:
            self.apple = (np.random.randint(0, self.columns), np.random.randint(0, self.rows))
        self.appleS.x = self.apple[0] * self.square_size
        self.appleS.y = self.apple[1] * self.square_size
        self.game_field = np.full((self.columns, self.rows), 0)
        self.game_field[self.head[0], self.head[1]] = self.length
        self.game_field[self.apple[0], self.apple[1]] = self.length + 1
        self.dir_list = []
        self.stuck = 0
        super().set_caption(str(self.length - 1))

    def on_close(self):
        """
        Hide window instead of closing.

        Since same window can be used for every game, its better to just hide/unhide it,
        rather than create a new one every time.

        :return: Nothing
        """
        self.end_game()

    def end_game(self):
        """
        Set the game to its inactive state.

        Set some parameters to default values to make game inactive.

        :return: Nothing
        """
        self.active = 0
        self.final_score = self.length - 1
        self.set_visible(False)

    def collision_sides(self):
        """
        Check for collisions with window borders.

        :return: Nothing
        """
        new_pos = (self.head[0] + self.direction[0], self.head[1] + self.direction[1])
        if new_pos[0] < 0 or new_pos[0] > self.columns - 1 or new_pos[1] < 0 or new_pos[1] > self.rows - 1:
            self.end_game()

    def collision_apple(self):
        """
        Check if snake eated the apple.

        When snake hits the apple, increase the length of the snake and place new apple.

        :return: Nothing
        """
        if self.head[0] == self.apple[0] and self.head[1] == self.apple[1]:
            self.length = self.length + 1
            for i in range(0, self.columns):
                for j in range(0, self.rows):
                    if self.game_field[i, j] != 0:
                        self.game_field[i, j] += 1
            super().set_caption(str(self.length - 1))
            self.place_apple()

    def collision_body(self):
        """
        Check if snake hit itself.

        If yes, then end the game.

        :return: Nothing
        """
        new_pos = (self.head[0] + self.direction[0], self.head[1] + self.direction[1])
        if new_pos[0] >= self.columns or new_pos[1] >= self.rows:
            self.end_game()
        elif 0 < self.game_field[new_pos[0], new_pos[1]] < self.length:
            self.end_game()

    def update_game_field(self):
        """
        Update numpy array representing the game situation.

        :return: Nothing
        """
        self.game_field -= 1
        self.game_field[self.head[0], self.head[1]] = self.length
        self.game_field[self.apple[0], self.apple[1]] = self.length + 1
        self.game_field = np.clip(self.game_field, 0, None)

    def update(self, dt):
        """
        Update game situation.

        Check for collisions, update positions, graphics and calculate path

        :param dt: Number of seconds since the last tick
        :return: Nothing
        """
        if self.active == 1:
            self.keypress = 0
            if not self.dir_list and self.stuck == 0 and self.play_style != 1:
                self.get_direction()
            self.update_direction()
            self.collision_sides()
            self.collision_body()
            if self.active == 1:
                self.head = (self.head[0] + self.direction[0], self.head[1] + self.direction[1])
                self.collision_apple()
                self.update_game_field()
                self.update_graphics()
