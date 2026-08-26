# LeetCode Easy Two Pointers Problems - Complete Study Guide

**69 Problems | LeetCode Two Pointers Study Plan | Sorted by Problem Number**

Source: https://leetcode.com/problem-list/two-pointers/ (Easy difficulty)

---

## Table of Contents

- [Problems #26 - #680](#problems-26---680)
- [Problems #696 - #2200](#problems-696---2200)
- [Problems #2367 - #3992](#problems-2367---3992)
- [Solutions](#solutions)
- [Legend](#legend)

---

## Problems #26 - #680

| S.No. | Status | # | Problem | Acceptance | Link | Solution | Why Two Pointers |
|-------|--------|---|---------|-----------|------|----------|-------------------|
| 1 | ✅ | 26 | Remove Duplicates from Sorted Array | 63.6% | [LeetCode](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | [View](#26-remove-duplicates-from-sorted-array) | Fast/slow pointers overwrite the array in place — one reads, one writes |
| 2 | ✅ | 27 | Remove Element | 62.4% | [LeetCode](https://leetcode.com/problems/remove-element/) | [View](#27-remove-element) | Fast/slow pointers skip the target value while compacting the array |
| 3 | ✅ | 28 | Find the Index of the First Occurrence in a String | 47.2% | [LeetCode](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) | [View](#28-find-the-index-of-the-first-occurrence-in-a-string) | A sliding window pointer walks haystack, comparing each candidate substring against needle |
| 4 | ✅ | 88 | Merge Sorted Array | 55.6% | [LeetCode](https://leetcode.com/problems/merge-sorted-array/) | [View](#88-merge-sorted-array) | Two pointers walk both arrays from the back, merging in place |
| 5 | ✅ | 125 | Valid Palindrome | 54.1% | [LeetCode](https://leetcode.com/problems/valid-palindrome/) | [View](#125-valid-palindrome) | Two pointers converge from both ends, skipping non-alphanumeric characters |
| 6 | ✅ | 141 | Linked List Cycle | 54.9% | [LeetCode](https://leetcode.com/problems/linked-list-cycle/) | [View](#141-linked-list-cycle) | Fast/slow pointers (Floyd's) detect a loop because they move at different speeds |
| 7 | ✅ | 160 | Intersection of Two Linked Lists | 64.5% | [LeetCode](https://leetcode.com/problems/intersection-of-two-linked-lists/) | [View](#160-intersection-of-two-linked-lists) | Two pointers swap heads on reaching the end, equalizing total distance traveled |
| 8 | ⬜ | 170 | Two Sum III - Data structure design | 39.2% | [LeetCode](https://leetcode.com/problems/two-sum-iii-data-structure-design/) | - | On sorted stored values, two pointers converge to find a pair summing to the target |
| 9 | ⬜ | 202 | Happy Number | 60.1% | [LeetCode](https://leetcode.com/problems/happy-number/) | - | Fast/slow pointers (Floyd's) detect cycling in the repeated digit-square-sum sequence |
| 10 | ⬜ | 234 | Palindrome Linked List | 58.6% | [LeetCode](https://leetcode.com/problems/palindrome-linked-list/) | - | Fast/slow pointer finds the middle, then two pointers compare from both halves |
| 11 | ⬜ | 246 | Strobogrammatic Number | 47.5% | [LeetCode](https://leetcode.com/problems/strobogrammatic-number/) | - | Two pointers converge from both ends, checking each rotationally-valid digit pair |
| 12 | ⬜ | 283 | Move Zeroes | 64.3% | [LeetCode](https://leetcode.com/problems/move-zeroes/) | - | Fast/slow pointers shift non-zero elements forward in place |
| 13 | ⬜ | 344 | Reverse String | 81.2% | [LeetCode](https://leetcode.com/problems/reverse-string/) | - | Two pointers swap characters from opposite ends, moving inward |
| 14 | ⬜ | 345 | Reverse Vowels of a String | 62.1% | [LeetCode](https://leetcode.com/problems/reverse-vowels-of-a-string/) | - | Two pointers converge from both ends, swapping only vowel positions |
| 15 | ⬜ | 349 | Intersection of Two Arrays | 78.2% | [LeetCode](https://leetcode.com/problems/intersection-of-two-arrays/) | - | Two pointers walk both sorted arrays together to find shared elements |
| 16 | ⬜ | 350 | Intersection of Two Arrays II | 60.2% | [LeetCode](https://leetcode.com/problems/intersection-of-two-arrays-ii/) | - | Two pointers walk both sorted arrays, matching elements including duplicates |
| 17 | ⬜ | 392 | Is Subsequence | 49.4% | [LeetCode](https://leetcode.com/problems/is-subsequence/) | - | Two pointers advance through both strings in lockstep, one only on a match |
| 18 | ⬜ | 408 | Valid Word Abbreviation | 37.0% | [LeetCode](https://leetcode.com/problems/valid-word-abbreviation/) | - | Two pointers walk the word and the abbreviation together |
| 19 | ⬜ | 455 | Assign Cookies | 55.4% | [LeetCode](https://leetcode.com/problems/assign-cookies/) | - | Two pointers on sorted children and cookies greedily match smallest-fit pairs |
| 20 | ⬜ | 541 | Reverse String II | 54.4% | [LeetCode](https://leetcode.com/problems/reverse-string-ii/) | - | A pointer marks each chunk boundary; an inner two-pointer swap reverses it |
| 21 | ⬜ | 557 | Reverse Words in a String III | 84.1% | [LeetCode](https://leetcode.com/problems/reverse-words-in-a-string-iii/) | - | Two pointers reverse the characters within each word in place |
| 22 | ⬜ | 653 | Two Sum IV - Input is a BST | 63.6% | [LeetCode](https://leetcode.com/problems/two-sum-iv-input-is-a-bst/) | - | In-order traversal gives sorted values, then two pointers converge to the target sum |
| 23 | ⬜ | 680 | Valid Palindrome II | 44.6% | [LeetCode](https://leetcode.com/problems/valid-palindrome-ii/) | - | Two pointers converge from both ends, allowed one mismatch skip on either side |

## Problems #696 - #2200

| S.No. | Status | # | Problem | Acceptance | Link | Solution | Why Two Pointers |
|-------|--------|---|---------|-----------|------|----------|-------------------|
| 24 | ⬜ | 696 | Count Binary Substrings | 70.5% | [LeetCode](https://leetcode.com/problems/count-binary-substrings/) | - | Two pointers track consecutive run lengths, comparing adjacent groups |
| 25 | ⬜ | 821 | Shortest Distance to a Character | 73.0% | [LeetCode](https://leetcode.com/problems/shortest-distance-to-a-character/) | - | Two passes with a pointer tracking the nearest occurrence seen so far |
| 26 | ⬜ | 832 | Flipping an Image | 84.0% | [LeetCode](https://leetcode.com/problems/flipping-an-image/) | - | Two pointers per row swap-and-invert symmetric elements |
| 27 | ⬜ | 844 | Backspace String Compare | 50.2% | [LeetCode](https://leetcode.com/problems/backspace-string-compare/) | - | Two pointers walk both strings backward, skipping backspaced characters |
| 28 | ⬜ | 876 | Middle of the Linked List | 82.3% | [LeetCode](https://leetcode.com/problems/middle-of-the-linked-list/) | - | Fast pointer moves 2x the speed of the slow pointer |
| 29 | ⬜ | 905 | Sort Array By Parity | 76.6% | [LeetCode](https://leetcode.com/problems/sort-array-by-parity/) | - | Two pointers converge from both ends, swapping odd/even values |
| 30 | ⬜ | 917 | Reverse Only Letters | 69.0% | [LeetCode](https://leetcode.com/problems/reverse-only-letters/) | - | Two pointers converge from both ends, skipping non-letter characters |
| 31 | ⬜ | 922 | Sort Array By Parity II | 71.3% | [LeetCode](https://leetcode.com/problems/sort-array-by-parity-ii/) | - | Two pointers step through even-indexed and odd-indexed slots together |
| 32 | ⬜ | 925 | Long Pressed Name | 33.1% | [LeetCode](https://leetcode.com/problems/long-pressed-name/) | - | Two pointers walk name and typed strings in parallel, allowing repeats |
| 33 | ⬜ | 942 | DI String Match | 81.3% | [LeetCode](https://leetcode.com/problems/di-string-match/) | - | Two pointers track a low/high bound, assigned based on each instruction |
| 34 | ⬜ | 977 | Squares of a Sorted Array | 74.1% | [LeetCode](https://leetcode.com/problems/squares-of-a-sorted-array/) | - | Two pointers from both ends compare magnitudes, filling the result from the back |
| 35 | ⬜ | 1089 | Duplicate Zeros | 54.0% | [LeetCode](https://leetcode.com/problems/duplicate-zeros/) | - | A read pointer scans while a second tracks the shifted write position |
| 36 | ⬜ | 1099 | Two Sum Less Than K | 62.2% | [LeetCode](https://leetcode.com/problems/two-sum-less-than-k/) | - | Sort the array, then two pointers converge to maximize the sum under k |
| 37 | ⬜ | 1332 | Remove Palindromic Subsequences | 77.2% | [LeetCode](https://leetcode.com/problems/remove-palindromic-subsequences/) | - | Two pointers converge from both ends to check whether it's already a palindrome |
| 38 | ⬜ | 1346 | Check If N and Its Double Exist | 42.0% | [LeetCode](https://leetcode.com/problems/check-if-n-and-its-double-exist/) | - | On a sorted array, two pointers check value/double pairs |
| 39 | ⬜ | 1385 | Find the Distance Value Between Two Arrays | 72.2% | [LeetCode](https://leetcode.com/problems/find-the-distance-value-between-two-arrays/) | - | Two pointers over the sorted second array bound each comparison |
| 40 | ⬜ | 1455 | Check If a Word Occurs As a Prefix of Any Word in a Sentence | 68.8% | [LeetCode](https://leetcode.com/problems/check-if-a-word-occurs-as-a-prefix-of-any-word-in-a-sentence/) | - | Two pointers scan sentence word boundaries and compare against the prefix |
| 41 | ⬜ | 1768 | Merge Strings Alternately | 82.2% | [LeetCode](https://leetcode.com/problems/merge-strings-alternately/) | - | Two pointers advance through both strings, alternating characters |
| 42 | ⬜ | 1826 | Faulty Sensor | 50.5% | [LeetCode](https://leetcode.com/problems/faulty-sensor/) | - | Two pointers compare both arrays in parallel, skipping past the mismatch |
| 43 | ⬜ | 1961 | Check If String Is a Prefix of Array | 52.9% | [LeetCode](https://leetcode.com/problems/check-if-string-is-a-prefix-of-array/) | - | Two pointers track position across the words array and the target string |
| 44 | ⬜ | 2000 | Reverse Prefix of Word | 86.5% | [LeetCode](https://leetcode.com/problems/reverse-prefix-of-word/) | - | Two pointers reverse characters up to a found index |
| 45 | ⬜ | 2108 | Find First Palindromic String in the Array | 84.1% | [LeetCode](https://leetcode.com/problems/find-first-palindromic-string-in-the-array/) | - | Two pointers converge from both ends to check each string |
| 46 | ⬜ | 2200 | Find All K-Distant Indices in an Array | 77.2% | [LeetCode](https://leetcode.com/problems/find-all-k-distant-indices-in-an-array/) | - | A pointer/window tracks distance around each key index |

## Problems #2367 - #3992

| S.No. | Status | # | Problem | Acceptance | Link | Solution | Why Two Pointers |
|-------|--------|---|---------|-----------|------|----------|-------------------|
| 47 | ⬜ | 2367 | Number of Arithmetic Triplets | 85.6% | [LeetCode](https://leetcode.com/problems/number-of-arithmetic-triplets/) | - | Two pointers scan the sorted array for equal-difference triplets |
| 48 | ⬜ | 2441 | Largest Positive Integer That Exists With Its Negative | 74.5% | [LeetCode](https://leetcode.com/problems/largest-positive-integer-that-exists-with-its-negative/) | - | Two pointers from both ends of a value-sorted array find matching +/- pairs |
| 49 | ⬜ | 2460 | Apply Operations to an Array | 74.8% | [LeetCode](https://leetcode.com/problems/apply-operations-to-an-array/) | - | Fast/slow pointers merge equal adjacent pairs, then shift zeros to the end |
| 50 | ⬜ | 2465 | Number of Distinct Averages | 59.1% | [LeetCode](https://leetcode.com/problems/number-of-distinct-averages/) | - | After sorting, two pointers repeatedly pair the smallest with the largest |
| 51 | ⬜ | 2511 | Maximum Enemy Forts That Can Be Captured | 41.8% | [LeetCode](https://leetcode.com/problems/maximum-enemy-forts-that-can-be-captured/) | - | Two pointers scan for a capturable `1...0...-1` pattern |
| 52 | ⬜ | 2540 | Minimum Common Value | 60.7% | [LeetCode](https://leetcode.com/problems/minimum-common-value/) | - | Two pointers walk both sorted arrays together to the first common value |
| 53 | ⬜ | 2562 | Find the Array Concatenation Value | 72.1% | [LeetCode](https://leetcode.com/problems/find-the-array-concatenation-value/) | - | Two pointers from both ends concatenate and sum each pair |
| 54 | ⬜ | 2570 | Merge Two 2D Arrays by Summing Values | 81.7% | [LeetCode](https://leetcode.com/problems/merge-two-2d-arrays-by-summing-values/) | - | Two pointers merge two sorted arrays by matching ids, same family as #88 |
| 55 | ⬜ | 2697 | Lexicographically Smallest Palindrome | 81.7% | [LeetCode](https://leetcode.com/problems/lexicographically-smallest-palindrome/) | - | Two pointers converge from both ends, picking the smaller of each mismatched pair |
| 56 | ⬜ | 2824 | Count Pairs Whose Sum is Less than Target | 87.6% | [LeetCode](https://leetcode.com/problems/count-pairs-whose-sum-is-less-than-target/) | - | Sort the array, then two pointers converge while counting valid pairs |
| 57 | ⬜ | 2903 | Find Indices With Index and Value Difference I | 60.1% | [LeetCode](https://leetcode.com/problems/find-indices-with-index-and-value-difference-i/) | - | A trailing pointer tracks the running min/max seen so far while scanning |
| 58 | ⬜ | 2970 | Count the Number of Incremovable Subarrays I | 56.5% | [LeetCode](https://leetcode.com/problems/count-the-number-of-incremovable-subarrays-i/) | - | Two pointers/window scan for valid removable-subarray boundaries |
| 59 | ⬜ | 3194 | Minimum Average of Smallest and Largest Elements | 85.1% | [LeetCode](https://leetcode.com/problems/minimum-average-of-smallest-and-largest-elements/) | - | Sort, then two pointers repeatedly pair the smallest with the largest remaining |
| 60 | ⬜ | 3633 | Earliest Finish Time for Land and Water Rides I | 73.0% | [LeetCode](https://leetcode.com/problems/earliest-finish-time-for-land-and-water-rides-i/) | - | Two pointers over sorted ride-start times pick the earliest valid pairing |
| 61 | ⬜ | 3643 | Flip Square Submatrix Vertically | 79.2% | [LeetCode](https://leetcode.com/problems/flip-square-submatrix-vertically/) | - | Two pointers (top row / bottom row) swap while flipping the submatrix |
| 62 | ⬜ | 3667 | Sort Array By Absolute Value | 86.8% | [LeetCode](https://leetcode.com/problems/sort-array-by-absolute-value/) | - | Two pointers from both ends of the value-sorted array merge by absolute value |
| 63 | ⬜ | 3750 | Minimum Number of Flips to Reverse Binary String | 77.1% | [LeetCode](https://leetcode.com/problems/minimum-number-of-flips-to-reverse-binary-string/) | - | Two pointers compare the string against its reverse from both ends |
| 64 | ⬜ | 3794 | Reverse String Prefix | 89.5% | [LeetCode](https://leetcode.com/problems/reverse-string-prefix/) | - | Two pointers reverse characters within the given prefix length |
| 65 | ⬜ | 3823 | Reverse Letters Then Special Characters in a String | 82.4% | [LeetCode](https://leetcode.com/problems/reverse-letters-then-special-characters-in-a-string/) | - | Two pointers converge from both ends, skipping specials and swapping letters |
| 66 | ⬜ | 3884 | First Matching Character From Both Ends | 81.5% | [LeetCode](https://leetcode.com/problems/first-matching-character-from-both-ends/) | - | Two pointers converge from both ends, comparing characters directly |
| 67 | ⬜ | 3936 | Minimum Swaps to Move Zeros to End | 60.5% | [LeetCode](https://leetcode.com/problems/minimum-swaps-to-move-zeros-to-end/) | - | Fast/slow pointers shift non-zero elements forward, same family as #283 |
| 68 | ⬜ | 3940 | Limit Occurrences in Sorted Array | 73.4% | [LeetCode](https://leetcode.com/problems/limit-occurrences-in-sorted-array/) | - | Fast/slow pointers overwrite in place while capping the allowed occurrence count |
| 69 | ⬜ | 3992 | Rearrange String to Avoid Character Pair | 78.2% | [LeetCode](https://leetcode.com/problems/rearrange-string-to-avoid-character-pair/) | - | A pointer scans adjacent characters, swapping ahead to break repeated pairs |

---

## Solutions

### 26. Remove Duplicates from Sorted Array

**Approach:** Two Pointers (Fast & Slow)

```java
class Solution {
    public int removeDuplicates(int[] nums) {
        //O(n) time, O(1) space
        int slow = 1;//start with 1, as array will have at least one unique as arr[0]
        for (int fast = 1; fast < nums.length; fast++){//start with arr[1]
            if(nums[fast] != nums[slow-1]){
                nums[slow] = nums[fast];//move unique element found to slow index
                slow++;//move slow to next, only when non-repeated found 
            }
        }
        return slow;//number of unique elements
    }
}
```

**Dry Run — Input:** `nums = [1,1,2]` → expected `slow=2`, `nums=[1,2,_]`

| fast | nums[fast] | nums[slow-1] | Compare | Action | slow after | nums state |
|------|------------|---------------|---------|--------|-------------|------------|
| start | - | - | - | `slow=1` | 1 | [1,1,2] |
| 1 | 1 | nums[0]=1 | `1 != 1`? No | skip | 1 | [1,1,2] |
| 2 | 2 | nums[0]=1 | `2 != 1`? Yes | `nums[1]=2`, `slow++` | 2 | [1,2,2] |

**Return `2`.** First 2 elements: `[1,2]` ✅

[⬆ Back to Top](#table-of-contents)

### 27. Remove Element

**Approach:** Two Pointers (Fast & Slow)

```java
class Solution {
    //O(n) time, O(1) space
    public int removeElement(int[] nums, int val) {
        int slow = 0;
        for(int fast =0; fast < nums.length; fast++){//fast will move next everytime
            if(val != nums[fast]){
                nums[slow] = nums[fast];
                slow++;//slow will move only when not matched to value
            }
        }
        return slow;//count after removing given value
    }
}
```

**Dry Run — Input:** `nums = [3,2,2,3]`, `val = 3` → expected `slow=2`, `nums=[2,2,_,_]`

| fast | nums[fast] | val != nums[fast]? | Action | slow after | nums state |
|------|------------|------------------------|--------|-------------|------------|
| 0 | 3 | false | skip | 0 | [3,2,2,3] |
| 1 | 2 | true | `nums[0]=2`, `slow++` | 1 | [2,2,2,3] |
| 2 | 2 | true | `nums[1]=2`, `slow++` | 2 | [2,2,2,3] |
| 3 | 3 | false | skip | 2 | [2,2,2,3] |

**Return `2`.** First 2 elements: `[2,2]` ✅

[⬆ Back to Top](#table-of-contents)

### 28. Find the Index of the First Occurrence in a String

**Approach:** Sliding Window (substring comparison)

```java
class Solution {
    public int strStr(String haystack, String needle) {
        //O(n·m) time (n is for haystack loop, m is for needle substring loop) / O(1) space

        //loop should not run if needle first char matches with as last char of haystack (haystack=xya, needle=ay)
        for(int i=0; i <= haystack.length() - needle.length(); i++){
            if(needle.charAt(0) == haystack.charAt(i)){
                if(haystack.substring(i,i+needle.length()).equals(needle)){
                    return i;
                }
            }
        }
        return -1;
    }
}
```

**Dry Run — Input:** `haystack = "leetcode"`, `needle = "leeto"` → expected `-1`

`haystack.length()=8`, `needle.length()=5`, loop runs `i = 0` to `8-5 = 3`.

| i | haystack.charAt(i) | matches needle[0]='l'? | substring(i, i+5) | equals "leeto"? | Result |
|---|---------------------|--------------------------|---------------------|-------------------|--------|
| 0 | 'l' | yes | "leetc" | no | continue |
| 1 | 'e' | no | - | - | skip |
| 2 | 'e' | no | - | - | skip |
| 3 | 't' | no | - | - | skip |

Loop ends (`i=4` fails `i<=3`). Return `-1`. ✅

[⬆ Back to Top](#table-of-contents)

### 88. Merge Sorted Array

**Approach:** Two Pointers (merge from the back)

**Hint Video:** https://www.youtube.com/shorts/R2EdWO88I5k?feature=share

```java
class Solution {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        //Time - O (n+m) -> n is for first array, m is for 2nd array, Space complexity - O(1)
        int i = m-1, j = n-1, k = nums1.length-1;//point to the last of each array
        for(;i>=0 && j>=0;){
            //move larget number to the last position of arr1, and move respective pointer to 1 left
            if(nums1[i]>nums2[j]){
                nums1[k] = nums1[i];
                i--;
            }else{
                nums1[k] = nums2[j];
                j--;
            }
            k--;//move 0's pointer position to left in either case
        }
        if(i==-1){//if first array exhausted, copy 2nd arr to first one as it is
            for(int cnt=j;cnt>=0;cnt--){
                nums1[cnt] = nums2[j];
                j--;
            }
        }//if 2nd array is exhausted, there is no need to copy arr1 to arr1, its already and sorted.
    }
}
```

**Dry Run — Input:** `nums1 = [1,2,3,0,0,0]`, `m = 3`, `nums2 = [2,5,6]`, `n = 3` → expected `[1,2,2,3,5,6]`

Start: `i=2, j=2, k=5`

| Iter | nums1[i] | nums2[j] | Compare | Action | i,j,k after | nums1 state |
|------|----------|----------|---------|--------|--------------|-------------|
| 1 | 3 | 6 | `3>6`? No | `nums1[5]=nums2[2]=6`, `j--` | i=2,j=1,k=4 | [1,2,3,0,0,**6**] |
| 2 | 3 | 5 | `3>5`? No | `nums1[4]=nums2[1]=5`, `j--` | i=2,j=0,k=3 | [1,2,3,0,**5**,6] |
| 3 | 3 | 2 | `3>2`? Yes | `nums1[3]=nums1[2]=3`, `i--` | i=1,j=0,k=2 | [1,2,3,**3**,5,6] |
| 4 | 2 | 2 | `2>2`? No | `nums1[2]=nums2[0]=2`, `j--` | i=1,j=-1,k=1 | [1,2,**2**,3,5,6] |

Loop ends (`j=-1`). Since `i=1` (not `-1`), the cleanup block is skipped — `nums1[0..1] = [1,2]` are original values already in the correct spot.

**Final:** `[1,2,2,3,5,6]` ✅

[⬆ Back to Top](#table-of-contents)

### 125. Valid Palindrome

**Approach:** Two Pointers

```java
class Solution {
    public boolean isPalindrome(String s) {
        //time - O(n), space - (1)
        int start=0, end = s.length()-1;
        while(start<end){
            //keep ignoring non-alphanumric chars
            if(!Character.isLetterOrDigit(s.charAt(start))){
                start++;
            }else if(!Character.isLetterOrDigit(s.charAt(end))){
                end--;
            }
            else if(Character.toLowerCase(s.charAt(start))!=Character.toLowerCase(s.charAt(end))){//compare same case of char
                return false;
            }else{//both chars matched, move to next ones (forward and backward)
                start++;
                end--;
            }
        }
        return true;
    }
}
```

**Dry Run — Input:** `s = "race a car"` → expected `false`

Indices: `0:r 1:a 2:c 3:e 4:' ' 5:a 6:' ' 7:c 8:a 9:r`

| Iter | start (char) | end (char) | Action | New start, end |
|------|--------------|------------|--------|-----------------|
| 1 | 0:'r' | 9:'r' | both alnum, match | start=1, end=8 |
| 2 | 1:'a' | 8:'a' | both alnum, match | start=2, end=7 |
| 3 | 2:'c' | 7:'c' | both alnum, match | start=3, end=6 |
| 4 | 3:'e' | 6:' ' | end is non-alnum → skip it | start=3, end=5 |
| 5 | 3:'e' | 5:'a' | both alnum, **mismatch** → return `false` | - |

[⬆ Back to Top](#table-of-contents)

### 141. Linked List Cycle

**Approach:** Floyd's Cycle Detection (Fast & Slow Pointers)

```java
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode slow = head;//slow moves by 1 step
        ListNode fast = head;//fast moves by 2 steps
        while(fast!=null && fast.next!=null){
            slow = slow.next;
            fast = fast.next.next;
            if(slow == fast) return true;//cycle is detected, return true
        }
        return false;//found null node to end the loop, hence no cycle
    }
}
```

**Dry Run — Input:** `head = [3,2,0,-4]`, `pos = 1` (tail node `-4` connects back to node at index `1`, value `2`)

| Iter | slow | fast | slow == fast? |
|------|------|------|----------------|
| start | 3 | 3 | (not checked yet) |
| 1 | 2 | 0 | no |
| 2 | 0 | 2 | no |
| 3 | -4 | -4 | **yes** → cycle detected, return `true` |

[⬆ Back to Top](#table-of-contents)

### 160. Intersection of Two Linked Lists

**Approach:** Two Pointers (redirect on null)

**Hint Video:** https://www.youtube.com/shorts/WjK-_KN0_Ck?t=97&feature=share

```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        ListNode pa = headA;
        ListNode pb = headB;
        while(pa!=pb){
            if(pa==null)
                pa = headB;//when pa reaches to the end of 1st, point to headB
            else
                pa = pa.next;//else move to next

            if(pb==null)
                pb = headA;//when pb reaches to the end of 2nd, point to headA
            else
                pb = pb.next;//else move to next
        }
        if(pa==pb) return pa;
        return null;
    }
}
```

**Dry Run — Input:** `listA = [4,1,8,4,5]`, `listB = [5,6,1,8,4,5]`, `skipA = 2`, `skipB = 3` (shared tail `[8,4,5]`, intersection value `8`)

Nodes labeled by list + position (value in parens). `a1(4), a2(1)` are A's own nodes; `b1(5), b2(6), b3(1)` are B's own nodes; `c1(8), c2(4), c3(5)` are the **shared** tail nodes (same objects reachable from both lists).

| Iter | pa | pb | pa == pb? |
|------|----|----|-----------|
| start | a1(4) | b1(5) | no |
| 1 | a2(1) | b2(6) | no |
| 2 | c1(8) | b3(1) | no |
| 3 | c2(4) | c1(8) | no |
| 4 | c3(5) | c2(4) | no |
| 5 | b1(5) *(pa hit null → redirected to headB)* | c3(5) | no — **different nodes, same value!** |
| 6 | b2(6) | a1(4) *(pb hit null → redirected to headA)* | no |
| 7 | b3(1) | a2(1) | no — **different nodes, same value again!** |
| 8 | c1(8) | c1(8) | **yes — same node** → return `c1` (val `8`) |

Note iterations 5 and 7: `pa`/`pb` land on nodes with the *same value* but they're genuinely different node objects (`b1` vs `c3`, `b3` vs `a2`) — this only works correctly because the comparison is by reference (`==`), not by value.

**Dry Run — Input (no intersection, different lengths):** `A = [1,2,3]`, `B = [5,6,7,8]` → expected `null`

| Iter | pa | pb | Note |
|------|----|----|------|
| 0 | 1 | 5 | start |
| 1 | 2 | 6 | |
| 2 | 3 | 7 | |
| 3 | `null` → redirect → 5 | 8 | `pa` exhausted A (3 steps) |
| 4 | 6 | `null` → redirect → 1 | `pb` exhausted B (4 steps), one iteration later than `pa` since B is longer |
| 5 | 7 | 2 | |
| 6 | 8 | 3 | |
| 7 | `null` | `null` | both exhausted their *second* list at the same time (`pa`'s total steps = `lenA+lenB` = 7, same for `pb`) |

Loop condition `pa != pb` → `null != null` → **false** → exits immediately, before either pointer gets a chance to redirect again. Return `null`. ✅ Confirms the redirect trick works regardless of the length difference between the two lists — both pointers always cover the same *total* distance (`lenA+lenB`) before concluding "no intersection."

[⬆ Back to Top](#table-of-contents)

---

## Legend

- ⬜ Not attempted
- ✅ Solution submitted

**Total Problems:** 69  
**Solved:** 7/69  
**Status:** In Progress  
**Last Updated:** 2026-08-21
