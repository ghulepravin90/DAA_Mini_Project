"""
Flask Web Application for Algorithm Visualizer and Complexity Analyzer (DAA Mini Project).
Author: DAA Project
"""

import os
import sys
import random
from flask import Flask, render_template, request, jsonify

from algorithms.sorting import SORTING_METADATA, SORT_DISPATCHER
from algorithms.searching import SEARCH_METADATA, trace_linear_search, trace_binary_search
from algorithms.graphs import (
    GRAPH_METADATA, PRESET_GRAPHS, trace_bfs, trace_dfs, trace_dijkstra
)
from algorithms.backtracking import (
    BACKTRACKING_METADATA, PRESET_SUDOKU, trace_n_queens, trace_sudoku
)
from algorithms.benchmark import (
    run_sorting_benchmark, run_searching_benchmark, generate_array
)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    """Returns theoretical complexities, paradigms, and pseudocodes for all algorithms."""
    return jsonify({
        "sorting": SORTING_METADATA,
        "searching": SEARCH_METADATA,
        "graphs": GRAPH_METADATA,
        "backtracking": BACKTRACKING_METADATA,
        "preset_graphs": PRESET_GRAPHS,
        "preset_sudoku": PRESET_SUDOKU
    })


@app.route('/api/generate_array', methods=['POST'])
def api_generate_array():
    data = request.get_json() or {}
    size = int(data.get('size', 16))
    distribution = data.get('distribution', 'random')
    # Limit size between 5 and 64 for visualization clarity
    size = max(5, min(size, 64))
    arr = generate_array(size, distribution)
    return jsonify({"array": arr, "size": len(arr), "distribution": distribution})


@app.route('/api/sort', methods=['POST'])
def api_sort():
    data = request.get_json() or {}
    algorithm = data.get('algorithm', 'merge_sort')
    arr = data.get('array', [])
    algorithm2 = data.get('algorithm2')  # For dual comparison / race mode

    if not arr:
        arr = [34, 12, 89, 45, 23, 7, 56, 91, 18, 62]

    # Bound array size for visualizer trace
    if len(arr) > 60:
        arr = arr[:60]

    if algorithm not in SORT_DISPATCHER:
        return jsonify({"error": f"Unknown algorithm: {algorithm}"}), 400

    trace1 = SORT_DISPATCHER[algorithm](list(arr))
    meta1 = SORTING_METADATA.get(algorithm, {})

    response = {
        "algorithm": algorithm,
        "meta": meta1,
        "trace": trace1,
        "total_steps": len(trace1)
    }

    if algorithm2 and algorithm2 in SORT_DISPATCHER:
        trace2 = SORT_DISPATCHER[algorithm2](list(arr))
        meta2 = SORTING_METADATA.get(algorithm2, {})
        response["comparison"] = {
            "algorithm": algorithm2,
            "meta": meta2,
            "trace": trace2,
            "total_steps": len(trace2)
        }

    return jsonify(response)


@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.get_json() or {}
    algorithm = data.get('algorithm', 'binary_search')
    arr = data.get('array', [12, 23, 34, 45, 56, 67, 78, 89, 90])
    target = data.get('target')

    if target is None:
        target = arr[len(arr) // 2]
    else:
        try:
            target = int(target)
        except ValueError:
            target = 45

    if algorithm == 'linear_search':
        trace = trace_linear_search(arr, target)
    elif algorithm == 'binary_search':
        trace = trace_binary_search(arr, target)
    else:
        return jsonify({"error": f"Unknown search algorithm: {algorithm}"}), 400

    meta = SEARCH_METADATA.get(algorithm, {})
    return jsonify({
        "algorithm": algorithm,
        "target": target,
        "meta": meta,
        "trace": trace,
        "total_steps": len(trace)
    })


@app.route('/api/graph', methods=['POST'])
def api_graph():
    data = request.get_json() or {}
    algorithm = data.get('algorithm', 'dijkstra')
    graph_type = data.get('graph_type', 'standard')
    start_node = data.get('start_node', 'A')
    end_node = data.get('end_node', 'F')

    if graph_type in PRESET_GRAPHS:
        graph_data = PRESET_GRAPHS[graph_type]
    elif "custom_graph" in data:
        graph_data = data["custom_graph"]
    else:
        graph_data = PRESET_GRAPHS['standard']

    # Ensure start node exists
    valid_ids = [n["id"] for n in graph_data["nodes"]]
    if start_node not in valid_ids:
        start_node = valid_ids[0]

    if algorithm == 'bfs':
        trace = trace_bfs(graph_data, start_node)
    elif algorithm == 'dfs':
        trace = trace_dfs(graph_data, start_node)
    elif algorithm == 'dijkstra':
        trace = trace_dijkstra(graph_data, start_node, end_node)
    else:
        return jsonify({"error": f"Unknown graph algorithm: {algorithm}"}), 400

    meta = GRAPH_METADATA.get(algorithm, {})
    return jsonify({
        "algorithm": algorithm,
        "graph_data": graph_data,
        "meta": meta,
        "trace": trace,
        "total_steps": len(trace)
    })


@app.route('/api/backtrack', methods=['POST'])
def api_backtrack():
    data = request.get_json() or {}
    algorithm = data.get('algorithm', 'n_queens')

    if algorithm == 'n_queens':
        n = int(data.get('n', 4))
        n = max(4, min(n, 8))  # 4 to 8 for fast, clean rendering
        trace = trace_n_queens(n)
        meta = BACKTRACKING_METADATA.get("n_queens", {})
        return jsonify({
            "algorithm": "n_queens",
            "n": n,
            "meta": meta,
            "trace": trace,
            "total_steps": len(trace)
        })
    elif algorithm == 'sudoku':
        preset_key = data.get('preset', 'easy')
        grid = data.get('grid')
        if not grid and preset_key in PRESET_SUDOKU:
            grid = PRESET_SUDOKU[preset_key]
        trace = trace_sudoku(grid)
        meta = BACKTRACKING_METADATA.get("sudoku_solver", {})
        return jsonify({
            "algorithm": "sudoku",
            "meta": meta,
            "trace": trace,
            "total_steps": len(trace)
        })
    else:
        return jsonify({"error": f"Unknown backtracking algorithm: {algorithm}"}), 400


@app.route('/api/benchmark/sorting', methods=['POST'])
def api_benchmark_sorting():
    data = request.get_json() or {}
    algorithms = data.get('algorithms', ['bubble_sort', 'merge_sort', 'quick_sort'])
    sizes = data.get('sizes', [50, 100, 200, 500, 1000])
    distribution = data.get('distribution', 'random')
    # Filter sizes to prevent huge slowdowns in browser
    sizes = [max(10, min(s, 2000)) for s in sizes]

    bench_results = run_sorting_benchmark(algorithms, sizes, distribution)
    return jsonify(bench_results)


@app.route('/api/benchmark/searching', methods=['POST'])
def api_benchmark_searching():
    data = request.get_json() or {}
    sizes = data.get('sizes', [100, 500, 1000, 5000, 10000])
    target_position = data.get('target_position', 'random')
    bench_results = run_searching_benchmark(sizes, target_position)
    return jsonify(bench_results)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"================================================================")
    print(f"🚀 DAA Algorithm Visualizer & Complexity Analyzer is running!")
    print(f"📍 Open in your browser: http://127.0.0.1:{port}")
    print(f"================================================================")
    app.run(host='127.0.0.1', port=port, debug=False)
