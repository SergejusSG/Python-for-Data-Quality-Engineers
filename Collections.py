
import random                 # standard module for randomness (choosing counts/values)
import string                 # gives us ascii letters for dict keys

# 1) Generate a random list of dictionaries
def generate_list_of_dicts() -> list[dict]:
    """Create a random list (length 2..10) of dicts with letter keys and 0..100 values."""
    n_dicts = random.randint(2, 10)      # choose how many dicts we will generate (between 2 and 10)
    dicts = []                           # this will hold all generated dicts

    for _ in range(n_dicts):             # loop n_dicts times
        num_keys = random.randint(1, 7)  # choose how many keys for this dict (1..7 random letters)
        # pick distinct letter keys (no duplicates within one dict)
        keys = random.sample(string.ascii_lowercase, num_keys)
        # build one dict: each key gets a random int value 0..100
        d = {k: random.randint(0, 100) for k in keys}
        dicts.append(d)                  # add the dict to our list

    return dicts                         # return list like [{'a':5,'b':7}, {'a':3,'c':35}]

# 2) Merge dicts using the rules
def merge_with_rules(dict_list: list[dict]) -> dict:
    """
    Rules:
    - If a key appears in multiple dicts, keep the MAX value and rename key to 'key_<dict_index_of_max>'.
    - If a key appears only once across all dicts, keep the key as-is.
    Tie-breaking rule: if max value is equal in multiple dicts, keep the earliest dict index.
    """
    best = {}    # maps key -> (max_value_found, dict_index_where_that_max_was_found)
    counts = {}  # maps key -> number_of_times_key_appears_across_all_dicts

    # Go through each dict, keeping track of counts and best (max) value per key
    for idx, d in enumerate(dict_list, start=1):  # enumerate gives 1-based dict index
        for k, v in d.items():                    # iterate keys and values in this dict
            counts[k] = counts.get(k, 0) + 1      # count how many times key appears overall
            # update best if key is new OR we found a bigger value
            if (k not in best) or (v > best[k][0]):
                best[k] = (v, idx)
            # if v == best[k][0], we keep earlier idx (do nothing)

    # Build the final merged dict according to counts and best
    merged = {}
    for k, (max_v, idx_of_max) in best.items():   # iterate keys with their winning max and its dict index
        if counts[k] == 1:                        # key appeared only once
            merged[k] = max_v                     # keep key as-is
        else:
            merged[f"{k}_{idx_of_max}"] = max_v   # key appeared multiple times -> rename with index
    return merged                                  # return the merged dict

import random
import string

def generate_list_of_dicts() -> list[dict]:
    # Create a random list (2..10) of dicts keyed by letters with values 0..100
    n_dicts = random.randint(2, 10)
    dicts = []
    for _ in range(n_dicts):
        num_keys = random.randint(1, 7)
        keys = random.sample(string.ascii_lowercase, num_keys)
        d = {k: random.randint(0, 100) for k in keys}
        dicts.append(d)
    return dicts

def merge_with_rules(dict_list: list[dict]) -> dict:
    # If key appears multiple times: keep max value and rename to key_<dict_index_of_max>
    # If appears once: keep as-is
    best = {}    # key -> (max_value, dict_index_of_max)
    counts = {}  # key -> occurrences

    for idx, d in enumerate(dict_list, start=1):
        for k, v in d.items():
            counts[k] = counts.get(k, 0) + 1
            if (k not in best) or (v > best[k][0]):
                best[k] = (v, idx)

    merged = {}
    for k, (max_v, idx_of_max) in best.items():
        if counts[k] == 1:
            merged[k] = max_v
        else:
            merged[f"{k}_{idx_of_max}"] = max_v
    return merged

if __name__ == "__main__":
    # Optional: fix the seed for reproducible results while debugging
    # random.seed(42)

    data = generate_list_of_dicts()
    result = merge_with_rules(data)

    print("Generated list of dicts:")
    print(data)
    print("\nMerged result:")
    print(result)
