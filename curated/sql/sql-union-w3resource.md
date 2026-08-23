# SQL UNION — Practice Set (w3resource)

Source: [w3resource SQL Union Exercises](https://www.w3resource.com/sql-exercises/union/sql-union.php) (9 exercises).

Uses the same Salesman / Customer / Orders schema as [sql-joins-w3resource.md](sql-joins-w3resource.md).

## Table Structures & Sample Data

**salesman**

| salesman_id | name | city | commission |
|---|---|---|---|
| 5001 | James Hoog | New York | 0.15 |
| 5002 | Nail Knite | Paris | 0.13 |
| 5005 | Pit Alex | London | 0.11 |
| 5006 | Mc Lyon | Paris | 0.14 |
| 5007 | Paul Adam | Rome | 0.13 |
| 5003 | Lauson Hen | San Jose | 0.12 |

**customer**

| customer_id | cust_name | city | grade | salesman_id |
|---|---|---|---|---|
| 3002 | Nick Rimando | New York | 100 | 5001 |
| 3007 | Brad Davis | New York | 200 | 5001 |
| 3005 | Graham Zusi | California | 200 | 5002 |
| 3008 | Julian Green | London | 300 | 5002 |
| 3004 | Fabian Johnson | Paris | 300 | 5006 |
| 3009 | Geoff Cameron | Berlin | 100 | 5003 |
| 3003 | Jozy Altidor | Moscow | 200 | 5007 |
| 3001 | Brad Guzan | London | NULL | 5005 |

**orders**

| ord_no | purch_amt | ord_date | customer_id | salesman_id |
|---|---|---|---|---|
| 70001 | 150.5 | 2012-10-05 | 3005 | 5002 |
| 70009 | 270.65 | 2012-09-10 | 3001 | 5005 |
| 70002 | 65.26 | 2012-10-05 | 3002 | 5001 |
| 70004 | 110.5 | 2012-08-17 | 3009 | 5003 |
| 70007 | 948.5 | 2012-09-10 | 3005 | 5002 |
| 70005 | 2400.6 | 2012-07-27 | 3007 | 5001 |
| 70008 | 5760 | 2012-09-10 | 3002 | 5001 |
| 70010 | 1983.43 | 2012-10-10 | 3004 | 5006 |
| 70003 | 2480.4 | 2012-10-10 | 3009 | 5003 |
| 70012 | 250.45 | 2012-06-27 | 3008 | 5002 |
| 70011 | 75.29 | 2012-08-17 | 3003 | 5007 |
| 70013 | 3045.6 | 2012-04-25 | 3002 | 5001 |

---

## Exercises & Solutions

### 1. Find All Salespeople and Customers Located in London
Return ID, name, and a type label for each London-based salesperson/customer.

```sql
SELECT salesman_id "ID", name, 'Salesman'
FROM salesman
WHERE city='London'
UNION
(SELECT customer_id "ID", cust_name, 'Customer'
FROM customer
WHERE city='London')
```

### 2. Find Distinct Salespeople and Their Cities
Return salesman_id and city, combining values sourced from both `customer.salesman_id`/`city` and `salesman.salesman_id`/`city`.

```sql
SELECT salesman_id, city
FROM customer

UNION

(SELECT salesman_id, city
FROM salesman)
```

### 3. Find All Salespeople and Customers Involved in the Inventory System
Combine distinct salesman_id/customer_id pairs from `customer` and `orders`.

```sql
SELECT salesman_id, customer_id
FROM customer

UNION

(SELECT salesman_id, customer_id
FROM orders)
```

### 4. Find the Largest and Smallest Orders on Each Date
Return salesperson ID, name, order no., a "highest on"/"lowest on" label, and order date.

```sql
SELECT a.salesman_id, name, ord_no, 'highest on', ord_date
FROM salesman a, orders b
WHERE a.salesman_id = b.salesman_id
AND b.purch_amt = (
    SELECT MAX(purch_amt)
    FROM orders c
    WHERE c.ord_date = b.ord_date
)

UNION

SELECT a.salesman_id, name, ord_no, 'lowest on', ord_date
FROM salesman a, orders b
WHERE a.salesman_id = b.salesman_id
AND b.purch_amt = (
    SELECT MIN(purch_amt)
    FROM orders c
    WHERE c.ord_date = b.ord_date
)
```

### 5. Largest and Smallest Orders on Each Date, Sorted
Same as #4, sorted on the 3rd column (`ord_no`).

```sql
SELECT a.salesman_id, name, ord_no, 'highest on', ord_date
FROM salesman a, orders b
WHERE a.salesman_id = b.salesman_id
AND b.purch_amt = (
    SELECT MAX(purch_amt)
    FROM orders c
    WHERE c.ord_date = b.ord_date
)

UNION

SELECT a.salesman_id, name, ord_no, 'lowest on', ord_date
FROM salesman a, orders b
WHERE a.salesman_id = b.salesman_id
AND b.purch_amt = (
    SELECT MIN(purch_amt)
    FROM orders c
    WHERE c.ord_date = b.ord_date
)

ORDER BY 3
```

### 6. Salespeople Matching Customer City, or "NO MATCH"
Return salesperson ID, name, customer name, commission — flagging salespeople with no customer in their city, sorted by name descending.

```sql
SELECT salesman.salesman_id, name, cust_name, commission
FROM salesman, customer
WHERE salesman.city = customer.city
UNION
SELECT salesman_id, name, 'NO MATCH', commission
FROM salesman
WHERE NOT city = ANY
    (SELECT city
     FROM customer)
ORDER BY 2 DESC
```

### 7. Append MATCHED / NO MATCH Labels by City
Return salesperson ID, name, city, and a MATCHED/NO MATCH flag.

```sql
SELECT a.salesman_id, name, a.city, 'MATCHED'
FROM salesman a, customer b
WHERE a.city = b.city
UNION
SELECT salesman_id, name, city, 'NO MATCH'
FROM salesman
WHERE NOT city = ANY
    (SELECT city
     FROM customer)
ORDER BY 2 DESC
```

### 8. Classify Customers by Rating (High/Low)
Customers with grade ≥ 300 labeled "High Rating", others "Low Rating".

```sql
SELECT customer_id, city, grade, 'High Rating'
FROM customer
WHERE grade >= 300
UNION
SELECT customer_id, city, grade, 'Low Rating'
FROM customer
WHERE grade < 300
```

### 9. Salespeople and Customers with More Than One Order
Return ID, name for both customers and salespeople who appear on more than one order.

```sql
SELECT customer_id as "ID", cust_name as "NAME"
FROM customer a
WHERE 1 <
    (SELECT COUNT(*)
     FROM orders b
     WHERE a.customer_id = b.customer_id)

UNION

SELECT salesman_id as "ID", name as "NAME"
FROM salesman a
WHERE 1 <
    (SELECT COUNT(*)
     FROM orders b
     WHERE a.salesman_id = b.salesman_id)

ORDER BY 2
```
