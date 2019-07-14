"""
4.1-2 
    Write pseudocode for the brute-force method of solving the maximum-subarray
    problem. It should run in Theta(n^2) time.

    brute-force-maximum-subarray(A):
        low = 0
        high = 0
        max_sum = 0

        for i = 0 to A.length
            sum = A[i]
            for j = i + 1 to A.length
                sum += A[j]
                if sum > max_sum
                    max_sum = sum
                    low = i
                    high = j
        
        return (low, high, max_sum)
"""

# 4.1-3

from typing import List

def brute_force_maximum_subarray(a: List[int]) -> (int, int, int):
    """Finds the subarray that corresponds to the maximum sum.
    Does so in a brute-force manner.

    Returns the low and high indices, along with the sum.
    O(n^2)
    """
    low = 0
    high = 0
    max_sum = 0

    for i in range(0, len(a)):
        s = a[i]
        for j in range(i + 1, len(a)):
            s += a[j]
            if s > max_sum:
                max_sum = s
                low = i
                high = j
    
    return (low, high, max_sum)

def divide_n_conquer_maximum_subarray(a: List[int]) -> (int, int, int):
    """Finds the subarray that corresponds to the maximum sum.
    Does so in a d&q manner.

    Returns the low and high indices, along with the sum.
    O(n lg n)
    """

    return find_maximum_subarray(a, 0, len(a))

def find_maximum_subarray(
        a:    List[int],
        low:  int,
        high: int,
    ) -> (int, int, int):
    """Finds the maximum subarray that is [low, high)."""

    if low == high - 1:
        return (low, high, a[low])

    mid = int((high + low) / 2) # Converting to int ≈ floor

    left_low, left_high, left_max = find_maximum_subarray(a, low, mid)
    right_low, right_high, right_max = find_maximum_subarray(a, mid, high)
    cross_low, cross_high, cross_max = _find_max_crossing_subarray(a, low, mid, high)

    m = max([left_max, right_max, cross_max])
    if m == cross_max:
        return (cross_low, cross_high, cross_max)
    elif m == right_max:
        return (right_low, right_high, right_max)
    else:
        return (left_low, left_high, left_max)

def _find_max_crossing_subarray(
        a:    List[int],
        low:  int,
        mid:  int,
        high: int,
    ) -> (int, int, int):
    """Finds the maximum subarray within bounds, that crosses mid."""
    # Observation
    #   A crossing maximum subarray will always have a part that goes from
    #   low to mid, and another that goes from mid to high.
    # Find them both separately and then return the union of both

    left = mid
    left_max_sum = 0
    left_sum = 0
    for i in reversed(range(low, mid)):
        left_sum += a[i]
        if left_sum > left_max_sum:
            left_max_sum = left_sum
            left = i
    
    right = mid
    right_max_sum = 0
    right_sum = 0
    for j in range(mid, high):
        right_sum += a[j]
        if right_sum > right_max_sum:
            right_max_sum = right_sum
            right = j

    return (left, right, left_max_sum + right_max_sum)



if __name__ == "__main__":
    a = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
    expected = (7, 10, 43)
    result = brute_force_maximum_subarray(a)
    print("brute-force result", result)
    assert result == expected

    result = divide_n_conquer_maximum_subarray(a)
    print("divide-and-conquer result", result)
    assert result == expected

