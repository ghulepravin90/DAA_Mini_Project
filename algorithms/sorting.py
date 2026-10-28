"""
Sorting Algorithms module with step-by-step trace generation and benchmark execution.
Designed for DAA (Design and Analysis of Algorithms).
"""

from typing import List, Dict, Any
import copy


SORTING_METADATA = {
    "bubble_sort": {
        "name": "Bubble Sort",
        "paradigm": "Brute Force / Comparison",
        "best_time": "O(n)",
        "avg_time": "O(n²)",
        "worst_time": "O(n²)",
        "space": "O(1)",
        "stable": True,
        "in_place": True,
        "description": "Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.",
        "pseudocode": [
            "procedure bubbleSort(A : list of sortable items)",
            "    n := length(A)",
            "    for i := 0 to n - 1 do:",
            "        swapped := false",
            "        for j := 0 to n - i - 2 do:",
            "            if A[j] > A[j + 1] then:",
            "                swap(A[j], A[j + 1])",
            "                swapped := true",
            "        if not swapped then break"
        ]
    },
    "insertion_sort": {
        "name": "Insertion Sort",
        "paradigm": "Incremental Approach",
        "best_time": "O(n)",
        "avg_time": "O(n²)",
        "worst_time": "O(n²)",
        "space": "O(1)",
        "stable": True,
        "in_place": True,
        "description": "Builds the sorted array one item at a time by repeatedly taking the next element and inserting it into its correct position among previously sorted elements.",
        "pseudocode": [
            "procedure insertionSort(A : list of sortable items)",
            "    for i := 1 to length(A) - 1 do:",
            "        key := A[i]",
            "        j := i - 1",
            "        while j >= 0 and A[j] > key do:",
            "            A[j + 1] := A[j]",
            "            j := j - 1",
            "        A[j + 1] := key"
        ]
    },
    "selection_sort": {
        "name": "Selection Sort",
        "paradigm": "Greedy / Brute Force",
        "best_time": "O(n²)",
        "avg_time": "O(n²)",
        "worst_time": "O(n²)",
        "space": "O(1)",
        "stable": False,
        "in_place": True,
        "description": "Divides input into sorted and unsorted regions, repeatedly finding the minimum element from the unsorted region and moving it to the sorted region.",
        "pseudocode": [
            "procedure selectionSort(A : list of sortable items)",
            "    for i := 0 to length(A) - 2 do:",
            "        min_idx := i",
            "        for j := i + 1 to length(A) - 1 do:",
            "            if A[j] < A[min_idx] then min_idx := j",
            "        if min_idx != i then:",
            "            swap(A[i], A[min_idx])"
        ]
    },
    "merge_sort": {
        "name": "Merge Sort",
        "paradigm": "Divide and Conquer",
        "best_time": "O(n log n)",
        "avg_time": "O(n log n)",
        "worst_time": "O(n log n)",
        "space": "O(n)",
        "stable": True,
        "in_place": False,
        "description": "Divides array into halves, recursively sorts each half using Divide & Conquer, then merges the two sorted halves into one.",
        "pseudocode": [
            "procedure mergeSort(A, left, right):",
            "    if left < right then:",
            "        mid := floor((left + right) / 2)",
            "        mergeSort(A, left, mid)",
            "        mergeSort(A, mid + 1, right)",
            "        merge(A, left, mid, right)",
            "procedure merge(A, left, mid, right):",
            "    copy subarrays L = A[left..mid], R = A[mid+1..right]",
            "    merge L and R back into A[left..right] in sorted order"
        ]
    },
    "quick_sort": {
        "name": "Quick Sort",
        "paradigm": "Divide and Conquer (Partitioning)",
        "best_time": "O(n log n)",
        "avg_time": "O(n log n)",
        "worst_time": "O(n²)",
        "space": "O(log n)",
        "stable": False,
        "in_place": True,
        "description": "Selects a 'pivot' element, partitions array elements into those less than and greater than the pivot, and recursively sorts subarrays.",
        "pseudocode": [
            "procedure quickSort(A, low, high):",
            "    if low < high then:",
            "        pi := partition(A, low, high)",
            "        quickSort(A, low, pi - 1)",
            "        quickSort(A, pi + 1, high)",
            "procedure partition(A, low, high):",
            "    pivot := A[high]",
            "    i := low - 1",
            "    for j := low to high - 1 do:",
            "        if A[j] < pivot then: i := i + 1; swap(A[i], A[j])",
            "    swap(A[i + 1], A[high])",
            "    return i + 1"
        ]
    },
    "heap_sort": {
        "name": "Heap Sort",
        "paradigm": "Heap Data Structure / Selection",
        "best_time": "O(n log n)",
        "avg_time": "O(n log n)",
        "worst_time": "O(n log n)",
        "space": "O(1)",
        "stable": False,
        "in_place": True,
        "description": "Builds a Max-Heap from the array, repeatedly extracts the maximum root element placing it at the end, and restores the heap property.",
        "pseudocode": [
            "procedure heapSort(A):",
            "    n := length(A)",
            "    for i := floor(n / 2) - 1 down to 0: heapify(A, n, i)",
            "    for i := n - 1 down to 1 do:",
            "        swap(A[0], A[i])",
            "        heapify(A, i, 0)",
            "procedure heapify(A, n, i):",
            "    largest := i, left := 2*i + 1, right := 2*i + 2",
            "    if left < n and A[left] > A[largest] then largest := left",
            "    if right < n and A[right] > A[largest] then largest := right",
            "    if largest != i then swap(A[i], A[largest]); heapify(A, n, largest)"
        ]
    }
}


def trace_bubble_sort(arr: List[int]) -> List[Dict[str, Any]]:
    steps = []
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0

    steps.append({
        "type": "init",
        "array": list(a),
        "indices": [],
        "description": f"Initial array of size {n}.",
        "pseudo_line": 0,
        "comparisons": comparisons,
        "swaps": swaps
    })

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            steps.append({
                "type": "compare",
                "array": list(a),
                "indices": [j, j + 1],
                "description": f"Comparing A[{j}]={a[j]} and A[{j+1}]={a[j+1]}",
                "pseudo_line": 5,
                "comparisons": comparisons,
                "swaps": swaps
            })
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
                steps.append({
                    "type": "swap",
                    "array": list(a),
                    "indices": [j, j + 1],
                    "description": f"Swapped A[{j}] and A[{j+1}] because {a[j+1]} > {a[j]}",
                    "pseudo_line": 6,
                    "comparisons": comparisons,
                    "swaps": swaps
                })
        steps.append({
            "type": "sorted_element",
            "array": list(a),
            "indices": [n - i - 1],
            "description": f"Element at index {n - i - 1} ({a[n - i - 1]}) is now in its correct sorted position.",
            "pseudo_line": 4,
            "comparisons": comparisons,
            "swaps": swaps
        })
        if not swapped:
            steps.append({
                "type": "info",
                "array": list(a),
                "indices": [],
                "description": "No swaps occurred in this pass. Array is already sorted (Early termination).",
                "pseudo_line": 8,
                "comparisons": comparisons,
                "swaps": swaps
            })
            break

    steps.append({
        "type": "finished",
        "array": list(a),
        "indices": list(range(n)),
        "description": f"Bubble Sort complete! Total comparisons: {comparisons}, Total swaps: {swaps}.",
        "pseudo_line": 8,
        "comparisons": comparisons,
        "swaps": swaps
    })
    return steps


def trace_insertion_sort(arr: List[int]) -> List[Dict[str, Any]]:
    steps = []
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0

    steps.append({
        "type": "init",
        "array": list(a),
        "indices": [0],
        "description": f"Single element A[0]={a[0]} is trivially sorted.",
        "pseudo_line": 1,
        "comparisons": comparisons,
        "swaps": swaps
    })

    for i in range(1, n):
        key = a[i]
        j = i - 1
        steps.append({
            "type": "select_key",
            "array": list(a),
            "indices": [i],
            "key": key,
            "description": f"Current key to insert: {key} from index {i}.",
            "pseudo_line": 2,
            "comparisons": comparisons,
            "swaps": swaps
        })

        while j >= 0:
            comparisons += 1
            steps.append({
                "type": "compare",
                "array": list(a),
                "indices": [j, j + 1],
                "description": f"Comparing key {key} with A[{j}]={a[j]}",
                "pseudo_line": 4,
                "comparisons": comparisons,
                "swaps": swaps
            })
            if a[j] > key:
                a[j + 1] = a[j]
                swaps += 1
                steps.append({
                    "type": "shift",
                    "array": list(a),
                    "indices": [j, j + 1],
                    "description": f"Shifted {a[j]} rightwards to index {j+1}",
                    "pseudo_line": 5,
                    "comparisons": comparisons,
                    "swaps": swaps
                })
                j -= 1
            else:
                break

        a[j + 1] = key
        swaps += 1
        steps.append({
            "type": "insert",
            "array": list(a),
            "indices": [j + 1],
            "description": f"Placed key {key} into position {j+1}.",
            "pseudo_line": 7,
            "comparisons": comparisons,
            "swaps": swaps
        })

    steps.append({
        "type": "finished",
        "array": list(a),
        "indices": list(range(n)),
        "description": f"Insertion Sort complete! Comparisons: {comparisons}, Shifts/Writes: {swaps}.",
        "pseudo_line": 7,
        "comparisons": comparisons,
        "swaps": swaps
    })
    return steps


def trace_selection_sort(arr: List[int]) -> List[Dict[str, Any]]:
    steps = []
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0

    steps.append({
        "type": "init",
        "array": list(a),
        "indices": [],
        "description": "Initial array for Selection Sort.",
        "pseudo_line": 0,
        "comparisons": 0,
        "swaps": 0
    })

    for i in range(n - 1):
        min_idx = i
        steps.append({
            "type": "set_min",
            "array": list(a),
            "indices": [min_idx],
            "description": f"Starting pass {i}. Current minimum candidate is A[{min_idx}]={a[min_idx]}.",
            "pseudo_line": 2,
            "comparisons": comparisons,
            "swaps": swaps
        })

        for j in range(i + 1, n):
            comparisons += 1
            steps.append({
                "type": "compare",
                "array": list(a),
                "indices": [min_idx, j],
                "description": f"Comparing current min A[{min_idx}]={a[min_idx]} with A[{j}]={a[j]}.",
                "pseudo_line": 4,
                "comparisons": comparisons,
                "swaps": swaps
            })
            if a[j] < a[min_idx]:
                min_idx = j
                steps.append({
                    "type": "new_min",
                    "array": list(a),
                    "indices": [min_idx],
                    "description": f"Found new minimum: A[{min_idx}]={a[min_idx]}.",
                    "pseudo_line": 4,
                    "comparisons": comparisons,
                    "swaps": swaps
                })

        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
            steps.append({
                "type": "swap",
                "array": list(a),
                "indices": [i, min_idx],
                "description": f"Swapping minimum A[{min_idx}] with position {i}.",
                "pseudo_line": 6,
                "comparisons": comparisons,
                "swaps": swaps
            })
        steps.append({
            "type": "sorted_element",
            "array": list(a),
            "indices": [i],
            "description": f"Element at index {i} ({a[i]}) is now sorted.",
            "pseudo_line": 1,
            "comparisons": comparisons,
            "swaps": swaps
        })

    steps.append({
        "type": "finished",
        "array": list(a),
        "indices": list(range(n)),
        "description": f"Selection Sort complete! Comparisons: {comparisons}, Swaps: {swaps}.",
        "pseudo_line": 6,
        "comparisons": comparisons,
        "swaps": swaps
    })
    return steps


def trace_merge_sort(arr: List[int]) -> List[Dict[str, Any]]:
    steps = []
    a = list(arr)
    n = len(a)
    stats = {"comparisons": 0, "swaps": 0}

    steps.append({
        "type": "init",
        "array": list(a),
        "indices": [],
        "description": "Initial array for Merge Sort.",
        "pseudo_line": 0,
        "comparisons": 0,
        "swaps": 0
    })

    def merge(left: int, mid: int, right: int):
        L = a[left:mid + 1]
        R = a[mid + 1:right + 1]
        i = 0
        j = 0
        k = left

        steps.append({
            "type": "merge_start",
            "array": list(a),
            "indices": list(range(left, right + 1)),
            "subarrays": {"left": [left, mid], "right": [mid + 1, right]},
            "description": f"Merging subarrays A[{left}..{mid}] and A[{mid+1}..{right}].",
            "pseudo_line": 5,
            "comparisons": stats["comparisons"],
            "swaps": stats["swaps"]
        })

        while i < len(L) and j < len(R):
            stats["comparisons"] += 1
            steps.append({
                "type": "compare",
                "array": list(a),
                "indices": [left + i, mid + 1 + j],
                "description": f"Comparing L[{i}]={L[i]} with R[{j}]={R[j]}.",
                "pseudo_line": 7,
                "comparisons": stats["comparisons"],
                "swaps": stats["swaps"]
            })
            if L[i] <= R[j]:
                a[k] = L[i]
                stats["swaps"] += 1
                i += 1
            else:
                a[k] = R[j]
                stats["swaps"] += 1
                j += 1
            steps.append({
                "type": "overwrite",
                "array": list(a),
                "indices": [k],
                "description": f"Placed {a[k]} at index {k}.",
                "pseudo_line": 8,
                "comparisons": stats["comparisons"],
                "swaps": stats["swaps"]
            })
            k += 1

        while i < len(L):
            a[k] = L[i]
            stats["swaps"] += 1
            steps.append({
                "type": "overwrite",
                "array": list(a),
                "indices": [k],
                "description": f"Copying remaining L[{i}]={L[i]} into index {k}.",
                "pseudo_line": 8,
                "comparisons": stats["comparisons"],
                "swaps": stats["swaps"]
            })
            i += 1
            k += 1

        while j < len(R):
            a[k] = R[j]
            stats["swaps"] += 1
            steps.append({
                "type": "overwrite",
                "array": list(a),
                "indices": [k],
                "description": f"Copying remaining R[{j}]={R[j]} into index {k}.",
                "pseudo_line": 8,
                "comparisons": stats["comparisons"],
                "swaps": stats["swaps"]
            })
            j += 1
            k += 1

    def merge_sort_rec(left: int, right: int):
        if left < right:
            mid = (left + right) // 2
            steps.append({
                "type": "divide",
                "array": list(a),
                "indices": [left, mid, right],
                "description": f"Divide: split range [{left}..{right}] at mid={mid}.",
                "pseudo_line": 2,
                "comparisons": stats["comparisons"],
                "swaps": stats["swaps"]
            })
            merge_sort_rec(left, mid)
            merge_sort_rec(mid + 1, right)
            merge(left, mid, right)

    merge_sort_rec(0, n - 1)

    steps.append({
        "type": "finished",
        "array": list(a),
        "indices": list(range(n)),
        "description": f"Merge Sort complete! Comparisons: {stats['comparisons']}, Writes: {stats['swaps']}.",
        "pseudo_line": 0,
        "comparisons": stats["comparisons"],
        "swaps": stats["swaps"]
    })
    return steps


def trace_quick_sort(arr: List[int]) -> List[Dict[str, Any]]:
    steps = []
    a = list(arr)
    n = len(a)
    stats = {"comparisons": 0, "swaps": 0}

    steps.append({
        "type": "init",
        "array": list(a),
        "indices": [],
        "description": "Initial array for Quick Sort (Lomuto Partition Scheme).",
        "pseudo_line": 0,
        "comparisons": 0,
        "swaps": 0
    })

    def partition(low: int, high: int) -> int:
        pivot = a[high]
        i = low - 1
        steps.append({
            "type": "pivot",
            "array": list(a),
            "indices": [high],
            "description": f"Chosen pivot A[{high}]={pivot} for range [{low}..{high}].",
            "pseudo_line": 6,
            "comparisons": stats["comparisons"],
            "swaps": stats["swaps"]
        })

        for j in range(low, high):
            stats["comparisons"] += 1
            steps.append({
                "type": "compare",
                "array": list(a),
                "indices": [j, high],
                "description": f"Comparing A[{j}]={a[j]} with pivot {pivot}.",
                "pseudo_line": 9,
                "comparisons": stats["comparisons"],
                "swaps": stats["swaps"]
            })
            if a[j] < pivot:
                i += 1
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    stats["swaps"] += 1
                    steps.append({
                        "type": "swap",
                        "array": list(a),
                        "indices": [i, j],
                        "description": f"A[{j}] < pivot: swapped A[{i}] and A[{j}].",
                        "pseudo_line": 9,
                        "comparisons": stats["comparisons"],
                        "swaps": stats["swaps"]
                    })

        a[i + 1], a[high] = a[high], a[i + 1]
        stats["swaps"] += 1
        steps.append({
            "type": "pivot_placed",
            "array": list(a),
            "indices": [i + 1],
            "description": f"Pivot {pivot} placed in its final sorted position at index {i + 1}.",
            "pseudo_line": 10,
            "comparisons": stats["comparisons"],
            "swaps": stats["swaps"]
        })
        return i + 1

    def quick_sort_rec(low: int, high: int):
        if low < high:
            pi = partition(low, high)
            quick_sort_rec(low, pi - 1)
            quick_sort_rec(pi + 1, high)

    quick_sort_rec(0, n - 1)

    steps.append({
        "type": "finished",
        "array": list(a),
        "indices": list(range(n)),
        "description": f"Quick Sort complete! Comparisons: {stats['comparisons']}, Swaps: {stats['swaps']}.",
        "pseudo_line": 0,
        "comparisons": stats["comparisons"],
        "swaps": stats["swaps"]
    })
    return steps


def trace_heap_sort(arr: List[int]) -> List[Dict[str, Any]]:
    steps = []
    a = list(arr)
    n = len(a)
    stats = {"comparisons": 0, "swaps": 0}

    steps.append({
        "type": "init",
        "array": list(a),
        "indices": [],
        "description": "Initial array for Heap Sort.",
        "pseudo_line": 0,
        "comparisons": 0,
        "swaps": 0
    })

    def heapify(length: int, i: int):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < length:
            stats["comparisons"] += 1
            if a[left] > a[largest]:
                largest = left

        if right < length:
            stats["comparisons"] += 1
            if a[right] > a[largest]:
                largest = right

        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            stats["swaps"] += 1
            steps.append({
                "type": "heapify",
                "array": list(a),
                "indices": [i, largest],
                "description": f"Heapify: Swapped parent A[{i}] with largest child A[{largest}].",
                "pseudo_line": 10,
                "comparisons": stats["comparisons"],
                "swaps": stats["swaps"]
            })
            heapify(length, largest)

    # Build max heap
    steps.append({
        "type": "info",
        "array": list(a),
        "indices": [],
        "description": "Phase 1: Building initial Max-Heap bottom-up.",
        "pseudo_line": 2,
        "comparisons": stats["comparisons"],
        "swaps": stats["swaps"]
    })

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    steps.append({
        "type": "heap_built",
        "array": list(a),
        "indices": [0],
        "description": f"Max-Heap constructed! Root element A[0]={a[0]} is the maximum.",
        "pseudo_line": 2,
        "comparisons": stats["comparisons"],
        "swaps": stats["swaps"]
    })

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        stats["swaps"] += 1
        steps.append({
            "type": "extract_max",
            "array": list(a),
            "indices": [0, i],
            "description": f"Extracted max {a[i]} to sorted position {i}. Restoring heap for size {i}.",
            "pseudo_line": 4,
            "comparisons": stats["comparisons"],
            "swaps": stats["swaps"]
        })
        heapify(i, 0)

    steps.append({
        "type": "finished",
        "array": list(a),
        "indices": list(range(n)),
        "description": f"Heap Sort complete! Comparisons: {stats['comparisons']}, Swaps: {stats['swaps']}.",
        "pseudo_line": 0,
        "comparisons": stats["comparisons"],
        "swaps": stats["swaps"]
    })
    return steps


SORT_DISPATCHER = {
    "bubble_sort": trace_bubble_sort,
    "insertion_sort": trace_insertion_sort,
    "selection_sort": trace_selection_sort,
    "merge_sort": trace_merge_sort,
    "quick_sort": trace_quick_sort,
    "heap_sort": trace_heap_sort
}
