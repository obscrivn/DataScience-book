# 09 From Related Tables to Analysis-Ready Data

## Big Idea

A useful data analysis often begins with a relational database, but the final dataset for analysis is usually not the original database schema. Instead, we pull the relevant tables together, define the unit of observation, and then clean, join, and aggregate the data until each row means what we think it means.

This chapter is a short companion to the introductory database material. It is designed for students with a range of backgrounds: some have already seen SQL, while others need a brief refresher before doing analysis in Python.

**Reading guide:** Allow about 15–20 minutes. Focus on the logic of the example and the validation checks, not on memorizing SQL syntax.

## Recommended reading sequence

Use the existing introduction as foundational reading, then read this companion chapter.

1. [1.1 Why Databases Still Matter](https://obscrivn.github.io/databasebook/why-databases-still-matter.html)
2. [1.2 Relational Databases and SQL](https://obscrivn.github.io/databasebook/intro-relational.html)
3. [1.3 SQLite](https://obscrivn.github.io/databasebook/sqlite_intro.html)
4. [Join Types](https://obscrivn.github.io/databasebook/join.html)
5. This chapter: From Related Tables to Analysis-Ready Data

## Review of the existing introduction

The introductory database material is useful, but not every idea needs equal emphasis for Applied Data Science. The goal is to keep the essentials and move quickly to the analytical decisions that matter most.

| Category | What to do in this week | Why |
| --- | --- | --- |
| Retain | Tables, rows, columns, schemas, keys, relationships, and basic SQL joins | These are the building blocks for relational reasoning |
| Condense | Database history, product comparisons, server setup, and administration details | Useful context, but not necessary for analysis work |
| Adapt | Relational concepts to an analytical workflow: unit of observation, join choices, and data validation | This is where students connect database structure to analysis |
| Omit | Deep database design theory, advanced normalization examples, and long syntax drills | They are not needed for a focused, applied reading |

## Database refresher for experienced students

If you already know databases, this section is a quick check rather than a full lesson.

- A **table** stores records of the same type.
- A **row** is one record.
- A **column** describes one attribute of the record.
- A **primary key** uniquely identifies a row in a table.
- A **foreign key** links a row in one table to a row in another table.
- A **relationship** describes how rows in one table connect to rows in another.

In a relational dataset, the data are often spread across several tables because each table captures one entity or one type of event. That structure is efficient and reliable for storing information, but it is not always the easiest shape for analysis.

## Why is the data often spread across multiple tables?

A company may store information in separate tables for:

- customers
- orders
- products
- order items
- payments
- shipments

Each table has its own purpose. A customer table records customer information. An order table records each order event. An order item table records which product was included in which order and how many units were purchased.

That design is useful because it avoids duplication. A customer name is stored once, not repeated on every order. A product price is stored once, not copied into every order line. But when an analyst wants to answer a business question, those tables must be combined.

The question is not whether the database is “correct.” The question is: what does the analyst need the final table to represent?

## One row represents one observation

Before joining tables, define the unit of observation.

- One row in `customers` = one customer.
- One row in `orders` = one order placed by one customer.
- One row in `order_items` = one product line within an order.

The final analytical dataset should have a clear unit of observation as well. For example:

- one row per customer if the question is “Which customers spent the most?”
- one row per order if the question is “How much revenue did each order generate?”
- one row per order item if the question is “Which products sold the most units?”

This is the most important concept in relational analysis. If the rows represent different units before and after a join, then counts, means, totals, and percentages can be wrong even when the SQL runs successfully.

## Worked example: customers, orders, and order items

Suppose we have a small business with three tables.

```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    city TEXT
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_name TEXT,
    quantity INTEGER,
    unit_price REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

Sample rows:

```sql
INSERT INTO customers (customer_id, customer_name, city) VALUES
    (1, 'Aisha', 'Chicago'),
    (2, 'Miguel', 'Boston'),
    (3, 'Priya', 'Chicago');

INSERT INTO orders (order_id, customer_id, order_date) VALUES
    (101, 1, '2025-01-05'),
    (102, 1, '2025-01-12'),
    (103, 2, '2025-01-15');

INSERT INTO order_items (order_item_id, order_id, product_name, quantity, unit_price) VALUES
    (1, 101, 'Notebook', 2, 8.00),
    (2, 101, 'Pen', 5, 1.50),
    (3, 102, 'Backpack', 1, 45.00),
    (4, 103, 'Notebook', 3, 8.00),
    (5, 103, 'Marker Set', 2, 12.00);
```

### Question

Which customers spent the most money?

### Prediction

If we join the tables correctly, the final table should have one row per customer. The customer total should represent the sum of all their order items.

## Keys and relationship cardinality

The shape of the join depends on the relationship between the tables.

- `customers` to `orders`: one customer can have many orders.
- `orders` to `order_items`: one order can have many items.

This is a classic one-to-many relationship.

A join tells the database to match rows by key values. In SQLite, a simple join is written like this:

```sql
SELECT c.customer_id, c.customer_name, o.order_id, o.order_date
FROM customers c
JOIN orders o
  ON c.customer_id = o.customer_id;
```

This returns one row for each matching customer-order pair. The unit of observation here is **customer-order**.

Now join the order items:

```sql
SELECT c.customer_id, c.customer_name, o.order_id, oi.product_name, oi.quantity, oi.unit_price
FROM customers c
JOIN orders o
  ON c.customer_id = o.customer_id
JOIN order_items oi
  ON o.order_id = oi.order_id;
```

This query is valid, but it produces a row for each order item. The important fact is that the number of rows grows when an order contains more than one item.

### Why repeated rows are expected

If a customer places one order with several items, the join will repeat the customer and order information for each item. This is not a data error. It is the normal result of matching a one-to-many relationship.

The problem appears when the analyst forgets that the new table is now at the **order-item** level instead of the **customer** level or **order** level.

## When should we use INNER JOIN versus LEFT JOIN?

Use an `INNER JOIN` when you only want records that match in both tables.

```sql
SELECT c.customer_id, c.customer_name, o.order_id
FROM customers c
INNER JOIN orders o
  ON c.customer_id = o.customer_id;
```

This returns only customers who have at least one order:

| customer_id | customer_name | order_id |
| --- | --- | --- |
| 1 | Aisha | 101 |
| 1 | Aisha | 102 |
| 2 | Miguel | 103 |

Priya is absent because she has no orders.

Use a `LEFT JOIN` when you want to keep all rows from the left table, even when there is no matching row on the right.

```sql
SELECT c.customer_id, c.customer_name, o.order_id
FROM customers c
LEFT JOIN orders o
  ON c.customer_id = o.customer_id;
```

This keeps Priya in the output, with `NULL` in the order columns:

| customer_id | customer_name | order_id |
| --- | --- | --- |
| 1 | Aisha | 101 |
| 1 | Aisha | 102 |
| 2 | Miguel | 103 |
| 3 | Priya | NULL |

That is useful when you need to retain customers who have never placed an order. But it also changes the interpretation: the result may combine matched and unmatched customers, so you must decide whether `NULL` means “no order yet” or “missing data.”

## A valid SQL query can still produce a misleading summary

Consider the following query:

```sql
SELECT c.customer_id, c.customer_name, COUNT(*) AS rows_in_join
FROM customers c
JOIN orders o
  ON c.customer_id = o.customer_id
JOIN order_items oi
  ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name;
```

This query returns:

| customer_id | customer_name | rows_in_join |
| --- | --- | --- |
| 1 | Aisha | 3 |
| 2 | Miguel | 2 |

Priya does not appear because the `INNER JOIN` excludes customers with no orders. The result is still at the **order-item** level, not the **customer** or **order** level. Aisha has two orders and three order items across them, so the count of matched rows is 3, not the number of orders or customers.

This is exactly the sort of mistake that creates an apparent trend or summary that is easy to trust but wrong to interpret.

If the intended unit is **order**, we should count distinct orders rather than total rows:

```sql
SELECT c.customer_id, c.customer_name, COUNT(DISTINCT o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o
  ON c.customer_id = o.customer_id
LEFT JOIN order_items oi
  ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name;
```

Result:

| customer_id | customer_name | order_count |
| --- | --- | --- |
| 1 | Aisha | 2 |
| 2 | Miguel | 1 |
| 3 | Priya | 0 |

The distinction matters: counting rows after a one-to-many join counts line items, while counting distinct order IDs counts orders.

## Aggregate before joining when the analysis is at a higher level

If we want one row per customer and the question is “How much did each customer spend?”, the correct pattern is to aggregate the order items to the customer level before joining to the customer table.

```sql
SELECT
    c.customer_id,
    c.customer_name,
    COALESCE(customer_totals.total_spend, 0) AS total_spend
FROM customers c
LEFT JOIN (
    SELECT
        o.customer_id,
        SUM(oi.quantity * oi.unit_price) AS total_spend
    FROM orders o
    JOIN order_items oi
      ON o.order_id = oi.order_id
    GROUP BY o.customer_id
) AS customer_totals
  ON c.customer_id = customer_totals.customer_id;
```

Result:

| customer_id | customer_name | total_spend |
| --- | --- | --- |
| 1 | Aisha | 68.50 |
| 2 | Miguel | 48.00 |
| 3 | Priya | 0.00 |

This table has one row per customer, which matches the intended unit of observation. The `LEFT JOIN` keeps Priya in the output even though she has no recorded orders, and the total is `0.00` because there are no matching items.

This is an analysis-ready dataset because each row now represents a single customer and the summary is calculated at that level.

## How missing values affect counts and summaries

Missing values can silently distort analysis. A `LEFT JOIN` may keep a customer who has no orders, but if the analyst does not account for `NULL` values, they may generate incorrect totals, counts, or percentages.

For example:

```sql
SELECT
    c.customer_id,
    COUNT(DISTINCT o.order_id) AS number_of_orders,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_spend
FROM customers c
LEFT JOIN orders o
  ON c.customer_id = o.customer_id
LEFT JOIN order_items oi
  ON o.order_id = oi.order_id
GROUP BY c.customer_id;
```

The `COUNT(DISTINCT o.order_id)` counts orders rather than order items, while `SUM(oi.quantity * oi.unit_price)` would return `NULL` for a customer with no matching order items unless we use `COALESCE`. In SQLite, `SUM` ignores `NULL` values, but the result may still look valid without a clear explanation of what is missing.

This is not an error in SQL. It is a reminder that analysts must understand what is missing and whether missing rows represent “no purchase,” “no data,” or “not applicable.”

## Checks before using the result for analysis

Before treating a joined table as ready for Python, verify the following:

- Does each row represent the intended unit of observation?
- Are the keys unique where they should be unique?
- Are there unmatched records after the join?
- Are row counts larger than expected because of one-to-many matches?
- Are totals or means calculated at the correct level?
- Does the dataset include customers, orders, or products that should be excluded?
- Are missing values explained rather than silently interpreted?

A few quick checks help:

```sql
SELECT COUNT(*) AS rows_in_join
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id;
```

```sql
SELECT c.customer_id, COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id;
```

```sql
SELECT COUNT(*) AS customers_without_orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

These checks quickly reveal whether the join is behaving the way the analyst expects.

## Reasoning questions

1. A customer has two orders, and each order has three items. After a join of all three tables, how many rows do you expect if the query is at the order-item level? Why?
2. If the analyst wants one row per customer, is `COUNT(*)` a reliable summary after a join with `order_items`? Explain your reasoning.
3. When would you prefer a `LEFT JOIN` over an `INNER JOIN` in an analysis on customer transactions? What does each one keep or exclude?
4. A query returns a high total spend for one customer. What should you check before trusting that number?

## Final takeaways

- Relational databases are designed to store data efficiently, not necessarily to produce a final analysis table.
- The single most important step is to define the unit of observation.
- One-to-many joins will often create repeated rows; that is expected.
- `INNER JOIN` and `LEFT JOIN` answer different questions.
- Grouping and aggregation are often required before the table is ready for analysis.
- Validation checks matter because a SQL query can be valid and still be misleading.

## Checklist for working with relational data

Before moving a query result into pandas for analysis, verify that you can answer each of these:

- What does one row represent?
- What are the relevant keys?
- What type of relationship connects the tables?
- Did I choose the right join?
- Are there unmatched records or repeated rows?
- Am I summarizing at the intended level?
- Are the counts and totals consistent with the chosen unit of observation?

If the answer is “yes” to all of these, the dataset is much more likely to be trustworthy for a Python analysis.

## Alignment to learning objectives

| Learning objective | How this reading supports it |
| --- | --- |
| Explain how relational data supports data science workflows through tables, keys, and relationships. | The chapter introduces the customer-order-item example and explains how structured tables map to actual analysis questions. |
| Identify what one row represents and determine the intended unit of observation for an analysis. | The chapter repeatedly emphasizes unit-of-observation checks before interpreting summaries. |
| Use SQL to explore and summarize data. | The examples use SQLite-friendly SQL for selection, joining, grouping, and summarizing. |
| Combine related tables using appropriate joins and explain how join choices affect the resulting records. | The chapter compares `INNER JOIN` and `LEFT JOIN` and shows how joins change the table structure. |
| Evaluate query results by checking key uniqueness, missing matches, repeated records, and unexpected changes in counts or summaries. | The “checks before analysis” and reasoning questions directly target validation. |
| Construct and validate an analysis-ready dataset for use in Python. | The final section shows a cleaned and aggregated customer-level dataset suitable for pandas. |

## References

- [1.1 Why Databases Still Matter](https://obscrivn.github.io/databasebook/why-databases-still-matter.html)
- [1.2 Relational Databases and SQL](https://obscrivn.github.io/databasebook/intro-relational.html)
- [1.3 SQLite](https://obscrivn.github.io/databasebook/sqlite_intro.html)
- [Join Types](https://obscrivn.github.io/databasebook/join.html)
