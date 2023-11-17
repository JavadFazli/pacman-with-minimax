# Define the game board and the initial state of the game
import random


board = [
    "####################",
    "#..................#",
    "#.###.#.###.#......#",
    "#.#...#...#.#......#",
    "#.#.#.#.#.#.#......#",
    "#..................#",
    "#.#.#.#.#.#.#......#",
    "#.#...#...#.#......#",
    "#.###.#.###.#......#",
    "#..................#",
    "####################"
]
pacman_pos = (3, 1)
ghost_pos = [ (9, 9),(7,14)]

score = 0

# Define the game rules
def move_pacman(board, pacman_pos, move,real):
    # Move Pacman in the specified direction
    if move == "up":
        new_pos = (pacman_pos[0] - 1, pacman_pos[1])
    elif move == "down":
        new_pos = (pacman_pos[0] + 1, pacman_pos[1])
    elif move == "left":
        new_pos = (pacman_pos[0], pacman_pos[1] - 1)
    elif move == "right":
        new_pos = (pacman_pos[0], pacman_pos[1] + 1)

    if new_pos[0] < 0 or new_pos[0] >= len(board) or new_pos[1] < 0 or new_pos[1] >= len(board[0]):
        if real:
            return (pacman_pos[0],pacman_pos[1],0)
        return pacman_pos   
    # Check if the new position is valid
    if board[new_pos[0]][new_pos[1]] == "#":
        if real:
            return (pacman_pos[0],pacman_pos[1],0)
        return pacman_pos
    

    # Check if Pacman has eaten a dot
    if board[new_pos[0]][new_pos[1]] == ".":

        index = new_pos[1]
        if real:
            new_s = board[new_pos[0]][:index] + '_'+board[new_pos[0]][index+1:]
            board[new_pos[0]]=new_s
            return (new_pos[0],new_pos[1],9)
    if real:
        return (new_pos[0],new_pos[1],-1)
    return new_pos

def move_ghost_random(board, ghost_pos):
    # Move the ghosts randomly
    r=random.randint(0,3)
    if r==0 :
        new_pos = (ghost_pos[0] - 1, ghost_pos[1])
    elif r==1:
        new_pos = (ghost_pos[0] + 1, ghost_pos[1])
    elif r==2:
        new_pos = (ghost_pos[0], ghost_pos[1] - 1)
    elif r==3: 
        new_pos = (ghost_pos[0], ghost_pos[1] + 1)

    if new_pos[0] < 0 or new_pos[0] >= len(board) or new_pos[1] < 0 or new_pos[1] >= len(board[0]): 
        return ghost_pos
    if board[new_pos[0]][new_pos[1]] == "#":
        return ghost_pos
    return new_pos
def move_ghost(board, ghost_pos,move):
    # Move the ghosts randomly
    
    if move=='up':
        new_pos = (ghost_pos[0] - 1, ghost_pos[1])
    elif move=='down' :
        new_pos = (ghost_pos[0] + 1, ghost_pos[1])
    elif move=='left':
        new_pos = (ghost_pos[0], ghost_pos[1] - 1)
    elif move=='right': 
        new_pos = (ghost_pos[0], ghost_pos[1] + 1)

    if new_pos[0] < 0 or new_pos[0] >= len(board) or new_pos[1] < 0 or new_pos[1] >= len(board[0]): 
        return ghost_pos
    if board[new_pos[0]][new_pos[1]] == "#":
        return ghost_pos
    return new_pos

def is_game_over(board, pacman_pos, ghost_pos):
    # Check if the game is over
    if pacman_pos in ghost_pos:
        return 'L'
    if not any("." in row for row in board):
        return 'W'
    return 'F'

def utility(board, pacman_pos, ghost_pos,eaten,iteration): 
    s=0
    
    for row in board:
        for i in row:
            if i=='_':
                s+=10
    
    
    s=s-iteration+len(eaten)*10
    return s

def e_utility(board, pacman_pos, ghost_pos,eaten,iteration):
    # Evaluate the utility of the current state of the game
    s=0
    for row in board:
        for i in row:
            if i=='_':
                s+=10
    s=s-iteration
    md=100
    for ghost in ghost_pos:
        if abs(ghost[0]-pacman_pos[0])+abs(ghost[1]-pacman_pos[1])<md:
            md=abs(ghost[0]-pacman_pos[0])+abs(ghost[1]-pacman_pos[1])
    
    if md<4:
        ml=-(27-md)*4.5
    else:
        ml=-(27-md)*3
    ml=0
    return s+len(eaten)*10+ml

# Implement the Minimax algorithm
def minimax(board, pacman_pos, ghost_pos, depth, is_maximizing,eaten,iteration):
    # Evaluate the current state of the game
    if not is_game_over(board, pacman_pos, ghost_pos)=='F':
        return utility(board, pacman_pos, ghost_pos,eaten,iteration)
    if depth == 0:
        return e_utility(board, pacman_pos, ghost_pos,eaten,iteration)


    if is_maximizing==2:
        best_score = float("-inf")
        for move in ["up", "down", "left", "right"]:
            new_pacman_pos = move_pacman(board, pacman_pos, move,False)
            if board[new_pacman_pos[0]][new_pacman_pos[1]] == ".":
                if  not new_pacman_pos in eaten    :
                    eaten.append([new_pacman_pos,iteration])
                    # print('eaten:',eaten)
            score = minimax(board, new_pacman_pos, ghost_pos, depth - 1, 1,eaten.copy(),iteration+1)
            best_score = max(best_score, score)
        return best_score
    elif is_maximizing==1:
        best_score = float("inf")
        for move in ["up", "down", "left", "right"]:
            new_ghost_pos = move_ghost(board, ghost_pos[0],move)
            ghost_pos[0]=new_ghost_pos
            score = minimax(board, pacman_pos, ghost_pos, depth - 1, 0,eaten.copy(),iteration)
            best_score = min(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for move in ["up", "down", "left", "right"]:
            new_ghost_pos = move_ghost(board, ghost_pos[1],move)
            ghost_pos[1]=new_ghost_pos
            score = minimax(board, pacman_pos, ghost_pos, depth - 1, 2,eaten.copy(),iteration)
            best_score = min(best_score, score)
        return best_score

# Update the game state based on the moves of Pacman and the ghosts
score_now=0
iteration=0
game_over='F'
while game_over=='F':
    iteration+=1
    # Determine the best move for Pacman using the Minimax algorithm
    best_score = float("-inf")
    best_move = None
    for move in ["up", "down", "left", "right"]:
        new_pacman_pos = move_pacman(board, pacman_pos, move,False)
        score = minimax(board, new_pacman_pos, ghost_pos.copy(), 7, False,[],iteration)
        # print('move ',move,':',score)
        if score > best_score:
            best_score = score
            best_move = move
        if score == best_score:
            best_move = random.choice([best_move, move])

    # Move Pacman and the ghosts
    new_pacman = move_pacman(board, pacman_pos, best_move,True)
    pacman_pos=(new_pacman[0],new_pacman[1])

    score_now+=new_pacman[2]
    for i in range(len(ghost_pos)):
            new_ghost_pos = move_ghost_random(board, ghost_pos[i])
            ghost_pos[i]=new_ghost_pos
    # Check if the game is over
    game_over = is_game_over(board, pacman_pos, ghost_pos)
    for row in range(len(board)):
        for i in range(len(board[row])):
            if pacman_pos[0]==row and pacman_pos[1]==i and (row,i) in ghost_pos:
                print('X',end='')
            elif pacman_pos[0]==row and pacman_pos[1]==i:
                print('P',end='')
            elif (row,i) in ghost_pos:
                print('G',end='')
            else:
                print(board[row][i],end='')
        print(' ')
    print('pacman_pos:',pacman_pos)
    print('ghost_pos:',ghost_pos)
    print('best score:',best_score)
    print('iteration:',iteration)
    print('score_now:',score_now)
# Print the final score of the game
if game_over=='W':
    print("Final:", 'win')  
if game_over=='L':
    print("Final:", 'lose')




