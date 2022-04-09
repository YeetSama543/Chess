#contains functionality of the game

from Board import Board
from Piece import *
from Game_Constants import *

turn = 0

def get_clicked_square(mouse_pos: tuple, board: Board) -> list:
    relative_x = mouse_pos[0] - board.pos[0]
    relative_y = mouse_pos[1] - board.pos[1]
    return [relative_y // SQUARE_SIZE, relative_x // SQUARE_SIZE] #x and y get flipped since first val represents the row# and second is col#

def clicked_on_board(mouse_pos: tuple, board: Board) -> bool:
    min_x = board.pos[0]
    max_x = board.pos[0] + BOARD_SIZE
    min_y = board.pos[1]
    max_y = board.pos[1] + BOARD_SIZE

    if mouse_pos[0] > min_x and mouse_pos[0] < max_x:
        if mouse_pos[1] > min_y and mouse_pos[1] < max_y:
            return True
    return False

def is_valid_square(square: list) -> bool:
    if square[0] > 7 or square[0] < 0 or square[1] > 7 or square[1] < 0:
        return False
    return True

#these move generating helper functions DO NOT account for special rules, such as check
def __generate_attacked_squares_pawn(pawn: Piece, position: list):
    attacked_squares = []
    #determine if the pawn has previously moved
    has_moved = True
    if pawn.get_color() == Color.WHITE and pawn.square[0] == 6:
        has_moved = False
    elif pawn.get_color() == Color.BLACK and pawn.square[0] == 1:
        has_moved = False

    #use color to determine candidate squares to add
    if pawn.get_color() == Color.WHITE:
        square_in_front = [pawn.square[0] - 1, pawn.square[1]]
        square_two_ahead = [pawn.square[0] - 2, pawn.square[1]]
        diag_left = [pawn.square[0] - 1, pawn.square[1] - 1]
        diag_right = [pawn.square[0] - 1, pawn.square[1] + 1]
    else: #pawn is black
        square_in_front = [pawn.square[0] + 1, pawn.square[1]]
        square_two_ahead = [pawn.square[0] + 2, pawn.square[1]]
        diag_left = [pawn.square[0] + 1, pawn.square[1] - 1]
        diag_right = [pawn.square[0] + 1, pawn.square[1] + 1]

    #check if pawn can move forward
    if is_valid_square(square_in_front) and not position[square_in_front[0]][square_in_front[1]]:
        attacked_squares.append(square_in_front)
        #now check if pawn can move forward twice
        if not has_moved and is_valid_square(square_two_ahead) and not position[square_two_ahead[0]][square_two_ahead[1]]:
            attacked_squares.append(square_two_ahead)
    #check if pawn can move diagonally
    if is_valid_square(diag_left) and position[diag_left[0]][diag_left[1]]:
        if position[diag_left[0]][diag_left[1]].get_color() != pawn.get_color():
            attacked_squares.append(diag_left)
    if is_valid_square(diag_right) and position[diag_right[0]][diag_right[1]]:
        if position[diag_right[0]][diag_right[1]].get_color() != pawn.get_color():
            attacked_squares.append(diag_right)

    #handle ep
    ep_square = ep(board)
    if ep_square:
        if ep_square in [diag_left, diag_right]:
            attacked_squares.append(ep_square)

    return attacked_squares

def __generate_attacked_squares_knight(knight: Piece, position: list):
    attacked_squares = []
    for i in [-2,2]:
        for j in [-1,1]:
            potential_square_vertical = [knight.square[0] + i, knight.square[1] + j]
            potential_square_horizontal = [knight.square[0] + j, knight.square[1] + i]

            if is_valid_square(potential_square_vertical):
                if not position[potential_square_vertical[0]][potential_square_vertical[1]]: #no piece on square
                    attacked_squares.append(potential_square_vertical)
                elif position[potential_square_vertical[0]][potential_square_vertical[1]].get_color() != knight.get_color():
                    attacked_squares.append(potential_square_vertical)
            
            if is_valid_square(potential_square_horizontal):
                if not position[potential_square_horizontal[0]][potential_square_horizontal[1]]: #no piece on square
                    attacked_squares.append(potential_square_horizontal)
                elif position[potential_square_horizontal[0]][potential_square_horizontal[1]].get_color() != knight.get_color():
                    attacked_squares.append(potential_square_horizontal)
    return attacked_squares
    
def __generate_attacked_squares_rook(rook: Piece, position: list):
    attacked_squares = []
    #up
    valid = True
    row = rook.square[0]
    col = rook.square[1]
    while valid:
        row -= 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != rook.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == rook.get_color():
                valid = False
        else:
            valid = False
    #down
    valid = True
    row = rook.square[0]
    col = rook.square[1]
    while valid:
        row += 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != rook.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == rook.get_color():
                valid = False
        else:
            valid = False
    #right
    valid = True
    row = rook.square[0]
    col = rook.square[1]
    while valid:
        col += 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != rook.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == rook.get_color():
                valid = False
        else:
            valid = False
    #left
    valid = True
    row = rook.square[0]
    col = rook.square[1]
    while valid:
        col -= 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != rook.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == rook.get_color():
                valid = False
        else:
            valid = False

    return attacked_squares

def __generate_attacked_squares_bishop(bishop: Piece, position: list):
    attacked_squares = []

    #down-right
    valid = True
    row = bishop.square[0]
    col = bishop.square[1]
    while valid:
        row += 1
        col += 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != bishop.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == bishop.get_color():
                valid = False
        else:
            valid = False
    #down-left
    valid = True
    row = bishop.square[0]
    col = bishop.square[1]
    while valid:
        row += 1
        col -= 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != bishop.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == bishop.get_color():
                valid = False
        else:
            valid = False
    #up-right
    valid = True
    row = bishop.square[0]
    col = bishop.square[1]
    while valid:
        row -= 1
        col += 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != bishop.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == bishop.get_color():
                valid = False
        else:
            valid = False
    #up-left
    valid = True
    row = bishop.square[0]
    col = bishop.square[1]
    while valid:
        row -= 1
        col -= 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != bishop.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == bishop.get_color():
                valid = False
        else:
            valid = False

    return attacked_squares

def __generate_attacked_squares_queen(queen: Piece, position: list):
    #queen is combination of rook and bishop
    #so generate moves for rook and bishop and return both together

    rook_squares = __generate_attacked_squares_rook(queen, position)
    bishop_squares = __generate_attacked_squares_bishop(queen, position)
    attacked_squares = rook_squares + bishop_squares

    return attacked_squares

def __generate_attacked_squares_king(king: Piece, position: list):
    attacked_squares = []
    #we include the original square of the king as part of the squares we check in the
    #following for loop, but since the king's color is equal to itself, the square won't be added

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            potential_square = [king.square[0] + i, king.square[1] + j]
            if is_valid_square(potential_square):
                if not position[potential_square[0]][potential_square[1]]: #no piece on square
                    attacked_squares.append(potential_square)
                elif position[potential_square[0]][potential_square[1]].get_color() != king.get_color():
                    attacked_squares.append(potential_square)

    return attacked_squares

def generate_attacked_squares(piece: Piece, board: Board):
    attacked_squares = []
    if piece.type == Type.BLACK_PAWN or piece.type == Type.WHITE_PAWN:
        attacked_squares = __generate_attacked_squares_pawn(piece,board)
    elif piece.type == Type.BLACK_ROOK or piece.type == Type.WHITE_ROOK:
        attacked_squares = __generate_attacked_squares_rook(piece,board)
    elif piece.type == Type.BLACK_KNIGHT or piece.type == Type.WHITE_KNIGHT:
        attacked_squares = __generate_attacked_squares_knight(piece,board)
    elif piece.type == Type.BLACK_BISHOP or piece.type == Type.WHITE_BISHOP:
        attacked_squares = __generate_attacked_squares_bishop(piece,board)
    elif piece.type == Type.BLACK_QUEEN or piece.type == Type.WHITE_QUEEN:
        attacked_squares = __generate_attacked_squares_queen(piece,board)
    elif piece.type == Type.BLACK_KING or piece.type == Type.WHITE_KING:
        attacked_squares = __generate_attacked_squares_king(piece,board)
    ###Handle special rules here###
    
    ###############################
    return attacked_squares

def is_check(position: list) -> bool:
    global turn
    danger_squares = []
    king_square = []

    for row in position:
        for col in row:
            piece_on_square = position[row][col]
            if piece_on_square: #there is a piece on square
                if piece_on_square.get_color().value != turn: #color of piece is diff from person making a move
                    danger_squares.append(generate_attacked_squares(piece_on_square, position))
                elif turn == 0 and piece_on_square.type == Type.WHITE_KING:
                    king_square = piece_on_square.square
                elif turn == 1 and piece_on_square.type == Type.BLACK_KING:
                    king_square = piece_on_square.square

    return king_square in danger_squares
                


def is_win(board: Board):
    pass

def change_turn(board: Board): #changes turn. Also resets clicked piece
    global turn
    turn += 1
    turn %= 2
    board.clicked_piece = None

def pawn_promotion(board: Board) -> bool: #returns promotion square if a pawn can promote, None otherwise
    for i in range(8):
        p1 = board.get_piece_on_square([0, i])
        p2 = board.get_piece_on_square([7, i])

        if p1:
            if p1.type == Type.WHITE_PAWN:
                return p1.square
        if p2:
            if p2.type == Type.BLACK_PAWN:
                return p2.square
    return None

def get_pawn_promotion_choice(board: Board) -> Type:
    valid_choice = False
    while not valid_choice:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    if turn == 0: #white
                        choice = Type.WHITE_QUEEN
                    else: #black
                        choice = Type.BLACK_QUEEN
                    
                    valid_choice = True
                if event.key == pg.K_n:
                    if turn == 0: #white
                        choice = Type.WHITE_KNIGHT
                    else: #black
                        choice = Type.BLACK_KNIGHT

                    valid_choice = True
                if event.key == pg.K_b:
                    if turn == 0: #white
                        choice = Type.WHITE_BISHOP
                    else: #black
                        choice = Type.BLACK_BISHOP

                    valid_choice = True
                if event.key == pg.K_r:
                    if turn == 0: #white
                        choice = Type.WHITE_ROOK
                    else: #black
                        choice = Type.BLACK_ROOK

                    valid_choice = True

    return choice

def promote(board: Board, square: list):
    choice = get_pawn_promotion_choice(board)

    board.remove_piece(board.get_piece_on_square(square))
    board.add(Piece(choice, square))

def ep(board: Board):
    global turn
    if board.moves != []:
        last_move = board.moves[-1]

        if turn == 0: #white to move, look for black pawn moves
            if last_move[0] == Type.BLACK_PAWN and last_move[1][0] == 3: #last pawn move is a candidate
                for move in reversed(board.moves[:-1]):
                    if move[0] == Type.BLACK_PAWN and move[1][1] == last_move[1][1]: #same black pawn that last moved
                        return None

                #pawn never moved before last turn, but is on a double moved square. Thus
                #pawn must have just double moved. so we construct the ep square and return
                ep_square = []
                ep_square.append(last_move[1][0] - 1)
                ep_square.append(last_move[1][1])
                
                return ep_square

            else: #no possible ep
                return None
        else: #black to move, look for white pawn moves
            if last_move[0] == Type.WHITE_PAWN and last_move[1][0] == 4: #last pawn move is a candidate
                for move in reversed(board.moves[:-1]):
                    if move[0] == Type.WHITE_PAWN and move[1][1] == last_move[1][1]: #same white pawn that last moved
                        return None

                #pawn never moved before last turn, but is on a double moved square. Thus
                #pawn must have just double moved. so we construct the ep square and return
                ep_square = []
                ep_square.append(last_move[1][0] + 1)
                ep_square.append(last_move[1][1])
                
                return ep_square

            else: #no possible ep
                return None
    else:
        return None
    