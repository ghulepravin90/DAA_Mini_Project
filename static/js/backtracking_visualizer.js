/**
 * Backtracking Visualizer Component: N-Queens Problem & Sudoku Solver
 */

class BacktrackingVisualizer {
    constructor() {
        this.problem = 'n_queens';
        this.trace = [];
        this.stepIdx = 0;
        this.isPlaying = false;
        this.timer = null;
        this.speed = 120;
        this.solutionsCount = 0;

        this.initDOMElements();
        this.bindEvents();
    }

    initDOMElements() {
        this.dom = {
            problemSelect: document.getElementById('backtrackProblemSelect'),
            nQueensControls: document.getElementById('nQueensControls'),
            nQueensSizeSelect: document.getElementById('nQueensSizeSelect'),
            sudokuControls: document.getElementById('sudokuControls'),
            sudokuPresetSelect: document.getElementById('sudokuPresetSelect'),
            chessboardArea: document.getElementById('chessboardArea'),
            chessboard: document.getElementById('chessboard'),
            sudokuArea: document.getElementById('sudokuArea'),
            sudokuBoard: document.getElementById('sudokuBoard'),
            speedSlider: document.getElementById('backtrackSpeedSlider'),
            btnPlay: document.getElementById('btnBacktrackPlay'),
            btnPrev: document.getElementById('btnBacktrackPrev'),
            btnNext: document.getElementById('btnBacktrackNext'),
            btnReset: document.getElementById('btnBacktrackReset'),
            stageTitle: document.getElementById('backtrackStageTitle'),
            stepBadge: document.getElementById('backtrackStepBadge'),
            solutionsBadge: document.getElementById('backtrackSolutionsBadge'),
            complexityBadge: document.getElementById('backtrackComplexityBadge'),
            narration: document.getElementById('backtrackNarration'),
            analysisText: document.getElementById('backtrackAnalysisText'),
            pseudocode: document.getElementById('backtrackPseudocode')
        };
    }

    bindEvents() {
        window.addEventListener('algoscope_meta_ready', () => {
            this.switchProblem();
            this.updateMetadataCard();
        });

        this.dom.problemSelect.addEventListener('change', () => {
            this.switchProblem();
        });

        this.dom.nQueensSizeSelect.addEventListener('change', () => this.fetchTrace());
        this.dom.sudokuPresetSelect.addEventListener('change', () => this.fetchTrace());

        this.dom.speedSlider.addEventListener('input', (e) => {
            this.speed = parseInt(e.target.value);
            if (this.isPlaying) {
                this.pause();
                this.play();
            }
        });

        this.dom.btnPlay.addEventListener('click', () => {
            if (this.isPlaying) this.pause();
            else this.play();
        });

        this.dom.btnPrev.addEventListener('click', () => this.stepBackward());
        this.dom.btnNext.addEventListener('click', () => this.stepForward());
        this.dom.btnReset.addEventListener('click', () => this.reset());
    }

    switchProblem() {
        this.problem = this.dom.problemSelect.value;
        const isNQueens = (this.problem === 'n_queens');

        this.dom.nQueensControls.style.display = isNQueens ? 'inline-flex' : 'none';
        this.dom.sudokuControls.style.display = isNQueens ? 'none' : 'inline-flex';
        this.dom.chessboardArea.style.display = isNQueens ? 'flex' : 'none';
        this.dom.sudokuArea.style.display = isNQueens ? 'none' : 'flex';

        this.updateMetadataCard();
        this.fetchTrace();
    }

    async fetchTrace() {
        this.pause();
        const payload = { algorithm: this.problem };

        if (this.problem === 'n_queens') {
            payload.n = parseInt(this.dom.nQueensSizeSelect.value);
        } else {
            payload.preset = this.dom.sudokuPresetSelect.value;
        }

        try {
            const res = await fetch('/api/backtrack', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            this.trace = data.trace || [];
            this.reset();
        } catch (e) {
            console.error('Failed to fetch backtracking trace', e);
        }
    }

    renderChessboard(step = {}) {
        const n = parseInt(this.dom.nQueensSizeSelect.value);
        const board = this.dom.chessboard;
        board.innerHTML = '';
        board.style.gridTemplateColumns = `repeat(${n}, 54px)`;
        board.style.gridTemplateRows = `repeat(${n}, 54px)`;

        const placements = step.board || [];
        const conflictPos = step.conflict;
        const activeRow = step.row;
        const activeCol = step.col;

        for (let r = 0; r < n; r++) {
            for (let c = 0; c < n; c++) {
                const cell = document.createElement('div');
                const isLight = (r + c) % 2 === 0;
                cell.className = `chess-cell ${isLight ? 'light' : 'dark'}`;

                // Has Queen
                if (placements[r] === c) {
                    cell.textContent = '👑';
                    cell.classList.add('queen');
                }

                // Visual highlights for current check
                if (r === activeRow && c === activeCol) {
                    if (step.type === 'place_queen') {
                        cell.classList.add('safe');
                    } else if (step.type === 'conflict') {
                        cell.classList.add('conflict');
                        cell.textContent = '⚔️';
                    } else if (step.type === 'backtrack') {
                        cell.classList.add('backtrack-cell');
                    }
                }

                // Highlight conflicting queen
                if (conflictPos && conflictPos[0] === r && conflictPos[1] === c) {
                    cell.style.boxShadow = '0 0 14px #ef4444 inset';
                    cell.style.borderColor = '#ef4444';
                }

                board.appendChild(cell);
            }
        }
    }

    renderSudoku(step = {}) {
        const board = this.dom.sudokuBoard;
        board.innerHTML = '';

        const grid = step.grid || (AppState.metadata && AppState.metadata.preset_sudoku ? AppState.metadata.preset_sudoku.easy : []);
        const fixed = step.fixed || [];

        for (let r = 0; r < 9; r++) {
            for (let c = 0; c < 9; c++) {
                const cell = document.createElement('div');
                cell.className = 'sudoku-cell';
                const val = grid[r] ? grid[r][c] : 0;
                cell.textContent = val !== 0 ? val : '';

                if (fixed[r] && fixed[r][c]) {
                    cell.classList.add('fixed');
                }

                if (step.row === r && step.col === c) {
                    if (step.type === 'place_num') cell.classList.add('valid-trial');
                    else if (step.type === 'invalid_num') cell.classList.add('conflict-trial');
                    else if (step.type === 'backtrack') cell.classList.add('active-trial');
                }

                board.appendChild(cell);
            }
        }
    }

    applyStep(idx) {
        if (!this.trace || idx >= this.trace.length) return;
        const step = this.trace[idx];

        if (this.problem === 'n_queens') {
            this.renderChessboard(step);
            if (step.type === 'solution_found') {
                this.solutionsCount++;
                this.dom.solutionsBadge.textContent = `Solutions: ${this.solutionsCount}`;
                soundSynth.playTone(85, 10, 100, 0.2);
            } else if (step.type === 'place_queen') {
                soundSynth.playTone(60, 10, 100);
            } else if (step.type === 'backtrack') {
                soundSynth.playTone(25, 10, 100);
            }
        } else {
            this.renderSudoku(step);
            if (step.type === 'place_num') soundSynth.playTone(55, 10, 100);
            else if (step.type === 'backtrack') soundSynth.playTone(25, 10, 100);
        }

        this.dom.stepBadge.textContent = `Step: ${idx + 1} / ${this.trace.length}`;
        this.dom.narration.textContent = step.description;

        // Pseudocode line
        const metaKey = (this.problem === 'n_queens') ? 'n_queens' : 'sudoku_solver';
        if (AppState.metadata && AppState.metadata.backtracking) {
            const meta = AppState.metadata.backtracking[metaKey];
            if (meta && meta.pseudocode) {
                renderPseudocode('backtrackPseudocode', meta.pseudocode, step.pseudo_line);
            }
        }
    }

    play() {
        if (!this.trace || this.trace.length === 0) return;
        this.isPlaying = true;
        this.dom.btnPlay.innerHTML = '⏸ Pause';
        this.dom.btnPlay.classList.remove('btn-primary');
        this.dom.btnPlay.classList.add('btn-warning');

        const stepLoop = () => {
            if (!this.isPlaying) return;

            if (this.stepIdx < this.trace.length) {
                this.applyStep(this.stepIdx);
                this.stepIdx++;
                this.timer = setTimeout(stepLoop, this.speed);
            } else {
                this.pause();
                this.dom.narration.textContent = '✅ Backtracking Search Concluded!';
            }
        };

        stepLoop();
    }

    pause() {
        this.isPlaying = false;
        if (this.timer) {
            clearTimeout(this.timer);
            this.timer = null;
        }
        this.dom.btnPlay.innerHTML = '▶ Solve';
        this.dom.btnPlay.classList.remove('btn-warning');
        this.dom.btnPlay.classList.add('btn-primary');
    }

    stepForward() {
        this.pause();
        if (this.stepIdx < this.trace.length) {
            this.applyStep(this.stepIdx);
            this.stepIdx++;
        }
    }

    stepBackward() {
        this.pause();
        if (this.stepIdx > 1) {
            this.stepIdx -= 2;
            this.applyStep(this.stepIdx);
            this.stepIdx++;
        } else if (this.stepIdx === 1) {
            this.reset();
        }
    }

    reset() {
        this.pause();
        this.stepIdx = 0;
        this.solutionsCount = 0;
        this.dom.solutionsBadge.textContent = 'Solutions: 0';
        this.dom.stepBadge.textContent = `Step: 0 / ${this.trace.length}`;
        this.dom.narration.textContent = 'Click Solve or Step Forward to start backtracking.';

        if (this.problem === 'n_queens') {
            this.renderChessboard();
        } else {
            this.renderSudoku();
        }
        this.updateMetadataCard();
    }

    updateMetadataCard() {
        if (!AppState.metadata || !AppState.metadata.backtracking) return;
        const metaKey = (this.problem === 'n_queens') ? 'n_queens' : 'sudoku_solver';
        const meta = AppState.metadata.backtracking[metaKey];
        if (!meta) return;

        this.dom.stageTitle.textContent = meta.name;
        this.dom.complexityBadge.textContent = meta.time_complexity;
        this.dom.analysisText.textContent = meta.description;

        renderPseudocode('backtrackPseudocode', meta.pseudocode, 0);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.BacktrackingVisualizer = new BacktrackingVisualizer();
});
