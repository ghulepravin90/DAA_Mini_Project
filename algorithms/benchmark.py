"""
Benchmark and Empirical Complexity Analyzer module.
Measures real CPU execution time and operation counts across varying input sizes N.
Designed for DAA (Design and Analysis of Algorithms).
"""

import time
import random
import math
from typing import List, Dict, Any


def generate_array(size: int, distribution: str = "random") -> List[int]:
    if distribution == "sorted":
        return list(range(1, size + 1))
    elif distribution == "reverse":
        return list(range(size, 0, -1))
    elif distribution == "nearly_sorted":
        arr = list(range(1, size + 1))
        # Swap 5% of elements
        num_swaps = max(1, int(size * 0.05))
        for _ in range(num_swaps):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    else:  # random
        return [random.randint(1, size * 10) for _ in range(size)]


# Fast sorting implementations with comparison & swap tracking
def bench_bubble_sort(arr: List[int]) -> tuple[int, int]:
    a = list(arr)
    n = len(a)
    comps = 0
    swaps = 0
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return comps, swaps


def bench_insertion_sort(arr: List[int]) -> tuple[int, int]:
    a = list(arr)
    comps = 0
    swaps = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j + 1] = a[j]
                swaps += 1
                j -= 1
            else:
                break
        a[j + 1] = key
        swaps += 1
    return comps, swaps


def bench_selection_sort(arr: List[int]) -> tuple[int, int]:
    a = list(arr)
    n = len(a)
    comps = 0
    swaps = 0
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comps += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
    return comps, swaps


def bench_merge_sort(arr: List[int]) -> tuple[int, int]:
    a = list(arr)
    comps = [0]
    swaps = [0]

    def merge_sort_rec(lst: List[int]) -> List[int]:
        if len(lst) <= 1:
            return lst
        mid = len(lst) // 2
        left = merge_sort_rec(lst[:mid])
        right = merge_sort_rec(lst[mid:])
        res = []
        i = j = 0
        while i < len(left) and j < len(right):
            comps[0] += 1
            if left[i] <= right[j]:
                res.append(left[i])
                i += 1
            else:
                res.append(right[j])
                j += 1
            swaps[0] += 1
        while i < len(left):
            res.append(left[i])
            swaps[0] += 1
            i += 1
        while j < len(right):
            res.append(right[j])
            swaps[0] += 1
            j += 1
        return res

    merge_sort_rec(a)
    return comps[0], swaps[0]


def bench_quick_sort(arr: List[int]) -> tuple[int, int]:
    a = list(arr)
    comps = [0]
    swaps = [0]

    def qsort(low: int, high: int):
        if low < high:
            pivot = a[high]
            i = low - 1
            for j in range(low, high):
                comps[0] += 1
                if a[j] < pivot:
                    i += 1
                    a[i], a[j] = a[j], a[i]
                    swaps[0] += 1
            a[i + 1], a[high] = a[high], a[i + 1]
            swaps[0] += 1
            pi = i + 1
            qsort(low, pi - 1)
            qsort(pi + 1, high)

    qsort(0, len(a) - 1)
    return comps[0], swaps[0]


def bench_heap_sort(arr: List[int]) -> tuple[int, int]:
    a = list(arr)
    n = len(a)
    comps = [0]
    swaps = [0]

    def heapify(length: int, i: int):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < length:
            comps[0] += 1
            if a[left] > a[largest]:
                largest = left
        if right < length:
            comps[0] += 1
            if a[right] > a[largest]:
                largest = right
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            swaps[0] += 1
            heapify(length, largest)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        swaps[0] += 1
        heapify(i, 0)

    return comps[0], swaps[0]


SORT_BENCH_MAP = {
    "bubble_sort": bench_bubble_sort,
    "insertion_sort": bench_insertion_sort,
    "selection_sort": bench_selection_sort,
    "merge_sort": bench_merge_sort,
    "quick_sort": bench_quick_sort,
    "heap_sort": bench_heap_sort
}


def run_sorting_benchmark(
    algorithms: List[str],
    sizes: List[int],
    distribution: str = "random",
    repetitions: int = 3
) -> Dict[str, Any]:
    results = {
        algo: {
            "sizes": [],
            "times_ms": [],
            "comparisons": [],
            "swaps": []
        }
        for algo in algorithms if algo in SORT_BENCH_MAP
    }

    for size in sizes:
        # Generate base arrays for fair identical comparison across algorithms
        test_arrays = [generate_array(size, distribution) for _ in range(repetitions)]

        for algo in list(results.keys()):
            bench_fn = SORT_BENCH_MAP[algo]
            durations = []
            comp_counts = []
            swap_counts = []

            for base_arr in test_arrays:
                t_start = time.perf_counter()
                comps, swaps = bench_fn(base_arr)
                t_end = time.perf_counter()
                durations.append((t_end - t_start) * 1000.0)  # ms
                comp_counts.append(comps)
                swap_counts.append(swaps)

            avg_time = sum(durations) / len(durations)
            avg_comps = sum(comp_counts) / len(comp_counts)
            avg_swaps = sum(swap_counts) / len(swap_counts)

            results[algo]["sizes"].append(size)
            results[algo]["times_ms"].append(round(avg_time, 4))
            results[algo]["comparisons"].append(int(avg_comps))
            results[algo]["swaps"].append(int(avg_swaps))

    # Theoretical curves for reference (normalized to middle data point)
    ref_n = sizes[-1] if sizes else 1000
    theoretical = {
        "n": sizes,
        "O_n": [round(n / ref_n, 4) for n in sizes],
        "O_n_logn": [round((n * math.log2(max(2, n))) / (ref_n * math.log2(max(2, ref_n))), 4) for n in sizes],
        "O_n_sq": [round((n * n) / (ref_n * ref_n), 4) for n in sizes]
    }

    return {
        "algorithms": results,
        "sizes": sizes,
        "distribution": distribution,
        "theoretical": theoretical
    }


def run_searching_benchmark(
    sizes: List[int],
    target_position: str = "random"
) -> Dict[str, Any]:
    results = {
        "linear_search": {"sizes": [], "times_us": [], "comparisons": []},
        "binary_search": {"sizes": [], "times_us": [], "comparisons": []}
    }

    for size in sizes:
        arr = sorted(generate_array(size, "random"))

        if target_position == "worst":
            target = -999999  # not present
        elif target_position == "best":
            target = arr[size // 2]  # mid element for binary search
        else:
            target = arr[random.randint(0, size - 1)]

        # Linear search
        t0 = time.perf_counter()
        l_comps = 0
        for x in arr:
            l_comps += 1
            if x == target:
                break
        t1 = time.perf_counter()
        linear_us = (t1 - t0) * 1_000_000.0

        # Binary search
        t2 = time.perf_counter()
        b_comps = 0
        low, high = 0, size - 1
        while low <= high:
            b_comps += 1
            mid = (low + high) // 2
            if arr[mid] == target:
                break
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        t3 = time.perf_counter()
        binary_us = (t3 - t2) * 1_000_000.0

        results["linear_search"]["sizes"].append(size)
        results["linear_search"]["times_us"].append(round(linear_us, 3))
        results["linear_search"]["comparisons"].append(l_comps)

        results["binary_search"]["sizes"].append(size)
        results["binary_search"]["times_us"].append(round(binary_us, 3))
        results["binary_search"]["comparisons"].append(b_comps)

    return {
        "results": results,
        "sizes": sizes,
        "target_position": target_position
    }
