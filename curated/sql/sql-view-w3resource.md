# SQL VIEW — Practice Set (w3resource)

Source: [w3resource SQL View Exercises](https://www.w3resource.com/sql-exercises/view/sql-view.php) (16 exercises).

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

### 1. View of New York Salespeople
Create a view for salespeople who belong to New York.

```sql
CREATE VIEW newyorkstaff
AS SELECT *
FROM salesman
WHERE city = 'New York';
```

### 2. View of All Salespersons (ID, Name, City)
Create a view, then demonstrate that a simple view is updatable — update salesman 5007's city through it.

```sql
CREATE VIEW salesown
AS SELECT salesman_id, name, city
FROM salesman;

UPDATE salesown
SET city = 'London'
WHERE salesman_id = 5007;
```

### 3. Locate Salespeople in New York via a View
Query the view from #1, adding an extra filter on commission.

```sql
CREATE VIEW newyorkstaff
AS SELECT *
FROM salesman
WHERE city = 'New York';

SELECT *
FROM newyorkstaff
WHERE commission > 0.13;
```

### 4. Count of Customers per Grade
```sql
CREATE VIEW gradecount (grade, number)
AS SELECT grade, COUNT(*)
FROM customer
GROUP BY grade;
```

### 5. Unique Customer Count, Avg & Total Purchase Amount per Date
```sql
CREATE VIEW totalforday
AS SELECT ord_date, COUNT(DISTINCT customer_id), AVG(purch_amt), SUM(purch_amt)
FROM orders
GROUP BY ord_date;
```

### 6. Order, Salesman & Customer Combined View
Return order number, purchase amount, salesman ID, salesman name, and customer name.

```sql
CREATE VIEW nameorders
AS SELECT ord_no, purch_amt, a.salesman_id, name, cust_name
FROM orders a, customer b, salesman c
WHERE a.customer_id = b.customer_id
AND a.salesman_id = c.salesman_id;
```

### 7. Salesperson Handling the Highest Order of the Day
```sql
CREATE VIEW elitsalesman
AS SELECT b.ord_date, a.salesman_id, a.name
FROM salesman a, orders b
WHERE a.salesman_id = b.salesman_id
AND b.purch_amt =
    (SELECT MAX (purch_amt)
       FROM orders c
       WHERE c.ord_date = b.ord_date);
```

### 8. Salesperson with the Highest Order ≥ 3 Times
Builds on the `elitsalesman` view from #7 — salespeople who appear in it at least 3 times.

```sql
CREATE VIEW incentive
AS SELECT DISTINCT salesman_id, name
FROM elitsalesman a
WHERE 3 <=
   (SELECT COUNT (*)
    FROM elitsalesman b
    WHERE a.salesman_id = b.salesman_id);
```

### 9. Customers with the Highest Grade
```sql
CREATE VIEW highgrade
AS SELECT *
FROM customer
WHERE grade =
    (SELECT MAX (grade)
     FROM customer);
```

### 10. Count of Salespeople per City
```sql
CREATE VIEW citynum
AS SELECT city, COUNT (DISTINCT salesman_id)
FROM salesman
GROUP BY city;
```

### 11. Average & Total Purchase Amount per Salesperson
```sql
CREATE VIEW norders
AS SELECT name, AVG(purch_amt), SUM(purch_amt)
FROM salesman, orders
WHERE salesman.salesman_id = orders.salesman_id
GROUP BY name;
```

### 12. Salespeople Working with Multiple Clients
```sql
CREATE VIEW mcustomer
AS SELECT *
FROM salesman a
WHERE 1 <
   (SELECT COUNT(*)
     FROM customer b
     WHERE a.salesman_id = b.salesman_id);
```

### 13. Matching Customer & Salesman Cities
```sql
CREATE VIEW citymatch(custcity, salescity)
AS SELECT DISTINCT a.city, b.city
FROM customer a, salesman b
WHERE a.salesman_id = b.salesman_id;
```

### 14. Number of Orders per Day
```sql
CREATE VIEW dateord(ord_date, odcount)
AS SELECT ord_date, COUNT (*)
FROM orders
GROUP BY ord_date;
```

### 15. Salespeople Who Placed Orders on October 10th, 2012
```sql
CREATE VIEW salesmanonoct
AS SELECT *
FROM salesman
WHERE salesman_id IN
    (SELECT salesman_id
         FROM orders
         WHERE ord_date = '2012-10-10');
```

### 16. Salespeople Who Issued Orders on Aug 17 or Oct 10, 2012
Return salesperson ID, order number, customer ID.

```sql
CREATE VIEW sorder
AS SELECT salesman_id, ord_no, customer_id
FROM orders
WHERE ord_date IN ('2012-08-17', '2012-10-10');
```
