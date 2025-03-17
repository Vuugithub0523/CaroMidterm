import numpy as np

class Board:
    def __init__(self, size=50):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.win_length = 5
        self.last_move = None

    def place_mark(self, row, col, player):
        """Place a mark on the board."""
        if row < 0 or row >= self.size or col < 0 or col >= self.size or self.grid[row][col] != 0:
            return False
            
        self.grid[row][col] = player
        self.last_move = (row, col)
        return True
        
    def check_win(self, row, col):
        """Check if the last move resulted in a win."""
        if row is None or col is None:
            return False
            
        player = self.grid[row][col]
        if player == 0:
            return False
            
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)],  # Diagonal /
            [(1, -1), (-1, 1)]   # Diagonal \
        ]
        
        for dir_pair in directions:
            count = 1
            
            # Check in both directions
            for dx, dy in dir_pair:
                r, c = row, col
                for _ in range(self.win_length - 1):
                    r, c = r + dx, c + dy
                    if 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == player:
                        count += 1
                    else:
                        break
            
            if count >= self.win_length:
                return True
        
        return False

    def is_full(self):
        """Check if the board is full."""
        return np.count_nonzero(self.grid) == self.size * self.size

    def reset(self):
        """Reset the board."""
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.last_move = None

    def get_empty_cells(self):
        """Get a list of all empty cells."""
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.grid[i][j] == 0]

    def get_candidate_moves(self):
        """Get empty cells that are adjacent to filled cells."""
        if np.count_nonzero(self.grid) == 0:
            # First move - return center area
            center = self.size // 2
            return [(i, j) for i in range(center-2, center+3) for j in range(center-2, center+3)]
            
        candidates = set()
        directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
        
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] != 0:  # If cell is filled
                    for dx, dy in directions:
                        for distance in range(1, 3):  # Look 1-2 cells away
                            nx, ny = i + dx*distance, j + dy*distance
                            if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[nx][ny] == 0:
                                candidates.add((nx, ny))
        
        return list(candidates) if candidates else self.get_empty_cells()[:10]  # Limit to 10 random cells if no candidates