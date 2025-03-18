import copy
import sys
import pygame
import random
import numpy as np
import subprocess  # Import subprocess module
from constants import *
from menuGame import create_menu_window 
# Function to run menuGame.py
def run_menu_game():
    subprocess.run(["python", "d:/Documents/Python/Python-Project/TicTacToe/python-tictactoe-ai-yt/menuGame.py"])

# --- PYGAME SETUP ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

# --- CLASSES ---

class Board:

    def __init__(self):
        self.squares = np.zeros((5, 5))  # 5x5 board
        self.empty_sqrs = self.squares  # [squares]
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''

        # vertical wins
        for col in range(5):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] == self.squares[3][col] == self.squares[4][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(5):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] == self.squares[row][3] == self.squares[row][4] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] == self.squares[3][3] == self.squares[4][4] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[4][0] == self.squares[3][1] == self.squares[2][2] == self.squares[1][3] == self.squares[0][4] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # no win yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(5):
            for col in range(5):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 25  # 5x5 = 25 cells

    def isempty(self):
        return self.marked_sqrs == 0
class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # --- RANDOM ---
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[idx]  # (row, col)

    # --- MINIMAX ---
    def minimax(self, board, maximizing, depth, max_depth=1, alpha=-float('inf'), beta=float('inf')):
        # Terminal case
        case = board.final_state()

        if case == 1:  # Player 1 (AI) wins
            return 1 + depth, None

        if case == 2:  # Player 2 (human) wins
            return -1 + depth, None

        if board.isfull() or max_depth <= depth:  # Draw or max depth reached
            
            return 0, None

        empty_sqrs = board.get_empty_sqrs()

        if maximizing:
            max_eval = -float('inf')
            best_move = None

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)  # AI (player 1) move
                eval, _ = self.minimax(temp_board, False, depth + 1, max_depth, alpha, beta)  # Minimize

                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break  # Prune branch

            return max_eval, best_move

        else:
            min_eval = float('inf')
            best_move = None

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)  # Player (human) move
                eval, _ = self.minimax(temp_board, True, depth + 1, max_depth, alpha, beta)  # Maximize

                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

                beta = min(beta, min_eval)
                if beta <= alpha:
                    break  # Prune branch

            return min_eval, best_move

    # --- MAIN EVAL ---
    def eval(self, main_board, max_depth):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False, depth=0, max_depth=max_depth)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        return move  # row, col

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   # 1-cross  # 2-circles
        self.gamemode = 'ai'  # pvp or ai
        self.running = True
        self.show_lines()
        self.turn_count = 0  # Tổng số lượt chơi
        self.player_moves = 0  # Số lượt đi của người chơi

    # --- DRAW METHODS ---
    def show_lines(self):
        screen.fill(BG_COLOR)
        # Draw vertical lines
        for i in range(1, 5):  # for a 5x5 grid, 4 vertical lines
            pygame.draw.line(screen, LINE_COLOR, (i * SQSIZE, 0), (i * SQSIZE, HEIGHT), LINE_WIDTH)
        # Draw horizontal lines
        for i in range(1, 5):  # for a 5x5 grid, 4 horizontal lines
            pygame.draw.line(screen, LINE_COLOR, (0, i * SQSIZE), (WIDTH, i * SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross (X)
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # draw circle (O)
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    # --- OTHER METHODS ---
    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1
        self.turn_count += 1  # Tổng số lượt chơi
        if self.player == 1:  # Nếu lượt đi của người chơi
            self.player_moves += 1  # Tăng số lượt đi của người chơi

    def change_gamemode(self, gamemode):
        self.gamemode = gamemode

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():
    # --- OBJECTS ---
    game = Game()
    board = game.board
    ai = game.ai

    create_menu_window(game)
    # --- MAINLOOP ---
    while True:

        # pygame events
        for event in pygame.event.get():

            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # keydown event
            if event.type == pygame.KEYDOWN:


                # r-restart the game
                if event.key == pygame.K_r:
                    game.reset()

                # Change AI difficulty
                if event.key == pygame.K_0:
                    ai.level = 0
                elif event.key == pygame.K_1:
                    ai.level = 1

            # click event to make a move
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row, col = pos[1] // SQSIZE, pos[0] // SQSIZE

                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

        # AI turn
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()

            # Cập nhật max_depth cho AI sau mỗi 2 lượt đi của người chơi
            max_depth = 4 + (game.player_moves // 2)

            print("max_depth: ", max_depth)
            row, col = ai.eval(board, max_depth)
            game.make_move(row, col)

            if game.isover():
                game.running = False

        pygame.display.update()

main()