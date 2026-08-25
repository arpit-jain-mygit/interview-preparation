# LeetCode Easy SQL (Database) Problems - Complete Study Guide

**55 Problems | LeetCode Database Study Plan | Free/Non-Premium, Sorted by Problem Number**

Source: https://leetcode.com/problemset/database/ (Easy difficulty, excludes premium-only problems)

---

## Table of Contents

- [Problems #175 - #627](#problems-175---627)
- [Problems #1050 - #1527](#problems-1050---1527)
- [Problems #1581 - #1978](#problems-1581---1978)
- [Problems #2356 - #3793](#problems-2356---3793)
- [Solutions](#solutions)
- [Legend](#legend)

---

## Problems #175 - #627

| S.No. | Status | # | Problem | Acceptance | Link | Solution | Key Concept |
|-------|--------|---|---------|-----------|------|----------|--------------|
| 1 | ✅ | 175 | Combine Two Tables | 79.9% | [LeetCode](https://leetcode.com/problems/combine-two-tables/) | [View](#175-combine-two-tables) | LEFT JOIN to keep all rows from the left table regardless of a match |
| 2 | ✅ | 181 | Employees Earning More Than Their Managers | 73.8% | [LeetCode](https://leetcode.com/problems/employees-earning-more-than-their-managers/) | [View](#181-employees-earning-more-than-their-managers) | Self JOIN, comparing each employee's salary to their manager's salary |
| 3 | ✅ | 182 | Duplicate Emails | 74.2% | [LeetCode](https://leetcode.com/problems/duplicate-emails/) | [View](#182-duplicate-emails) | GROUP BY email with HAVING COUNT(*) > 1 |
| 4 | ✅ | 183 | Customers Who Never Order | 72.3% | [LeetCode](https://leetcode.com/problems/customers-who-never-order/) | [View](#183-customers-who-never-order) | LEFT JOIN with a NULL check (or NOT IN) to find unmatched rows |
| 5 | ✅ | 196 | Delete Duplicate Emails | 66.6% | [LeetCode](https://leetcode.com/problems/delete-duplicate-emails/) | [View](#196-delete-duplicate-emails) | Self JOIN DELETE, keeping the row with the smaller id per email |
| 6 | ✅ | 197 | Rising Temperature | 52.0% | [LeetCode](https://leetcode.com/problems/rising-temperature/) | [View](#197-rising-temperature) | Self JOIN on consecutive dates using DATEDIFF |
| 7 | ⬜ | 511 | Game Play Analysis I | 76.6% | [LeetCode](https://leetcode.com/problems/game-play-analysis-i/) | - | GROUP BY player_id, MIN(event_date) |
| 8 | ⬜ | 577 | Employee Bonus | 78.0% | [LeetCode](https://leetcode.com/problems/employee-bonus/) | - | LEFT JOIN, filtering for bonus < 1000 or NULL |
| 9 | ⬜ | 584 | Find Customer Referee | 73.4% | [LeetCode](https://leetcode.com/problems/find-customer-referee/) | - | WHERE with `!=` and NULL handling (`OR referee_id IS NULL`) |
| 10 | ⬜ | 586 | Customer Placing the Largest Number of Orders | 64.7% | [LeetCode](https://leetcode.com/problems/customer-placing-the-largest-number-of-orders/) | - | GROUP BY customer_number, ORDER BY COUNT(*) DESC LIMIT 1 |
| 11 | ⬜ | 595 | Big Countries | 68.8% | [LeetCode](https://leetcode.com/problems/big-countries/) | - | WHERE with an OR across two independent conditions |
| 12 | ⬜ | 596 | Classes With at Least 5 Students | 64.7% | [LeetCode](https://leetcode.com/problems/classes-with-at-least-5-students/) | - | GROUP BY class HAVING COUNT(*) >= 5 |
| 13 | ⬜ | 607 | Sales Person | 66.3% | [LeetCode](https://leetcode.com/problems/sales-person/) | - | NOT IN subquery to exclude salespeople tied to a specific company's orders |
| 14 | ⬜ | 610 | Triangle Judgement | 75.1% | [LeetCode](https://leetcode.com/problems/triangle-judgement/) | - | CASE WHEN applying the triangle inequality theorem |
| 15 | ⬜ | 619 | Biggest Single Number | 72.0% | [LeetCode](https://leetcode.com/problems/biggest-single-number/) | - | Subquery: GROUP BY HAVING COUNT(*) = 1, then MAX() |
| 16 | ⬜ | 620 | Not Boring Movies | 75.2% | [LeetCode](https://leetcode.com/problems/not-boring-movies/) | - | WHERE filtering on an odd id (MOD) and a text condition |
| 17 | ⬜ | 627 | Swap Salary | 84.9% | [LeetCode](https://leetcode.com/problems/swap-salary/) | - | UPDATE with CASE WHEN to flip an enum-like column |

## Problems #1050 - #1527

| S.No. | Status | # | Problem | Acceptance | Link | Solution | Key Concept |
|-------|--------|---|---------|-----------|------|----------|--------------|
| 18 | ⬜ | 1050 | Actors and Directors Who Cooperated At Least Three Times | 71.4% | [LeetCode](https://leetcode.com/problems/actors-and-directors-who-cooperated-at-least-three-times/) | - | GROUP BY actor_id, director_id HAVING COUNT(*) >= 3 |
| 19 | ⬜ | 1068 | Product Sales Analysis I | 86.1% | [LeetCode](https://leetcode.com/problems/product-sales-analysis-i/) | - | Simple JOIN on product_id |
| 20 | ⬜ | 1075 | Project Employees I | 67.2% | [LeetCode](https://leetcode.com/problems/project-employees-i/) | - | JOIN + GROUP BY with ROUND(AVG(experience_years)) |
| 21 | ⬜ | 1084 | Sales Analysis III | 48.2% | [LeetCode](https://leetcode.com/problems/sales-analysis-iii/) | - | GROUP BY product_id HAVING all sales fall inside a date range |
| 22 | ⬜ | 1141 | User Activity for the Past 30 Days I | 51.4% | [LeetCode](https://leetcode.com/problems/user-activity-for-the-past-30-days-i/) | - | Date range filter + GROUP BY day, COUNT(DISTINCT user_id) |
| 23 | ⬜ | 1148 | Article Views I | 76.8% | [LeetCode](https://leetcode.com/problems/article-views-i/) | - | DISTINCT filter where author_id = viewer_id |
| 24 | ⬜ | 1179 | Reformat Department Table | 76.4% | [LeetCode](https://leetcode.com/problems/reformat-department-table/) | - | Pivot rows to columns using conditional SUM per month |
| 25 | ⬜ | 1211 | Queries Quality and Percentage | 54.5% | [LeetCode](https://leetcode.com/problems/queries-quality-and-percentage/) | - | GROUP BY query_name with ROUND(AVG(...), 2) ratio calculations |
| 26 | ⬜ | 1251 | Average Selling Price | 37.8% | [LeetCode](https://leetcode.com/problems/average-selling-price/) | - | LEFT JOIN on a date range, weighted average via SUM/SUM |
| 27 | ⬜ | 1280 | Students and Examinations | 61.8% | [LeetCode](https://leetcode.com/problems/students-and-examinations/) | - | CROSS JOIN students × subjects, LEFT JOIN exams, GROUP BY COUNT |
| 28 | ⬜ | 1327 | List the Products Ordered in a Period | 72.0% | [LeetCode](https://leetcode.com/problems/list-the-products-ordered-in-a-period/) | - | JOIN + GROUP BY HAVING SUM(unit) >= 100, filtered by date range |
| 29 | ⬜ | 1378 | Replace Employee ID With The Unique Identifier | 83.8% | [LeetCode](https://leetcode.com/problems/replace-employee-id-with-the-unique-identifier/) | - | LEFT JOIN to preserve unmatched employees |
| 30 | ⬜ | 1407 | Top Travellers | 57.7% | [LeetCode](https://leetcode.com/problems/top-travellers/) | - | LEFT JOIN + GROUP BY SUM(distance), ORDER BY |
| 31 | ⬜ | 1484 | Group Sold Products By The Date | 78.2% | [LeetCode](https://leetcode.com/problems/group-sold-products-by-the-date/) | - | GROUP BY sell_date with GROUP_CONCAT(DISTINCT product) |
| 32 | ⬜ | 1517 | Find Users With Valid E-Mails | 35.4% | [LeetCode](https://leetcode.com/problems/find-users-with-valid-e-mails/) | - | REGEXP pattern matching against an email format |
| 33 | ⬜ | 1527 | Patients With a Condition | 39.2% | [LeetCode](https://leetcode.com/problems/patients-with-a-condition/) | - | LIKE pattern matching for a word-boundary prefix code |

## Problems #1581 - #1978

| S.No. | Status | # | Problem | Acceptance | Link | Solution | Key Concept |
|-------|--------|---|---------|-----------|------|----------|--------------|
| 34 | ⬜ | 1581 | Customer Who Visited but Did Not Make Any Transactions | 68.4% | [LeetCode](https://leetcode.com/problems/customer-who-visited-but-did-not-make-any-transactions/) | - | LEFT JOIN, WHERE transaction IS NULL, GROUP BY COUNT |
| 35 | ⬜ | 1587 | Bank Account Summary II | 83.0% | [LeetCode](https://leetcode.com/problems/bank-account-summary-ii/) | - | JOIN + GROUP BY SUM(amount) HAVING > 10000 |
| 36 | ⬜ | 1633 | Percentage of Users Attended a Contest | 61.0% | [LeetCode](https://leetcode.com/problems/percentage-of-users-attended-a-contest/) | - | JOIN, COUNT(DISTINCT) divided by total users via a scalar subquery |
| 37 | ⬜ | 1661 | Average Time of Process per Machine | 66.9% | [LeetCode](https://leetcode.com/problems/average-time-of-process-per-machine/) | - | Self JOIN pairing 'start' and 'end' rows, AVG(end - start) |
| 38 | ⬜ | 1667 | Fix Names in a Table | 60.7% | [LeetCode](https://leetcode.com/problems/fix-names-in-a-table/) | - | CONCAT with UPPER/LOWER + SUBSTRING to fix casing |
| 39 | ⬜ | 1683 | Invalid Tweets | 85.2% | [LeetCode](https://leetcode.com/problems/invalid-tweets/) | - | WHERE filtering on LENGTH(content) |
| 40 | ⬜ | 1693 | Daily Leads and Partners | 86.9% | [LeetCode](https://leetcode.com/problems/daily-leads-and-partners/) | - | GROUP BY date_id, make_name with COUNT(DISTINCT ...) |
| 41 | ⬜ | 1729 | Find Followers Count | 69.6% | [LeetCode](https://leetcode.com/problems/find-followers-count/) | - | GROUP BY user_id, COUNT(*), ORDER BY user_id |
| 42 | ⬜ | 1731 | The Number of Employees Which Report to Each Employee | 53.8% | [LeetCode](https://leetcode.com/problems/the-number-of-employees-which-report-to-each-employee/) | - | Self JOIN GROUP BY manager, COUNT(*) + ROUND(AVG(age)) |
| 43 | ⬜ | 1741 | Find Total Time Spent by Each Employee | 86.4% | [LeetCode](https://leetcode.com/problems/find-total-time-spent-by-each-employee/) | - | GROUP BY emp_id, event_day, SUM(out_time - in_time) |
| 44 | ⬜ | 1757 | Recyclable and Low Fat Products | 88.6% | [LeetCode](https://leetcode.com/problems/recyclable-and-low-fat-products/) | - | WHERE combining two flag-column conditions |
| 45 | ⬜ | 1789 | Primary Department for Each Employee | 75.2% | [LeetCode](https://leetcode.com/problems/primary-department-for-each-employee/) | - | UNION of explicit primary rows and single-department employees |
| 46 | ⬜ | 1795 | Rearrange Products Table | 85.5% | [LeetCode](https://leetcode.com/problems/rearrange-products-table/) | - | UNPIVOT via UNION ALL across store columns, filtering NOT NULL |
| 47 | ⬜ | 1873 | Calculate Special Bonus | 57.1% | [LeetCode](https://leetcode.com/problems/calculate-special-bonus/) | - | CASE WHEN combining an even-id check and a name-prefix check |
| 48 | ⬜ | 1890 | The Latest Login in 2020 | 77.1% | [LeetCode](https://leetcode.com/problems/the-latest-login-in-2020/) | - | GROUP BY user_id, MAX(time_stamp), filtered to a single year |
| 49 | ⬜ | 1965 | Employees With Missing Information | 73.5% | [LeetCode](https://leetcode.com/problems/employees-with-missing-information/) | - | UNION + GROUP BY HAVING COUNT(*) = 1 to find unmatched ids |
| 50 | ⬜ | 1978 | Employees Whose Manager Left the Company | 48.9% | [LeetCode](https://leetcode.com/problems/employees-whose-manager-left-the-company/) | - | LEFT JOIN self, salary threshold + manager id not present in table |

## Problems #2356 - #3793

| S.No. | Status | # | Problem | Acceptance | Link | Solution | Key Concept |
|-------|--------|---|---------|-----------|------|----------|--------------|
| 51 | ⬜ | 2356 | Number of Unique Subjects Taught by Each Teacher | 89.3% | [LeetCode](https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher/) | - | GROUP BY teacher_id, COUNT(DISTINCT subject_id) |
| 52 | ⬜ | 3436 | Find Valid Emails | 43.3% | [LeetCode](https://leetcode.com/problems/find-valid-emails/) | - | REGEXP pattern validation against a stricter email format |
| 53 | ⬜ | 3465 | Find Products with Valid Serial Numbers | 28.8% | [LeetCode](https://leetcode.com/problems/find-products-with-valid-serial-numbers/) | - | REGEXP pattern match on a fixed serial-number format |
| 54 | ⬜ | 3570 | Find Books with No Available Copies | 54.7% | [LeetCode](https://leetcode.com/problems/find-books-with-no-available-copies/) | - | GROUP BY book_id HAVING SUM(available_copies) = 0 |
| 55 | ⬜ | 3793 | Find Users with High Token Usage | 57.1% | [LeetCode](https://leetcode.com/problems/find-users-with-high-token-usage/) | - | GROUP BY / window function comparing usage against a threshold |

---

## Solutions

### 175. Combine Two Tables

**Approach:** LEFT JOIN

```sql
select p.firstName, p.lastName, a.city, a.state
from Person p
left join Address a on p.personId = a.personId;
```

### 181. Employees Earning More Than Their Managers

**Approach:** Self JOIN

The `Employee` table is read twice under two aliases — `e` for the employee row, `m` for the manager row — paired wherever `e.managerId = m.id`, then filtered to `e.salary > m.salary`.

**View 1 — `e` (the employee copy)**
```
e.id | e.name  | e.salary | e.managerId
-----+---------+----------+------------
  1  | Joe     |  70000   |     3
  2  | Henry   |  80000   |     4
  3  | Sam     |  60000   |    null
  4  | Max     |  90000   |    null
```

**View 2 — `m` (the manager copy, same table)**
```
m.id | m.name  | m.salary
-----+---------+---------
  1  | Joe     |  70000
  2  | Henry   |  80000
  3  | Sam     |  60000
  4  | Max     |  90000
```

**Join them on `e.managerId = m.id`:**
```
e.name (salary) | matches               | m.name (salary)
-----------------+-----------------------+-----------------
Joe    (70000)  | mId 3 = id 3          | Sam  (60000)
Henry  (80000)  | mId 4 = id 4          | Max  (90000)
Sam    (60000)  | mId null → no match   | —
Max    (90000)  | mId null → no match   | —
```

**Apply `e.salary > m.salary`:**
```
Joe    70000 > 60000  → true   → kept
Henry  80000 > 90000  → false  → dropped
```

**Result:**
```
Employee
--------
Joe
```

```sql
select e.name as Employee
from Employee e
join Employee m ON e.managerId = m.id
where e.salary > m.salary;
```

### 182. Duplicate Emails

**Approach 1: GROUP BY + HAVING**

```sql
select Email
from Person p
group by email
having count(email) > 1;
```

**Approach 2: Subquery (filter the aggregate with WHERE instead of HAVING)**

`WHERE` runs before `SELECT`, so a `SELECT`-list alias in the *same* query isn't visible to that query's own `WHERE` clause yet. A subquery sidesteps this: it runs to completion first, producing a materialized derived table with real, named columns — so the outer query can filter on them with a plain `WHERE`.

**Step 1 — source table `Person`**
```
id | email
---+-----------
1  | a@b.com
2  | c@d.com
3  | a@b.com
```

**Step 2 — inner query runs to completion first**
```sql
select email, count(*) as cnt
from Person
group by email
```
```
email     | cnt
----------+-----
a@b.com   |  2      <- grouped 2 rows (id 1, id 3)
c@d.com   |  1      <- grouped 1 row (id 2)
```
This result is now a materialized table, aliased `t`. `cnt` is a finished column, not an in-flight alias.

**Step 3 — outer query treats `t` like any ordinary table**
```sql
select email
from t          -- t = { email, cnt }, just columns now
where cnt > 1   -- plain column filter, nothing special about it
```
```
email     | cnt
----------+-----
a@b.com   |  2      <- cnt > 1 ✓ kept
c@d.com   |  1      <- cnt > 1 ✗ dropped
```

**Step 4 — result**
```
email
--------
a@b.com
```

```sql
select email
from (
  select email, count(*) as cnt
  from Person
  group by email
) t
where cnt > 1;
```

### 183. Customers Who Never Order

**Approach 1: NOT IN subquery**

```sql
select c.name as Customers
from Customers c
where c.id not in (select customerId from Orders);
```

**Approach 2: LEFT JOIN + IS NULL** (NULL-safe by construction — keeps every customer via the outer join, then filters for the ones with no matching order row)

```sql
select c.name as Customers
from Customers c
left join Orders o on c.id = o.customerId
where o.customerId is null;
```

### 196. Delete Duplicate Emails

**Approach:** Self JOIN DELETE — keep the row with the smallest `id` per email, delete the rest.

**Step 1 — source table `Person`**
```
id | email
---+------------------
1  | john@example.com
2  | bob@example.com
3  | john@example.com
```

**Step 2a — raw cross join `Person p1, Person p2` (every row × every row, no filter yet)**
```
p1.id | p1.email          | p2.id | p2.email
------+-------------------+-------+------------------
  1   | john@example.com  |   1   | john@example.com
  1   | john@example.com  |   2   | bob@example.com
  1   | john@example.com  |   3   | john@example.com
  2   | bob@example.com   |   1   | john@example.com
  2   | bob@example.com   |   2   | bob@example.com
  2   | bob@example.com   |   3   | john@example.com
  3   | john@example.com  |   1   | john@example.com
  3   | john@example.com  |   2   | bob@example.com
  3   | john@example.com  |   3   | john@example.com
```
3 rows × 3 rows = 9 pairs total, unrelated to email — this is what a self join is before any condition narrows it down.

**Step 2b — apply `on p1.email = p2.email`, keep only matching-email pairs**
```
p1.id | p1.email          | p2.id | p2.email          | same email?
------+-------------------+-------+-------------------+-------------
  1   | john@example.com  |   1   | john@example.com  | yes  ✓ kept
  1   | john@example.com  |   2   | bob@example.com    | no   ✗ dropped
  1   | john@example.com  |   3   | john@example.com  | yes  ✓ kept
  2   | bob@example.com   |   1   | john@example.com   | no   ✗ dropped
  2   | bob@example.com   |   2   | bob@example.com    | yes  ✓ kept
  2   | bob@example.com   |   3   | john@example.com   | no   ✗ dropped
  3   | john@example.com  |   1   | john@example.com  | yes  ✓ kept
  3   | john@example.com  |   2   | bob@example.com    | no   ✗ dropped
  3   | john@example.com  |   3   | john@example.com  | yes  ✓ kept
```
9 raw pairs → 5 survive: 4 for the john group `{1,3}` (2×2), 1 for the bob group `{2}` (1×1).

**Step 3 — apply `where p1.id > p2.id` on those 5 surviving pairs, mark matches for delete**
```
p1.id | p2.id | p1.id > p2.id ?  | outcome
------+-------+------------------+-------------------
  1   |   1   |  1 > 1 = false   | not marked
  1   |   3   |  1 > 3 = false   | not marked
  3   |   1   |  3 > 1 = true    | ✗ mark p1 (id=3) for delete
  3   |   3   |  3 > 3 = false   | not marked
  2   |   2   |  2 > 2 = false   | not marked
```
Row `id=1` (john) never finds a smaller-id partner sharing its email → never marked → keeper.
Row `id=3` (john) finds `id=1`, which is smaller → marked → deleted.
Row `id=2` (bob) has no one else sharing its email at all → never marked → keeper.

**Step 4 — result after DELETE**
```
id | email
---+------------------
1  | john@example.com
2  | bob@example.com
```
`id=3` is removed; the smallest-id row per email is the only one left standing.

**MySQL** — supports multi-table `DELETE ... JOIN`, so the alias to delete from (`p1`) must be named right after `DELETE`, since a join alone doesn't say which side's rows to remove:

```sql
delete p1
from Person p1
join Person p2 on p1.email = p2.email
where p1.id > p2.id;
```

**Oracle** — `DELETE` only ever operates on one table; there's no `JOIN` clause allowed in a `DELETE` statement at all. Same logic, expressed as a single-table delete with a correlated subquery:

```sql
delete from Person p1
where exists (
  select 1 from Person p2
  where p2.email = p1.email
    and p2.id < p1.id
);
```

Or the simpler `MIN(id)` form — Oracle has no restriction against referencing the table being deleted from inside its own subquery (MySQL does, and needs an extra derived-table wrapper to work around it):

```sql
delete from Person p1
where p1.id not in (
  select min(id) from Person group by email
);
```

### 197. Rising Temperature

**Approach:** Self JOIN on consecutive calendar dates, not on `id` adjacency.

An `id`-based join (`w2.id = w1.id + 1`) looks tempting since `id` and `recordDate` often happen to increase together — but `id` is just a primary key with no guaranteed relationship to date order. Counterexample that breaks it:

```
id | recordDate  | temperature
1  | 2000-12-16  |     3
2  | 2000-12-15  |    -1
```

Here `id=1`'s date (Dec 16) is *later* than `id=2`'s date (Dec 15) — the id order and date order are reversed. `w2.id = w1.id+1` pairs `w1=1` (Dec 16) as "yesterday" and `w2=2` (Dec 15) as "today," backwards from reality, so the temperature check runs on the wrong pair and misses the correct answer (`id=1`, since Dec 16's temp of 3 is greater than the real previous day Dec 15's temp of -1). The fix: join on `recordDate` adjacency directly, so it's correct regardless of what the `id`s happen to be.

```sql
select w2.id
from weather w1, weather w2
where w2.recordDate = w1.recordDate + 1
  and w2.temperature > w1.temperature;
```

---

## Legend

- ⬜ Not attempted
- ✅ Solution submitted

**Total Problems:** 55
**Solved:** 6/55
**Status:** In Progress
**Last Updated:** 2026-08-24
