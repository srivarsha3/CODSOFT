import math

# Initialize the board
board = [' ' for _ in range(9)]

def print_board():
    print()
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')
    print()

def is_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    return any(all(board[i] == player for i in condition) for condition in win_conditions)

def is_draw(board):
    return ' ' not in board

def get_available_moves(board):
    return [i for i, spot in enumerate(board) if spot == ' ']

def minimax(board, is_maximizing):
    if is_winner(board, 'O'):
        return 1
    elif is_winner(board, 'X'):
        return -1
    elif is_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(board):
            board[move] = 'O'
            score = minimax(board, False)
            board[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves(board):
            board[move] = 'X'
            score = minimax(board, True)
            board[move] = ' '
            best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -math.inf
    best_move = None
    for move in get_available_moves(board):
        board[move] = 'O'
        score = minimax(board, False)
        board[move] = ' '
        if score > best_score:
            best_score = score
            best_move = move
    board[best_move] = 'O'

def player_move():
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            if board[move] == ' ':
                board[move] = 'X'
                break
            else:
                print("Spot already taken.")
        except (ValueError, IndexError):
            print("Invalid move. Please choose a number between 1 and 9.")

def play_game():
    print("Welcome to Tic-Tac-Toe! You are 'X' and AI is 'O'")
    print_board()
    while True:
        player_move()
        print_board()
        if is_winner(board, 'X'):
            print("You win! 🎉")
            break
        if is_draw(board):
            print("It's a draw! 🤝")
            break

        print("AI's turn...")
        ai_move()
        print_board()
        if is_winner(board, 'O'):
            print("AI wins! 🤖")
            break
        if is_draw(board):
            print("It's a draw! 🤝")
            break

# Start the game
play_game()
1
