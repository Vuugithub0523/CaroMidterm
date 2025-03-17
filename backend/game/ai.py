import random
from .board import Board

class AI:
    def __init__(self, board):
        self.board = board

    def make_move(self, player, depth=2):
        """Make an AI move using minimax algorithm."""
        move = self.find_best_move(player, depth)
        if move:
            row, col = move
            self.board.place_mark(row, col, player)
            return move
        return None

    def find_best_move(self, player, depth):
        """Find the best move using minimax."""
        candidate_moves = self.board.get_candidate_moves()
        
        if not candidate_moves:
            return None
            
        # Randomize candidates to add variety
        random.shuffle(candidate_moves)
        
        best_score = float('-inf')
        best_move = None
        
        for move in candidate_moves[:15]:  # Limit to 15 best candidates for performance
            row, col = move
            # Make move
            self.board.grid[row][col] = player
            
            # Calculate score
            score = self.minimax(depth-1, False, float('-inf'), float('inf'), player, 3-player, row, col)
            
            # Undo move
            self.board.grid[row][col] = 0
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

    def minimax(self, depth, is_maximizing, alpha, beta, max_player, min_player, row, col):
        """Minimax algorithm with alpha-beta pruning."""
        # Check for terminal state
        if self.board.check_win(row, col):
            return 100 if not is_maximizing else -100
            
        if self.board.is_full() or depth == 0:
            return self.evaluate_board(max_player, min_player)
        
        # Get limited set of candidate moves
        candidate_moves = self.board.get_candidate_moves()[:10]  # Limit candidates for performance
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in candidate_moves:
                row, col = move
                if self.board.grid[row][col] == 0:
                    self.board.grid[row][col] = max_player
                    eval = self.minimax(depth-1, False, alpha, beta, max_player, min_player, row, col)
                    self.board.grid[row][col] = 0
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for move in candidate_moves:
                row, col = move
                if self.board.grid[row][col] == 0:
                    self.board.grid[row][col] = min_player
                    eval = self.minimax(depth-1, True, alpha, beta, max_player, min_player, row, col)
                    self.board.grid[row][col] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def evaluate_board(self, player, opponent):
        """Heuristic evaluation of the board."""
        score = 0
        
        # Check for patterns in different directions
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)],  # Diagonal /
            [(1, -1), (-1, 1)]   # Diagonal \
        ]
        
        # Find areas with pieces and evaluate them
        non_zero_positions = [(i, j) for i in range(self.board.size) 
                             for j in range(self.board.size) if self.board.grid[i][j] != 0]
        
        # If too many positions, sample some
        if len(non_zero_positions) > 50:
            non_zero_positions = random.sample(non_zero_positions, 50)
        
        for i, j in non_zero_positions:
            current = self.board.grid[i][j]
            
            for dir_pair in directions:
                for dx, dy in dir_pair:
                    # Count consecutive pieces
                    consecutive = 0
                    empty_after = False
                    
                    for step in range(self.board.win_length):
                        nx, ny = i + dx*step, j + dy*step
                        if 0 <= nx < self.board.size and 0 <= ny < self.board.size:
                            if self.board.grid[nx][ny] == current:
                                consecutive += 1
                            elif self.board.grid[nx][ny] == 0:
                                empty_after = True
                                break
                            else:
                                break
                        else:
                            break
                    
                    # Score based on consecutive pieces and whether it's open-ended
                    if empty_after and consecutive > 0:
                        value = consecutive ** 2  # Square for exponential value
                        if current == player:
                            score += value
                        else:
                            score -= value * 1.5  # Weight opponent threats more
        
        # Add a small random factor to avoid deterministic play
        score += random.uniform(-0.5, 0.5)
        
        return score