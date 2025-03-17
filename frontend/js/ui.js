/**
 * UI Manager Class - Handles UI elements and interactions
 */
class UiManager {
    constructor() {
        // Game mode elements
        this.twoPlayerBtn = document.getElementById('two-player-btn');
        this.aiBtn = document.getElementById('ai-btn');
        
        // Control buttons
        this.newGameBtn = document.getElementById('new-game-btn');
        this.resetBtn = document.getElementById('reset-btn');
        
        // Zoom controls
        this.zoomInBtn = document.getElementById('zoom-in');
        this.zoomOutBtn = document.getElementById('zoom-out');
        
        // Status and info elements
        this.statusElement = document.getElementById('status');
        this.positionText = document.getElementById('position-text');
        this.moveHistoryList = document.getElementById('move-history');
        
        // Game state
        this.currentMode = 'two_player';
        this.moveHistory = [];
    }
    
    /**
     * Set up event listeners for UI elements
     */
    setupEventListeners(callbacks) {
        // Mode selection
        this.twoPlayerBtn.addEventListener('click', () => {
            this.setGameMode('two_player');
            if (callbacks.onModeChange) {
                callbacks.onModeChange('two_player');
            }
        });
        
        this.aiBtn.addEventListener('click', () => {
            this.setGameMode('ai');
            if (callbacks.onModeChange) {
                callbacks.onModeChange('ai');
            }
        });
        
        // Game controls
        this.newGameBtn.addEventListener('click', () => {
            if (callbacks.onNewGame) {
                callbacks.onNewGame();
            }
        });
        
        this.resetBtn.addEventListener('click', () => {
            if (callbacks.onResetGame) {
                callbacks.onResetGame();
            }
        });
        
        // Zoom controls
        this.zoomInBtn.addEventListener('click', () => {
            if (callbacks.onZoomIn) {
                callbacks.onZoomIn();
            }
        });
        
        this.zoomOutBtn.addEventListener('click', () => {
            if (callbacks.onZoomOut) {
                callbacks.onZoomOut();
            }
        });
    }
    
    /**
     * Set the current game mode and update UI accordingly
     * @param {string} mode - Game mode ('two_player' or 'ai')
     */
    setGameMode(mode) {
        this.currentMode = mode;
        
        // Update UI to reflect selected mode
        if (mode === 'two_player') {
            this.twoPlayerBtn.classList.add('active');
            this.aiBtn.classList.remove('active');
        } else {
            this.twoPlayerBtn.classList.remove('active');
            this.aiBtn.classList.add('active');
        }
        
        this.updateStatus(`Mode changed to ${mode}`);
    }
    
    /**
     * Update the status message
     * @param {string} message - Status message to display
     */
    updateStatus(message) {
        this.statusElement.textContent = message;
    }
    
    /**
     * Update the position text
     * @param {string} position - Current position text
     */
    updatePosition(position) {
        this.positionText.textContent = position;
    }
    
    /**
     * Add a move to the move history
     * @param {string} move - Move notation
     */
    addMoveToHistory(move) {
        this.moveHistory.push(move);
        this.updateMoveHistory();
    }
    
    /**
     * Clear the move history
     */
    clearMoveHistory() {
        this.moveHistory = [];
        this.updateMoveHistory();
    }
    
    /**
     * Update the move history display
     */
    updateMoveHistory() {
        // Clear the current list
        while (this.moveHistoryList.firstChild) {
            this.moveHistoryList.removeChild(this.moveHistoryList.firstChild);
        }
        
        // Add all moves to the list
        this.moveHistory.forEach((move, index) => {
            const listItem = document.createElement('li');
            listItem.textContent = `${index + 1}. ${move}`;
            this.moveHistoryList.appendChild(listItem);
        });
        
        // Scroll to the bottom of the list
        this.moveHistoryList.scrollTop = this.moveHistoryList.scrollHeight;
    }
    
    /**
     * Disable all UI controls
     */
    disableControls() {
        this.twoPlayerBtn.disabled = true;
        this.aiBtn.disabled = true;
        this.newGameBtn.disabled = true;
        this.resetBtn.disabled = true;
    }
    
    /**
     * Enable all UI controls
     */
    enableControls() {
        this.twoPlayerBtn.disabled = false;
        this.aiBtn.disabled = false;
        this.newGameBtn.disabled = false;
        this.resetBtn.disabled = false;
    }
}

// Export the UiManager class
export default UiManager;