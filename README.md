# postgres-playground

## Instructions to Run Locally

- Install and start Docker
- `docker compose up -d`: start postgres container on background
- `docker ps`: list all running containers
- `docker exec -it <container_id> psql -U postgres -W postgres`: run psql

## Notes

### 03. Row variables, row values, row types

```sql
DROP TABLE IF EXISTS "T";
CREATE TABLE "T" (a int PRIMARY KEY,
                  b text,
                  c boolean,
                  d int);

INSERT INTO "T" VALUES
  (1, 'x', true, 10),
  (2, 'y', true, 40),
  (3, 'x', false, 30),
  (4, 'y', false, 20),
  (5, 'x', true, NULL);

TABLE "T"; -- SELECT t.* FROM "T" as t
/* # Output #
 a | b | c | d
---+---+---+----
 1 | x | t | 10
 2 | y | t | 40
 3 | x | f | 30
 4 | y | f | 20
 5 | x | t |
(5 rows) */
```

```sql
DROP TABLE IF EXISTS "T1";

DROP TYPE IF EXISTS "t";
CREATE TYPE "t" AS (a int, b text, c boolean, d int);

CREATE TABLE "T1" OF "t";
ALTER TABLE "T1" ADD PRIMARY KEY (a);

INSERT INTO "T1" TABLE "T";

TABLE "T1";
/* # Output #
 a | b | c | d
---+---+---+----
 1 | x | t | 10
 2 | y | t | 40
 3 | x | f | 30
 4 | y | f | 20
 5 | x | t |
(5 rows) */
```

### 04. SELECT/FROM/WHERE

```sql
SELECT 1 + 2 AS "sUm", 'chs' || 'dwn' AS UserName;
/* # Output #
 sUm | username
-----+----------
   3 | chsdwn
(1 row) */

VALUES (1),
       (2);
/* # Output #
 column1
---------
       1
       2
(2 rows) */

VALUES (1, 2);
/* # Output #
 column1 | column2
---------+---------
       1 |       2
(1 row) */

VALUES (false, 0),
       (true, 1),
       (NULL, NULL);
/* # Output #
 column1 | column2
---------+---------
 f       |       0
 t       |       1
         |
(3 rows) */

SELECT t.* FROM (VALUES (false, 0),
                        (true, 1)) AS t(truth, "binary");
/* # Output #
 truth | binary
-------+--------
 f     |      0
 t     |      1
(2 rows) */

SELECT t1.*, t2.*
FROM "T" AS t1,
     "T" AS t2(a2, b2, c2, d2);
/* # Output #
 a | b | c | d  | a2 | b2 | c2 | d2
---+---+---+----+----+----+----+----
 1 | x | t | 10 |  1 | x  | t  | 10
 1 | x | t | 10 |  2 | y  | t  | 40
 1 | x | t | 10 |  3 | x  | f  | 30
 1 | x | t | 10 |  4 | y  | f  | 20
 1 | x | t | 10 |  5 | x  | t  |
 2 | y | t | 40 |  1 | x  | t  | 10
 2 | y | t | 40 |  2 | y  | t  | 40
 2 | y | t | 40 |  3 | x  | f  | 30
 2 | y | t | 40 |  4 | y  | f  | 20
 2 | y | t | 40 |  5 | x  | t  |
 3 | x | f | 30 |  1 | x  | t  | 10
 3 | x | f | 30 |  2 | y  | t  | 40
 3 | x | f | 30 |  3 | x  | f  | 30
 3 | x | f | 30 |  4 | y  | f  | 20
 3 | x | f | 30 |  5 | x  | t  |
 4 | y | f | 20 |  1 | x  | t  | 10
 4 | y | f | 20 |  2 | y  | t  | 40
 4 | y | f | 20 |  3 | x  | f  | 30
 4 | y | f | 20 |  4 | y  | f  | 20
 4 | y | f | 20 |  5 | x  | t  |
 5 | x | t |    |  1 | x  | t  | 10
 5 | x | t |    |  2 | y  | t  | 40
 5 | x | t |    |  3 | x  | f  | 30
 5 | x | t |    |  4 | y  | f  | 20
 5 | x | t |    |  5 | x  | t  |
(25 rows) */

SELECT onetwo.num, t.*
FROM (VALUES ('1'), ('2')) AS onetwo(num), "T" as t;
/* # Output #
 num | a | b | c | d
-----+---+---+---+----
 1   | 1 | x | t | 10
 2   | 1 | x | t | 10
 1   | 2 | y | t | 40
 2   | 2 | y | t | 40
 1   | 3 | x | f | 30
 2   | 3 | x | f | 30
 1   | 4 | y | f | 20
 2   | 4 | y | f | 20
 1   | 5 | x | t |
 2   | 5 | x | t |
(10 rows) */

SELECT onetwo.num, t.*
FROM (VALUES ('1'), ('2')) AS onetwo(num), "T" as t
WHERE onetwo.num = '2';
/* # Output #
 num | a | b | c | d
-----+---+---+---+----
 2   | 1 | x | t | 10
 2   | 2 | y | t | 40
 2   | 3 | x | f | 30
 2   | 4 | y | f | 20
 2   | 5 | x | t |
(5 rows) */

SELECT t.*
FROM "T" as t
WHERE t.a * 10 = t.d;
/* # Output #
 a | b | c | d
---+---+---+----
 1 | x | t | 10
 3 | x | f | 30
(2 rows) */

SELECT t.*
FROM "T" AS t
WHERE t.c; -- WHERE t.c = true;
/* # Output #
 a | b | c | d
---+---+---+----
 1 | x | t | 10
 2 | y | t | 40
 5 | x | t |
(3 rows) */

SELECT t.*
FROM "T" as t
WHERE t.d IS NULL;
/* # Output #
 a | b | c | d
---+---+---+---
 5 | x | t |
(1 row) */

SELECT t.d, t.d IS NULL, t.d = NULL -- t.d = NULL yields NULL != true
FROM "T" AS t;
/* # Output #
 d  | ?column? | ?column?
----+----------+----------
 10 | f        |
 40 | f        |
 30 | f        |
 20 | f        |
    | t        |
(5 rows) */

SELECT t1.a, t1.b || ',' || t2.b AS b1b2, t2.a
FROM "T" AS t1, "T" AS t2
WHERE t1.a BETWEEN t2.a - 1 AND t2.a + 1;
/* # Output #
 a | b1b2 | a
---+------+---
 1 | x,x  | 1
 2 | y,x  | 1
 1 | x,y  | 2
 2 | y,y  | 2
 3 | x,y  | 2
 2 | y,x  | 3
 3 | x,x  | 3
 4 | y,x  | 3
 3 | x,y  | 4
 4 | y,y  | 4
 5 | x,y  | 4
 4 | y,x  | 5
 5 | x,x  | 5
(13 rows) */
```

### 05. Subqueries and Correlation

```sql
SELECT 2 + (SELECT t.d AS _
            FROM "T" as t
            WHERE t.a = 2) AS "The Answer";
/* # Output #
 The Answer
------------
         42
(1 row) */

SELECT t1.*
FROM "T" as t1
WHERE t1.b <> (SELECT t2.b
               FROM "T" AS t2
               WHERE t1.a = t2.a);
/* # Output #
 a | b | c | d
---+---+---+---
(0 rows) */
```

### 06. ORDER BY/OFFSET/LIMIT/DISTINCT [ON]

- ASC is default.
- NULL is larger than any non-NULL value.

```sql
SELECT t.*
FROM "T" AS t
ORDER BY t.d ASC NULLS FIRST;
/* # Output #
 a | b | c | d
---+---+---+----
 5 | x | t |
 1 | x | t | 10
 4 | y | f | 20
 3 | x | f | 30
 2 | y | t | 40
(5 rows) */

SELECT t.*
FROM "T" AS t
ORDER BY t.b DESC, t.c;
/* # Output #
 a | b | c | d
---+---+---+----
 4 | y | f | 20
 2 | y | t | 40
 3 | x | f | 30
 1 | x | t | 10
 5 | x | t |
(5 rows) */

SELECT t.*, t.d / t.a AS ratio
FROM "T" AS t
ORDER BY ratio;
/* # Output #
 a | b | c | d  | ratio
---+---+---+----+-------
 4 | y | f | 20 |     5
 1 | x | t | 10 |    10
 3 | x | f | 30 |    10
 2 | y | t | 40 |    20
 5 | x | t |    |
(5 rows) */

VALUES (1, 'one'),
       (2, 'two'),
       (3, 'three')
ORDER BY column1 DESC;
/* # Output #
 column1 | column2
---------+---------
       3 | three
       2 | two
       1 | one
(3 rows) */

SELECT t.*
FROM "T" AS t
ORDER BY t.a DESC
OFFSET 1
LIMIT 3;
/* # Output #
 a | b | c | d
---+---+---+----
 4 | y | f | 20
 3 | x | f | 30
 2 | y | t | 40
(3 rows) */
```

- Groups rows by `t.c` column and picks the row that has the smallest `t.d` value from each group.

```sql
SELECT DISTINCT ON (t.c) t.*
FROM "T" as t
ORDER BY t.c, t.d;
/* # Output #
 a | b | c | d
---+---+---+----
 4 | y | f | 20
 1 | x | t | 10
(2 rows) */

TABLE "T" ORDER BY "T".c, "T".d;
/* # Output #
 a | b | c | d
---+---+---+----
 4 | y | f | 20 -- 1st row of the 1st group
 3 | x | f | 30
 1 | x | t | 10 -- 1st row of the 2nd group
 2 | y | t | 40
 5 | x | t |
(5 rows) */

SELECT DISTINCT t.*
FROM (VALUES ('a', 1),
             ('a', 1),
             ('b', 2)) AS t;
/* # Output #
 column1 | column2
---------+---------
 b       |       2
 a       |       1
(2 rows) */
```

### 07. Aggregates (ordered, filtered, unique)

```sql
SELECT COUNT(*) AS "#rows",
       COUNT(t.d) AS "#d",
       SUM(t.d) AS "sum(d)",
       MAX(t.b) AS "max(b)",
       bool_and(t.c) AS "bool_and(c)",
       bool_or(t.d = 30) AS "bool_or(c=30)"
FROM "T" as t
WHERE true;
/* # Output #
 #rows | #d | sum(d) | max(b) | bool_and(c) | bool_or(c=30)
-------+----+--------+--------+-------------+---------------
     5 |  4 |    100 | y      | f           | t
(1 row) */

SELECT COUNT(*) AS "#rows",
       COUNT(t.d) AS "#d",
       SUM(t.d) AS "sum(d)",
       MAX(t.b) AS "max(b)",
       bool_and(t.c) AS "bool_and(c)",
       bool_or(t.d = 30) AS "bool_or(c=30)"
FROM "T" as t
WHERE false; -- empty rows
/* # Output #
 #rows | #d | sum(d) | max(b) | bool_and(c) | bool_or(c=30)
-------+----+--------+--------+-------------+---------------
     0 |  0 |        |        |             |
(1 row) */

SELECT string_agg(t.a::text, ',' ORDER BY t.d) AS "all a"
FROM "T" AS t;
/* # Output #
   all a
-----------
 1,4,3,2,5
(1 row) */

SELECT SUM(t.d) FILTER (WHERE t.c) AS "sum(t.d WHERE t.c)",
       SUM(t.d) AS "sum(t.d)"
FROM "T" as t;
/* # Output #
 sum(t.d WHERE t.c) | sum(t.d)
--------------------+----------
                 50 |      100
(1 row) */

SELECT SUM(CASE WHEN t.c THEN t.d ELSE 0 END) AS "sum(t.d WHERE t.c)", -- 0 <=> NULL
       SUM(t.d) AS "sum(t.d)"
FROM "T" AS t;
/* # Output #
 sum(t.d WHERE t.c) | sum(t.d)
--------------------+----------
                 50 |      100
(1 row) */

SELECT SUM(t.d) FILTER (WHERE t.b = 'x') AS "sum('x')",
       SUM(t.d) FILTER (WHERE t.b = 'y') AS "sum('y')",
       SUM(t.d) FILTER (WHERE t.b NOT IN ('x', 'y')) AS "sum(not 'x' or 'y')"
FROM "T" AS t;
/* # Output #
 sum('x') | sum('y') | sum(not 'x' or 'y')
----------+----------+---------------------
       40 |       60 |
(1 row) */

SELECT COUNT(DISTINCT t.c) AS "count of unique non-null t.c",
       COUNT(t.c) AS "count of non-null t.c"
FROM "T" AS t;
/* # Output #
 count of unique non-null t.c | count of non-null t.c
------------------------------+-----------------------
                            2 |                     5
(1 row) */
```

### 08. GROUP BY, grouping + aggregation, pseudo aggregate the()

```sql
SELECT t.b AS "b",
       COUNT(*) AS "count",
       SUM(t.d) AS "sum(d)",
       bool_and(t.a % 2 = 0) AS "a is even",
       string_agg(t.a::text, ';') AS "all a"
FROM "T" AS t
GROUP BY t.b; -- HAVING: acts like WHERE but after grouping
/* # Output #
 b | count | sum(d) | a is even | all a
---+-------+--------+-----------+-------
 y |     2 |     60 | t         | 2;4
 x |     3 |     40 | f         | 1;3;5
(2 rows) */

SELECT t.b AS "b",
       COUNT(*) AS "count",
       SUM(t.d) AS "sum(d)",
       bool_and(t.a % 2 = 0) AS "a is even",
       string_agg(t.a::text, ';') AS "all a"
FROM "T" AS t
GROUP BY t.b
HAVING COUNT(*) > 2;
/* # Output #
 b | count | sum(d) | a is even | all a
---+-------+--------+-----------+-------
 x |     3 |     40 | f         | 1;3;5
(1 row) */

SELECT t.a % 2 AS "a odd?",
       COUNT(*) as "count"
FROM "T" as t
GROUP BY t.a % 2;
/* # Output #
 a odd? | count
--------+-------
      0 |     2
      1 |     3
(2 rows) */

SELECT t.b AS "b",
       t.a % 2 AS "a odd?"
FROM "T" AS t
GROUP BY t.b, t.a % 2;
/* # Output #
 b | a odd?
---+--------
 y |      0
 x |      1
(2 rows) */
```

### 09. Bag/set operations: UNION/INTERSECT/EXCEPT

```sql
SELECT t.*
FROM "T" AS t
WHERE t.c
  UNION ALL
SELECT t.*
FROM "T" AS t
WHERE NOT t.c;
/* # Output #
 a | b | c | d
---+---+---+----
 1 | x | t | 10
 2 | y | t | 40
 5 | x | t |
 3 | x | f | 30
 4 | y | f | 20
(5 rows) */

SELECT t.b
FROM "T" AS t
WHERE t.c
  UNION
SELECT t.b
FROM "T" AS t
WHERE NOT t.c;
/* # Output #
 b
---
 x
 y
 x
 x
 y
(5 rows) */

SELECT t.b
FROM "T" AS t
WHERE t.c
  UNION
SELECT t.b
FROM "T" AS t
WHERE NOT t.c;
/* # Output #
 b
---
 x
 y
(2 rows) */

SELECT 1 AS q, t.b
FROM "T" AS t
WHERE t.c
  UNION ALL
SELECT 2 AS q, t.b
FROM "T" AS t
WHERE NOT t.c;
/* # Output #
 q | b
---+---
 1 | x
 1 | y
 1 | x
 2 | x
 2 | y
(5 rows) */

SELECT t.b
FROM "T" AS t
WHERE t.c       -- 'x' 'y' 'x'
  EXCEPT ALL
SELECT t.b
FROM "T" AS t
WHERE NOT t.c;  -- 'x' 'y'
/* # Output #
 b
---
 x
(1 row) */

SELECT t.b
FROM "T" AS t
WHERE NOT t.c -- 'x' 'y'
  EXCEPT ALL
SELECT t.b
FROM "T" AS t
WHERE t.c;    -- 'x' 'y' 'x'
/* # Output #
 b
---
(0 rows) */
```

### 10. Syntactic sugar: GROUPING SETS/ROLLUP/CUBE

```sql
DROP TABLE IF EXISTS prehistoric;
CREATE TABLE prehistoric (class text,
                          "herbivore?" boolean,
                          legs int,
                          species text);

INSERT INTO prehistoric VALUES
  ('mammalia', true, 2, 'Megatherium'),
  ('mammalia', true, 4, 'Paraceratherium'),
  ('mammalia', false, 2, NULL),
  ('mammalia', false, 4, 'Sabretooth'),
  ('reptilia', true, 2, 'Iguanodon'),
  ('reptilia', true, 4, 'Brachiosaurus'),
  ('reptilia', false, 2, 'Velociraptor'),
  ('reptilia', false, 4, NULL);
```

#### `GROUPING SETS`

```sql
SELECT p.class,
       p."herbivore?",
       p.legs,
       string_agg(p.species, ', ') AS species -- string_agg ignores NULL
FROM prehistoric AS p
GROUP BY GROUPING SETS ((class), ("herbivore?"), (legs));
/* # Output #
  class   | herbivore? | legs |                        species
----------+------------+------+--------------------------------------------------------
 reptilia |            |      | Iguanodon, Brachiosaurus, Velociraptor
 mammalia |            |      | Megatherium, Paraceratherium, Sabretooth
          | f          |      | Sabretooth, Velociraptor
          | t          |      | Megatherium, Paraceratherium, Iguanodon, Brachiosaurus
          |            |    4 | Paraceratherium, Sabretooth, Brachiosaurus
          |            |    2 | Megatherium, Iguanodon, Velociraptor
(6 rows) */
```

- Without using GROUPING SETS the same result can be acquired by using three GROUP BY and two UNION ALL.

```sql
SELECT p.class,
       NULL::boolean AS "herbivore?",
       NULL::int AS legs,
       string_agg(p.species, ', ') AS species
FROM prehistoric AS p
GROUP BY p.class
  /* # Output #
    class   | herbivore? | legs |                 species
  ----------+------------+------+------------------------------------------
  reptilia |            |      | Iguanodon, Brachiosaurus, Velociraptor
  mammalia |            |      | Megatherium, Paraceratherium, Sabretooth
  (2 rows) */

  UNION ALL

SELECT NULL::text AS class,
       p."herbivore?",
       NULL::int AS legs,
       string_agg(p.species, ', ') AS species
FROM prehistoric AS p
GROUP BY p."herbivore?"
  /* # Output #
  class | herbivore? | legs |                        species
  -------+------------+------+--------------------------------------------------------
        | f          |      | Sabretooth, Velociraptor
        | t          |      | Megatherium, Paraceratherium, Iguanodon, Brachiosaurus
  (2 rows) */

  UNION ALL

SELECT NULL::text AS class,
       NULL::boolean AS "herbivore?",
       p.legs AS legs,
       string_agg(p.species, ', ') AS species
FROM prehistoric AS p
GROUP BY p.legs;
  /* # Output #
  class | herbivore? | legs |                  species
  -------+------------+------+--------------------------------------------
        |            |    4 | Paraceratherium, Sabretooth, Brachiosaurus
        |            |    2 | Megatherium, Iguanodon, Velociraptor
  (2 rows) */

/* # Final Output #
  class   | herbivore? | legs |                        species
----------+------------+------+--------------------------------------------------------
 reptilia |            |      | Iguanodon, Brachiosaurus, Velociraptor
 mammalia |            |      | Megatherium, Paraceratherium, Sabretooth
          | f          |      | Sabretooth, Velociraptor
          | t          |      | Megatherium, Paraceratherium, Iguanodon, Brachiosaurus
          |            |    4 | Paraceratherium, Sabretooth, Brachiosaurus
          |            |    2 | Megatherium, Iguanodon, Velociraptor
(6 rows) */
```

#### `ROLLUP`

```sql
SELECT p.class,
       p."herbivore?",
       p.legs,
       string_agg(p.species, ', ') AS species
FROM prehistoric AS p
GROUP BY ROLLUP (class, "herbivore?", legs);
/* # Output #
  class   | herbivore? | legs |                                     species

----------+------------+------+----------------------------------------------------------------------------------
 mammalia | f          |    2 |
 mammalia | f          |    4 | Sabretooth
 mammalia | f          |      | Sabretooth
 mammalia | t          |    2 | Megatherium
 mammalia | t          |    4 | Paraceratherium
 mammalia | t          |      | Megatherium, Paraceratherium
 mammalia |            |      | Sabretooth, Megatherium, Paraceratherium
 reptilia | f          |    2 | Velociraptor
 reptilia | f          |    4 |
 reptilia | f          |      | Velociraptor
 reptilia | t          |    2 | Iguanodon
 reptilia | t          |    4 | Brachiosaurus
 reptilia | t          |      | Iguanodon, Brachiosaurus
 reptilia |            |      | Velociraptor, Iguanodon, Brachiosaurus
          |            |      | Sabretooth, Megatherium, Paraceratherium, Velociraptor, Iguanodon, Brachiosaurus
(15 rows) */

SELECT string_agg(p.species, ', ') AS species
FROM prehistoric AS p
GROUP BY (); -- same as w/o GROUP BY
/* # Output #
                                     species
----------------------------------------------------------------------------------
 Megatherium, Paraceratherium, Sabretooth, Iguanodon, Brachiosaurus, Velociraptor
(1 row) */
```

#### `CUBE`

```sql
SELECT p.class,
       p."herbivore?",
       p.legs,
       string_agg(p.species, ', ') AS species
FROM prehistoric AS p
GROUP BY CUBE (class, "herbivore?", legs);
/* # Output #
  class   | herbivore? | legs |                                     species
----------+------------+------+----------------------------------------------------------------------------------
 mammalia | f          |    2 |
 mammalia | f          |    4 | Sabretooth
 mammalia | f          |      | Sabretooth
 mammalia | t          |    2 | Megatherium
 mammalia | t          |    4 | Paraceratherium
 mammalia | t          |      | Megatherium, Paraceratherium
 mammalia |            |      | Sabretooth, Megatherium, Paraceratherium
 reptilia | f          |    2 | Velociraptor
 reptilia | f          |    4 |
 reptilia | f          |      | Velociraptor
 reptilia | t          |    2 | Iguanodon
 reptilia | t          |    4 | Brachiosaurus
 reptilia | t          |      | Iguanodon, Brachiosaurus
 reptilia |            |      | Velociraptor, Iguanodon, Brachiosaurus
          |            |      | Sabretooth, Megatherium, Paraceratherium, Velociraptor, Iguanodon, Brachiosaurus
          | f          |    2 | Velociraptor
          | f          |    4 | Sabretooth
          | f          |      | Velociraptor, Sabretooth
          | t          |    2 | Megatherium, Iguanodon
          | t          |    4 | Paraceratherium, Brachiosaurus
          | t          |      | Megatherium, Iguanodon, Paraceratherium, Brachiosaurus
          |            |    4 | Sabretooth, Paraceratherium, Brachiosaurus
          |            |    2 | Megatherium, Velociraptor, Iguanodon
 reptilia |            |    4 | Brachiosaurus
 mammalia |            |    2 | Megatherium
 mammalia |            |    4 | Sabretooth, Paraceratherium
 reptilia |            |    2 | Velociraptor, Iguanodon
(27 rows) */
```

### 11. SQL reading vs. evaluation order, CTEs (WITH)

```sql
WITH
  prehistoric(class, "herbivore?", legs, species) AS (
    VALUES ('mammalia', true, 2, 'Megatherium'),
           ('reptilia', false, 4, NULL)
  )
SELECT MAX(p.legs)
FROM prehistoric AS p;
/* # Output #
 max
-----
   4
(1 row) */
```
