import random
import uuid
from flask import Blueprint, request, jsonify
from game.board import Board
from game.ai import AI
from game.utils import create_game_state

# Create blueprint
api_bp = Blueprint('api', __name__)

# Dictionary to store active games
active_games = {}

class Game:
    def __init__(self, size=50):
        self.board = Board(size)
        self.current_player = 1  # 1 for X, 2 for O
        self.game_over = False
        self.winner = None
        self.ai = AI(self.board)
        self.mode = 'two_player'  # 'two_player' or 'ai'

@api_bp.route('/new-game', methods=['POST'])
def new_game():
    """Create a new game."""
    data = request.json or {}
    size = data.get('size', 50)
    mode = data.get('mode', 'two_player')
    
    game_id = str(uuid.uuid4())
    game = Game(size)
    game.mode = mode
    
    active_games[game_id] = game
    
    return jsonify({
        "gameId": game_id,
        "mode": mode,
        **create_game_state(game_id, game.board, game.current_player, game.game_over, game.winner)
    })

@api_bp.route('/game/<game_id>', methods=['GET'])
def get_game(game_id):
    """Get the current state of a game."""
    game = active_games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    return jsonify(create_game_state(game_id, game.board, game.current_player, game.game_over, game.winner))

@api_bp.route('/game/<game_id>/move', methods=['POST'])
def make_move(game_id):
    """Make a move in a game."""
    game = active_games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    if game.game_over:
        return jsonify({"error": "Game is over"}), 400
    
    data = request.json
    row = data.get('row')
    col = data.get('col')
    
    # Validate input
    if row is None or col is None:
        return jsonify({"error": "Row and column must be provided"}), 400
    
    # Make the move
    if not game.board.place_mark(row, col, game.current_player):
        return jsonify({"error": "Invalid move"}), 400
    
    # Check for win
    # Check for win
    if game.board.check_win(row, col):
        game.game_over = True
        game.winner = game.current_player
    # Check for draw
    elif game.board.is_full():
        game.game_over = True
    else:
        # Switch player
        game.current_player = 3 - game.current_player
        
        # If AI mode and it's AI's turn, make AI move
        if game.mode == 'ai' and game.current_player == 2 and not game.game_over:
            ai_row, ai_col = game.ai.make_move(game.current_player, depth=2)
            
            # Check if AI won
            if game.board.check_win(ai_row, ai_col):
                game.game_over = True
                game.winner = game.current_player
            # Check for draw after AI move
            elif game.board.is_full():
                game.game_over = True
            else:
                # Switch back to player
                game.current_player = 3 - game.current_player
    
    return jsonify(create_game_state(game_id, game.board, game.current_player, game.game_over, game.winner))

@api_bp.route('/game/<game_id>/ai-move', methods=['POST'])
def ai_move(game_id):
    """Force AI to make a move (for testing or AI vs AI)."""
    game = active_games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    if game.game_over:
        return jsonify({"error": "Game is over"}), 400
    
    data = request.json or {}
    depth = data.get('depth', 2)
    
    # Make AI move
    move = game.ai.make_move(game.current_player, depth=depth)
    if not move:
        return jsonify({"error": "AI could not make a move"}), 400
    
    ai_row, ai_col = move
    
    # Check if AI won
    if game.board.check_win(ai_row, ai_col):
        game.game_over = True
        game.winner = game.current_player
    # Check for draw
    elif game.board.is_full():
        game.game_over = True
    else:
        # Switch player
        game.current_player = 3 - game.current_player
    
    return jsonify(create_game_state(game_id, game.board, game.current_player, game.game_over, game.winner))

@api_bp.route('/game/<game_id>/reset', methods=['POST'])
def reset_game(game_id):
    """Reset a game."""
    game = active_games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    game.board.reset()
    game.current_player = 1
    game.game_over = False
    game.winner = None
    
    # Update game mode if provided
    data = request.json or {}
    if 'mode' in data:
        game.mode = data['mode']
    
    return jsonify(create_game_state(game_id, game.board, game.current_player, game.game_over, game.winner))

@api_bp.route('/games', methods=['GET'])
def list_games():
    """List all active games."""
    games_list = []
    for game_id, game in active_games.items():
        games_list.append({
            "gameId": game_id,
            "mode": game.mode,
            "gameOver": game.game_over,
            "winner": game.winner
        })
    
    return jsonify({"games": games_list})

@api_bp.route('/game/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    """Delete a game."""
    if game_id in active_games:
        del active_games[game_id]
        return jsonify({"message": "Game deleted successfully"})
    else:
        return jsonify({"error": "Game not found"}), 404