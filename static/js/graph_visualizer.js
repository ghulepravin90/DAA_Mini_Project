/**
 * Graph Visualizer Component: BFS, DFS, and Dijkstra
 * Interactive HTML5 Canvas Graph Rendering
 */

class GraphVisualizer {
    constructor() {
        this.canvas = document.getElementById('graphCanvas');
        this.ctx = this.canvas ? this.canvas.getContext('2d') : null;

        this.graphData = null;
        this.trace = [];
        this.stepIdx = 0;
        this.isPlaying = false;
        this.timer = null;
        this.speed = 450;

        this.initDOMElements();
        this.bindEvents();
    }

    initDOMElements() {
        this.dom = {
            algoSelect: document.getElementById('graphAlgoSelect'),
            presetSelect: document.getElementById('graphPresetSelect'),
            startSelect: document.getElementById('graphStartSelect'),
            destSelect: document.getElementById('graphDestSelect'),
            destLabel: document.getElementById('graphDestLabel'),
            speedSlider: document.getElementById('graphSpeedSlider'),
            btnPlay: document.getElementById('btnGraphPlay'),
            btnPrev: document.getElementById('btnGraphPrev'),
            btnNext: document.getElementById('btnGraphNext'),
            btnReset: document.getElementById('btnGraphReset'),
            stageTitle: document.getElementById('graphStageTitle'),
            paradigmBadge: document.getElementById('graphParadigmBadge'),
            stepBadge: document.getElementById('graphStepBadge'),
            visitedBadge: document.getElementById('graphVisitedBadge'),
            narration: document.getElementById('graphNarration'),
            stateTitle: document.getElementById('graphStateTitle'),
            stateContent: document.getElementById('graphStateContent'),
            complexityBadge: document.getElementById('graphComplexityBadge'),
            pseudocode: document.getElementById('graphPseudocode')
        };
    }

    bindEvents() {
        window.addEventListener('algoscope_meta_ready', () => {
            this.loadPresetGraph();
            this.updateMetadataCard();
        });

        this.dom.algoSelect.addEventListener('change', () => {
            const algo = this.dom.algoSelect.value;
            const isDijkstra = algo === 'dijkstra';
            this.dom.destLabel.style.display = isDijkstra ? 'inline-block' : 'none';
            this.dom.destSelect.style.display = isDijkstra ? 'inline-block' : 'none';
            this.updateMetadataCard();
            this.fetchTrace();
        });

        this.dom.presetSelect.addEventListener('change', () => {
            this.loadPresetGraph();
        });

        this.dom.startSelect.addEventListener('change', () => this.fetchTrace());
        this.dom.destSelect.addEventListener('change', () => this.fetchTrace());

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

    loadPresetGraph() {
        const presetKey = this.dom.presetSelect.value;
        if (!AppState.metadata || !AppState.metadata.preset_graphs) return;

        this.graphData = JSON.parse(JSON.stringify(AppState.metadata.preset_graphs[presetKey]));
        this.populateNodeSelects();
        this.draw();
        this.fetchTrace();
    }

    populateNodeSelects() {
        if (!this.graphData) return;
        const nodes = this.graphData.nodes.map(n => n.id);

        this.dom.startSelect.innerHTML = nodes.map((n, i) =>
            `<option value="${n}" ${i === 0 ? 'selected' : ''}>${n}</option>`
        ).join('');

        this.dom.destSelect.innerHTML = nodes.map((n, i) =>
            `<option value="${n}" ${i === nodes.length - 1 ? 'selected' : ''}>${n}</option>`
        ).join('');
    }

    async fetchTrace() {
        this.pause();
        const algo = this.dom.algoSelect.value;
        const presetKey = this.dom.presetSelect.value;
        const start = this.dom.startSelect.value;
        const end = this.dom.destSelect.value;

        try {
            const res = await fetch('/api/graph', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    algorithm: algo,
                    graph_type: presetKey,
                    start_node: start,
                    end_node: end
                })
            });
            const data = await res.json();
            this.trace = data.trace || [];
            this.reset();
        } catch (e) {
            console.error('Failed to fetch graph trace', e);
        }
    }

    draw(activeState = {}) {
        if (!this.ctx || !this.graphData) return;
        const ctx = this.ctx;
        const width = this.canvas.width;
        const height = this.canvas.height;

        ctx.clearRect(0, 0, width, height);

        const nodes = this.graphData.nodes;
        const edges = this.graphData.edges;

        const visitedNodes = new Set(activeState.visited || []);
        const currentNode = activeState.current_node;
        const activeEdgeStr = activeState.active_edge; // e.g. "A-B"
        const shortestPathNodes = activeState.shortest_path || [];

        // 1. Draw Edges
        edges.forEach(edge => {
            const uNode = nodes.find(n => n.id === edge.u);
            const vNode = nodes.find(n => n.id === edge.v);
            if (!uNode || !vNode) return;

            const edgeKey1 = `${edge.u}-${edge.v}`;
            const edgeKey2 = `${edge.v}-${edge.u}`;
            const isActive = (activeEdgeStr === edgeKey1 || activeEdgeStr === edgeKey2);

            let strokeColor = '#334155';
            let lineWidth = 2;

            if (isActive) {
                strokeColor = '#f59e0b';
                lineWidth = 4;
            }

            ctx.beginPath();
            ctx.moveTo(uNode.x, uNode.y);
            ctx.lineTo(vNode.x, vNode.y);
            ctx.strokeStyle = strokeColor;
            ctx.lineWidth = lineWidth;
            ctx.stroke();

            // Draw Edge Weight
            if (edge.weight !== undefined) {
                const midX = (uNode.x + vNode.x) / 2;
                const midY = (uNode.y + vNode.y) / 2;

                ctx.beginPath();
                ctx.arc(midX, midY, 12, 0, 2 * Math.PI);
                ctx.fillStyle = '#1e293b';
                ctx.fill();
                ctx.strokeStyle = '#475569';
                ctx.lineWidth = 1;
                ctx.stroke();

                ctx.fillStyle = '#94a3b8';
                ctx.font = '10px JetBrains Mono';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(edge.weight, midX, midY);
            }
        });

        // 2. Draw Nodes
        nodes.forEach(node => {
            const isCurrent = (currentNode === node.id);
            const isVisited = visitedNodes.has(node.id);
            const isTarget = (this.dom.algoSelect.value === 'dijkstra' && node.id === this.dom.destSelect.value);

            let fillColor = '#1e293b';
            let borderColor = '#64748b';
            let textColor = '#f8fafc';
            const radius = 22;

            if (isCurrent) {
                fillColor = '#38bdf8';
                borderColor = '#0284c7';
                textColor = '#0f172a';
            } else if (isVisited) {
                fillColor = '#10b981';
                borderColor = '#059669';
                textColor = '#ffffff';
            } else if (isTarget) {
                borderColor = '#ec4899';
            }

            // Glow for active node
            if (isCurrent) {
                ctx.save();
                ctx.beginPath();
                ctx.arc(node.x, node.y, radius + 6, 0, 2 * Math.PI);
                ctx.fillStyle = 'rgba(56, 189, 248, 0.25)';
                ctx.fill();
                ctx.restore();
            }

            ctx.beginPath();
            ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI);
            ctx.fillStyle = fillColor;
            ctx.fill();
            ctx.lineWidth = 3;
            ctx.strokeStyle = borderColor;
            ctx.stroke();

            // Node Label
            ctx.fillStyle = textColor;
            ctx.font = 'bold 14px Inter';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(node.id, node.x, node.y);

            // If Dijkstra, display tentative distance above node
            if (activeState.distances && activeState.distances[node.id] !== undefined) {
                const distVal = activeState.distances[node.id];
                ctx.fillStyle = isVisited ? '#34d399' : '#38bdf8';
                ctx.font = 'bold 11px JetBrains Mono';
                ctx.fillText(`d=${distVal}`, node.x, node.y - radius - 8);
            }
        });
    }

    applyStep(idx) {
        if (!this.trace || idx >= this.trace.length) return;
        const step = this.trace[idx];

        this.draw(step);
        this.dom.stepBadge.textContent = `Step: ${idx + 1} / ${this.trace.length}`;
        this.dom.visitedBadge.textContent = `Visited: ${step.visited ? step.visited.length : 0}`;
        this.dom.narration.textContent = step.description;

        // Update Side Panel state
        const algo = this.dom.algoSelect.value;
        if (algo === 'dijkstra') {
            this.dom.stateTitle.textContent = 'Distance Table & Priority Queue';
            let html = '<table style="width: 100%; border-collapse: collapse; text-align: left;">';
            html += '<tr style="border-bottom: 1px solid var(--border-color); color: var(--text-muted); font-size: 0.75rem;"><th>Node</th><th>Dist</th><th>Parent</th></tr>';
            if (step.distances) {
                Object.keys(step.distances).sort().forEach(nId => {
                    const d = step.distances[nId];
                    const p = step.parents ? (step.parents[nId] || '—') : '—';
                    const isVis = step.visited && step.visited.includes(nId);
                    const color = isVis ? '#10b981' : (d !== '∞' ? '#38bdf8' : 'var(--text-muted)');
                    html += `<tr style="color: ${color}; padding: 2px 0;"><td><strong>${nId}</strong></td><td>${d}</td><td>${p}</td></tr>`;
                });
            }
            html += '</table>';
            this.dom.stateContent.innerHTML = html;
        } else if (algo === 'bfs') {
            this.dom.stateTitle.textContent = 'FIFO Queue State';
            const queueItems = (step.queue || []).map(q => `<span style="background: var(--bg-primary); padding: 4px 8px; border-radius: 4px; border: 1px solid var(--accent); color: var(--accent);">${q}</span>`).join(' ← ');
            this.dom.stateContent.innerHTML = `
                <div style="margin-bottom: 0.5rem; color: var(--text-muted);">Front → Rear:</div>
                <div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;">${queueItems || '<em>(Queue is Empty)</em>'}</div>
                <div style="margin-top: 0.75rem; color: var(--text-secondary);">Traversal Order: <strong>${(step.traversal || []).join(' → ')}</strong></div>
            `;
        } else if (algo === 'dfs') {
            this.dom.stateTitle.textContent = 'Call Stack (Recursion)';
            const stackItems = (step.stack || []).map(s => `<div style="background: var(--bg-primary); padding: 4px 8px; border-radius: 4px; border: 1px solid #a855f7; color: #a855f7; margin-bottom: 3px;">Frame: DFS('${s}')</div>`).join('');
            this.dom.stateContent.innerHTML = `
                <div style="color: var(--text-muted); margin-bottom: 0.3rem;">Top of Stack:</div>
                <div>${stackItems || '<em>(Call Stack is Empty)</em>'}</div>
                <div style="margin-top: 0.75rem; color: var(--text-secondary);">Traversal Order: <strong>${(step.traversal || []).join(' → ')}</strong></div>
            `;
        }

        // Pseudocode line
        if (AppState.metadata && AppState.metadata.graphs) {
            const meta = AppState.metadata.graphs[algo];
            if (meta && meta.pseudocode) {
                renderPseudocode('graphPseudocode', meta.pseudocode, step.pseudo_line);
            }
        }

        // Tone
        soundSynth.playTone(40, 10, 100);
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
                this.dom.narration.textContent = '✅ Traversal Completed!';
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
        this.dom.btnPlay.innerHTML = '▶ Run';
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
        this.draw();
        this.dom.stepBadge.textContent = `Step: 0 / ${this.trace.length}`;
        this.dom.visitedBadge.textContent = 'Visited: 0';
        this.dom.narration.textContent = 'Click Run or Step Forward to start traversal.';
        this.dom.stateContent.innerHTML = '<span style="color: var(--text-muted);">Ready to initialize.</span>';
        this.updateMetadataCard();
    }

    updateMetadataCard() {
        if (!AppState.metadata || !AppState.metadata.graphs) return;
        const algoKey = this.dom.algoSelect.value;
        const meta = AppState.metadata.graphs[algoKey];
        if (!meta) return;

        this.dom.stageTitle.textContent = meta.name;
        this.dom.paradigmBadge.textContent = meta.paradigm;
        this.dom.complexityBadge.textContent = meta.time_complexity;

        renderPseudocode('graphPseudocode', meta.pseudocode, 0);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.GraphVisualizer = new GraphVisualizer();
});
