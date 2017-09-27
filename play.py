from snake import Board, Snake

moves = {'w': 3, 'a': 2, 's': 1, 'd': 0}


def print_board(board):
    for row in board:
        print(' '.join(map(str, row)))


def play():
    board = Board(Board.DEFAULT_WIDTH, Board.DEFAULT_HEIGHT)
    snake = Snake(board, Snake.DEFAULT_BODY, Snake.DEFAULT_GROW)
    last_move = 'd'

    while True:
        print_board(board.board_as_ints())
        move = input("Move with wasd: ")
        if len(move):
            last_move = move
        else:
            move = last_move
        board.move(moves[move])


if __name__ == '__main__':
    play()
