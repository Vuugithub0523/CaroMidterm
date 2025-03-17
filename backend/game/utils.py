def board_to_dict(board):
    """Convert board to dictionary for JSON response."""
    return {
        "grid": board.grid.tolist(),
        "size": board.size,
        "lastMove": board.last_move
    }

def create_game_state(game_id, board, current_player, game_over, winner):
    """Create a game state dictionary for JSON response."""
    return {
        "gameId": game_id,
        "board": board_to_dict(board),
        "currentPlayer": current_player,
        "gameOver": game_over,
        "winner": winner
    }