document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const solveBtn = document.getElementById('solve-btn');
    const mazeWrapper = document.getElementById('maze-wrapper');
    const statsPanel = document.getElementById('stats-panel');
    const statAlgo = document.getElementById('stat-algo');
    const statTime = document.getElementById('stat-time');
    const widthInput = document.getElementById('width');
    const heightInput = document.getElementById('height');
    const algorithmSelect = document.getElementById('algorithm');

    // New elements
    const drawBtn = document.getElementById('draw-btn');
    const eraseBtn = document.getElementById('erase-btn');
    const blankBtn = document.getElementById('blank-btn');
    const clearSolBtn = document.getElementById('clear-sol-btn');
    const toggle3DBtn = document.getElementById('toggle-3d-btn');
    const exportBtn = document.getElementById('export-btn');

    // Theme switching logic
    const appTabs = document.querySelectorAll('.app-tab');
    appTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            appTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            document.body.className = tab.dataset.theme;
        });
    });

    let currentMaze = null;
    let isProcessing = false;
    let isDrawing = false;
    let currentTool = 'draw'; // 'draw' or 'erase'

    const setLoading = (loading) => {
        isProcessing = loading;
        generateBtn.disabled = loading;
        solveBtn.disabled = loading || !currentMaze;
        if (loading) {
            document.body.style.cursor = 'wait';
        } else {
            document.body.style.cursor = 'default';
        }
    };

    const renderMaze = () => {
        if (!currentMaze || currentMaze.length === 0) return;
        
        const rows = currentMaze.length;
        const cols = currentMaze[0].length;
        
        mazeWrapper.innerHTML = '';
        mazeWrapper.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
        mazeWrapper.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
        
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.dataset.row = i;
                cell.dataset.col = j;
                
                const val = currentMaze[i][j];
                if (val === '0') {
                    cell.classList.add('wall');
                } else if (val === '1') {
                    cell.classList.add('path');
                } else if (val === '2') {
                    cell.classList.add('solution');
                }
                
                if (i === 1 && j === 1) {
                    cell.classList.add('start');
                } else if (i === rows - 2 && j === cols - 2) {
                    cell.classList.add('end');
                }
                
                mazeWrapper.appendChild(cell);
            }
        }
    };

    const findShortestPath = (mazeGrid) => {
        const rows = mazeGrid.length;
        const cols = mazeGrid[0].length;
        const start = {r: 1, c: 1};
        const end = {r: rows - 2, c: cols - 2};
        
        const queue = [[start]];
        const visited = new Set([`1,1`]);
        const dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]];
        
        while(queue.length > 0) {
            const path = queue.shift();
            const curr = path[path.length - 1];
            
            if (curr.r === end.r && curr.c === end.c) {
                return path;
            }
            
            for (let d of dirs) {
                const nr = curr.r + d[0];
                const nc = curr.c + d[1];
                
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) {
                    if (mazeGrid[nr][nc] === '2' && !visited.has(`${nr},${nc}`)) {
                        visited.add(`${nr},${nc}`);
                        queue.push([...path, {r: nr, c: nc}]);
                    }
                }
            }
        }
        return [];
    };

    let animationInterval = null;

    const animatePath = (path) => {
        if (animationInterval) clearInterval(animationInterval);
        
        // Remove existing entity if any
        const existingEntity = document.querySelector('.moving-entity');
        if (existingEntity) existingEntity.remove();

        if (path.length === 0) return;

        const entity = document.createElement('div');
        entity.className = 'moving-entity';
        mazeWrapper.appendChild(entity);

        let step = 0;
        animationInterval = setInterval(() => {
            if (step >= path.length) {
                clearInterval(animationInterval);
                return;
            }
            
            const node = path[step];
            // Update entity position
            entity.style.gridRowStart = node.r + 1;
            entity.style.gridColumnStart = node.c + 1;
            
            // Draw trail
            const cell = document.querySelector(`.cell[data-row="${node.r}"][data-col="${node.c}"]`);
            if (cell) {
                cell.classList.add('solution-trail');
            }
            
            step++;
        }, 50); // 50ms per step speed
    };

    // Drawing logic
    mazeWrapper.addEventListener('mousedown', (e) => {
        if (e.target.classList.contains('cell')) {
            isDrawing = true;
            applyTool(e.target);
        }
        e.preventDefault(); // prevent dragging issues
    });

    window.addEventListener('mouseup', () => {
        isDrawing = false;
    });

    mazeWrapper.addEventListener('mouseover', (e) => {
        if (isDrawing && e.target.classList.contains('cell')) {
            applyTool(e.target);
        }
    });

    const applyTool = (cell) => {
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);
        
        // Don't modify start/end
        const rows = currentMaze.length;
        const cols = currentMaze[0].length;
        if ((row === 1 && col === 1) || (row === rows - 2 && col === cols - 2)) return;

        // Clear solution first if we are editing
        clearSolution();

        if (currentTool === 'draw') {
            currentMaze[row][col] = '0';
            cell.className = 'cell wall'; // override existing classes
        } else if (currentTool === 'erase') {
            currentMaze[row][col] = '1';
            cell.className = 'cell path';
        }
    };

    drawBtn.addEventListener('click', () => {
        currentTool = 'draw';
        drawBtn.classList.add('active');
        eraseBtn.classList.remove('active');
    });

    eraseBtn.addEventListener('click', () => {
        currentTool = 'erase';
        eraseBtn.classList.add('active');
        drawBtn.classList.remove('active');
    });

    blankBtn.addEventListener('click', () => {
        if (!currentMaze) return;
        const rows = currentMaze.length;
        const cols = currentMaze[0].length;
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                currentMaze[i][j] = '0'; // Wall
            }
        }
        currentMaze[1][1] = '1'; // Ensure start and end are paths initially
        currentMaze[rows-2][cols-2] = '1';
        renderMaze();
        statsPanel.style.display = 'none';
    });

    const clearSolution = () => {
        if (!currentMaze) return;
        let needsRender = false;
        const rows = currentMaze.length;
        const cols = currentMaze[0].length;
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                if (currentMaze[i][j] === '2') {
                    currentMaze[i][j] = '1';
                    needsRender = true;
                }
            }
        }
        if (needsRender) renderMaze();
        statsPanel.style.display = 'none';
    };

    clearSolBtn.addEventListener('click', clearSolution);

    toggle3DBtn.addEventListener('click', () => {
        mazeWrapper.classList.toggle('isometric');
    });

    exportBtn.addEventListener('click', () => {
        // Remove isometric class temporarily if present
        const wasIsometric = mazeWrapper.classList.contains('isometric');
        if (wasIsometric) {
            mazeWrapper.classList.remove('isometric');
        }
        
        // Wait a frame for class removal to take effect before capturing
        setTimeout(() => {
            html2canvas(mazeWrapper, {
                backgroundColor: '#1a1c29', // matches --wall-color
                scale: 2 // High-res capture
            }).then(canvas => {
                const link = document.createElement('a');
                link.download = 'neon-maze.png';
                link.href = canvas.toDataURL('image/png');
                link.click();
                
                if (wasIsometric) {
                    mazeWrapper.classList.add('isometric');
                }
            });
        }, 50);
    });

    const generateMaze = async () => {
        setLoading(true);
        statsPanel.style.display = 'none';
        
        try {
            let m = parseInt(heightInput.value);
            let n = parseInt(widthInput.value);
            
            const response = await fetch(`/api/maze/generate?m=${m}&n=${n}`);
            const data = await response.json();
            
            currentMaze = data.maze;
            renderMaze();
            solveBtn.disabled = false;
        } catch (error) {
            console.error('Error generating maze:', error);
            alert('Failed to generate maze.');
        } finally {
            setLoading(false);
        }
    };

    const solveMaze = async () => {
        if (!currentMaze) return;
        setLoading(true);
        
        // Clear any existing solution before solving again
        clearSolution();
        
        try {
            const algo = algorithmSelect.value;
            const response = await fetch('/api/maze/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    maze: currentMaze,
                    algorithm: algo
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                alert(data.error);
                return;
            }
            
            currentMaze = data.maze;
            renderMaze();
            
            const path = findShortestPath(currentMaze);
            animatePath(path);
            
            statsPanel.style.display = 'block';
            statAlgo.textContent = algorithmSelect.options[algorithmSelect.selectedIndex].text;
            statTime.textContent = `${data.time.toFixed(4)} seconds`;
            
        } catch (error) {
            console.error('Error solving maze:', error);
            alert('Failed to solve maze.');
        } finally {
            setLoading(false);
        }
    };

    const compareBtn = document.getElementById('compare-btn');
    const compareModal = document.getElementById('compare-modal');
    const closeModal = document.getElementById('close-modal');
    const comparisonGrid = document.getElementById('comparison-grid');
    const fastestAlgoName = document.getElementById('fastest-algo-name');
    const shortestAlgoName = document.getElementById('shortest-algo-name');

    const renderMiniMaze = (maze, container) => {
        const rows = maze.length;
        const cols = maze[0].length;
        container.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
        container.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
        
        const fragment = document.createDocumentFragment();
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                const cell = document.createElement('div');
                cell.classList.add('mini-cell');
                const val = maze[i][j];
                if (val === '0') cell.classList.add('wall');
                else if (val === '1') cell.classList.add('path');
                else if (val === '2') cell.classList.add('solution');
                
                if (i === 1 && j === 1) cell.classList.add('start');
                else if (i === rows - 2 && j === cols - 2) cell.classList.add('end');
                
                fragment.appendChild(cell);
            }
        }
        container.appendChild(fragment);
    };

    const compareAlgorithms = async () => {
        if (!currentMaze) return;
        setLoading(true);
        compareBtn.innerHTML = '<span>⚡ Running Comparison...</span>';
        
        try {
            const response = await fetch('/api/maze/compare', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ maze: currentMaze })
            });
            
            const results = await response.json();
            comparisonGrid.innerHTML = '';
            
            let fastest = { name: '', time: Infinity };
            let shortest = { name: '', length: Infinity };
            
            const algoNames = {
                'dfs': 'Depth-First Search',
                'bfs': 'Breadth-First Search',
                'dijkstra': "Dijkstra's Algorithm",
                'astar': 'A* Search',
                'aco': 'Ant Colony Optimization',
                'ga': 'Genetic Algorithm',
                'pso': 'Particle Swarm Optimization'
            };

            Object.entries(results).forEach(([key, data]) => {
                const name = algoNames[key];
                if (data.time < fastest.time) fastest = { name, time: data.time };
                if (data.pathLength < shortest.length) shortest = { name, length: data.pathLength };
                
                const card = document.createElement('div');
                card.className = 'algo-card';
                card.innerHTML = `
                    <div class="algo-card-header">
                        <h3>${name}</h3>
                    </div>
                    <div class="mini-maze-container" id="mini-maze-${key}"></div>
                    <div class="algo-metrics">
                        <div class="metric">
                            <span class="metric-label">⏱ Time</span>
                            <span class="metric-value">${data.time.toFixed(3)} ms</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">📏 Path Length</span>
                            <span class="metric-value path">${data.pathLength} cells</span>
                        </div>
                    </div>
                `;
                comparisonGrid.appendChild(card);
                renderMiniMaze(data.maze, card.querySelector('.mini-maze-container'));
            });

            fastestAlgoName.textContent = fastest.name.toUpperCase();
            shortestAlgoName.textContent = shortest.name.toUpperCase();
            
            compareModal.style.display = 'block';
            document.body.style.overflow = 'hidden'; // Prevent scrolling

        } catch (error) {
            console.error('Error comparing algorithms:', error);
            alert('Failed to compare algorithms.');
        } finally {
            setLoading(false);
            compareBtn.innerHTML = '<span>⚡ Compare Algorithms</span>';
        }
    };

    compareBtn.addEventListener('click', compareAlgorithms);
    closeModal.addEventListener('click', () => {
        compareModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    });

    window.addEventListener('click', (e) => {
        if (e.target === compareModal) {
            compareModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });

    generateBtn.addEventListener('click', generateMaze);
    solveBtn.addEventListener('click', solveMaze);

    generateMaze();
});
