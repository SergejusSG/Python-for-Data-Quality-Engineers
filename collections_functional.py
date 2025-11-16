"""
Functional refactor of the collections homework.

Typical spec (EPAM Module 2):
1) Generate a list of N (2..10) dicts with random letter keys and values 0..100.
2) Merge them into a single dict:
   - For duplicate keys, keep the MAX value
   - And rename the kept key to include the index of the dict with that max (e.g., 'a_3')
3) Show both the input list and the merged dict.

Refactor goals:
- Pure functions
- Deterministic mode with a seed for tests
- Type hints + docstrings
"""

from __future__ import annotations
import random
import string
from typing import List, Dict, Tuple, Optional

def generate_random_dict(min_keys: int = 2, max_keys: int = 10) -> Dict[str, int]:
    """
    Create one random dict with 2..max_keys distinct letter keys
    and values in 0..100.
    """
    k = random.randint(min_keys, max_keys)
    # Choose random distinct letters for keys
    keys = random.sample(string.ascii_lowercase, k=k)
    return {key: random.randint(0, 100) for key in keys}

def generate_list_of_dicts(n: int | None = None) -> List[Dict[str, int]]:
    """
    Generate a list of dicts.
    If n is None, choose 2..10.
    """
    if n is None:
        n = random.randint(2, 10)
    return [generate_random_dict() for _ in range(n)]

def merge_by_max_with_index(dicts: List[Dict[str, int]]) -> Dict[str, int]:
    """
    Merge dicts into a single dict where for any duplicate letter key
    we keep the maximum value, and rename the key to include the 1-based
    index of the source dict that contributed the max (e.g., 'a_2').

    If a key appears in only one dict, keep it as-is (no suffix).
    """
    # Map key -> (max_value, best_dict_index)   (index is 1-based)
    winners: Dict[str, Tuple[int, int]] = {}

    for idx, d in enumerate(dicts, start=1):
        for k, v in d.items():
            if k not in winners or v > winners[k][0]:
                winners[k] = (v, idx)

    # Build the final dict with renamed keys if duplicates exist
    key_counts: Dict[str, int] = {}
    for d in dicts:
        for k in d:
            key_counts[k] = key_counts.get(k, 0) + 1

    result: Dict[str, int] = {}
    for k, (val, idx) in winners.items():
        new_key = f"{k}_{idx}" if key_counts[k] > 1 else k
        result[new_key] = val
    return result

def pipeline(seed: Optional[int] = None, n: Optional[int] = None) -> Tuple[List[Dict[str, int]], Dict[str, int]]:
    """
    Deterministic pipeline for tests and demos.
    - Optionally set a random seed
    - Optionally fix the number of dicts
    Returns:
        (list_of_dicts, merged_result)
    """
    if seed is not None:
        random.seed(seed)
    dicts = generate_list_of_dicts(n=n)
    merged = merge_by_max_with_index(dicts)
    return dicts, merged

if __name__ == "__main__":
    dicts, merged = pipeline(seed=42)  # deterministic demo
    print("Input dicts:")
    for i, d in enumerate(dicts, start=1):
        print(f"{i:2d}: {d}")
    print("\nMerged result:")
    print(merged)
