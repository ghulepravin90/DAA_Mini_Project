"""
Graph Algorithms module: BFS, DFS, and Dijkstra's Shortest Path.
Designed for DAA (Design and Analysis of Algorithms).
"""

from typing import Dict, List, Any, Optional
import heapq

GRAPH_METADATA = {
    "bfs": {
        "name": "Breadth-First Search (BFS)",
        "paradigm": "Level-Order Traversal (Queue-based)",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "description": "Explores the graph level by level from the source node using a FIFO queue. Guarantees the shortest path on unweighted graphs.",
        "pseudocode": [
            "procedure BFS(G, start_v):",
            "    let Q be a Queue",
            "    label start_v as visited; Q.enqueue(start_v)",
            "    while Q is not empty do:",
            "        v := Q.dequeue()",
            "        for each neighbor w of v in G.adjacentEdges(v) do:",
            "            if w is not visited then:",
            "                label w as visited; Q.enqueue(w)"
        ]
    },
    "dfs": {
        "name": "Depth-First Search (DFS)",
        "paradigm": "Deep Exploration / Backtracking (Stack-based)",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V) (recursion stack)",
        "description": "Explores as far as possible along each branch before backtracking using a LIFO stack or recursion.",
        "pseudocode": [
            "procedure DFS(G, v):",
            "    label v as visited",
            "    for each neighbor w of v in G.adjacentEdges(v) do:",
            "        if w is not visited then:",
            "            DFS(G, w)  // Recursive exploration"
        ]
    },
    "dijkstra": {
        "name": "Dijkstra's Algorithm",
        "paradigm": "Greedy Method",
        "time_complexity": "O((V + E) log V)",
        "space_complexity": "O(V)",
        "description": "Finds the shortest paths between nodes in a weighted graph with non-negative edge weights using a Greedy Priority Queue.",
        "pseudocode": [
            "procedure Dijkstra(G, source):",
            "    dist[s] := 0; dist[v] := infinity for all other v",
            "    insert all vertices into PriorityQueue Q with key dist[v]",
            "    while Q is not empty do:",
            "        u := extract_min(Q)",
            "        for each neighbor v of u do:",
            "            alt := dist[u] + weight(u, v)",
            "            if alt < dist[v] then:",
            "                dist[v] := alt; parent[v] := u; decrease_key(Q, v)"
        ]
    }
}

# Standard Preset Graphs with predefined 2D canvas coordinates
PRESET_GRAPHS = {
    "standard": {
        "nodes": [
            {"id": "A", "x": 120, "y": 120},
            {"id": "B", "x": 280, "y": 60},
            {"id": "C", "x": 280, "y": 200},
            {"id": "D", "x": 440, "y": 60},
            {"id": "E", "x": 440, "y": 200},
            {"id": "F", "x": 600, "y": 130}
        ],
        "edges": [
            {"u": "A", "v": "B", "weight": 4},
            {"u": "A", "v": "C", "weight": 2},
            {"u": "B", "v": "C", "weight": 1},
            {"u": "B", "v": "D", "weight": 5},
            {"u": "C", "v": "E", "weight": 8},
            {"u": "C", "v": "D", "weight": 10},
            {"u": "D", "v": "E", "weight": 2},
            {"u": "D", "v": "F", "weight": 6},
            {"u": "E", "v": "F", "weight": 3}
        ]
    },
    "tree": {
        "nodes": [
            {"id": "R", "x": 360, "y": 50},
            {"id": "A", "x": 200, "y": 130},
            {"id": "B", "x": 520, "y": 130},
            {"id": "C", "x": 120, "y": 220},
            {"id": "D", "x": 280, "y": 220},
            {"id": "E", "x": 440, "y": 220},
            {"id": "F", "x": 600, "y": 220}
        ],
        "edges": [
            {"u": "R", "v": "A", "weight": 3},
            {"u": "R", "v": "B", "weight": 5},
            {"u": "A", "v": "C", "weight": 2},
            {"u": "A", "v": "D", "weight": 4},
            {"u": "B", "v": "E", "weight": 1},
            {"u": "B", "v": "F", "weight": 6}
        ]
    }
}


def build_adj_list(nodes: List[Dict], edges: List[Dict], directed: bool = False):
    adj = {node["id"]: [] for node in nodes}
    for e in edges:
        u = e["u"]
        v = e["v"]
        w = e.get("weight", 1)
        adj[u].append((v, w))
        if not directed:
            adj[v].append((u, w))
    return adj


def trace_bfs(graph_data: Dict[str, Any], start_node: str) -> List[Dict[str, Any]]:
    nodes = graph_data["nodes"]
    edges = graph_data["edges"]
    adj = build_adj_list(nodes, edges)

    steps = []
    visited = set()
    queue = [start_node]
    visited.add(start_node)
    traversal_order = []
    active_edge = None

    steps.append({
        "type": "init",
        "current_node": start_node,
        "active_edge": None,
        "queue": list(queue),
        "visited": list(visited),
        "traversal": list(traversal_order),
        "description": f"BFS initialized at starting vertex '{start_node}'. Added to Queue and marked visited.",
        "pseudo_line": 2
    })

    while queue:
        u = queue.pop(0)
        traversal_order.append(u)

        steps.append({
            "type": "dequeue",
            "current_node": u,
            "active_edge": None,
            "queue": list(queue),
            "visited": list(visited),
            "traversal": list(traversal_order),
            "description": f"Dequeued vertex '{u}'. Now inspecting its adjacent neighbors.",
            "pseudo_line": 4
        })

        for v, weight in sorted(adj[u], key=lambda x: x[0]):
            edge_id = f"{u}-{v}"
            if v not in visited:
                visited.add(v)
                queue.append(v)
                steps.append({
                    "type": "visit_neighbor",
                    "current_node": u,
                    "target_node": v,
                    "active_edge": edge_id,
                    "queue": list(queue),
                    "visited": list(visited),
                    "traversal": list(traversal_order),
                    "description": f"Discovered unvisited neighbor '{v}' via edge ({u}, {v}). Enqueued '{v}'.",
                    "pseudo_line": 6
                })
            else:
                steps.append({
                    "type": "already_visited",
                    "current_node": u,
                    "target_node": v,
                    "active_edge": edge_id,
                    "queue": list(queue),
                    "visited": list(visited),
                    "traversal": list(traversal_order),
                    "description": f"Neighbor '{v}' is already visited. Skipping edge ({u}, {v}).",
                    "pseudo_line": 5
                })

    steps.append({
        "type": "finished",
        "current_node": None,
        "active_edge": None,
        "queue": [],
        "visited": list(visited),
        "traversal": list(traversal_order),
        "description": f"BFS Complete! Visited {len(traversal_order)} vertices in order: {' → '.join(traversal_order)}.",
        "pseudo_line": 0
    })
    return steps


def trace_dfs(graph_data: Dict[str, Any], start_node: str) -> List[Dict[str, Any]]:
    nodes = graph_data["nodes"]
    edges = graph_data["edges"]
    adj = build_adj_list(nodes, edges)

    steps = []
    visited = set()
    traversal_order = []
    call_stack = []

    steps.append({
        "type": "init",
        "current_node": start_node,
        "active_edge": None,
        "stack": [start_node],
        "visited": [],
        "traversal": [],
        "description": f"DFS initialized. Calling DFS on root vertex '{start_node}'.",
        "pseudo_line": 0
    })

    def dfs_rec(u: str, parent: Optional[str] = None):
        visited.add(u)
        traversal_order.append(u)
        call_stack.append(u)

        edge_id = f"{parent}-{u}" if parent else None
        steps.append({
            "type": "visit_node",
            "current_node": u,
            "active_edge": edge_id,
            "stack": list(call_stack),
            "visited": list(visited),
            "traversal": list(traversal_order),
            "description": f"Visited vertex '{u}'. Pushed to Call Stack.",
            "pseudo_line": 1
        })

        for v, weight in sorted(adj[u], key=lambda x: x[0]):
            candidate_edge = f"{u}-{v}"
            if v not in visited:
                steps.append({
                    "type": "explore_edge",
                    "current_node": u,
                    "target_node": v,
                    "active_edge": candidate_edge,
                    "stack": list(call_stack),
                    "visited": list(visited),
                    "traversal": list(traversal_order),
                    "description": f"Branching deeper from '{u}' into unvisited neighbor '{v}'.",
                    "pseudo_line": 4
                })
                dfs_rec(v, u)
            elif v != parent:
                steps.append({
                    "type": "back_edge",
                    "current_node": u,
                    "target_node": v,
                    "active_edge": candidate_edge,
                    "stack": list(call_stack),
                    "visited": list(visited),
                    "traversal": list(traversal_order),
                    "description": f"Neighbor '{v}' already visited (Cycle/Back Edge detected).",
                    "pseudo_line": 3
                })

        call_stack.pop()
        steps.append({
            "type": "backtrack",
            "current_node": u,
            "active_edge": None,
            "stack": list(call_stack),
            "visited": list(visited),
            "traversal": list(traversal_order),
            "description": f"All edges from '{u}' explored. Backtracking from '{u}'.",
            "pseudo_line": 4
        })

    dfs_rec(start_node)

    steps.append({
        "type": "finished",
        "current_node": None,
        "active_edge": None,
        "stack": [],
        "visited": list(visited),
        "traversal": list(traversal_order),
        "description": f"DFS Complete! Traversal order: {' → '.join(traversal_order)}.",
        "pseudo_line": 0
    })
    return steps


def trace_dijkstra(graph_data: Dict[str, Any], start_node: str, end_node: Optional[str] = None) -> List[Dict[str, Any]]:
    nodes = graph_data["nodes"]
    edges = graph_data["edges"]
    adj = build_adj_list(nodes, edges)

    steps = []
    dist = {n["id"]: float("inf") for n in nodes}
    parent = {n["id"]: None for n in nodes}
    dist[start_node] = 0

    # Priority queue stores tuples of (distance, node_id)
    pq = [(0, start_node)]
    visited = set()

    steps.append({
        "type": "init",
        "current_node": start_node,
        "distances": {k: ("∞" if v == float("inf") else v) for k, v in dist.items()},
        "pq": [(d, n) for d, n in pq],
        "visited": list(visited),
        "parents": dict(parent),
        "description": f"Dijkstra initialized with source '{start_node}'. dist[{start_node}]=0, all other dist=∞.",
        "pseudo_line": 1
    })

    while pq:
        current_dist, u = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)
        steps.append({
            "type": "extract_min",
            "current_node": u,
            "distances": {k: ("∞" if v == float("inf") else v) for k, v in dist.items()},
            "pq": [(d, n) for d, n in pq],
            "visited": list(visited),
            "parents": dict(parent),
            "description": f"Extracted vertex '{u}' with minimum tentative distance {current_dist}.",
            "pseudo_line": 4
        })

        if end_node and u == end_node:
            steps.append({
                "type": "target_reached",
                "current_node": u,
                "distances": {k: ("∞" if v == float("inf") else v) for k, v in dist.items()},
                "pq": [(d, n) for d, n in pq],
                "visited": list(visited),
                "parents": dict(parent),
                "description": f"Reached target destination '{end_node}' with optimal cost {current_dist}.",
                "pseudo_line": 4
            })
            break

        for v, weight in sorted(adj[u], key=lambda x: x[0]):
            edge_id = f"{u}-{v}"
            if v not in visited:
                new_dist = current_dist + weight
                steps.append({
                    "type": "inspect_edge",
                    "current_node": u,
                    "neighbor": v,
                    "active_edge": edge_id,
                    "edge_weight": weight,
                    "distances": {k: ("∞" if v == float("inf") else v) for k, v in dist.items()},
                    "pq": [(d, n) for d, n in pq],
                    "visited": list(visited),
                    "parents": dict(parent),
                    "description": f"Relaxation check: dist[{u}]({current_dist}) + weight({weight}) = {new_dist} vs current dist[{v}]({dist[v]}).",
                    "pseudo_line": 6
                })

                if new_dist < dist[v]:
                    old_dist = dist[v]
                    dist[v] = new_dist
                    parent[v] = u
                    heapq.heappush(pq, (new_dist, v))
                    steps.append({
                        "type": "relax_edge",
                        "current_node": u,
                        "neighbor": v,
                        "active_edge": edge_id,
                        "edge_weight": weight,
                        "distances": {k: ("∞" if v == float("inf") else v) for k, v in dist.items()},
                        "pq": [(d, n) for d, n in pq],
                        "visited": list(visited),
                        "parents": dict(parent),
                        "description": f"Relaxed edge ({u}, {v})! Updated dist[{v}] from {old_dist} to {new_dist}.",
                        "pseudo_line": 7
                    })

    # Reconstruct shortest paths
    shortest_paths = {}
    for node in nodes:
        n_id = node["id"]
        path = []
        curr = n_id
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        path.reverse()
        if path and path[0] == start_node:
            shortest_paths[n_id] = path

    steps.append({
        "type": "finished",
        "current_node": None,
        "distances": {k: ("∞" if v == float("inf") else v) for k, v in dist.items()},
        "pq": [],
        "visited": list(visited),
        "parents": dict(parent),
        "shortest_paths": shortest_paths,
        "description": "Dijkstra execution finished. All shortest paths computed from source.",
        "pseudo_line": 0
    })
    return steps
