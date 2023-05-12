"""

File:   favorite_things.py
Author:  ALIASGER TAIYEBI
Date:    11/5/2021
Section: 43
E-mail:  mz83097@UMBC.EDU
Description:
  this program displays allows you to play a game somewhat similar to snakes and ladders and then displays your final score

Game name:  BORED GAME
"""

import random

GRID_WIDTH = 8
GRID_HEIGHT = 3
DICE_SIDES = 6


def generate_random_map(length, the_seed=0):
    """
        :param length - the length of the map
        :param the_seed - the seed of the map
        :return: a randomly generated map based on a specific seed, and length.
    """
    if the_seed:
        random.seed(the_seed)
    map_list = []
    for _ in range(length - 2):
        random_points = random.randint(1, 100)
        random_position = random.randint(0, length - 1)
        map_list.append(random.choices(
            ['nop', f'add {random_points}', f'sub {random_points}', f'mul {random_points}', f'jmp {random_position}',
             'hlt'], weights=[5, 2, 2, 2, 3, 1], k=1)[0])

    return ['nop'] + map_list + ['hlt']


def make_grid(table_size):
    """
    :param table_size: this needs to be the length of the map
    :return: returns a display grid that you can then modify with fill_grid_square (it's a 2d-grid of characters)
    """
    floating_square_root = table_size ** (1 / 2)

    int_square_root = int(floating_square_root) + (1 if floating_square_root % 1 else 0)
    table_height = int_square_root
    if int_square_root * (int_square_root - 1) >= table_size:
        table_height -= 1

    the_display_grid = [[' ' if j % GRID_WIDTH else '*' for j in range(GRID_WIDTH * int_square_root + 1)]
                        if i % GRID_HEIGHT else ['*' for j in range(GRID_WIDTH * int_square_root + 1)]
                        for i in range(table_height * GRID_HEIGHT + 1)]
    return the_display_grid


def fill_grid_square(display_grid, size, index, message):
    """
    :param display_grid:  the grid that was made from make_grid
    :param size:  this needs to be the length of the total map, otherwise you may not be able to place things correctly.
    :param index: the index of the position where you want to display the message
    :param message: the message to display in the square at position index, separated by line returns.
    """
    floating_square_root = size ** (1 / 2)
    int_square_root = int(floating_square_root) + (1 if floating_square_root % 1 else 0)
    table_row = index // int_square_root
    table_col = index % int_square_root

    if table_row % 2 == 0:
        column_start = GRID_WIDTH * table_col
    else:
        column_start = GRID_WIDTH * (int_square_root - table_col - 1)

    for r, message_line in enumerate(message.split('\n')):
        for k, c in enumerate(message_line):
            display_grid[GRID_HEIGHT * table_row + 1 + r][column_start + 1 + k] = c


def roll_dice():
    """
        Call this function once per turn.

        :return: returns the dice roll
    """
    return random.randint(1, DICE_SIDES)


def display_map(map):
    """

    :param map: takes in the map and spaces on the map
    :return: it displays a complete map according to the seed and size
    """

    for row in map:
        print(' '.join(row))


def math_command(command, value, score):
    """

    :param command: takes in the command at the position
    :param value: takes in the value along with the command
    :param score: takes in the current score
    :return: returns the score after executing the command
    this function is called when player lands on a block that requires addition subtraction or multiplaction
    """
    if command == 'mul':
        score = score * value
    if command == 'add':
        score = score + value
    if command == 'sub':
        score = score - value
    return score


def play_game(game_map):
    """

    :param game_map: takes in the game map and the blocks with commands
    :return: returns final score and position along with command
    this is the function where the game is played, it rolls dice and implements commands on the board until it lands on the hlt space
    """

    score = 0
    position = 0
    size = int(len(game_map))
    while game_map[position] != 'hlt':  ## executes as long as player doesnt land on hlt
        dice = roll_dice()
        print("Pos:", position, "Score:", score, ",instruction", game_map[position], "Rolled", dice)

        position += dice
        if position >= size:
            position -= size
        cmd = game_map[position]
        cmd = cmd.split()
        while cmd[0] == 'jmp':  ## executes loop as long as player lands on jmp function
            position = int(cmd[1])
            if position >= size:
                position -= size
            cmd = game_map[position]
            cmd = cmd.split()
            if len(cmd) != 2:
                cmd = "test"
        if len(cmd) == 2:
            score = math_command(cmd[0], int(cmd[1]), score)  # # executes if player lands on a space that requires to
            # do math. calls math function

    print("final pos:", position, "final score:", score, "instruction hlt")


if __name__ == '__main__':

    check = "yes"
    while check == "yes":
        size_seed = input("Board Size and Seed: ")
        size_seed = size_seed.split()
        size = int(size_seed[0])
        seed = int(size_seed[1])
        space = generate_random_map(size, seed)
        map = make_grid(size)
        for i in range(size):
            fill_grid_square(map, size, i, str(i) + "\n" + space[i])
        display_map(map)
        play_game(space)
        check = input("do u want to play again?????? ")
