# SQL JOINS — Practice Set (w3resource)

Source: [w3resource SQL JOINS Exercises](https://www.w3resource.com/sql-exercises/sql-joins-exercises.php) (29 exercises).

All exercises use one of four schema groups. Sample data for each is below, followed by all 29 problems with solutions.

## Table Structures & Sample Data

### Group 1: Salesman / Customer / Orders

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

### Group 2: Company / Item (Product)

**company_mast**

| COM_ID | COM_NAME |
|---|---|
| 11 | Samsung |
| 12 | iBall |
| 13 | Epsion |
| 14 | Zebronics |
| 15 | Asus |
| 16 | Frontech |

**item_mast**

| PRO_ID | PRO_NAME | PRO_PRICE | PRO_COM |
|---|---|---|---|
| 101 | Mother Board | 3200.00 | 15 |
| 102 | Key Board | 450.00 | 16 |
| 103 | ZIP drive | 250.00 | 14 |
| 104 | Speaker | 550.00 | 16 |
| 105 | Monitor | 5000.00 | 11 |
| 106 | DVD drive | 900.00 | 12 |
| 107 | CD drive | 800.00 | 12 |
| 108 | Printer | 2600.00 | 13 |
| 109 | Refill cartridge | 350.00 | 13 |
| 110 | Mouse | 250.00 | 12 |

### Group 3: Employee / Department

**emp_department**

| DPT_CODE | DPT_NAME | DPT_ALLOTMENT |
|---|---|---|
| 57 | IT | 65000 |
| 63 | Finance | 15000 |
| 47 | HR | 240000 |
| 27 | RD | 55000 |
| 89 | QC | 75000 |

**emp_details**

| EMP_IDNO | EMP_FNAME | EMP_LNAME | EMP_DEPT |
|---|---|---|---|
| 127323 | Michale | Robbin | 57 |
| 526689 | Carlos | Snares | 63 |
| 843795 | Enric | Dosio | 57 |
| 328717 | Jhon | Snares | 63 |
| 444527 | Joseph | Dosni | 47 |
| 659831 | Zanifer | Emily | 47 |
| 847674 | Kuleswar | Sitaraman | 57 |
| 748681 | Henrey | Gabriel | 47 |
| 555935 | Alex | Manuel | 57 |
| 539569 | George | Mardy | 27 |
| 733843 | Mario | Saule | 63 |
| 631548 | Alan | Snappy | 27 |
| 839139 | Maria | Foster | 57 |

---

## Exercises & Solutions

### 1. Sales & City Matching
Find the salesperson and customer who reside in the same city. Return Salesman, cust_name and city.

```sql
SELECT salesman.name AS "Salesman", customer.cust_name, customer.city
FROM salesman, customer
WHERE salesman.city = customer.city;
```

### 2. Orders in Amount Range
Find orders where the order amount is between 500 and 2000. Return ord_no, purch_amt, cust_name, city.

```sql
SELECT a.ord_no, a.purch_amt,
       b.cust_name, b.city
FROM orders a, customer b
WHERE a.customer_id = b.customer_id
AND a.purch_amt BETWEEN 500 AND 2000;
```

### 3. Salesman-Customer Representation
Find the salesperson(s) and the customer(s) they represent. Return Customer Name, city, Salesman, commission.

```sql
SELECT a.cust_name AS "Customer Name",
       a.city,
       b.name AS "Salesman",
       b.commission
FROM customer a
INNER JOIN salesman b
ON a.salesman_id = b.salesman_id;
```

### 4. High Commission Salespeople
Find salespeople who received commissions of more than 12%. Return Customer Name, customer city, Salesman, commission.

```sql
SELECT a.cust_name AS "Customer Name",
       a.city,
       b.name AS "Salesman",
       b.commission
FROM customer a
INNER JOIN salesman b
ON a.salesman_id = b.salesman_id
WHERE b.commission > 0.12;
```

### 5. Different City & High Commission
Find salespeople who do not live in the same city as their customers and earn a commission > 12%.

```sql
SELECT a.cust_name AS "Customer Name",
       a.city,
       b.name AS "Salesman",
       b.city,
       b.commission
FROM customer a
INNER JOIN salesman b
ON a.salesman_id = b.salesman_id
WHERE b.commission > 0.12
AND a.city <> b.city;
```

### 6. Order Details Report
Retrieve order number, order date, purchase amount, customer name, customer grade, salesman name, and salesman commission.

```sql
SELECT a.ord_no, a.ord_date, a.purch_amt,
       b.cust_name AS "Customer Name", b.grade,
       c.name AS "Salesman", c.commission
FROM orders a
INNER JOIN customer b
ON a.customer_id = b.customer_id
INNER JOIN salesman c
ON a.salesman_id = c.salesman_id;
```

### 7. Join All Tables Uniquely
Join salesman, customer, and orders such that shared columns appear once and only matching rows are returned.

```sql
SELECT *
FROM orders
NATURAL JOIN customer
NATURAL JOIN salesman;
```

> Caution: `NATURAL JOIN` matches on identically-named columns automatically — risky if same-named columns have different meanings across tables.

### 8. Customer & Salesman Sorted by Customer_ID
Display customer name, city, grade, salesman name, salesman city — all customers, sorted by ascending customer_id.

```sql
SELECT a.cust_name, a.city, a.grade,
       b.name AS "Salesman", b.city
FROM customer a
LEFT JOIN salesman b
ON a.salesman_id = b.salesman_id
ORDER BY a.customer_id;
```

### 9. Customers with Grade Less Than 300
Same as above, filtered to grade < 300.

```sql
SELECT a.cust_name, a.city, a.grade,
       b.name AS "Salesman", b.city
FROM customer a
LEFT OUTER JOIN salesman b
ON a.salesman_id = b.salesman_id
WHERE a.grade < 300
ORDER BY a.customer_id;
```

### 10. Customer Order Report by Date
List customer name, city, order number, order date, order amount — including customers with no orders — sorted by order date.

```sql
SELECT a.cust_name, a.city, b.ord_no, b.ord_date,
       b.purch_amt AS "Order Amount"
FROM customer a
LEFT OUTER JOIN orders b
ON a.customer_id = b.customer_id
ORDER BY b.ord_date;
```

### 11. Order & Salesperson Report
Combine customer, order, and salesperson info — customers with no orders or multiple orders.

```sql
SELECT a.cust_name, a.city, b.ord_no,
       b.ord_date, b.purch_amt AS "Order Amount",
       c.name, c.commission
FROM customer a
LEFT OUTER JOIN orders b
ON a.customer_id = b.customer_id
LEFT OUTER JOIN salesman c
ON c.salesman_id = b.salesman_id;
```

### 12. Salespersons List (Including Unassigned)
List salespeople who work for one or more customers, or have none, in ascending order.

```sql
SELECT a.cust_name, a.city, a.grade,
       b.name AS "Salesman", b.city
FROM customer a
RIGHT OUTER JOIN salesman b
ON b.salesman_id = a.salesman_id
ORDER BY b.salesman_id;
```

### 13. Comprehensive Sales & Order Report
Salespeople with/without customers, and customers with/without orders — all joined together.

```sql
SELECT a.cust_name, a.city, a.grade,
       b.name AS "Salesman",
       c.ord_no, c.ord_date, c.purch_amt
FROM customer a
RIGHT OUTER JOIN salesman b
ON b.salesman_id = a.salesman_id
RIGHT OUTER JOIN orders c
ON c.customer_id = a.customer_id;
```

### 14. Salesmen List with Order and Grade Criteria
Salespeople (with or without customers) whose customers placed orders ≥ 2000 and have a grade assigned.

```sql
SELECT a.cust_name, a.city, a.grade,
       b.name AS "Salesman",
       c.ord_no, c.ord_date, c.purch_amt
FROM customer a
RIGHT OUTER JOIN salesman b
ON b.salesman_id = a.salesman_id
LEFT OUTER JOIN orders c
ON c.customer_id = a.customer_id
WHERE c.purch_amt >= 2000
AND a.grade IS NOT NULL;
```

### 15. Customer Order Placement Report
Customers who placed one or more orders (or none), plus orders from customers not on the list — return customer name, city, order number, order date, purchase amount.

```sql
SELECT a.cust_name, a.city, b.ord_no,
       b.ord_date, b.purch_amt AS "Order Amount"
FROM customer a
LEFT OUTER JOIN orders b
ON a.customer_id = b.customer_id;
```

### 16. Customer Order & Grade Report
Same fields as #15, using a FULL OUTER JOIN, restricted to customers with a grade.

```sql
SELECT a.cust_name, a.city, b.ord_no,
       b.ord_date, b.purch_amt AS "Order Amount"
FROM customer a
FULL OUTER JOIN orders b
ON a.customer_id = b.customer_id
WHERE a.grade IS NOT NULL;
```

> Note: MySQL has no native `FULL OUTER JOIN` — emulate with `LEFT JOIN UNION RIGHT JOIN`. Works directly in PostgreSQL/SQL Server/Oracle.

### 17. Salesman-Customer Full Combination
Combine each row of salesman with each row of customer (Cartesian product).

```sql
SELECT *
FROM salesman a
CROSS JOIN customer b;
```

### 18. Cartesian Product with City Flag
Cartesian product limited to salespeople who have a city.

```sql
SELECT *
FROM salesman a
CROSS JOIN customer b
WHERE a.city IS NOT NULL;
```

### 19. Cartesian Product with Valid City & Grade
Cartesian product limited to salespeople with a city AND customers with a grade.

```sql
SELECT *
FROM salesman a
CROSS JOIN customer b
WHERE a.city IS NOT NULL
AND b.grade IS NOT NULL;
```

### 20. Cartesian Product with Non Matching Cities
Same as #19, plus salesman city must differ from customer city.

```sql
SELECT *
FROM salesman a
CROSS JOIN customer b
WHERE a.city IS NOT NULL
AND b.grade IS NOT NULL
AND a.city <> b.city;
```

### 21. Matched Company & Item Join
Select all rows from `item_mast` and `company_mast` where `pro_com` matches `com_id`.

```sql
SELECT *
FROM item_mast
INNER JOIN company_mast
ON item_mast.pro_com = company_mast.com_id;
```

### 22. Product & Company Details
Display item name, price, and company name.

```sql
SELECT item_mast.pro_name, pro_price, company_mast.com_name
FROM item_mast
INNER JOIN company_mast
ON item_mast.pro_com = company_mast.com_id;
```

### 23. Average Price by Company
Average item price per company.

```sql
SELECT AVG(pro_price), company_mast.com_name
FROM item_mast
INNER JOIN company_mast
ON item_mast.pro_com = company_mast.com_id
GROUP BY company_mast.com_name;
```

### 24. Average Price (>=350) by Company
Same as #23, restricted to companies whose average price ≥ 350.

```sql
SELECT AVG(pro_price), company_mast.com_name
FROM item_mast
INNER JOIN company_mast
ON item_mast.pro_com = company_mast.com_id
GROUP BY company_mast.com_name
HAVING AVG(pro_price) >= 350;
```

### 25. Most Expensive Product by Company
Find the most expensive product of each company. Return pro_name, pro_price, com_name.

```sql
SELECT A.pro_name, A.pro_price, F.com_name
FROM item_mast A
INNER JOIN company_mast F
ON A.pro_com = F.com_id
AND A.pro_price =
   (
     SELECT MAX(A.pro_price)
     FROM item_mast A
     WHERE A.pro_com = F.com_id
   );
```

### 26. Employee & Department Full Report
Display all employee data with their department info.

```sql
SELECT emp_idno, A.emp_fname AS "First Name", emp_lname AS "Last Name",
       B.dpt_name AS "Department", emp_dept, dpt_code, dpt_allotment
FROM emp_details A
INNER JOIN emp_department B
ON A.emp_dept = B.dpt_code;
```

### 27. Employee Name & Department Sanction
Display first/last name, department name, and sanction (allotment) amount.

```sql
SELECT emp_details.emp_fname AS "First Name", emp_lname AS "Last Name",
       emp_department.dpt_name AS "Department",
       dpt_allotment AS "Amount Allotted"
FROM emp_details
INNER JOIN emp_department
ON emp_details.emp_dept = emp_department.dpt_code;
```

### 28. High Budget Departments Employee List
Employees belonging to departments with budget > Rs. 50000.

```sql
SELECT emp_details.emp_fname AS "First Name", emp_lname AS "Last Name"
FROM emp_details
INNER JOIN emp_department
ON emp_details.emp_dept = emp_department.dpt_code
AND emp_department.dpt_allotment > 50000;
```

### 29. Departments with More Than Two Employees
Names of departments with more than 2 employees.

```sql
SELECT emp_department.dpt_name
FROM emp_details
INNER JOIN emp_department
ON emp_dept = dpt_code
GROUP BY emp_department.dpt_name
HAVING COUNT(*) > 2;
```
