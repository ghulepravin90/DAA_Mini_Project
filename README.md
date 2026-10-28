# AlgoScope — Algorithm Visualizer & Complexity Analyzer
**A Comprehensive Interactive Platform for Design and Analysis of Algorithms (DAA)**

---

## 📌 1. Project Overview & Objectives

**AlgoScope** is an interactive, academic-grade web platform developed for the **Design and Analysis of Algorithms (DAA)** curriculum. It bridges the gap between theoretical algorithm analysis and empirical runtime behavior through:

1. **Step-by-Step Visualization**: Granular inspection of state transitions, pointer updates, and recursive state-space trees with speed control, step-by-step navigation, and sound synthesis.
2. **Dual-Algorithm Race Comparison**: Direct side-by-side execution of two sorting algorithms on identical data sets to visualize efficiency differences in real time.
3. **Empirical vs. Theoretical Complexity Analysis**: Real Python CPU execution time and operation counter measurements across varying input sizes ($N = 50 \dots 2000$), plotted interactively with theoretical asymptotic curves.
4. **Interactive Pseudocode Highlighting**: Simultaneous line-by-line tracing of formal DAA pseudocode as the algorithm executes.
5. **DAA Viva & Examination Guide**: Curated theoretical cheat sheet, Master Theorem formulations, and answers to common oral examination questions.

---

## 🗂️ 2. Algorithms Implemented

### 📊 Sorting Algorithms
| Algorithm | Paradigm | Best Case | Average Case | Worst Case | Auxiliary Space | Stable? | In-Place? |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Merge Sort** | Divide & Conquer | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Yes | No |
| **Quick Sort** | Divide & Conquer (Partitioning) | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ | No | Yes |
| **Heap Sort** | Selection / Max-Heap | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(1)$ | No | Yes |
| **Insertion Sort**| Incremental | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes | Yes |
| **Bubble Sort** | Brute Force / Exchange | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes | Yes |
| **Selection Sort**| Greedy / Selection | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | No | Yes |

### 🔍 Searching Algorithms
| Algorithm | Paradigm | Best Case | Average Case | Worst Case | Auxiliary Space | Prerequisite |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Binary Search** | Decrease & Conquer | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(1)$ | Sorted Array |
| **Linear Search** | Brute Force / Sequential | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ | None |

### 🕸️ Graph Algorithms
| Algorithm | Paradigm | Time Complexity | Auxiliary Space | Key Characteristics |
| :--- | :--- | :---: | :---: | :--- |
| **Breadth-First Search (BFS)** | Level-Order (FIFO Queue) | $O(V + E)$ | $O(V)$ | Finds shortest path in unweighted graphs |
| **Depth-First Search (DFS)** | Backtracking (LIFO Stack) | $O(V + E)$ | $O(V)$ | Cycle detection, topological sorting |
| **Dijkstra's Algorithm** | Greedy (Min-Heap / PQ) | $O((V + E) \log V)$ | $O(V)$ | Single-source shortest path (non-negative weights) |

### ♟️ Backtracking Algorithms
| Algorithm | Paradigm | Worst Time | Space | Constraints Checked |
| :--- | :--- | :---: | :---: | :--- |
| **N-Queens Problem** | State-Space Tree Exploration | $O(N!)$ | $O(N)$ | Row, column, and diagonal conflicts |
| **Sudoku Solver** | Constraint Satisfaction | $O(9^{m})$ | $O(m)$ | Row, column, and $3 \times 3$ subgrid duplicates |

---

## 🏗️ 3. System Architecture & Tech Stack

```
algo_visualizer_daa/
├── app.py                     # Flask REST API backend & server
├── requirements.txt           # Python dependencies (flask)
├── run.bat                    # One-click Windows runner
├── run.sh                     # Linux/Mac runner
├── README.md                  # Complete documentation & project report
├── algorithms/
│   ├── __init__.py
│   ├── sorting.py             # Sorting engines + step trace generators
│   ├── searching.py           # Linear & Binary search tracers
│   ├── graphs.py              # BFS, DFS, Dijkstra algorithms & graph structures
│   ├── backtracking.py        # N-Queens & Sudoku solver tracers
│   └── benchmark.py           # Real CPU timing (perf_counter) & operation counters
├── templates/
│   └── index.html             # Single Page Application (SPA) dashboard layout
└── static/
    ├── css/
    │   └── style.css          # Modern dark/light theme, slate palette, animations
    └── js/
        ├── main.js            # Tabs, theme toggle, Web Audio API sound synthesizer
        ├── sorting_visualizer.js      # Bar chart animation, dual race comparative engine
        ├── searching_visualizer.js    # Array cell inspection & pointer tag visualizer
        ├── graph_visualizer.js        # HTML5 Canvas node-edge traversal & shortest paths
        ├── backtracking_visualizer.js # Chessboard and Sudoku state-space visualizer
        └── complexity_analyzer.js     # Chart.js empirical benchmarking vs Big-O curves
```

### Core Technologies:
- **Backend**: Python 3.10+, Flask
- **Frontend**: HTML5, CSS3 (Modern Flexbox/Grid), JavaScript (ES6+), HTML5 Canvas
- **Visual Analytics**: Chart.js for empirical benchmarking plots
- **Audio Synthesis**: Web Audio API oscillator for frequency-mapped auditory feedback during execution

---

## 🚀 4. How to Run the Project

### Prerequisites:
Make sure Python 3.8+ is installed on your machine.

### Installation:
1. Open a terminal or Command Prompt in the project folder:
   ```bash
   cd "C:\Users\Pravin Ghule\.gemini\antigravity\scratch\algo_visualizer_daa"
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Execution:
- **Windows**: Double-click `run.bat` or run:
  ```cmd
  python app.py
  ```
- **Linux / macOS**:
  ```bash
  python app.py
  ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 💡 5. Key Features & Walkthrough

1. **Dual Race Comparative Mode**:
   - Check the **"Dual Race Mode"** box in the Sorting tab to select two algorithms (e.g., *Quick Sort* vs. *Merge Sort*) and watch them sort identical arrays side by side.
2. **Web Audio Synthesizer**:
   - Click the 🔊 icon in the upper right to enable audio beeps mapped to the element values being compared.
3. **Real Empirical Complexity Benchmark**:
   - Navigate to the **📈 Complexity Analyzer** tab, select which algorithms and input sizes ($N$) to test, and click **Run Empirical Benchmark**.
   - The backend runs real Python benchmarks using `time.perf_counter()` and plots the actual execution curves vs. Big-O mathematical predictions.
4. **Interactive Pseudocode Tracing**:
   - As the visualization advances, the corresponding line in the DAA pseudocode panel is highlighted in real time.

---

## 🎓 6. DAA Viva Voce Questions & Answers

### Q1: Why does Quick Sort achieve $O(n \log n)$ on average but $O(n^2)$ in the worst case?
> **Answer**: Quick Sort's performance depends on the pivot selection. If the pivot divides the array into roughly equal halves ($\frac{n}{2}$ and $\frac{n}{2}$), the recursion tree has depth $\log_2 n$, giving $O(n \log n)$ total work. If the pivot consistently turns out to be the minimum or maximum element (e.g., sorting an already-sorted array with the last element as pivot), the partition is unbalanced ($1$ and $n-1$), yielding a recursion depth of $n$ and $O(n^2)$ runtime. Randomized pivot selection or Median-of-Three solves this issue.

### Q2: What is the Master Theorem and when can it NOT be applied?
> **Answer**: The Master Theorem solves recurrences of the form $T(n) = a T(n / b) + f(n)$ where $a \ge 1$ and $b > 1$. It compares $f(n)$ with $n^{\log_b a}$.
> It **cannot** be applied when:
> - $T(n)$ is non-polynomial (e.g., $T(n) = 2T(n/2) + n!$).
> - $a$ is not a constant (e.g., $T(n) = n T(n/2) + n$).
> - $b \le 1$ or subproblems have non-uniform sizes (e.g., $T(n) = T(n-1) + n$).

### Q3: Why is Dijkstra's algorithm greedy, and why does it fail on negative edge weights?
> **Answer**: Dijkstra makes the greedy choice by permanently fixing the shortest distance to the unvisited vertex with the minimum tentative distance. Once a vertex is extracted from the Priority Queue, it is never reconsidered. If an edge has a negative weight, a longer path with fewer hops could later be reduced below the greedy distance, making the algorithm produce incorrect results. For negative weights, the Bellman-Ford algorithm ($O(VE)$) or Floyd-Warshall ($O(V^3)$) must be used.
