def calculate_path(game_field, length, head, apple, width, height):
    """
    A* algorithm for calculating path from head of the snake to apple.

    Unocuppied squares are free to move.
    Cost for each movement (Up, Down, Left, Right) is 1.
    For body of the snake check, if it will stil be there, when snake will move to its location.
        yes: This square is the wall / blocked space.
        no: This square is free square / space.

    :param game_field: Numpy array of the game situation
    :param length: Length of the snake
    :param head: Position of the head of the snake
    :param apple: Position of the apple
    :param width: Columns in game (squares in one row).
    :param height: Rows in game (squares in one column).
    :return: List of direction (where to move square by square).
    """
    opened = []  # List of squares, that can lead to apple
    closed = []  # List of checked squares
    opened.append((head[0], head[1], -1, -1, 0, abs(head[0] - apple[0]) + abs(head[1] - apple[1]), 0))
    # shortcut     x        y        Px  Py  g  h                                                  f
    # index        0        1        2   3   4  5                                                  6
    # Px=X of parent square, Py=Y of parent square, g=move cost from start, h=move cost to finish, f=g+h
    while len(opened) > 0:  # If there are squares to check, check them.
        value = opened[0][4]
        index = 0
        for i in range(1, len(opened)):
            if opened[i][6] < value:
                value = opened[i][6]
                index = i
        sel = opened[index]  # Selected square
        opened.remove(opened[index])
        suc = []  # Successors - Squares next to selected square (Up, Down, Left, Right)
        check_overlap = (sel[4] + 1 > game_field[sel[0] - 1][sel[1]] != 0)  # Body will disappear before head arrival.
        """
        For each side check if its not out of bounds and if it will have unoccupied square on head arrival.
        If both are true, add that square to successors.
        """
        if sel[0] > 0:
            if game_field[sel[0] - 1][sel[1]] == 0 or game_field[sel[0] - 1][sel[1]] >= length + 1 or check_overlap:
                suc.append((sel[0] - 1, sel[1], sel[0], sel[1]))
        if sel[0] < width-1:
            if game_field[sel[0] + 1][sel[1]] == 0 or game_field[sel[0] + 1][sel[1]] == length + 1 or check_overlap:
                suc.append((sel[0] + 1, sel[1], sel[0], sel[1]))
        if sel[1] > 0:
            if game_field[sel[0]][sel[1] - 1] == 0 or game_field[sel[0]][sel[1] - 1] == length + 1 or check_overlap:
                suc.append((sel[0], sel[1] - 1, sel[0], sel[1]))
        if sel[1] < height-1:
            if game_field[sel[0]][sel[1] + 1] == 0 or game_field[sel[0]][sel[1] + 1] == length + 1 or check_overlap:
                suc.append((sel[0], sel[1] + 1, sel[0], sel[1]))
        for i in suc:  # For successors check following and decide if to end algorithm, keep or discard successor.
            if i[0] == apple[0] and i[1] == apple[1]:  # If successor is at the apple position, end algorithm.
                dir_list = [(i[0] - sel[0], i[1] - sel[1])]  # Declare list, which will be returned.
                if sel[2] != -1 or sel[3] != -1:  # Check if there is more than 2 square in path.
                    dir_list.append((sel[0]-sel[2], sel[1]-sel[3]))
                temp = (sel[2], sel[3])
                while temp != (-1, -1):  # Backtrack to start using parents.
                    for i in closed:
                        if temp[0] == i[0] and temp[1] == i[1]:
                            if i[2] != -1 or i[3] != -1:
                                dir_list.append((temp[0]-i[2], temp[1]-i[3]))
                            temp = (i[2], i[3])
                            break
                return dir_list  # Return completed list of directions.
            g = sel[4] + 1  # Set distance from start (last square+1).
            h = abs(i[0] - apple[0]) + abs(i[1] - apple[1])  # Calculate distance from apple.
            i = (i[0], i[1], i[2], i[3], g, h, g + h)  # Put all the info about successor in one tuple.
            skip_i = 0  # if square is found in one list, it will not be in second one, therefore skip.
            for j in range(0, len(opened)):
                if opened[j][0] == i[0] and opened[j][1] == i[1]:  # If same square with lower 'f', skip.
                    if opened[j][6] <= i[6]:
                        skip_i = 1
                    break
            if skip_i == 0:
                for j in range(0, len(closed)):
                    if closed[j][0] == i[0] and closed[j][1] == i[1]:  # If same square with lower 'f', skip.
                        if closed[j][6] <= i[6]:
                            skip_i = 1
                        break
            if skip_i == 0:  # If square was not in the list or had lower 'f' than one in the list, add to opened list.
                opened.append(i)
        closed.append(sel)  # Put checked square in closed list.
