# LeetCode Easy Binary Search Problems - Complete Study Guide

**31 Problems | LeetCode Binary Search Study Plan | Sorted by Problem Number**

Source: https://leetcode.com/problem-list/binary-search/ (Easy difficulty)

---

## Table of Contents

- [Problems #35 - #441](#problems-35---441)
- [Problems #704 - #1385](#problems-704---1385)
- [Problems #1539 - #3633](#problems-1539---3633)
- [Solutions](#solutions)
- [Legend](#legend)

---

## Problems #35 - #441

| S.No. | Status | # | Problem | Acceptance | Link | Solution | Why Binary Search |
|-------|--------|---|---------|-----------|------|----------|--------------------|
| 1 | ⬜ | 35 | Search Insert Position | 52.2% | [LeetCode](https://leetcode.com/problems/search-insert-position/) | - | Classic binary search for the target's index, or its sorted insertion point if absent |
| 2 | ⬜ | 69 | Sqrt(x) | 42.3% | [LeetCode](https://leetcode.com/problems/sqrtx/) | - | Binary search over the answer space `[0, x]` for the largest integer whose square ≤ x |
| 3 | ⬜ | 268 | Missing Number | 72.7% | [LeetCode](https://leetcode.com/problems/missing-number/) | - | On the sorted array, binary search where `arr[i] != i` to find the first mismatch (the missing number) |
| 4 | ⬜ | 270 | 🔒 Closest Binary Search Tree Value | 49.1% | [LeetCode](https://leetcode.com/problems/closest-binary-search-tree-value/) | - | BST traversal narrows left/right each step based on comparison to target, same shape as binary search |
| 5 | ⬜ | 278 | First Bad Version | 47.6% | [LeetCode](https://leetcode.com/problems/first-bad-version/) | - | Binary search over version numbers using the monotonic `isBadVersion` API to find the first bad one |
| 6 | ⬜ | 349 | Intersection of Two Arrays | 78.3% | [LeetCode](https://leetcode.com/problems/intersection-of-two-arrays/) | - | Sort one array, then binary search it for each element of the other to test membership |
| 7 | ⬜ | 350 | Intersection of Two Arrays II | 60.3% | [LeetCode](https://leetcode.com/problems/intersection-of-two-arrays-ii/) | - | Sort one array, then binary search it for each element of the other, allowing repeated matches |
| 8 | ⬜ | 367 | Valid Perfect Square | 45.1% | [LeetCode](https://leetcode.com/problems/valid-perfect-square/) | - | Binary search `[1, num]` for an integer whose square equals num |
| 9 | ⬜ | 374 | Guess Number Higher or Lower | 58.3% | [LeetCode](https://leetcode.com/problems/guess-number-higher-or-lower/) | - | Binary search narrows the candidate range using the higher/lower feedback from `guess()` |
| 10 | ⬜ | 441 | Arranging Coins | 48.6% | [LeetCode](https://leetcode.com/problems/arranging-coins/) | - | Binary search over possible row counts for the largest complete staircase using `k(k+1)/2 <= n` |

## Problems #704 - #1385

| S.No. | Status | # | Problem | Acceptance | Link | Solution | Why Binary Search |
|-------|--------|---|---------|-----------|------|----------|--------------------|
| 11 | ⬜ | 704 | Binary Search | 61.4% | [LeetCode](https://leetcode.com/problems/binary-search/) | - | The textbook implementation — halve the search space each step on a sorted array |
| 12 | ⬜ | 744 | Find Smallest Letter Greater Than Target | 59.6% | [LeetCode](https://leetcode.com/problems/find-smallest-letter-greater-than-target/) | - | Binary search the sorted letters for the first one strictly greater than target (upper bound) |
| 13 | ⬜ | 888 | Fair Candy Swap | 65.6% | [LeetCode](https://leetcode.com/problems/fair-candy-swap/) | - | Sort/hash one array, then binary search (or lookup) for the exact candy count that balances totals |
| 14 | ⬜ | 1064 | 🔒 Fixed Point | 64.3% | [LeetCode](https://leetcode.com/problems/fixed-point/) | - | On the sorted array, binary search for the smallest index where `arr[i] == i` |
| 15 | ⬜ | 1099 | 🔒 Two Sum Less Than K | 62.1% | [LeetCode](https://leetcode.com/problems/two-sum-less-than-k/) | - | Sort the array, then two pointers/binary search converge to maximize the pair sum under k |
| 16 | ⬜ | 1150 | 🔒 Check If a Number Is Majority Element in a Sorted Array | 59.9% | [LeetCode](https://leetcode.com/problems/check-if-a-number-is-majority-element-in-a-sorted-array/) | - | Binary search the first and last occurrence of target to check if its count exceeds n/2 |
| 17 | ⬜ | 1213 | 🔒 Intersection of Three Sorted Arrays | 80.0% | [LeetCode](https://leetcode.com/problems/intersection-of-three-sorted-arrays/) | - | Binary search (or merge pointers) across three sorted arrays to find common elements |
| 18 | ⬜ | 1337 | The K Weakest Rows in a Matrix | 74.5% | [LeetCode](https://leetcode.com/problems/the-k-weakest-rows-in-a-matrix/) | - | Binary search each sorted row for the count of 1s (its "strength") before ranking rows |
| 19 | ⬜ | 1346 | Check If N and Its Double Exist | 42.0% | [LeetCode](https://leetcode.com/problems/check-if-n-and-its-double-exist/) | - | Sort the array, then binary search for each element's double (or half) |
| 20 | ⬜ | 1351 | Count Negative Numbers in a Sorted Matrix | 79.7% | [LeetCode](https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix/) | - | Binary search each row (sorted descending) for the first negative value, then sum the counts |
| 21 | ⬜ | 1385 | Find the Distance Value Between Two Arrays | 72.3% | [LeetCode](https://leetcode.com/problems/find-the-distance-value-between-two-arrays/) | - | Sort arr2, then binary search it for any value within distance d of each arr1 element |

## Problems #1539 - #3633

| S.No. | Status | # | Problem | Acceptance | Link | Solution | Why Binary Search |
|-------|--------|---|---------|-----------|------|----------|--------------------|
| 22 | ⬜ | 1539 | Kth Missing Positive Number | 63.9% | [LeetCode](https://leetcode.com/problems/kth-missing-positive-number/) | - | Binary search the index where `arr[i] - (i+1)` (count of missing numbers so far) first reaches k |
| 23 | ⬜ | 1608 | Special Array With X Elements Greater Than or Equal X | 67.0% | [LeetCode](https://leetcode.com/problems/special-array-with-x-elements-greater-than-or-equal-x/) | - | Sort the array, then binary search for the unique x where exactly x elements are ≥ x |
| 24 | ⬜ | 2089 | Find Target Indices After Sorting Array | 78.3% | [LeetCode](https://leetcode.com/problems/find-target-indices-after-sorting-array/) | - | After sorting, binary search the first/last occurrence bounds of the target value |
| 25 | ⬜ | 2389 | Longest Subsequence With Limited Sum | 73.8% | [LeetCode](https://leetcode.com/problems/longest-subsequence-with-limited-sum/) | - | Sort and prefix-sum the array, then binary search the prefix sums for each query |
| 26 | ⬜ | 2529 | Maximum Count of Positive Integer and Negative Integer | 74.2% | [LeetCode](https://leetcode.com/problems/maximum-count-of-positive-integer-and-negative-integer/) | - | Binary search the sorted array for the split points between negatives, zero, and positives |
| 27 | ⬜ | 2540 | Minimum Common Value | 60.7% | [LeetCode](https://leetcode.com/problems/minimum-common-value/) | - | Binary search the smaller/other sorted array for each element to find the first common value |
| 28 | ⬜ | 2824 | Count Pairs Whose Sum is Less than Target | 87.7% | [LeetCode](https://leetcode.com/problems/count-pairs-whose-sum-is-less-than-target/) | - | Sort the array, then binary search (or two pointers) for how many later elements complete a valid pair |
| 29 | ⬜ | 2970 | Count the Number of Incremovable Subarrays I | 56.7% | [LeetCode](https://leetcode.com/problems/count-the-number-of-incremovable-subarrays-i/) | - | Binary search the longest strictly-increasing prefix/suffix boundaries to bound valid subarrays |
| 30 | ⬜ | 3477 | Fruits Into Baskets II | 70.2% | [LeetCode](https://leetcode.com/problems/fruits-into-baskets-ii/) | - | Binary search each basket's capacity for the first one that can hold the current fruit type |
| 31 | ⬜ | 3633 | Earliest Finish Time for Land and Water Rides I | 72.6% | [LeetCode](https://leetcode.com/problems/earliest-finish-time-for-land-and-water-rides-i/) | - | Sort ride start times, then binary search for the earliest valid pairing after each land ride ends |

---

## Solutions

_No solutions submitted yet — entries will be added here (approach, code, and a dry run) as each problem gets solved, following the same format as [Two-Pointers-Problems.md](Two-Pointers-Problems.md)._

[⬆ Back to Top](#table-of-contents)

---

## Legend

- ⬜ Not attempted
- ✅ Solution submitted
- 🔒 LeetCode Premium (subscription required to view)

**Total Problems:** 31
**Solved:** 0/31
**Premium-locked:** 5 (#270, #1064, #1099, #1150, #1213)
**Status:** Not Started
**Last Updated:** 2026-09-14
