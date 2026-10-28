"""
Backtracking Algorithms module: N-Queens Problem and Sudoku Solver.
Designed for DAA (Design and Analysis of Algorithms).
"""

from typing import List, Dict, Any, Optional
import copy

BACKTRACKING_METADATA = {
    "n_queens": {
        "name": "N-Queens Problem",
        "paradigm": "Backtracking / State-Space Tree Exploration",
        "time_complexity": "O(N!)",
        "space_complexity": "O(N)",
        "description": "Places N chess queens on an N×N board such that no two queens threaten each other (no shared row, column, or diagonal).",
        "pseudocode": [
            "procedure solveNQueens(board, row, N):",
            "    if row = N then:",
            "        addSolution(board); return true",
            "    for col := 0 to N - 1 do:",
            "        if isSafe(board, row, col) then:",
            "            placeQueen(board, row, col)",
            "            solveNQueens(board, row + 1, N)",
            "            removeQueen(board, row, col)  // Backtrack",
            "    return false"
        ]
    },
    "sudoku_solver": {
        "name": "Sudoku Solver",
        "paradigm": "Constraint Satisfaction via Backtracking",
        "time_complexity": "O(9^(m)) where m is empty cells",
        "space_complexity": "O(m) recursion stack",
        "description": "Fills a 9×9 grid with digits 1 to 9 such that each row, column, and 3×3 subgrid contains each digit exactly once.",
        "pseudocode": [
            "procedure solveSudoku(grid):",
            "    find unassigned cell (row, col)",
            "    if none then return true  // Solved",
            "    for num := 1 to 9 do:",
            "        if isValid(grid, row, col, num) then:",
            "            grid[row][col] := num",
            "            if solveSudoku(grid) = true then return true",
            "            grid[row][col] := 0  // Backtrack",
            "    return false"
        ]
    }
}


def trace_n_queens(n: int = 4, max_steps: int = 400) -> List[Dict[str, Any]]:
    steps = []
    board = [-1] * n  # board[r] = column index where queen is placed in row r
    step_count = [0]
    solutions = []

    steps.append({
        "type": "init",
        "board": list(board),
        "row": 0,
        "col": 0,
        "n": n,
        "description": f"Initialized {n}x{n} chessboard. Finding placement for {n} non-attacking queens.",
        "pseudo_line": 0
    })

    def is_safe(row: int, col: int) -> tuple[bool, Optional[tuple[int, int]]]:
        for r in range(row):
            c = board[r]
            # Same column
            if c == col:
                return False, (r, c)
            # Same diagonal: |row - r| == |col - c|
            if abs(row - r) == abs(col - c):
                return False, (r, c)
        return True, None

    def solve(row: int):
        if step_count[0] >= max_steps:
            return

        if row == n:
            solutions.append(list(board))
            steps.append({
                "type": "solution_found",
                "board": list(board),
                "row": row,
                "col": -1,
                "n": n,
                "solution_index": len(solutions),
                "description": f"🎉 Solution #{len(solutions)} Found! All {n} queens safely placed.",
                "pseudo_line": 2
            })
            return

        for col in range(n):
            if step_count[0] >= max_steps:
                return

            step_count[0] += 1
            safe, conflict_pos = is_safe(row, col)

            if safe:
                board[row] = col
                steps.append({
                    "type": "place_queen",
                    "board": list(board),
                    "row": row,
                    "col": col,
                    "n": n,
                    "conflict": None,
                    "description": f"Queen placed at Row {row}, Col {col} (Valid position). Moving to row {row + 1}.",
                    "pseudo_line": 5
                })

                solve(row + 1)

                if step_count[0] >= max_steps:
                    return

                # Backtrack
                board[row] = -1
                step_count[0] += 1
                steps.append({
                    "type": "backtrack",
                    "board": list(board),
                    "row": row,
                    "col": col,
                    "n": n,
                    "conflict": None,
                    "description": f"Backtracking from Row {row}, Col {col}. Undoing queen placement.",
                    "pseudo_line": 7
                })
            else:
                steps.append({
                    "type": "conflict",
                    "board": list(board),
                    "row": row,
                    "col": col,
                    "n": n,
                    "conflict": conflict_pos,
                    "description": f"Row {row}, Col {col} conflicts with Queen at Row {conflict_pos[0]}, Col {conflict_pos[1]}.",
                    "pseudo_line": 4
                })

    solve(0)

    steps.append({
        "type": "finished",
        "board": list(board),
        "n": n,
        "total_solutions": len(solutions),
        "description": f"N-Queens search complete! Found {len(solutions)} valid solution(s) in {step_count[0]} state transitions.",
        "pseudo_line": 0
    })

    return steps


PRESET_SUDOKU = {
    "easy": [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],
    "mini_4x4": [
        [1, 0, 3, 0],
        [0, 0, 0, 2],
        [3, 0, 0, 0],
        [0, 1, 0, 4]
    ]
}


def trace_sudoku(grid_input: Optional[List[List[int]]] = None, max_steps: int = 500) -> List[Dict[str, Any]]:
    steps = []
    if not grid_input:
        grid_input = PRESET_SUDOKU["easy"]

    grid = [row[:] for row in grid_input]
    initial_fixed = [[(grid[r][c] != 0) for c in range(9)] for r in range(9)]
    step_count = [0]
    solved = [False]

    steps.append({
        "type": "init",
        "grid": [r[:] for r in grid],
        "fixed": initial_fixed,
        "description": "Sudoku Solver initialized. Starting row-major empty cell scan.",
        "pseudo_line": 0
    })

    def is_valid(r: int, c: int, val: int) -> tuple[bool, str]:
        # Check row
        for j in range(9):
            if j != c and grid[r][j] == val:
                return False, f"Row {r} already has value {val}"
        # Check column
        for i in range(9):
            if i != r and grid[i][c] == val:
                return False, f"Column {c} already has value {val}"
        # Check 3x3 box
        box_r, box_c = 3 * (r // 3), 3 * (c // 3)
        for i in range(box_r, box_r + 3):
            for j in range(box_c, box_c + 3):
                if (i != r or j != c) and grid[i][j] == val:
                    return False, f"3x3 Box already has value {val}"
        return True, "Valid"

    def find_empty() -> Optional[tuple[int, int]]:
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    return r, c
        return None

    def solve() -> bool:
        if step_count[0] >= max_steps:
            return False

        empty = find_empty()
        if not empty:
            solved[0] = True
            steps.append({
                "type": "solution_found",
                "grid": [r[:] for r in grid],
                "description": "🎉 Sudoku Puzzle Solved Successfully!",
                "pseudo_line": 2
            })
            return True

        r, c = empty
        for val in range(1, 10):
            if step_count[0] >= max_steps:
                return False

            step_count[0] += 1
            valid, reason = is_valid(r, c, val)

            if valid:
                grid[r][c] = val
                steps.append({
                    "type": "place_num",
                    "grid": [row[:] for row in grid],
                    "row": r,
                    "col": c,
                    "val": val,
                    "valid": True,
                    "description": f"Trying value {val} at ({r}, {c}). Constraint check passed.",
                    "pseudo_line": 5
                })

                if solve():
                    return True

                if step_count[0] >= max_steps:
                    return False

                # Backtrack
                grid[r][c] = 0
                step_count[0] += 1
                steps.append({
                    "type": "backtrack",
                    "grid": [row[:] for row in grid],
                    "row": r,
                    "col": c,
                    "val": 0,
                    "description": f"Dead end reached. Backtracking cell ({r}, {c}) to empty.",
                    "pseudo_line": 7
                })
            else:
                steps.append({
                    "type": "invalid_num",
                    "grid": [row[:] for row in grid],
                    "row": r,
                    "col": c,
                    "val": val,
                    "valid": False,
                    "description": f"Cannot place {val} at ({r}, {c}): {reason}.",
                    "pseudo_line": 4
                })

        return False

    solve()

    steps.append({
        "type": "finished",
        "grid": [r[:] for r in grid],
        "solved": solved[0],
        "steps_recorded": step_count[0],
        "description": f"Solver step sequence ended ({step_count[0]} steps recorded).",
        "pseudo_line": 0
    })
    return steps
