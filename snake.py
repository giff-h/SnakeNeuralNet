from copy import deepcopy
from random import choice
from typing import List, Tuple


Position = Tuple[int, int]


class GameOver(Exception):
    pass


class Board:
    DEFAULT_WIDTH = 20
    DEFAULT_HEIGHT = 20

    def __init__(self, width: int, height: int):
        self.width = width  # x
        self.height = height  # y
        self.board = [[False] * self.width for _ in range(self.height)]  # board[y][x], origin top-left
        self.snake = None
        self.food = None

    def get_board(self) -> list:
        return deepcopy(self.board)

    def get_food(self):
        return self.food.pos

    def get_pos(self, pos: Position) -> bool:
        return self.board[pos[1]][pos[0]]

    def set_pos(self, pos: Position, value: bool):
        self.board[pos[1]][pos[0]] = value

    def set_snake(self, snake):
        self.snake = snake
        for pos in self.snake.body:
            self.set_pos(pos, True)  # pos is an (x, y) coord

    def board_as_ints(self, food: bool=True):
        board = [list(map(int, row)) for row in self.board]
        if food:
            food_pos = self.get_food()
            board[food_pos[1]][food_pos[0]] = 8
        return board

    def drop_snake_part(self, pos: Position):
        self.set_pos(pos, False)

    def move_snake(self, direction: int) -> bool:
        head = self.snake.head()
        if direction == 0:  # right
            head = (head[0] + 1, head[1])
        elif direction == 1:  # down
            head = (head[0], head[1] + 1)
        elif direction == 2:  # left
            head = (head[0] - 1, head[1])
        elif direction == 3:  # up
            head = (head[0], head[1] - 1)

        if head[0] < 0 or head[0] == self.width or head[1] < 0 or head[1] == self.height:
            raise GameOver("You ran off the edge")
        if self.snake.collided(head):
            raise GameOver("You ate yourself")

        return self.food.eaten(head)

    def create_food(self):
        self.food = Food(self)
        self.update_food()

    def update_food(self):
        choices = [(x, y) for x in range(self.width) for y in range(self.height) if not self.get_pos((x, y))]
        if len(choices):
            self.food.set_pos(choice(choices))
        else:
            raise GameOver("You win!")


class Snake:
    DEFAULT_BODY = [(i, 0) for i in reversed(range(5))]  # top row
    DEFAULT_GROW = 1

    def __init__(self, board: Board, body: List[Position], grow: int):
        self.board = board
        self.body = body
        self.grow = grow
        self.growth_left = 0
        self.board.set_snake(self)
        self.board.create_food()

    def head(self) -> Position:
        return self.body[0]

    def move(self, direction: int) -> bool:
        consumed = self.board.move_snake(direction)
        if consumed:
            self.growth_left += self.grow

        if self.growth_left:
            self.growth_left -= 1
        else:
            self.board.drop_snake_part(self.body.pop())

        if consumed:
            self.board.update_food()

        return consumed

    def move_to(self, pos: Position):
        self.body.insert(0, pos)

    def collided(self, pos: Position) -> bool:
        return pos in self.body and not self.consumed_tail(pos)

    def consumed_tail(self, pos: Position) -> bool:
        return self.body[-1] == pos and self.growth_left


class Food:
    def __init__(self, board: Board):
        self.board = board
        self.pos = None

    def set_pos(self, pos: Position):
        self.pos = pos

    def eaten(self, pos: Position) -> bool:
        return self.pos == pos
