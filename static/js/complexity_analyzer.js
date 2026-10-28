/**
 * Complexity Analyzer Component: Real Empirical Benchmarks & Chart.js Visualizer
 */

class ComplexityAnalyzer {
    constructor() {
        this.timeChart = null;
        this.opsChart = null;
        this.initDOMElements();
        this.bindEvents();
    }

    initDOMElements() {
        this.dom = {
            btnRun: document.getElementById('btnRunBenchmark'),
            distSelect: document.getElementById('benchDistSelect'),
            maxSizeSelect: document.getElementById('benchMaxSizeSelect'),
            tableBody: document.querySelector('#benchSummaryTable tbody'),
            timeCanvas: document.getElementById('benchmarkTimeChart'),
            opsCanvas: document.getElementById('benchmarkOpsChart')
        };
    }

    bindEvents() {
        this.dom.btnRun.addEventListener('click', () => this.runBenchmark());

        window.addEventListener('algoscope_meta_ready', () => {
            // Pre-seed an initial benchmark run after a brief delay
            setTimeout(() => this.runBenchmark(), 400);
        });
    }

    getSelectedAlgorithms() {
        const checked = document.querySelectorAll('input[name="benchAlgo"]:checked');
        return Array.from(checked).map(c => c.value);
    }

    getSizes() {
        const choice = this.dom.maxSizeSelect.value;
        if (choice === 'small') return [50, 100, 200, 400];
        if (choice === 'large') return [100, 250, 500, 1000, 1800];
        return [50, 100, 250, 500, 1000];
    }

    async runBenchmark() {
        const algos = this.getSelectedAlgorithms();
        if (algos.length === 0) {
            alert('Please select at least one algorithm to benchmark.');
            return;
        }

        const sizes = this.getSizes();
        const dist = this.dom.distSelect.value;

        this.dom.btnRun.disabled = true;
        this.dom.btnRun.innerHTML = '⏳ Benchmarking in Python...';

        try {
            const res = await fetch('/api/benchmark/sorting', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    algorithms: algos,
                    sizes: sizes,
                    distribution: dist
                })
            });
            const data = await res.json();
            this.renderCharts(data);
            this.renderTable(data);
        } catch (e) {
            console.error('Benchmark failed', e);
            alert('Failed to execute benchmark. Check console.');
        } finally {
            this.dom.btnRun.disabled = false;
            this.dom.btnRun.innerHTML = '🚀 Run Empirical Benchmark';
        }
    }

    getAlgoColor(algoKey) {
        const colors = {
            'quick_sort': '#38bdf8',     // Sky blue
            'merge_sort': '#818cf8',     // Indigo
            'heap_sort': '#34d399',      // Emerald
            'insertion_sort': '#f59e0b', // Amber
            'bubble_sort': '#ef4444',    // Red
            'selection_sort': '#ec4899'  // Pink
        };
        return colors[algoKey] || '#94a3b8';
    }

    renderCharts(data) {
        if (!window.Chart) return;

        const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.08)';
        const textColor = isDark ? '#94a3b8' : '#475569';

        const sizes = data.sizes;
        const algoResults = data.algorithms;

        // 1. Time Chart Datasets
        const timeDatasets = Object.keys(algoResults).map(key => {
            const res = algoResults[key];
            const meta = AppState.metadata && AppState.metadata.sorting ? AppState.metadata.sorting[key] : null;
            const label = meta ? meta.name : key;
            const color = this.getAlgoColor(key);

            return {
                label: label,
                data: res.times_ms,
                borderColor: color,
                backgroundColor: color,
                borderWidth: 2.5,
                tension: 0.25,
                pointRadius: 4,
                pointHoverRadius: 6
            };
        });

        // 2. Ops (Comparisons) Datasets
        const opsDatasets = Object.keys(algoResults).map(key => {
            const res = algoResults[key];
            const meta = AppState.metadata && AppState.metadata.sorting ? AppState.metadata.sorting[key] : null;
            const label = meta ? meta.name : key;
            const color = this.getAlgoColor(key);

            return {
                label: label,
                data: res.comparisons,
                borderColor: color,
                backgroundColor: color,
                borderWidth: 2.5,
                tension: 0.25,
                pointRadius: 4,
                pointHoverRadius: 6
            };
        });

        // Destroy existing charts if any
        if (this.timeChart) this.timeChart.destroy();
        if (this.opsChart) this.opsChart.destroy();

        // Chart 1: Execution Time
        this.timeChart = new Chart(this.dom.timeCanvas, {
            type: 'line',
            data: {
                labels: sizes.map(s => `N=${s}`),
                datasets: timeDatasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: textColor, font: { family: 'Inter', size: 11 } }
                    },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => `${ctx.dataset.label}: ${ctx.raw} ms`
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: gridColor },
                        ticks: { color: textColor }
                    },
                    y: {
                        title: { display: true, text: 'Execution Time (ms)', color: textColor },
                        grid: { color: gridColor },
                        ticks: { color: textColor }
                    }
                }
            }
        });

        // Chart 2: Comparisons Count
        this.opsChart = new Chart(this.dom.opsCanvas, {
            type: 'line',
            data: {
                labels: sizes.map(s => `N=${s}`),
                datasets: opsDatasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: textColor, font: { family: 'Inter', size: 11 } }
                    },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => `${ctx.dataset.label}: ${ctx.raw.toLocaleString()} comparisons`
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: gridColor },
                        ticks: { color: textColor }
                    },
                    y: {
                        title: { display: true, text: 'Number of Comparisons', color: textColor },
                        grid: { color: gridColor },
                        ticks: { color: textColor }
                    }
                }
            }
        });
    }

    renderTable(data) {
        const tbody = this.dom.tableBody;
        tbody.innerHTML = '';

        const algoResults = data.algorithms;
        const sizes = data.sizes;
        const lastSizeIdx = sizes.length - 1;

        Object.keys(algoResults).forEach(key => {
            const res = algoResults[key];
            const meta = AppState.metadata && AppState.metadata.sorting ? AppState.metadata.sorting[key] : null;
            const name = meta ? meta.name : key;
            const theoClass = meta ? meta.avg_time : '—';

            // Show metrics for the largest tested N
            const maxN = sizes[lastSizeIdx];
            const timeVal = res.times_ms[lastSizeIdx];
            const compsVal = res.comparisons[lastSizeIdx];
            const swapsVal = res.swaps[lastSizeIdx];

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${name}</strong></td>
                <td><span style="font-family: var(--font-mono);">${maxN}</span></td>
                <td><span style="color: var(--accent); font-family: var(--font-mono); font-weight: 700;">${timeVal} ms</span></td>
                <td><span style="font-family: var(--font-mono);">${compsVal.toLocaleString()}</span></td>
                <td><span style="font-family: var(--font-mono);">${swapsVal.toLocaleString()}</span></td>
                <td><span class="badge badge-purple">${theoClass}</span></td>
            `;
            tbody.appendChild(tr);
        });
    }

    resizeCharts() {
        if (this.timeChart) this.timeChart.resize();
        if (this.opsChart) this.opsChart.resize();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.ComplexityAnalyzer = new ComplexityAnalyzer();
});
