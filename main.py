def get_coords(n):
    x = n % 9
    y = int(n / 9)
    return (x,y)

def print_board(board):
    print(" ")
    for x in range(0,9):
        y = x * 9
        print(board[y:y+3],board[y+3:y+6],board[y+6:y+9])
        if x % 3 - 2 == 0:
            print(" ")

def get_horiz_at_x(x, board):
    result = []
    for i in range(0,9):
        result.append(board[x+i*9])
    return result
    
def get_vert_at_y(y,board):
    return list(board[y*9:y*9+9])
    
def get_box_at_n(n,board):
    x,y = get_coords(n)
    first_y = int(y/3) * 3
    first_x = int(x/3) * 3
    fr = get_vert_at_y(first_y,board)[first_x: first_x+3]
    first_y += 1
    sr = get_vert_at_y(first_y,board)[first_x: first_x+3]
    first_y += 1
    tr = get_vert_at_y(first_y,board)[first_x: first_x+3]
    return fr + sr + tr

def get_possibles(n,board):
    x,y = get_coords(n)
    horizset = get_horiz_at_x(x, board)
    vertset = get_vert_at_y(y,board)
    boxset = get_box_at_n(n,board)
    takens = set(horizset + vertset + boxset)
    result = set()
    for i in range(1,10):
        if str(i) not in takens:
            result.add(str(i))
    return result

def get_superposs(board):
    superposs = {}
    for n in range(0,len(board)):
        if board[n] == '0':
            superposs[n] = get_possibles(n,board)
    return superposs

def get_smallest_poss(superposs):
    lowscore = 9
    for i in superposs:
        if len(superposs[i]) < lowscore:
            lowscore = len(superposs[i])
            locations = [i]
        elif len(superposs[i]) == lowscore:
            locations.append(i)
    return (lowscore,locations)

def check_sudoku(board):
    if "0" in board:
        return False
    for i in range(0,9):
        yset = get_vert_at_y(i, board)
        xset = get_horiz_at_x(i, board)
        n = ((i % 3) * 3) + (int(i/3) * 27)
        boxset = get_box_at_n(n,board)
        if len(set(xset)) < 9 or len(set(yset)) < 9 or len(set(boxset)) < 9:
            return False
    return True

encountereds = []
def solve_sudoku(board):
    encountereds.append(board)
    if check_sudoku(board):
        return board
    else:
        superposs = get_superposs(board)
        lowscore,locations = get_smallest_poss(superposs)
        if lowscore == 0:
            return False
        for loc in range(0,81):
            if board[loc] == '0':
                for trie in superposs[loc]:
                    newboard = board[:loc] + trie + board[loc + 1:]
                    if newboard not in encountereds:
                        print(newboard)
                        if solve_sudoku(newboard):
                            return board

def possible(n,i,board):
    x,y = get_coords(n)
    xset = get_horiz_at_x(x, board)
    yset = get_vert_at_y(y, board)
    boxset = get_box_at_n(n,board)
    if i in xset + yset + boxset:
        return False
    else:
        return True


def solve2_sudoku():
    global board
    for n in range(81):
        if board[n] == '0':
            for i in range(1,10):
                if possible(n,str(i),board):
                    board = board[:n] + str(i) + board[n + 1:]
                    solve2_sudoku()
                    board = board[:n] + '0' + board[n + 1:]
            return
    print(board)

stuck = '453921670927345801001876423348152967719430058506798214132689540864203109075014382'

board = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
solution = solve_sudoku(board)
solvedboard = '652781934941532786738946215263174598195368427874295361529617843386459172417823659'
hardboard = '800000000003600000070090200050007000000045700000100030001000068008500010090000400'
stuck = '869732541523684970470091283956827104382945706740160839231479068608503017095218400'
