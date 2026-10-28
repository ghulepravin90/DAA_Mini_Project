"""
Searching Algorithms module with step-by-step trace generation.
Designed for DAA (Design and Analysis of Algorithms).
"""

from typing import List, Dict, Any

SEARCH_METADATA = {
    "linear_search": {
        "name": "Linear Search",
        "paradigm": "Brute Force / Sequential",
        "best_time": "O(1)",
        "avg_time": "O(n)",
        "worst_time": "O(n)",
        "space": "O(1)",
        "requires_sorted": False,
        "description": "Sequentially checks each element of the list until a match is found or the whole list has been searched.",
        "pseudocode": [
            "procedure linearSearch(A, target):",
            "    for i := 0 to length(A) - 1 do:",
            "        if A[i] = target then:",
            "            return i  // Target found at index i",
            "    return -1  // Target not present"
        ]
    },
    "binary_search": {
        "name": "Binary Search",
        "paradigm": "Decrease and Conquer (Interval Halving)",
        "best_time": "O(1)",
        "avg_time": "O(log n)",
        "worst_time": "O(log n)",
        "space": "O(1)",
        "requires_sorted": True,
        "description": "Repeatedly targets the center of the sorted search space, halving the range depending on whether the target is smaller or larger than the midpoint.",
        "pseudocode": [
            "procedure binarySearch(A, target):",
            "    low := 0, high := length(A) - 1",
            "    while low <= high do:",
            "        mid := floor((low + high) / 2)",
            "        if A[mid] = target then: return mid",
            "        else if A[mid] < target then: low := mid + 1",
            "        else: high := mid - 1",
            "    return -1  // Not found"
        ]
    }
}


def trace_linear_search(arr: List[int], target: int) -> List[Dict[str, Any]]:
    steps = []
    n = len(arr)
    comparisons = 0

    steps.append({
        "type": "init",
        "array": list(arr),
        "target": target,
        "current_idx": None,
        "found": False,
        "description": f"Searching for target {target} in array of {n} elements.",
        "pseudo_line": 0,
        "comparisons": 0
    })

    found_index = -1
    for i in range(n):
        comparisons += 1
        steps.append({
            "type": "inspect",
            "array": list(arr),
            "target": target,
            "current_idx": i,
            "found": False,
            "description": f"Checking index {i}: A[{i}] = {arr[i]}. Comparing with target {target}.",
            "pseudo_line": 2,
            "comparisons": comparisons
        })

        if arr[i] == target:
            found_index = i
            steps.append({
                "type": "found",
                "array": list(arr),
                "target": target,
                "current_idx": i,
                "found": True,
                "description": f"Success! Target {target} found at index {i} in {comparisons} comparison(s).",
                "pseudo_line": 3,
                "comparisons": comparisons
            })
            break

    if found_index == -1:
        steps.append({
            "type": "not_found",
            "array": list(arr),
            "target": target,
            "current_idx": None,
            "found": False,
            "description": f"Target {target} was NOT found in the array after checking all {n} elements.",
            "pseudo_line": 4,
            "comparisons": comparisons
        })

    return steps


def trace_binary_search(arr: List[int], target: int) -> List[Dict[str, Any]]:
    steps = []
    # Ensure sorted
    a = sorted(list(arr))
    n = len(a)
    comparisons = 0

    low = 0
    high = n - 1
    found_index = -1

    steps.append({
        "type": "init",
        "array": list(a),
        "target": target,
        "low": low,
        "high": high,
        "mid": None,
        "description": f"Binary Search initialized for target {target}. Search space: indices [{low}..{high}].",
        "pseudo_line": 1,
        "comparisons": 0
    })

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1

        steps.append({
            "type": "inspect_mid",
            "array": list(a),
            "target": target,
            "low": low,
            "high": high,
            "mid": mid,
            "description": f"Calculated mid = floor(({low} + {high}) / 2) = {mid}. A[{mid}] = {a[mid]}.",
            "pseudo_line": 3,
            "comparisons": comparisons
        })

        if a[mid] == target:
            found_index = mid
            steps.append({
                "type": "found",
                "array": list(a),
                "target": target,
                "low": low,
                "high": high,
                "mid": mid,
                "description": f"Match found! A[{mid}] == {target}. Search concluded in {comparisons} comparison(s).",
                "pseudo_line": 4,
                "comparisons": comparisons
            })
            break
        elif a[mid] < target:
            steps.append({
                "type": "narrow_right",
                "array": list(a),
                "target": target,
                "low": low,
                "high": high,
                "mid": mid,
                "description": f"A[{mid}]={a[mid]} < {target}: target must lie in the right half. Setting low = {mid + 1}.",
                "pseudo_line": 5,
                "comparisons": comparisons
            })
            low = mid + 1
        else:
            steps.append({
                "type": "narrow_left",
                "array": list(a),
                "target": target,
                "low": low,
                "high": high,
                "mid": mid,
                "description": f"A[{mid}]={a[mid]} > {target}: target must lie in the left half. Setting high = {mid - 1}.",
                "pseudo_line": 6,
                "comparisons": comparisons
            })
            high = mid - 1

    if found_index == -1:
        steps.append({
            "type": "not_found",
            "array": list(a),
            "target": target,
            "low": low,
            "high": high,
            "mid": None,
            "description": f"low ({low}) > high ({high}). Target {target} does not exist in array.",
            "pseudo_line": 7,
            "comparisons": comparisons
        })

    return steps
