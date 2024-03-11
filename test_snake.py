import astar
import numpy as np
import snake


def test_path1():
	arr = np.full((5, 5), 0)
	arr[0][2] = 1
	arr[4][2] = 2
	target = [(1, 0), (1, 0), (1, 0), (1, 0)]
	assert astar.calculate_path(arr, 1, (0, 2), (4, 2), 5, 5) == target


def test_path2():
	arr = np.full((5, 5), 0)
	arr[0][0] = 1
	arr[4][4] = 2
	path = astar.calculate_path(arr, 1, (0, 0), (4, 4), 5, 5)
	assert path.count((1, 0)) == 4
	assert path.count((0, 1)) == 4
	assert len(path) == 8


def test_path3():
	arr = np.full((5, 5), 0)
	arr[0][0] = 1
	arr[4][4] = 2
	path1 = astar.calculate_path(arr, 1, (0, 0), (4, 4), 5, 5)
	arr[0][0] = 2
	arr[4][4] = 1
	path2 = astar.calculate_path(arr, 1, (4, 4), (0, 0), 5, 5)
	x = y = 0
	for i in path1:
		x += i[0]
		y += i[1]
	for i in path2:
		x += i[0]
		y += i[1]
	assert x == y == 0


def test_snk1():
	snk = snake.Snake(play_style=2)
	snk.run()
	snk.apple = (0, 0)
	snk.head = (1, 1)
	snk.update(snk)
	snk.update(snk)
	snk.end_game()
	assert snk.length == 2
	assert snk.final_score == 1


def test_snk2():
	snk = snake.Snake(play_style=2)
	snk.run()
	snk.apple = (0, 0)
	snk.head = (0, 5)
	snk.update(snk)
	snk.update(snk)
	snk.end_game()
	assert snk.length == 1
	assert snk.head == (0, 3)
	assert snk.final_score == 0


def test_snk3():
	snk = snake.Snake(play_style=1)
	snk.run()
	snk.apple = (1, 1)
	snk.head = (0, 0)
	snk.direction = (-1, 0)
	snk.update(snk)
	assert snk.length == 1
	assert snk.head == (0, 0)
	assert snk.active == 0
	assert snk.final_score == 0
