import pyglet as pg
import snake as snake

"""Basic declarations."""
window = pg.window.Window(width=250, height=250, caption='Snake')  # Menu window
background = pg.graphics.Batch()  # Button backgrounds
foreground = pg.graphics.Batch()  # Labels

# Manual play option
play_size = (150, 50)  # Size of the button
play_color = (55, 255, 55)  # Color of the button
play_color_hover = (55, 155, 55)  # Hover color of the button
play_position = (window.width / 2 - play_size[0] / 2, window.height - 50 - play_size[1])  # Position of the button
playS = pg.shapes.Rectangle(play_position[0], play_position[1],
                            play_size[0], play_size[1],
                            color=play_color, batch=background)  # Shape of the button
play_label = pg.text.Label('Manual play', font_name='Calibri', font_size=15,
                           x=play_position[0] + play_size[0] / 2,
                           y=play_position[1] + play_size[1] / 2,
                           anchor_x='center', anchor_y='center',
                           color=(0, 0, 0, 255), batch=foreground)  # Label of the button

# Automated play option
ai_size = (150, 50)  # Size of the button
ai_color = (55, 255, 55)  # Color of the button
ai_color_hover = (55, 155, 55)  # Hover color of the button
ai_position = (window.width / 2 - ai_size[0] / 2,
               window.height - 50 - play_size[1] - 25 - ai_size[1])  # Position of the button
aiS = pg.shapes.Rectangle(ai_position[0], ai_position[1],
                          ai_size[0], ai_size[1],
                          color=ai_color, batch=background)  # Shape of the button
ai_label = pg.text.Label('AI play', font_name='Calibri', font_size=15,
                         x=ai_position[0] + ai_size[0] / 2,
                         y=ai_position[1] + ai_size[1] / 2,
                         anchor_x='center', anchor_y='center',
                         color=(0, 0, 0, 255), batch=foreground)  # Label of the button

# Score Labels
score_label1 = pg.text.Label('Last score: 0', font_name='Calibri', font_size=10,
                             x=play_position[0] + play_size[0] / 2,
                             y=20,
                             anchor_x='center', anchor_y='center',
                             color=(255, 255, 255, 255), batch=foreground)
score_label2 = pg.text.Label('Last score: 0', font_name='Calibri', font_size=10,
                             x=play_position[0] + play_size[0] / 2,
                             y=10,
                             anchor_x='center', anchor_y='center',
                             color=(255, 255, 255, 255), batch=foreground)

cursor_hover = window.get_system_mouse_cursor(window.CURSOR_HAND)  # Hover cursor type
cursor_normal = window.get_system_mouse_cursor(window.CURSOR_DEFAULT)  # Normal cursor type
snake_instance = snake.Snake()  # Instance of class Snake
finished_runs = 0  # Counter for finished snake game
score_min = 0  # Lowest achieved score
score_max = 0  # Highest achieved score
score_avg = 0  # Average of achieved scores
score_list = []  # List of achieved score


@window.event
def on_draw():
    """
    Draw graphics to Menu window.

    Draw buttons background, its labels and standalone labels.

    :return: Nothing
    """
    global finished_runs
    global score_min
    global score_max
    global score_avg
    global score_list

    window.clear()
    score_label1.text = 'Last score: {}, Runs: {}'.format(snake_instance.final_score, finished_runs)
    score_label2.text = 'Score: min={}, max={}, avg={:.2f}'.format(score_min, score_max, score_avg)
    background.draw()  # Button backgrounds
    foreground.draw()  # Text


@window.event
def on_mouse_motion(x, y, dx, dy):
    """
    Is called, when mouse is moving.

    Used for checking, if mouse is hovering over the buttons.

    :param x: X axis position of the cursos.
    :param y: Y axis position of the cursos.
    :param dx: Distance traveled by cursor in X axis. Not used here.
    :param dy: Distance traveled by cursor in Y axis. Not used here.
    :return: Nothing
    """
    global playS
    global play_color
    global play_color_hover
    global play_position
    global play_size
    global aiS
    global ai_color
    global ai_color_hover
    global ai_position
    global ai_size
    global cursor_hover
    global cursor_normal
    global window

    if (play_position[0] <= x <= play_position[0] + play_size[0] and
            play_position[1] <= y <= play_position[1] + play_size[1]):
        playS.color = play_color_hover
        window.set_mouse_cursor(cursor_hover)
    else:
        playS.color = play_color
        window.set_mouse_cursor(cursor_normal)
    if (ai_position[0] <= x <= ai_position[0] + ai_size[0] and
            ai_position[1] <= y <= ai_position[1] + ai_size[1]):
        aiS.color = ai_color_hover
        window.set_mouse_cursor(cursor_hover)
    else:
        aiS.color = ai_color
        window.set_mouse_cursor(cursor_normal)


@window.event
def on_mouse_release(x, y, button, modifiers):
    """
    Is called, when mouse button is released.

    Checks, if mouse is hovering over the buttons and calls other functions depending on button, that is clicked.

    :param x: X axis position of the cursos.
    :param y: Y axis position of the cursos.
    :param button: Mouse button, that is being released. Not used here.
    :param modifiers: Information, if some of the special keys is being hold at the time of release.
                      (CTRL, SHIFT...) Not used here.
    :return: Nothing
    """
    global snake_instance

    if (play_position[0] <= x <= play_position[0] + play_size[0] and
            play_position[1] <= y <= play_position[1] + play_size[1]):
        snake_instance.play_style = 1
        snake_instance.run()
    if (ai_position[0] <= x <= ai_position[0] + ai_size[0] and
            ai_position[1] <= y <= ai_position[1] + ai_size[1]):
        snake_instance.play_style = 2
        snake_instance.run()

def test_run():
    """
    Used for forcing AI to play some amount of games.

    Used for fast testing for large number of playthroughs

    :return: Nothing
    """
    global finished_runs
    global score_min
    global score_max
    global score_avg
    global score_list

    if snake_instance.active == 0 and finished_runs < 101:
        if finished_runs > 0:
            score_list.append(snake_instance.final_score)
        if finished_runs == 1:
            score_min = score_avg = score_max = snake_instance.final_score
        else:
            if snake_instance.final_score > score_max:
                score_max = snake_instance.final_score
            if snake_instance.final_score < score_min:
                score_min = snake_instance.final_score
            if finished_runs > 0:
                score_avg = sum(score_list) / finished_runs
        print('run {0}.: min={1}, max={2}, avg={3}'.format(finished_runs, score_min, score_max, score_avg))
        snake_instance.play_style = 2
        snake_instance.run()
        finished_runs += 1

@window.event
def update(self):
    """
    Periodically updates parts of the program, that needs to be updated.

    Calls update function inside of the Snake class (updates movement, spawns, path calculating etc.).
    Update achieved score labels

    :param self: Itself. Can be used to access some variables etc. Not used here.
    :return: Nothing
    """
    global finished_runs
    global score_min
    global score_max
    global score_avg
    global score_list

    snake_instance.update(snake_instance)
    test_run()


pg.clock.schedule_interval(update, 1 / snake_instance.game_speed)  # Sets function, which is periodically called.
pg.app.run()  # Starts pyglet application
