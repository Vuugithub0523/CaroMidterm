/**
 * API Service for interacting with the backend
 */
class ApiService {
    constructor(baseUrl = 'http://localhost:5000/api') {
        this.baseUrl = baseUrl;
        this.gameId = null;
    }

    /**
     * Create a new game
     * @param {number} size - Board size
     * @param {string} mode - Game mode ('two_player' or 'ai')
     * @returns {Promise} - Game data
     */
    async createNewGame(size = 50, mode = 'two_player') {
        try {
            const response = await fetch(`${this.baseUrl}/new-game`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ size, mode })
            });
            
            if (!response.ok) {
                throw new Error('Failed to create new game');
            }
            
            const data = await response.json();
            this.gameId = data.gameId;
            return data;
        } catch (error) {
            console.error('Error creating new game:', error);
            throw error;
        }
    }

    /**
     * Get the current game state
     * @returns {Promise} - Game state data
     */
    async getGameState() {
        if (!this.gameId) {
            throw new Error('No active game');
        }
        
        try {
            const response = await fetch(`${this.baseUrl}/game/${this.gameId}`);
            
            if (!response.ok) {
                throw new Error('Failed to get game state');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting game state:', error);
            throw error;
        }
    }

    /**
     * Make a move in the game
     * @param {number} row - Row position
     * @param {number} col - Column position
     * @returns {Promise} - Updated game state
     */
    async makeMove(row, col) {
        if (!this.gameId) {
            throw new Error('No active game');
        }
        
        try {
            const response = await fetch(`${this.baseUrl}/game/${this.gameId}/move`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ row, col })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to make move');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error making move:', error);
            throw error;
        }
    }

    /**
     * Reset the current game
     * @param {string} mode - Game mode ('two_player' or 'ai')
     * @returns {Promise} - Reset game state
     */
    async resetGame(mode = null) {
        if (!this.gameId) {
            throw new Error('No active game');
        }try {
            const body = mode ? { mode } : {};
            const response = await fetch(`${this.baseUrl}/game/${this.gameId}/reset`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            });
            
            if (!response.ok) {
                throw new Error('Failed to reset game');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error resetting game:', error);
            throw error;
        }
    }

    /**
     * Request AI to make a move
     * @param {number} depth - AI search depth
     * @returns {Promise} - Updated game state
     */
    async requestAiMove(depth = 2) {
        if (!this.gameId) {
            throw new Error('No active game');
        }
        
        try {
            const response = await fetch(`${this.baseUrl}/game/${this.gameId}/ai-move`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ depth })
            });
            
            if (!response.ok) {
                throw new Error('Failed to get AI move');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting AI move:', error);
            throw error;
        }
    }
}

// Create and export API service
const apiService = new ApiService();