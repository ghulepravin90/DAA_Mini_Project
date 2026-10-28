/**
 * Searching Visualizer Component: Linear Search & Binary Search
 */

class SearchingVisualizer {
    constructor() {
        this.array = [];
        this.trace = [];
        this.stepIdx = 0;
        this.isPlaying = false;
        this.timer = null;
        this.speed = 350;

        this.initDOMElements();
        this.bindEvents();
    }

    initDOMElements() {
        this.dom = {
            algoSelect: document.getElementById('searchAlgoSelect'),
            targetInput: document.getElementById('searchTargetInput'),
            btnRandomTarget: document.getElementById('btnSearchRandomTarget'),
            sizeSlider: document.getElementById('searchSizeSlider'),
            sizeVal: document.getElementById('searchSizeVal'),
            btnNewArray: document.getElementById('btnSearchNewArray'),
            speedSlider: document.getElementById('searchSpeedSlider'),
            btnPlay: document.getElementById('btnSearchPlay'),
            btnPrev: document.getElementById('btnSearchPrev'),
            btnNext: document.getElementById('btnSearchNext'),
            btnReset: document.getElementById('btnSearchReset'),
            arrayContainer: document.getElementById('searchArrayContainer'),
            narration: document.getElementById('searchNarration'),
            stepBadge: document.getElementById('searchStepBadge'),
            compsBadge: document.getElementById('searchCompsBadge'),
            statusBadge: document.getElementById('searchStatusBadge'),
            stageTitle: document.getElementById('searchStageTitle'),
            paradigmBadge: document.getElementById('searchParadigmBadge'),
            reqBadge: document.getElementById('searchReqBadge'),
            bestTime: document.getElementById('searchBestTime'),
            avgTime: document.getElementById('searchAvgTime'),
            worstTime: document.getElementById('searchWorstTime'),
            space: document.getElementById('searchSpace'),
            description: document.getElementById('searchDescription'),
            pseudocode: document.getElementById('searchPseudocode')
        };
    }

    bindEvents() {
        window.addEventListener('algoscope_meta_ready', () => {
            this.generateArray();
            this.updateMetadataCard();
        });

        this.dom.algoSelect.addEventListener('change', () => {
            this.updateMetadataCard();
            this.generateArray();
        });

        this.dom.sizeSlider.addEventListener('input', (e) => {
            this.dom.sizeVal.textContent = e.target.value;
        });

        this.dom.sizeSlider.addEventListener('change', () => this.generateArray());
        this.dom.btnNewArray.addEventListener('click', () => this.generateArray());

        this.dom.btnRandomTarget.addEventListener('click', () => {
            if (this.array.length > 0) {
                // 80% chance of selecting an element in array, 20% random number
                if (Math.random() < 0.8) {
                    const picked = this.array[Math.floor(Math.random() * this.array.length)];
                    this.dom.targetInput.value = picked;
                } else {
                    this.dom.targetInput.value = Math.floor(Math.random() * 100);
                }
                this.fetchTrace();
            }
        });

        this.dom.targetInput.addEventListener('change', () => this.fetchTrace());

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

    generateArray() {
        this.pause();
        const size = parseInt(this.dom.sizeSlider.value);
        const algo = this.dom.algoSelect.value;

        // Generate unique numbers
        const set = new Set();
        while (set.size < size) {
            set.add(Math.floor(Math.random() * 90) + 10);
        }
        let arr = Array.from(set);

        // Binary search requires sorted array
        if (algo === 'binary_search') {
            arr.sort((a, b) => a - b);
        }

        this.array = arr;
        // Set target default to one in the middle
        this.dom.targetInput.value = arr[Math.floor(arr.length / 2)];
        this.renderArray();
        this.fetchTrace();
    }

    async fetchTrace() {
        this.pause();
        const algo = this.dom.algoSelect.value;
        const target = parseInt(this.dom.targetInput.value);

        try {
            const res = await fetch('/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    algorithm: algo,
                    array: this.array,
                    target: target
                })
            });
            const data = await res.json();
            this.trace = data.trace || [];
            this.reset();
        } catch (e) {
            console.error('Failed to fetch search trace', e);
        }
    }

    renderArray(activeState = {}) {
        const container = this.dom.arrayContainer;
        container.innerHTML = '';

        this.array.forEach((val, idx) => {
            const cell = document.createElement('div');
            cell.style.display = 'flex';
            cell.style.flexDirection = 'column';
            cell.style.alignItems = 'center';
            cell.style.minWidth = '46px';
            cell.style.margin = '4px';

            const box = document.createElement('div');
            box.style.width = '44px';
            box.style.height = '44px';
            box.style.display = 'flex';
            box.style.alignItems = 'center';
            box.style.justifyContent = 'center';
            box.style.borderRadius = '8px';
            box.style.border = '2px solid var(--border-color)';
            box.style.fontFamily = 'var(--font-mono)';
            box.style.fontWeight = '700';
            box.style.fontSize = '1.05rem';
            box.style.transition = 'all 0.2s';
            box.textContent = val;

            const pointerTag = document.createElement('span');
            pointerTag.style.fontSize = '0.72rem';
            pointerTag.style.fontWeight = '700';
            pointerTag.style.marginTop = '4px';
            pointerTag.style.fontFamily = 'var(--font-mono)';
            pointerTag.style.height = '16px';

            // Check pointers
            if (activeState.type === 'found' && (idx === activeState.mid || idx === activeState.current_idx)) {
                box.style.backgroundColor = '#10b981';
                box.style.color = '#ffffff';
                box.style.borderColor = '#059669';
                box.style.transform = 'scale(1.15)';
                box.style.boxShadow = '0 0 16px rgba(16, 185, 129, 0.7)';
                pointerTag.textContent = 'MATCH!';
                pointerTag.style.color = '#10b981';
            } else if (activeState.mid === idx) {
                box.style.backgroundColor = '#f59e0b';
                box.style.color = '#ffffff';
                box.style.borderColor = '#d97706';
                box.style.transform = 'scale(1.1)';
                pointerTag.textContent = 'MID';
                pointerTag.style.color = '#f59e0b';
            } else if (activeState.current_idx === idx) {
                box.style.backgroundColor = '#38bdf8';
                box.style.color = '#0f172a';
                box.style.borderColor = '#0284c7';
                pointerTag.textContent = 'SCAN';
                pointerTag.style.color = '#38bdf8';
            } else if (activeState.low === idx && activeState.high === idx) {
                box.style.borderColor = '#a855f7';
                pointerTag.textContent = 'L & H';
                pointerTag.style.color = '#a855f7';
            } else if (activeState.low === idx) {
                box.style.borderColor = '#38bdf8';
                pointerTag.textContent = 'LOW';
                pointerTag.style.color = '#38bdf8';
            } else if (activeState.high === idx) {
                box.style.borderColor = '#ef4444';
                pointerTag.textContent = 'HIGH';
                pointerTag.style.color = '#ef4444';
            } else {
                box.style.backgroundColor = 'var(--bg-secondary)';
                box.style.color = 'var(--text-primary)';

                // If binary search and out of bounds [low..high]
                if (activeState.low !== undefined && activeState.high !== undefined) {
                    if (idx < activeState.low || idx > activeState.high) {
                        box.style.opacity = '0.25';
                    }
                }
            }

            const idxLabel = document.createElement('span');
            idxLabel.style.fontSize = '0.68rem';
            idxLabel.style.color = 'var(--text-muted)';
            idxLabel.textContent = `[${idx}]`;

            cell.appendChild(box);
            cell.appendChild(pointerTag);
            cell.appendChild(idxLabel);
            container.appendChild(cell);
        });
    }

    applyStep(idx) {
        if (!this.trace || idx >= this.trace.length) return;
        const step = this.trace[idx];

        this.renderArray(step);
        this.dom.stepBadge.textContent = `Step: ${idx + 1} / ${this.trace.length}`;
        this.dom.compsBadge.textContent = `Comparisons: ${step.comparisons || 0}`;
        this.dom.narration.textContent = step.description;

        if (step.type === 'found') {
            this.dom.statusBadge.textContent = 'Found!';
            this.dom.statusBadge.className = 'badge badge-success';
        } else if (step.type === 'not_found') {
            this.dom.statusBadge.textContent = 'Not Found';
            this.dom.statusBadge.className = 'badge badge-warning';
        } else {
            this.dom.statusBadge.textContent = 'Searching...';
            this.dom.statusBadge.className = 'badge badge-info';
        }

        // Highlight pseudocode
        if (AppState.metadata && AppState.metadata.searching) {
            const meta = AppState.metadata.searching[this.dom.algoSelect.value];
            if (meta && meta.pseudocode) {
                renderPseudocode('searchPseudocode', meta.pseudocode, step.pseudo_line);
            }
        }

        // Sound tone
        const probeIdx = step.mid !== undefined && step.mid !== null ? step.mid : step.current_idx;
        if (probeIdx !== null && probeIdx !== undefined && this.array[probeIdx]) {
            soundSynth.playTone(this.array[probeIdx], 10, 100);
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
        this.dom.btnPlay.innerHTML = '▶ Search';
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
        this.renderArray();
        this.dom.stepBadge.textContent = `Step: 0 / ${this.trace.length}`;
        this.dom.compsBadge.textContent = 'Comparisons: 0';
        this.dom.statusBadge.textContent = 'Status: Ready';
        this.dom.statusBadge.className = 'badge badge-info';
        this.dom.narration.textContent = 'Select target and click Search.';
        this.updateMetadataCard();
    }

    updateMetadataCard() {
        if (!AppState.metadata || !AppState.metadata.searching) return;
        const algoKey = this.dom.algoSelect.value;
        const meta = AppState.metadata.searching[algoKey];
        if (!meta) return;

        this.dom.stageTitle.textContent = meta.name;
        this.dom.paradigmBadge.textContent = meta.paradigm;
        this.dom.bestTime.textContent = meta.best_time;
        this.dom.avgTime.textContent = meta.avg_time;
        this.dom.worstTime.textContent = meta.worst_time;
        this.dom.space.textContent = meta.space;
        this.dom.reqBadge.textContent = meta.requires_sorted ? 'Requires Sorted Array' : 'Any Array Order';
        this.dom.reqBadge.className = `badge ${meta.requires_sorted ? 'badge-warning' : 'badge-info'}`;
        this.dom.description.textContent = meta.description;

        renderPseudocode('searchPseudocode', meta.pseudocode, 0);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.SearchingVisualizer = new SearchingVisualizer();
});
