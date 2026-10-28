/**
 * AlgoScope - Main Controller & Audio Synthesizer
 * Handles Navigation, Theme, Audio API, and Global Metadata
 */

const AppState = {
    metadata: null,
    audioEnabled: false,
    audioCtx: null,
    activeTab: 'tab-sorting'
};

// Web Audio API Sound Synthesizer
class SoundSynthesizer {
    constructor() {
        this.ctx = null;
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
        }
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    playTone(val, minVal = 5, maxVal = 100, duration = 0.05) {
        if (!AppState.audioEnabled) return;
        try {
            this.init();
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            // Map value to frequency between 180Hz and 880Hz
            const norm = Math.max(0, Math.min(1, (val - minVal) / (maxVal - minVal || 1)));
            const freq = 180 + norm * 700;

            osc.type = 'triangle';
            osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

            gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start();
            osc.stop(this.ctx.currentTime + duration);
        } catch (e) {
            console.warn("Audio play error", e);
        }
    }
}

const soundSynth = new SoundSynthesizer();

// DOM Initialization
document.addEventListener('DOMContentLoaded', async () => {
    initNavigation();
    initThemeToggle();
    initAudioToggle();
    await fetchMetadata();
});

// Tab Navigation
function initNavigation() {
    const tabs = document.querySelectorAll('.nav-tab-btn');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetId = tab.getAttribute('data-tab');
            tabs.forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

            tab.classList.add('active');
            const targetPane = document.getElementById(targetId);
            if (targetPane) targetPane.classList.add('active');
            AppState.activeTab = targetId;

            // Trigger canvas or chart resize if needed
            if (targetId === 'tab-graphs' && window.GraphVisualizer) {
                window.GraphVisualizer.draw();
            } else if (targetId === 'tab-analyzer' && window.ComplexityAnalyzer) {
                window.ComplexityAnalyzer.resizeCharts();
            }
        });
    });
}

// Theme Toggle
function initThemeToggle() {
    const btn = document.getElementById('btnThemeToggle');
    const html = document.documentElement;

    btn.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme') || 'dark';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', newTheme);
        btn.innerHTML = newTheme === 'dark' ? '🌙' : '☀️';
        localStorage.setItem('algoscope_theme', newTheme);
    });

    const savedTheme = localStorage.getItem('algoscope_theme');
    if (savedTheme) {
        html.setAttribute('data-theme', savedTheme);
        btn.innerHTML = savedTheme === 'dark' ? '🌙' : '☀️';
    }
}

// Audio Toggle
function initAudioToggle() {
    const btn = document.getElementById('btnAudioToggle');
    btn.addEventListener('click', () => {
        AppState.audioEnabled = !AppState.audioEnabled;
        if (AppState.audioEnabled) {
            soundSynth.init();
            btn.classList.add('active');
            btn.innerHTML = '🔊';
            btn.title = 'Sound Synthesizer: ON';
        } else {
            btn.classList.remove('active');
            btn.innerHTML = '🔇';
            btn.title = 'Sound Synthesizer: OFF';
        }
    });
}

// Fetch Global Metadata from Flask Backend
async function fetchMetadata() {
    try {
        const res = await fetch('/api/metadata');
        const data = await res.json();
        AppState.metadata = data;

        // Dispatch ready event for components
        window.dispatchEvent(new CustomEvent('algoscope_meta_ready', { detail: data }));
    } catch (err) {
        console.error('Failed to fetch algorithm metadata:', err);
    }
}

// Helper: render pseudocode lines into container
function renderPseudocode(containerId, pseudocodeList, activeLineIndex = -1) {
    const container = document.getElementById(containerId);
    if (!container || !pseudocodeList) return;

    container.innerHTML = pseudocodeList.map((line, idx) => {
        const isActive = (idx === activeLineIndex) ? ' active' : '';
        const lineNum = (idx + 1).toString().padStart(2, '0');
        return `<div class="code-line${isActive}"><span style="color: var(--text-muted); margin-right: 8px;">${lineNum}</span>${escapeHtml(line)}</div>`;
    }).join('');

    // Scroll active line into view smoothly
    const activeEl = container.querySelector('.code-line.active');
    if (activeEl) {
        activeEl.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
