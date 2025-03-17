/**
 * Board Class - Handles rendering and interaction with the game board
 */
class GameBoard {
    constructor(canvasId, size = 50) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.size = size;
        this.cellSize = 20; // Default cell size in pixels
        this.viewportX = 0;
        this.viewportY = 0;
        this.grid = Array(size).fill().map(() => Array(size).fill(0));
        this.lastMove = null;
        this.highlighted = null;
        
        // Initialize canvas
        this.resizeCanvas();
        this.render();
        
        // Set up event listeners
        this.setupEventListeners();
    }
    
    /**
     * Resize the canvas to fit the board size
     */
    resizeCanvas() {
        const totalSize = this.size * this.cellSize;
        this.canvas.width = Math.min(totalSize, this.canvas.parentElement.clientWidth);
        this.canvas.height = Math.min(totalSize, 500);
        this.render();
    }
    
    /**
     * Set up mouse and touch event listeners
     */
    setupEventListeners() {
        // Mouse click handler
        this.canvas.addEventListener('click', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const scaleX = this.canvas.width / rect.width;
            const scaleY = this.canvas.height / rect.height;
            
            const canvasX = (e.clientX - rect.left) * scaleX;
            const canvasY = (e.clientY - rect.top) * scaleY;
            
            const gridX = Math.floor((canvasX + this.viewportX) / this.cellSize);
            const gridY = Math.floor((canvasY + this.viewportY) / this.cellSize);
            
            if (gridX >= 0 && gridX < this.size && gridY >= 0 && gridY < this.size) {
                this.onCellClick(gridY, gridX); // row, col format
            }
        });
        
        // Mouse move for position indication
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const scaleX = this.canvas.width / rect.width;
            const scaleY = this.canvas.height / rect.height;
            
            const canvasX = (e.clientX - rect.left) * scaleX;
            const canvasY = (e.clientY - rect.top) * scaleY;
            
            const gridX = Math.floor((canvasX + this.viewportX) / this.cellSize);
            const gridY = Math.floor((canvasY + this.viewportY) / this.cellSize);
            
            if (gridX >= 0 && gridX < this.size && gridY >= 0 && gridY < this.size) {
                this.updatePositionIndicator(gridY, gridX);
                this.highlighted = { row: gridY, col: gridX };
                this.render();
            }
        });
        
        // Mouse leave to clear highlight
        this.canvas.addEventListener('mouseleave', () => {
            this.highlighted = null;
            this.render();
        });
        
        // Drag to scroll the board
        let isDragging = false;
        let lastX, lastY;
        
        this.canvas.addEventListener('mousedown', (e) => {
            isDragging = true;
            lastX = e.clientX;
            lastY = e.clientY;
            this.canvas.style.cursor = 'grabbing';
        });
        
        window.addEventListener('mouseup', () => {
            isDragging = false;
            this.canvas.style.cursor = 'pointer';
        });
        
        window.addEventListener('mousemove', (e) => {
            if (isDragging) {
                const dx = e.clientX - lastX;
                const dy = e.clientY - lastY;
                lastX = e.clientX;
                lastY = e.clientY;
                
                this.viewportX = Math.max(0, Math.min(this.viewportX - dx, this.size * this.cellSize - this.canvas.width));
                this.viewportY = Math.max(0, Math.min(this.viewportY - dy, this.size * this.cellSize - this.canvas.height));
                
                this.render();
            }
        });
        
        // Handle window resize
        window.addEventListener('resize', () => {
            this.resizeCanvas();
        });
    }
    
    /**
     * Handle cell click - to be overridden by main.js
     */
    onCellClick(row, col) {
        console.log(`Cell clicked at row: ${row}, col: ${col}`);
        // This will be overridden
    }
    
    /**
     * Update position indicator - to be overridden by main.js
     */
    updatePositionIndicator(row, col) {
        console.log(`Position: ${row}, ${col}`);
        // This will be overridden
    }
    
    /**
     * Update the board grid with new data
     */
    updateGrid(grid, lastMove = null) {
        this.grid = grid;
        this.lastMove = lastMove;
        this.render();
    }
    
    /**
     * Zoom in the board view
     */
    zoomIn() {
        if (this.cellSize < 40) {
            const centerX = this.viewportX + this.canvas.width / 2;
            const centerY = this.viewportY + this.canvas.height / 2;
            
            this.cellSize += 5;
            
            this.viewportX = centerX - (this.canvas.width / 2 / this.cellSize) * this.cellSize;
            this.viewportY = centerY - (this.canvas.height / 2 / this.cellSize) * this.cellSize;
            
            this.viewportX = Math.max(0, Math.min(this.viewportX, this.size * this.cellSize - this.canvas.width));
            this.viewportY = Math.max(0, Math.min(this.viewportY, this.size * this.cellSize - this.canvas.height));
            
            this.render();
        }
    }
    
    /**
     * Zoom out the board view
     */
    zoomOut() {
        if (this.cellSize > 10) {
            const centerX = this.viewportX + this.canvas.width / 2;
            const centerY = this.viewportY + this.canvas.height / 2;
            
            this.cellSize -= 5;
            
            this.viewportX = centerX - (this.canvas.width / 2 / this.cellSize) * this.cellSize;
            this.viewportY = centerY - (this.canvas.height / 2 / this.cellSize) * this.cellSize;
            
            this.viewportX = Math.max(0, Math.min(this.viewportX, this.size * this.cellSize - this.canvas.width));
            this.viewportY = Math.max(0, Math.min(this.viewportY, this.size * this.cellSize - this.canvas.height));
            
            this.render();
        }
    }
    
    /**
     * Center the view on a specific cell
     */
    centerOnCell(row, col) {
        this.viewportX = (col * this.cellSize) - (this.canvas.width / 2) + (this.cellSize / 2);
        this.viewportY = (row * this.cellSize) - (this.canvas.height / 2) + (this.cellSize / 2);
        
        this.viewportX = Math.max(0, Math.min(this.viewportX, this.size * this.cellSize - this.canvas.width));
        this.viewportY = Math.max(0, Math.min(this.viewportY, this.size * this.cellSize - this.canvas.height));
        
        this.render();
    }
    
    /**
     * Render the game board
     */
    render() {
        // Clear canvas
        this.ctx.fillStyle = '#ffffff';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Calculate visible range
        const startCol = Math.floor(this.viewportX / this.cellSize);
        const endCol = Math.min(startCol + Math.ceil(this.canvas.width / this.cellSize) + 1, this.size);
        const startRow = Math.floor(this.viewportY / this.cellSize);
        const endRow = Math.min(startRow + Math.ceil(this.canvas.height / this.cellSize) + 1, this.size);
        
        // Draw grid lines
        this.ctx.strokeStyle = '#ccc';
        this.ctx.lineWidth = 1;
        
        // Draw columns
        for (let i = startCol; i <= endCol; i++) {
            const x = (i * this.cellSize) - this.viewportX;
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
        
        // Draw rows
        for (let i = startRow; i <= endRow; i++) {
            const y = (i * this.cellSize) - this.viewportY;
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }
        
        // Draw pieces
        for (let row = startRow; row < endRow; row++) {
            for (let col = startCol; col < endCol; col++) {
                const x = (col * this.cellSize) - this.viewportX;
                const y = (row * this.cellSize) - this.viewportY;
                
                // Draw highlighted cell
                if (this.highlighted && this.highlighted.row === row && this.highlighted.col === col) {
                    this.ctx.fillStyle = 'rgba(173, 216, 230, 0.5)';
                    this.ctx.fillRect(x, y, this.cellSize, this.cellSize);
                }
                
                // Draw piece
                if (this.grid[row][col] === 1) {
                    // Draw X (Player 1)
                    this.ctx.strokeStyle = '#3498db';
                    this.ctx.lineWidth = 2;
                    const padding = this.cellSize * 0.2;
                    this.ctx.beginPath();
                    this.ctx.moveTo(x + padding, y + padding);
                    this.ctx.lineTo(x + this.cellSize - padding, y + this.cellSize - padding);
                    this.ctx.moveTo(x + this.cellSize - padding, y + padding);
                    this.ctx.lineTo(x + padding, y + this.cellSize - padding);
                    this.ctx.stroke();
                } else if (this.grid[row][col] === 2) {
                    // Draw O (Player 2)
                    this.ctx.strokeStyle = '#e74c3c';
                    this.ctx.lineWidth = 2;
                    const radius = this.cellSize * 0.4;
                    this.ctx.beginPath();
                    this.ctx.arc(x + this.cellSize / 2, y + this.cellSize / 2, radius, 0, Math.PI * 2);
                    this.ctx.stroke();
                }
                
                // Highlight last move
                if (this.lastMove && this.lastMove[0] === row && this.lastMove[1] === col) {
                    this.ctx.fillStyle = 'rgba(255, 255, 0, 0.3)';
                    this.ctx.fillRect(x, y, this.cellSize, this.cellSize);
                }
            }
        }
    }
}