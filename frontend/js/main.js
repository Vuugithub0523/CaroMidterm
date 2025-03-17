/**
 * Main application script - Initializes the game and connects components
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize components
    const board = new GameBoard('board');
    const ui = new UiManager();
    
    // Game state variables
    let currentPlayer = 1;
    let gameOver = false;
    let winner = null;
    let gameMode = 'two_player';
    
    /**
     * Initialize a new game
     */
    async function initGame() {
        try {
            ui.updateStatus('Creating new game...');
            ui.disableControls();
            
            // Create new game via API
            const gameData = await apiService.createNewGame(board.size, gameMode);
            
            // Update board with initial state
            board.updateGrid(gameData.board.grid, gameData.board.lastMove);
            
            // Update game state
            currentPlayer = gameData.currentPlayer;
            gameOver = gameData.gameOver;
            winner = gameData.winner;
            
            // Update UI
            updateGameStatus();
            ui.clearMoveHistory();
            ui.enableControls();
            
            // Center view on the middle of the board
            const centerPos = Math.floor(board.size / 2);
            board.centerOnCell(centerPos, centerPos);
        } catch (error) {
            ui.updateStatus(`Error: ${error.message}`);
            ui.enableControls();
        }
    }
    
    /**
     * Make a move at the specified position
     */
    async function makeMove(row, col) {
        if (gameOver || board.grid[row][col] !== 0) {
            return;
        }
        
        try {
            ui.updateStatus('Making move...');
            ui.disableControls();
            
            // Send move to server
            const gameData = await apiService.makeMove(row, col);
            
            // Update board
            board.updateGrid(gameData.board.grid, gameData.board.lastMove);
            
            // Update game state
            currentPlayer = gameData.currentPlayer;
            gameOver = gameData.gameOver;
            winner = gameData.winner;
            
            // Add move to history
            const playerMark = board.grid[row][col] === 1 ? 'X' : 'O';
            ui.addMoveToHistory(`${playerMark} at (${row}, ${col})`);
            
            // Update UI
            updateGameStatus();
            ui.enableControls();
        } catch (error) {
            ui.updateStatus(`Error: ${error.message}`);
            ui.enableControls();
        }
    }
    
    /**
     * Reset the current game
     */
    async function resetGame() {
        try {
            ui.updateStatus('Resetting game...');
            ui.disableControls();
            
            // Reset game via API
            const gameData = await apiService.resetGame(gameMode);
            
            // Update board
            board.updateGrid(gameData.board.grid, gameData.board.lastMove);
            
            // Update game state
            currentPlayer = gameData.currentPlayer;
            gameOver = gameData.gameOver;
            winner = gameData.winner;
            
            // Update UI
            updateGameStatus();
            ui.clearMoveHistory();
            ui.enableControls();
        } catch (error) {
            ui.updateStatus(`Error: ${error.message}`);
            ui.enableControls();
        }
    }
    
    /**
     * Update game status display
     */
    function updateGameStatus() {
        if (gameOver) {
            if (winner) {
                const winnerText = winner === 1 ? 'X' : 'O';
                ui.updateStatus(`Game over! Player ${winnerText} wins!`);
            } else {
                ui.updateStatus('Game over! It\'s a draw!');
            }
        } else {
            const playerText = currentPlayer === 1 ? 'X' : 'O';
            ui.updateStatus(`Player ${playerText}'s turn`);
        }
    }
    
    /**
     * Change game mode
     */
    async function changeGameMode(mode) {
        gameMode = mode;
        
        // If there's an active game, reset it with the new mode
        if (apiService.gameId) {
            try {
                const gameData = await apiService.resetGame(mode);
                
                // Update board
                board.updateGrid(gameData.board.grid, gameData.board.lastMove);
                
                // Update game state
                currentPlayer = gameData.currentPlayer;
                gameOver = gameData.gameOver;
                winner = gameData.winner;
                
                // Update UI
                updateGameStatus();
                ui.clearMoveHistory();
            } catch (error) {
                ui.updateStatus(`Error changing mode: ${error.message}`);
            }
        }
    }
    
    // Set up board event handlers
    board.onCellClick = (row, col) => {
        if (!gameOver && !board.grid[row][col]) {
            makeMove(row, col);
        }
    };
    
    board.updatePositionIndicator = (row, col) => {
        ui.updatePosition(`Position: ${row}, ${col}`);
    };
    
    // Set up UI event listeners
    ui.setupEventListeners({
        onNewGame: initGame,
        onResetGame: resetGame,
        onModeChange: changeGameMode,
        onZoomIn: () => board.zoomIn(),
        onZoomOut: () => board.zoomOut()
    });
    
    // Initialize the game
    initGame();
});