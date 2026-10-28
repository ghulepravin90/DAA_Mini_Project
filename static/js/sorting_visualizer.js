/**
 * Sorting Visualizer Component
 * Supports Single Algorithm & Dual Race Comparative Mode
 */

class SortingVisualizer {
    constructor() {
        this.array = [];
        this.trace = [];
        this.stepIdx = 0;
        this.isPlaying = false;
        this.timer = null;
        this.speed = 220;

        // Dual Race Mode
        this.isDualMode = false;
        this.trace2 = [];
        this.stepIdx2 = 0;

        this.initDOMElements();
        this.bindEvents();
    }

    initDOMElements() {
        this.dom = {
            algoSelect: document.getElementById('sortAlgoSelect'),
            algoSelect2: document.getElementById('sortAlgoSelect2'),
            dualRaceCheck: document.getElementById('sortDualRaceCheck'),
            dualContainer: document.getElementById('sortDualRaceContainer'),
            sizeSlider: document.getElementById('sortSizeSlider'),
            sizeVal: document.getElementById('sortSizeVal'),
            distSelect: document.getElementById('sortDistSelect'),
            speedSlider: document.getElementById('sortSpeedSlider'),
            btnPlay: document.getElementById('btnSortPlay'),
            btnPrev: document.getElementById('btnSortPrev'),
            btnNext: document.getElementById('btnSortNext'),
            btnReset: document.getElementById('btnSortReset'),
            btnGenerate: document.getElementById('btnSortGenerate'),
            btnCustom: document.getElementById('btnSortCustom'),
            customBox: document.getElementById('customArrayBox'),
            customInput: document.getElementById('customArrayInput'),
            btnApplyCustom: document.getElementById('btnApplyCustomArray'),
            btnCloseCustom: document.getElementById('btnCloseCustomArray'),
            barContainer: document.getElementById('sortBarContainer'),
            barContainer2: document.getElementById('sortBarContainer2'),
            narration: document.getElementById('sortNarration'),
            stepBadge: document.getElementById('sortStepBadge'),
            compsBadge: document.getElementById('sortCompsBadge'),
            swapsBadge: document.getElementById('sortSwapsBadge'),
            compsBadge2: document.getElementById('sortCompsBadge2'),
            swapsBadge2: document.getElementById('sortSwapsBadge2'),
            stageTitle: document.getElementById('sortStageTitle'),
            stageTitle2: document.getElementById('sortStageTitle2'),
            paradigmBadge: document.getElementById('sortParadigmBadge'),
            paradigmBadge2: document.getElementById('sortParadigmBadge2'),
            bestTime: document.getElementById('sortBestTime'),
            avgTime: document.getElementById('sortAvgTime'),
            worstTime: document.getElementById('sortWorstTime'),
            space: document.getElementById('sortSpace'),
            stability: document.getElementById('sortStabilityBadge'),
            description: document.getElementById('sortDescription'),
            pseudocode: document.getElementById('sortPseudocode')
        };
    }

    bindEvents() {
        window.addEventListener('algoscope_meta_ready', () => {
            this.generateArray();
            this.updateMetadataCard();
        });

        this.dom.algoSelect.addEventListener('change', () => {
            this.updateMetadataCard();
            this.fetchTrace();
        });

        this.dom.algoSelect2.addEventListener('change', () => {
            if (this.isDualMode) this.fetchTrace();
        });

        this.dom.dualRaceCheck.addEventListener('change', (e) => {
            this.isDualMode = e.target.checked;
            this.dom.algoSelect2.style.display = this.isDualMode ? 'inline-block' : 'none';
            this.dom.dualContainer.style.display = this.isDualMode ? 'block' : 'none';
            this.fetchTrace();
        });

        this.dom.sizeSlider.addEventListener('input', (e) => {
            this.dom.sizeVal.textContent = e.target.value;
        });

        this.dom.sizeSlider.addEventListener('change', () => {
            this.generateArray();
        });

        this.dom.distSelect.addEventListener('change', () => {
            this.generateArray();
        });

        this.dom.speedSlider.addEventListener('input', (e) => {
            this.speed = parseInt(e.target.value);
            if (this.isPlaying) {
                this.pause();
                this.play();
            }
        });

        this.dom.btnGenerate.addEventListener('click', () => this.generateArray());

        this.dom.btnCustom.addEventListener('click', () => {
            this.dom.customBox.style.display = this.dom.customBox.style.display === 'none' ? 'block' : 'none';
        });

        this.dom.btnCloseCustom.addEventListener('click', () => {
            this.dom.customBox.style.display = 'none';
        });

        this.dom.btnApplyCustom.addEventListener('click', () => {
            const raw = this.dom.customInput.value;
            const parsed = raw.split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n));
            if (parsed.length >= 4) {
                this.array = parsed.slice(0, 40);
                this.dom.sizeSlider.value = this.array.length;
                this.dom.sizeVal.textContent = this.array.length;
                this.dom.customBox.style.display = 'none';
                this.renderBars(this.dom.barContainer, this.array);
                this.fetchTrace();
            } else {
                alert('Please enter at least 4 valid integers separated by commas.');
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

    async generateArray() {
        this.pause();
        const size = parseInt(this.dom.sizeSlider.value);
        const dist = this.dom.distSelect.value;

        try {
            const res = await fetch('/api/generate_array', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ size, distribution: dist })
            });
            const data = await res.json();
            this.array = data.array;
            this.renderBars(this.dom.barContainer, this.array);
            if (this.isDualMode) {
                this.renderBars(this.dom.barContainer2, this.array);
            }
            await this.fetchTrace();
        } catch (e) {
            console.error('Failed to generate array', e);
        }
    }

    async fetchTrace() {
        this.pause();
        const algo1 = this.dom.algoSelect.value;
        const algo2 = this.isDualMode ? this.dom.algoSelect2.value : null;

        try {
            const res = await fetch('/api/sort', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    algorithm: algo1,
                    algorithm2: algo2,
                    array: this.array
                })
            });
            const data = await res.json();
            this.trace = data.trace || [];
            this.stepIdx = 0;

            if (data.comparison) {
                this.trace2 = data.comparison.trace || [];
                this.stepIdx2 = 0;
            } else {
                this.trace2 = [];
            }

            this.reset();
        } catch (e) {
            console.error('Failed to fetch sorting trace', e);
        }
    }

    renderBars(container, arr, activeIndices = [], type = 'normal') {
        if (!container) return;
        const maxVal = Math.max(...arr, 1);
        container.innerHTML = '';

        arr.forEach((val, idx) => {
            const barContainer = document.createElement('div');
            barContainer.className = 'sort-bar-container';

            const bar = document.createElement('div');
            bar.className = 'sort-bar';
            const heightPercent = Math.max(12, Math.round((val / maxVal) * 92));
            bar.style.height = `${heightPercent}%`;

            if (activeIndices.includes(idx)) {
                if (type === 'compare') bar.classList.add('comparing');
                else if (type === 'swap' || type === 'overwrite' || type === 'shift') bar.classList.add('swapping');
                else if (type === 'pivot') bar.classList.add('pivot');
                else if (type === 'sorted_element' || type === 'finished') bar.classList.add('sorted');
            } else if (type === 'finished') {
                bar.classList.add('sorted');
            }

            const valLabel = document.createElement('span');
            valLabel.className = 'sort-bar-val';
            valLabel.textContent = val;

            barContainer.appendChild(bar);
            barContainer.appendChild(valLabel);
            container.appendChild(barContainer);
        });
    }

    applyStep(idx) {
        if (!this.trace || idx >= this.trace.length) return;
        const step = this.trace[idx];

        this.renderBars(this.dom.barContainer, step.array, step.indices || [], step.type);
        this.dom.stepBadge.textContent = `Step: ${idx + 1} / ${this.trace.length}`;
        this.dom.compsBadge.textContent = `Comparisons: ${step.comparisons || 0}`;
        this.dom.swapsBadge.textContent = `Swaps/Writes: ${step.swaps || 0}`;
        this.dom.narration.textContent = step.description;

        // Pseudocode line highlight
        if (AppState.metadata && AppState.metadata.sorting) {
            const meta = AppState.metadata.sorting[this.dom.algoSelect.value];
            if (meta && meta.pseudocode) {
                renderPseudocode('sortPseudocode', meta.pseudocode, step.pseudo_line);
            }
        }

        // Play Tone
        if (step.indices && step.indices.length > 0) {
            const sampleVal = step.array[step.indices[0]] || 20;
            soundSynth.playTone(sampleVal, 1, 100);
        }

        // Dual Race 2nd algorithm step update
        if (this.isDualMode && this.trace2 && this.trace2.length > 0) {
            const idx2 = Math.min(idx, this.trace2.length - 1);
            const step2 = this.trace2[idx2];
            this.renderBars(this.dom.barContainer2, step2.array, step2.indices || [], step2.type);
            this.dom.compsBadge2.textContent = `Comparisons: ${step2.comparisons || 0}`;
            this.dom.swapsBadge2.textContent = `Swaps/Writes: ${step2.swaps || 0}`;
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

            const maxSteps = this.isDualMode
                ? Math.max(this.trace.length, this.trace2.length)
                : this.trace.length;

            if (this.stepIdx < maxSteps) {
                this.applyStep(this.stepIdx);
                this.stepIdx++;
                this.timer = setTimeout(stepLoop, this.speed);
            } else {
                this.pause();
                this.dom.narration.textContent = '✅ Sorting Completed!';
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
        this.dom.btnPlay.innerHTML = '▶ Play';
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
        this.renderBars(this.dom.barContainer, this.array);
        if (this.isDualMode) {
            this.renderBars(this.dom.barContainer2, this.array);
        }
        this.dom.stepBadge.textContent = `Step: 0 / ${this.trace.length}`;
        this.dom.compsBadge.textContent = 'Comparisons: 0';
        this.dom.swapsBadge.textContent = 'Swaps/Writes: 0';
        if (this.dom.compsBadge2) this.dom.compsBadge2.textContent = 'Comparisons: 0';
        if (this.dom.swapsBadge2) this.dom.swapsBadge2.textContent = 'Swaps/Writes: 0';
        this.dom.narration.textContent = 'Ready to sort. Click Play or Step Forward.';
        this.updateMetadataCard();
    }

    updateMetadataCard() {
        if (!AppState.metadata || !AppState.metadata.sorting) return;
        const algoKey = this.dom.algoSelect.value;
        const meta = AppState.metadata.sorting[algoKey];
        if (!meta) return;

        this.dom.stageTitle.textContent = meta.name;
        this.dom.paradigmBadge.textContent = meta.paradigm;
        this.dom.bestTime.textContent = meta.best_time;
        this.dom.avgTime.textContent = meta.avg_time;
        this.dom.worstTime.textContent = meta.worst_time;
        this.dom.space.textContent = meta.space;
        this.dom.stability.textContent = meta.stable ? 'Stable' : 'Unstable';
        this.dom.stability.className = `badge ${meta.stable ? 'badge-success' : 'badge-warning'}`;
        this.dom.description.textContent = meta.description;

        renderPseudocode('sortPseudocode', meta.pseudocode, 0);

        if (this.isDualMode) {
            const algoKey2 = this.dom.algoSelect2.value;
            const meta2 = AppState.metadata.sorting[algoKey2];
            if (meta2) {
                this.dom.stageTitle2.textContent = meta2.name;
                this.dom.paradigmBadge2.textContent = meta2.paradigm;
            }
        }
    }
}

// Instantiate once DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.SortingVisualizer = new SortingVisualizer();
});
