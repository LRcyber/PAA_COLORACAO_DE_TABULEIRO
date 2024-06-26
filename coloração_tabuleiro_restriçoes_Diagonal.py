def is_valid(board, row, col, color, diag1_seq, diag2_seq):
    n = len(board)
    
    # Check for adjacent same color
    if row > 0 and board[row-1][col] == color:
        return False
    if col > 0 and board[row][col-1] == color:
        return False
    if row < n-1 and board[row+1][col] == color:
        return False
    if col < n-1 and board[row][col+1] == color:
        return False
    
    # Check diagonals
    if row == col:
        if diag1_seq[row] is not None and diag1_seq[row] != color:
            return False
    if row + col == n - 1:
        if diag2_seq[row] is not None and diag2_seq[row] != color:
            return False

    # Check 2x2 sub-boards
    sub_board_patterns = set()
    for i in range(n-1):
        for j in range(n-1):
            pattern = (board[i][j], board[i][j+1], board[i+1][j], board[i+1][j+1])
            if None not in pattern:
                sub_board_patterns.add(pattern)
    
    if row > 0 and col > 0:
        pattern = (board[row-1][col-1], board[row-1][col], board[row][col-1], color)
        if pattern in sub_board_patterns:
            return False
    if row > 0 and col < n-1:
        pattern = (board[row-1][col], board[row-1][col+1], color, board[row][col+1])
        if pattern in sub_board_patterns:
            return False
    if row < n-1 and col > 0:
        pattern = (board[row][col-1], color, board[row+1][col-1], board[row+1][col])
        if pattern in sub_board_patterns:
            return False
    if row < n-1 and col < n-1:
        pattern = (color, board[row][col+1], board[row+1][col], board[row+1][col+1])
        if pattern in sub_board_patterns:
            return False
    
    return True

def find_next_position(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                return (i, j)
    return None

def solve(board, colors, diag1_seq, diag2_seq):
    pos = find_next_position(board)
    if pos is None:
        return True  # board is fully filled
    
    row, col = pos
    for color in colors:
        if is_valid(board, row, col, color, diag1_seq, diag2_seq):
            board[row][col] = color
            
            # Update diagonals sequences if applicable
            diag1_temp, diag2_temp = diag1_seq[row], diag2_seq[row]
            if row == col:
                diag1_seq[row] = color
            if row + col == len(board) - 1:
                diag2_seq[row] = color

            # Ensure both diagonals have the same sequence
            if diag1_seq == diag2_seq:
                if solve(board, colors, diag1_seq, diag2_seq):
                    return True
            
            # Backtrack
            board[row][col] = None
            if row == col:
                diag1_seq[row] = diag1_temp
            if row + col == len(board) - 1:
                diag2_seq[row] = diag2_temp

    return False

def color_board():
    n = 7
    colors = ['A', 'L', 'V', 'P', 'C']
    board = [[None for _ in range(n)] for _ in range(n)]
    diag1_seq = [None] * n
    diag2_seq = [None] * n

    if solve(board, colors, diag1_seq, diag2_seq):
        for row in board:
            print(" ".join(row))
    else:
        print("No solution found")

# Call the function to solve the board
color_board()
