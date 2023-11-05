# postgres-playground

## Instructions to Run Locally

- Install and start Docker
- `docker compose up -d`: start postgres container on background
- `docker ps`: list all running containers
- `docker exec -it <container_id> psql -U postgres -W postgres`: run psql

## Chapter 2

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

### 12. Use case for WITH: dinosaur locomotion

```sql
DROP TABLE IF EXISTS dinosaurs;
CREATE TABLE dinosaurs (species text, height float, length float, legs int);

INSERT INTO dinosaurs(species, height, length, legs) VALUES
  ('Ceratosaurus',    4.0,  6.1,  2),
  ('Deinonychus',     1.5,  2.7,  2),
  ('Microvenator',    0.8,  1.2,  2),
  ('Plateosaurus',    2.1,  7.9,  2),
  ('Spinosaurus',     2.4,  12.2, 2),
  ('Tyrannosaurus',   7.0,  15.2, 2),
  ('Velociraptor',    0.6,  1.8,  2),
  ('Apatosaurus',     2.2,  22.9, 4),
  ('Brachiosaurus',   7.6,  30.5, 4),
  ('Diplodocus',      3.6,  27.1, 4),
  ('Supersaurus',     10.0, 30.5, 4),
  ('Albertosaurus',   4.6,  9.1,  NULL),
  ('Argentinosaurus', 10.7, 36.6, NULL),
  ('Compsognathus',   0.6,  0.9,  NULL),
  ('Gallimimus',      2.4,  5.5,  NULL),
  ('Mamenchisaurus',  5.3,  21.0, NULL),
  ('Oviraptor',       0.9,  1.5,  NULL),
  ('Ultrasaurus',     8.1,  30.5, NULL);
```

```sql
WITH bodies(legs, shape) AS (
  SELECT d.legs, avg(d.height / d.length) AS shape
  FROM dinosaurs AS d
  WHERE d.legs IS NOT NULL
  GROUP BY d.legs
)
  -- TABLE bodies;
  /* # Output #
  legs |        shape
  ------+---------------------
      4 | 0.20149009443419652
      2 |  0.4477662389355141
  (2 rows) */

SELECT d.species, d.height, d.length,
  (SELECT b.legs
   FROM bodies AS b
   ORDER BY abs(b.shape - d.height / d.length)
   LIMIT 1) AS legs
FROM dinosaurs AS d
WHERE d.legs IS NULL

  UNION ALL

SELECT d.*
FROM dinosaurs AS d
WHERE d.legs IS NOT NULL;
/* # Output #
     species     | height | length | legs
-----------------+--------+--------+------
 Albertosaurus   |    4.6 |    9.1 |    2
 Argentinosaurus |   10.7 |   36.6 |    4
 Compsognathus   |    0.6 |    0.9 |    2
 Gallimimus      |    2.4 |    5.5 |    2
 Mamenchisaurus  |    5.3 |     21 |    4
 Oviraptor       |    0.9 |    1.5 |    2
 Ultrasaurus     |    8.1 |   30.5 |    4
 Ceratosaurus    |      4 |    6.1 |    2
 Deinonychus     |    1.5 |    2.7 |    2
 Microvenator    |    0.8 |    1.2 |    2
 Plateosaurus    |    2.1 |    7.9 |    2
 Spinosaurus     |    2.4 |   12.2 |    2
 Tyrannosaurus   |      7 |   15.2 |    2
 Velociraptor    |    0.6 |    1.8 |    2
 Apatosaurus     |    2.2 |   22.9 |    4
 Brachiosaurus   |    7.6 |   30.5 |    4
 Diplodocus      |    3.6 |   27.1 |    4
 Supersaurus     |     10 |   30.5 |    4
(18 rows) */
```

## Chapter 3

### 13. Built-in data types, CAST, casting text literals

```sql
SELECT string_agg(t.typname, ', ') AS "data types"
FROM pg_catalog.pg_type AS t
WHERE t.typelem = 0   -- disregard array element types
  AND t.typrelid = 0; -- list non-composite types only
```

- data types:

`bool, bytea, char, int8, int2, int4, regproc, text, oid, tid, xid, cid, json, xml, pg_node_tree, pg_ndistinct, pg_dependencies, pg_mcv_list, pg_ddl_command, path, polygon, float4, float8, unknown, circle, money, macaddr, inet, cidr, macaddr8, aclitem, bpchar, varchar, date, time, timestamp, timestamptz, interval, timetz, bit, varbit, numeric, refcursor, regprocedure, regoper, regoperator, regclass, regtype, regrole, regnamespace, uuid, pg_lsn, tsvector, gtsvector, tsquery, regconfig, regdictionary, jsonb, jsonpath, txid_snapshot, int4range, numrange, tsrange, tstzrange, daterange, int8range, record, cstring, any, anyarray, void, trigger, event_trigger, language_handler, internal, opaque, anyelement, anynonarray, anyenum, fdw_handler, index_am_handler, tsm_handler, table_am_handler, anyrange, cardinal_number, character_data, sql_identifier, time_stamp, yes_or_no`

#### Type casts

- Runtime type conversion

```sql
SELECT 6.2::int; -- 6
SELECT 6.8::int; -- 7
SELECT date('13 Feb, 2000'); -- 2000-02-13
```

- Implicit conversion

```sql
INSERT INTO "T"(a,b,c,d) VALUES (6.2, NULL, 'true', '0');
/* # Inserted row #
 a | b | c | d
---+---+---+---
 6 |   | t | 0
(1 row) */

SELECT booleans.yup::boolean, booleans.nope::boolean
FROM (VALUES ('true', 'false'),
             ('True', 'False'),
             ('t',    'f'),
             ('1',    '0'),
             ('yes',  'no'),
             ('on',   'off')) AS booleans(yup, nope);
/* # Output #
 yup | nope
-----+------
 t   | f
 t   | f
 t   | f
 t   | f
 t   | f
 t   | f
(6 rows) */
```

- XML

```sql
SELECT $$<t a='42'><l/><r/></t>$$::xml;
/* # Output #
          xml
------------------------
 <t a='42'><l/><r/></t>
(1 row) */

SELECT $int$42$int$::int;
/* # Output #
 int4
------
   42
(1 row) */
```

- CSV

```sql
DELETE FROM "T";

COPY "T"(a,b,c,d) FROM STDIN WITH (FORMAT CSV, NULL '*');
1,x,true,10
2,y,true,40
3,x,false,30
4,y,false,20
5,x,true,*
\.

TABLE "T";
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

### 14. String data types (char/varchar/text), type numeric(s,p)

- `char`: `char(1)`
- `char(n)`: fixed length, blank (` `) padded if needed
- `varchar(n)`: varying length <= n characters
- `text`: varying length, unlimited

```sql
SELECT '01234'::char(3);
/* # Output #
 bpchar -- bpchar: blank-padded character
--------
 012
(1 row) */

SELECT t.c::char(10)
FROM (VALUES ('01234'),
             ('0123456789')
     ) AS t(c);
/* # Output #
     c
------------
 01234
 0123456789
(2 rows) */

SELECT t.c,
       length(t.c) AS chars,
       octet_length(t.c) AS bytes
FROM (VALUES ('x'),
             ('池'),
             ('😀😃')
     ) AS t(c);
/* # Output #
  c   | chars | bytes
------+-------+-------
 x    |     1 |     1
 池   |     1 |     3
 😀😃 |     2 |     8
(3 rows) */

SELECT octet_length('0123456789'::varchar(5)) AS c1,  -- 5 (truncation)
       octet_length('012'       ::varchar(5)) AS c2,  -- 3 (within limits)
       octet_length('012'       ::char(5)) AS c3,     -- 5 (blank padding in storage)
       length('012'             ::char(5)) AS c4,     -- 3 (padding in storage only)
       length('012  '           ::char(5)) AS c5;     -- 3 (trailing blanks removed)
/* # Output #
 c1 | c2 | c3 | c4 | c5
----+----+----+----+----
  5 |  3 |  5 |  3 |  3
(1 row) */
```

#### Numeric

```sql
\pset t on
SELECT (2::numeric)^100000; -- SQL syntax allows numeric(1000) only
\pset t off
/* # Output #
99900209301438450794403276433003359098042913905418169177152927386314583246425...
(1 row) */

EXPLAIN ANALYZE
WITH one_million_rows(x) AS (
  SELECT t.x::numeric(8,0)
  FROM generate_series(0,1000000) AS t(x)
)
SELECT t.x + t.x AS add
FROM one_million_rows AS t;
/* # Output #
 Planning Time: 0.030 ms
 Execution Time: 375.387 ms
(2 rows) */

EXPLAIN ANALYZE
WITH one_million_rows(x) AS (
  SELECT t.x::int
  FROM generate_series(0,1000000) AS t(x)
)
SELECT t.x + t.x AS add
FROM one_million_rows AS t;
/* # Output #
 Planning Time: 0.027 ms
 Execution Time: 195.863 ms
(2 rows) */
```

### 15. Types date/time/timestamp/interval, date/time arithmetics

```sql
SELECT 'now'::date AS "now (date)",
       'now'::time AS "now (time)",
       'now'::timestamp AS "now (timestamp)";
/* # Output #
 now (date) |   now (time)    |      now (timestamp)
------------+-----------------+----------------------------
 2023-10-30 | 11:48:10.652387 | 2023-10-30 11:48:10.652387
(1 row) */

SELECT 'now'::timestamp AS "now",
       'now'::timestamp with time zone AS "now with time zone",
       'now'::timestamptz AS "now tz";
/* # Output #
            now             |      now with time zone       |            now tz
----------------------------+-------------------------------+-------------------------------
 2023-10-30 11:50:21.777615 | 2023-10-30 11:50:21.777615+00 | 2023-10-30 11:50:21.777615+00
(1 row) */

SET datestyle='German,MDY';
SELECT '1-2-2000'::date;
/* # Output #
    date
------------
 02.01.2000
(1 row) */

SET datestyle='German,DMY';
SELECT '1-2-2000'::date;
/* # Output #
    date
------------
 01.02.2000
(1 row) */

SET datestyle='ISO,MDY'; -- default datestyle

SELECT COUNT(DISTINCT birthdays.d::date) AS interpretations
FROM (VALUES ('August 26, 1968'),
             ('Aug 26, 1968'),
             ('08.26.1968'),
             ('08-26-1968'),
             ('8/26/1968')) AS birthdays(d);
/* # Output #
 interpretations
-----------------
               1
(1 row) */

SELECT 'epoch'::timestamp AS epoch,
       'infinity'::timestamp AS infinity,
       'today'::date AS today,
       'yesterday'::date AS yesterday,
       'tomorrow'::date AS tomorrow;
/* # Output #
        epoch        | infinity |   today    | yesterday  |  tomorrow
---------------------+----------+------------+------------+------------
 1970-01-01 00:00:00 | infinity | 2023-10-30 | 2023-10-29 | 2023-10-31
(1 row) */

SELECT '1 year 2 months 3 days 4 hours 5 minutes 6 seconds'::interval;
/* # Output #
           interval
-------------------------------
 1 year 2 mons 3 days 04:05:06
(1 row) */

SELECT 'P1Y2M3DT4H5M6S'::interval; -- ISO 8601
/* # Output #
           interval
-------------------------------
 1 year 2 mons 3 days 04:05:06
(1 row) */

SELECT ('now'::timestamp - 'yesterday'::date)::interval;
/* # Output #
       interval
-----------------------
 1 day 12:30:20.951839
(1 row) */

\x on -- expanded display
SELECT 'Aug 31, 2035'::date - 'now'::timestamp AS retirement,
       'now'::date + '30 days'::interval AS in_one_month,
       'now'::date + 2 * '1 month'::interval AS in_two_months,
       'tomorrow'::date - 'now'::timestamp AS til_midnight,
       extract(hours from('tomorrow'::date - 'now'::timestamp)) AS hours_til_midnight,
       'tomorrow'::date - 'yesterday'::date AS two,
       make_interval(days => 'tomorrow'::date - 'yesterday'::date) AS two_days;
\x off
/* # Output #
-[ RECORD 1 ]------+--------------------------
retirement         | 4322 days 11:19:23.836858
in_one_month       | 2023-11-29 00:00:00
in_two_months      | 2023-12-30 00:00:00
til_midnight       | 11:19:23.836858
hours_til_midnight | 11
two                | 2
two_days           | 2 days */

SELECT (make_date(2023, months.m, 1) - '1 day'::interval)::date AS last_day_of_month
FROM generate_series(1,12) AS months(m);
/* # Output #
------------------+-----------
last_day_of_month | 2022-12-31
last_day_of_month | 2023-01-31
last_day_of_month | 2023-02-28
last_day_of_month | 2023-03-31
last_day_of_month | 2023-04-30
last_day_of_month | 2023-05-31
last_day_of_month | 2023-06-30
last_day_of_month | 2023-07-31
last_day_of_month | 2023-08-31
last_day_of_month | 2023-09-30
last_day_of_month | 2023-10-31
last_day_of_month | 2023-11-30 */

SELECT timezones.tz AS timezone,
       'now'::timestamp with time zone
        -
       ('now'::timestamp::text || ' ' || timezones.tz)::timestamp with time zone AS difference
FROM   (VALUES ('America/New_York'),
               ('Europe/Istanbul'),
               ('Asia/Tokyo'),
               ('PST'),
               ('UTC'),
               ('UTC-6'),
               ('+5')
       ) AS timezones(tz)
ORDER BY difference;
/* # Output #
-[ RECORD 1 ]----------------
timezone   | PST
difference | -08:00:00
-[ RECORD 2 ]----------------
timezone   | America/New_York
difference | -04:00:00
-[ RECORD 3 ]----------------
timezone   | UTC
difference | 00:00:00
-[ RECORD 4 ]----------------
timezone   | Europe/Istanbul
difference | 03:00:00
-[ RECORD 5 ]----------------
timezone   | +5
difference | 05:00:00
-[ RECORD 6 ]----------------
timezone   | UTC-6
difference | 06:00:00
-[ RECORD 7 ]----------------
timezone   | Asia/Tokyo
difference | 09:00:00 */

SELECT holidays.holiday
FROM (VALUES ('Easter',    'Apr  6, 2023', 'Apr 18, 2023'),
             ('Pentecost', 'Jun  2, 2023', 'Jun 13, 2023'),
             ('Summer',    'Jul 30, 2023', 'Sep  9, 2023'),
             ('Autumn',    'Oct 26, 2023', 'Oct 31, 2023'),
             ('Winter',    'Dec 23, 2023', 'Jan  9, 2024')) AS holidays(holiday, "start", "end")
WHERE (holidays.start::date, holidays.end::date) overlaps('today', 'today');
/* # Output #
-[ RECORD 1 ]---
holiday | Autumn */
```

### 16. User-defined types: enumerations (CREATE TYPE ... AS ENUM)

```sql
DROP TYPE IF EXISTS episode CASCADE; -- CASCADE: deletes episode columns
CREATE TYPE episode AS ENUM
  ('ANH', 'ESB', 'TPM', 'AOTC', 'ROTS', 'ROTJ', 'TFA', 'TLJ', 'TROS');

SELECT 'ESB'::episode;
/* # Output #
 episode
---------
 ESB
(1 row) */

DROP TABLE IF EXISTS starwars;
CREATE TABLE starwars(film episode PRIMARY KEY,
                      title text,
                      release date);

INSERT INTO starwars(film,title,release) VALUES
  ('TPM',  'The Phantom Menace',      'May 19, 1999'),
  ('AOTC', 'The Empire Strikes Back', 'May 16, 2002'),
  ('ROTS', 'Revenge of the Sith',     'May 19, 2005'),
  ('ANH',  'A New Hope',              'May 25, 1977'),
  ('ESB',  'The Empire Strikes Back', 'May 21, 1980'),
  ('ROTJ', 'Return of the Jedi',      'May 25, 1983'),
  ('TFA',  'The Force Awakens',       'Dec 18, 2015'),
  ('TLJ',  'The Last Jedi',           'Dec 15, 2017'),
  ('TROS', 'The Rise of Skywalker',   'Dec 19, 2019');

INSERT INTO starwars(film,title,release) VALUES
  ('R1', 'Rogue One', 'Dec 15, 2016');
/* # Output #
ERROR:  invalid input value for enum episode: "R1" */

SELECT s.*
FROM starwars AS s
ORDER BY s.release;
/* # Output #
 film |          title          |  release
------+-------------------------+------------
 ANH  | A New Hope              | 1977-05-25
 ESB  | The Empire Strikes Back | 1980-05-21
 ROTJ | Return of the Jedi      | 1983-05-25
 TPM  | The Phantom Menace      | 1999-05-19
 AOTC | The Empire Strikes Back | 2002-05-16
 ROTS | Revenge of the Sith     | 2005-05-19
 TFA  | The Force Awakens       | 2015-12-18
 TLJ  | The Last Jedi           | 2017-12-15
 TROS | The Rise of Skywalker   | 2019-12-19
(9 rows) */

SELECT s.*
FROM starwars AS s
ORDER BY s.film; -- the Star Wars Machete order
/* # Output #
 film |          title          |  release
------+-------------------------+------------
 ANH  | A New Hope              | 1977-05-25
 ESB  | The Empire Strikes Back | 1980-05-21
 TPM  | The Phantom Menace      | 1999-05-19
 AOTC | The Empire Strikes Back | 2002-05-16
 ROTS | Revenge of the Sith     | 2005-05-19
 ROTJ | Return of the Jedi      | 1983-05-25
 TFA  | The Force Awakens       | 2015-12-18
 TLJ  | The Last Jedi           | 2017-12-15
 TROS | The Rise of Skywalker   | 2019-12-19
(9 rows) */
```

### 17. Bit strings (bit(n)), BLOBS, and byte types (bytea)

#### Bitwise Operations

- `&`: and
- `|`: or
- `#`: xor
- `~`: not
- `<<`/`>>`: shift left/right,
- `get_bit()`
- `set_bit()`

#### String-like Operations

- `||`: concatenation
- `length()`
- `bit_length()`
- `position( in )`

```sql
SELECT B'00101010', X'2A', '00101010'::bit(8), 42::bit(8); -- X'2A': 2 * 4 bits
/* # Output #
 ?column? | ?column? |   bit    |   bit
----------+----------+----------+----------
 00101010 | 00101010 | 00101010 | 00101010
(1 row) */
```

```sql
SELECT encode('chsdwn', 'base64');
/* # Output #
  encode
----------
 Y2hzZHdu
(1 row) */
```

#### Install Python 3 and create language:

- List running container: `docker ps`
- Run the postgresql container's bash: `docker exec -it <container_id> bash`
- Update debian packages: `apt-get update`
- Install plpython3 package for PostgreSQL 12: `apt install postgresql-plpython3-12`
- Check python version and make sure its installed: `python3 --version`
- Create language:

```sql
CREATE LANGUAGE plpython3u;
```

```sql
DROP FUNCTION IF EXISTS read_blob(text) CASCADE;
CREATE FUNCTION read_blob(blob text) RETURNS bytea AS
$$
  try:
    file = open(blob, "rb")
    return file.read()
  except:
    pass
  # could not read file, return NULL
  return None
$$ LANGUAGE plpython3u;

DROP TYPE IF EXISTS edition CASCADE;
CREATE TYPE edition AS ENUM ('Portal 1', 'Portal 2');

DROP TABLE IF EXISTS glados;
CREATE TABLE glados (id int PRIMARY KEY,
                     voice bytea,
                     line text,
                     portal edition);

\set blob_path './glados-voice'
INSERT INTO glados(id, line, portal, voice)
  SELECT quotes.id, quotes.line, quotes.portal::edition,
         read_blob(:'blob_path' || quotes.mp3) AS voice
  FROM
    (VALUES (1, 'one', 'Portal 1', '1.mp3'),
            (2, 'two', 'Portal 2', '2.mp3')) AS quotes(id, line, portal, mp3);

SELECT g.id, g.line, g.portal,
       left(encode(g.voice, 'base64'), 20) AS voice
FROM glados AS g;
/* # Output #
 id | line |  portal  |        voice
----+------+----------+---------------------
  1 | one  | Portal 1 | UklGRvpIBABXQVZFZm10
  2 | two  | Portal 2 | UklGRjc6DABXQVZFZm10
(2 rows) */

COPY (
  SELECT translate(encode(g.voice, 'base64'), E'\n', '')
  FROM glados AS g
  WHERE g.id = 1
) TO PROGRAM 'base64 -D > /tmp/1.mp3';
```

### 18. Range/interval types and operations

```sql
SELECT '[5,10)'::int4range;
/* # Output #
 int4range
-----------
 [5,10)
(1 row) */

SELECT int4range(1,5,'[]');
/* # Output #
 int4range
-----------
 [1,6)
(1 row) */

SELECT int4range(1,5,'[]') * '[5,10)'::int4range;
/* # Output #
 ?column?
----------
 [5,6)
(1 row) */

SELECT int4range(1,5,'[)') * '[5,10)'::int4range;
/* # Output #
 ?column?
----------
 empty
(1 row) */
```

### 19. Geometric objects and operations, use case: shape scanner

- `point(x,y)`
- `line(x,y)`
- `box(p1,p2)`
- `[p1,...,pn]`: open path
- `(p1,...,pn)`: polygon
- `circle(p,r)`

#### Operations

|          | Operation            |                | Operation           |
| -------- | -------------------- | -------------- | ------------------- |
| `+`, `-` | translate            | `area()`       |                     |
| `*`      | scale                | `height()`     | height of box       |
| `@-@`    | length/circumference | `width()`      | width of box        |
| `@@`     | center               | `bound_box(,)` | bounding box        |
| `<->`    | distance between     | `diameter()`   | diameter of circle  |
| `&&`     | overlaps?            | `center()`     | center              |
| `<<`     | strictly left of?    | `isclosed()`   | path closed         |
| `?-\|`   | is perpendicular?    | `npoints()`    | # of points in path |
| `@>`     | contains?            | `pclose()`     | close an open path  |

```sql
\set N 100000
SELECT (COUNT(*)::float / :N) * 4 AS pi
FROM generate_series(1, :N) AS _
WHERE circle(point(0.5,0.5), 0.5) @> point(random(),random());
/* # Output #
   pi
--------
 3.1412
(1 row) */
```

### 20. JSON support (type jsonb) [and XML support]

```sql
VALUES (1, '{ "b": 1, "a": 2 }'::jsonb),  -- pair order flip
       (2, '{ "a": 1, "b": 2, "a": 3 }'), -- duplicate field
       (3, '[0,   false, null]');         -- whitespace normalization
/* # Output #
 column1 |     column2
---------+------------------
       1 | {"a": 2, "b": 1}
       2 | {"a": 3, "b": 2}
       3 | [0, false, null]
(3 rows) */

VALUES (1, '{ "b": 1, "a": 2 }'::json),   -- preserve pair order
       (2, '{ "a": 1, "b": 2, "a": 3 }'), -- preserve duplicates
       (3, '[0,   false, null]');         -- preserve whitespace
/* # Output #
 column1 |          column2
---------+----------------------------
       1 | { "b": 1, "a": 2 }
       2 | { "a": 1, "b": 2, "a": 3 }
       3 | [0,   false, null]
(3 rows) */

SELECT ('{ "a": 0, "b": { "b1": 1, "b2": 2 } }'::jsonb -> 'b' ->> 'b2')::int + 40;
/* # Output #
 ?column?
----------
       42
(1 row) */

SELECT row_to_json(t)::jsonb
FROM "T" AS t;
/* # Output #
               row_to_json
------------------------------------------
 {"a": 1, "b": "x", "c": true, "d": 10}
 {"a": 2, "b": "y", "c": true, "d": 40}
 {"a": 3, "b": "x", "c": false, "d": 30}
 {"a": 4, "b": "y", "c": false, "d": 20}
 {"a": 5, "b": "x", "c": true, "d": null}
(5 rows) */

SELECT array_to_json(array_agg(row_to_json(t)))::jsonb
FROM "T" AS t;
/* # Output #
[{"a": 1, "b": "x", "c": true, "d": 10}, {"a": 2, "b": "y", "c": true, "d": 40}, {"a": 3, "b": "x", "c": false, "d": 30}, {"a": 4, "b": "y", "c": false, "d": 20}, {"a": 5, "b": "x", "c": true, "d": null}] */

SELECT jsonb_pretty(array_to_json(array_agg(row_to_json(t)))::jsonb)
FROM "T" AS t;
/* # Output #
    jsonb_pretty
---------------------
 [                  +
     {              +
         "a": 1,    +
         "b": "x",  +
         "c": true, +
         "d": 10    +
     },             +
     {              +
         "a": 2,    +
         "b": "y",  +
         "c": true, +
         "d": 40    +
     },             +
     {              +
         "a": 3,    +
         "b": "x",  +
         "c": false,+
         "d": 30    +
     },             +
     {              +
         "a": 4,    +
         "b": "y",  +
         "c": false,+
         "d": 20    +
     },             +
     {              +
         "a": 5,    +
         "b": "x",  +
         "c": true, +
         "d": null  +
     }              +
 ]
(1 row) */
```

```sql
DROP TABLE IF EXISTS like_T_but_as_JSON;
CREATE TEMPORARY TABLE like_T_but_as_JSON(a) AS
  SELECT array_to_json(array_agg(row_to_json(t)))::jsonb
  FROM "T" AS t;

TABLE like_T_but_as_JSON;
/* # Output #
[{"a": 1, "b": "x", "c": true, "d": 10}, {"a": 2, "b": "y", "c": true, "d": 40}, {"a": 3, "b": "x", "c": false, "d": 30}, {"a": 4, "b": "y", "c": false, "d": 20}, {"a": 5, "b": "x", "c": true, "d": null}] */

SELECT o
FROM jsonb_array_elements((TABLE like_T_but_as_JSON)) AS objs(o);
/* # Output #
                    o
------------------------------------------
 {"a": 1, "b": "x", "c": true, "d": 10}
 {"a": 2, "b": "y", "c": true, "d": 40}
 {"a": 3, "b": "x", "c": false, "d": 30}
 {"a": 4, "b": "y", "c": false, "d": 20}
 {"a": 5, "b": "x", "c": true, "d": null}
(5 rows) */

SELECT t.*
FROM jsonb_array_elements((TABLE like_T_but_as_JSON)) AS objs(o),
     jsonb_each(o) AS t;
/* # Output #
 key | value
-----+-------
 a   | 1
 b   | "x"
 c   | true
 d   | 10
 a   | 2
 b   | "y"
 c   | true
 d   | 40
 a   | 3
 b   | "x"
 c   | false
 d   | 30
 a   | 4
 b   | "y"
 c   | false
 d   | 20
 a   | 5
 b   | "x"
 c   | true
 d   | null
(20 rows) */

SELECT t.*
FROM jsonb_array_elements((TABLE like_T_but_as_JSON)) AS objs(o),
     jsonb_to_record(o) AS t(a int, b text, c boolean, d int);
/* # Output #
 a | b | c | d
---+---+---+----
 1 | x | t | 10
 2 | y | t | 40
 3 | x | f | 30
 4 | y | f | 20
 5 | x | t |
(5 rows) */

SELECT t.*
FROM jsonb_array_elements((TABLE like_T_but_as_JSON)) AS objs(o),
     jsonb_populate_record(NULL::"T", o) AS t;
/* # Output #
 a | b | c | d
---+---+---+----
 1 | x | t | 10
 2 | y | t | 40
 3 | x | f | 30
 4 | y | f | 20
 5 | x | t |
(5 rows) */

SELECT t.*
FROM jsonb_populate_recordset(NULL::"T", (TABLE like_T_but_as_JSON)) AS t;
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

### 21. Sequences, key generation via GENERATED ALWAYS AS IDENTITY

```sql
CREATE SEQUENCE <seq> -- sequence name
  [ INCREMENT <inc> ] -- advance by <inc> (default: 1)
  [ MINVALUE <min> ]  -- range of valid counter values
  [ MAXVALUE <max> ]  --  (defaults: [1...2^63-1])
  [ START <start> ]   -- start (default: <min>, <max>)
  [ [NO] CYCLE ]      -- wrap around or error
```

```sql
DROP SEQUENCE IF EXISTS seq;
CREATE SEQUENCE seq START 41 MAXVALUE 100 CYCLE;

SELECT nextval('seq');      -- 41
SELECT nextval('seq');      -- 42
SELECT currval('seq');      -- 42
SELECT setval('seq', 100);  -- 100 (side effect)
SELECT nextval('seq');      -- 1   (wrap around)

TABLE seq;
/* # Output #
 last_value | log_cnt | is_called
------------+---------+-----------
          1 |      32 | t
(1 row) */

SELECT setval('seq', 100, false); -- 100 (is_called: false)
SELECT nextval('seq');            -- 100
```

```sql
DROP TABLE IF EXISTS self_concious_T;
CREATE TABLE self_concious_T (me int GENERATED ALWAYS AS IDENTITY,
                              a int,
                              b text,
                              c boolean,
                              d int);

TABLE self_concious_T_me_seq;
/* # Output #
 last_value | log_cnt | is_called
------------+---------+-----------
          1 |       0 | f
(1 row) */

INSERT INTO self_concious_T(a,b,c,d)
  VALUES (1, 'x', true, 10),
         (2, 'y', true, 40);

INSERT INTO self_concious_T(a,b,c,d)
  VALUES (5, 'x', true, NULL),
         (4, 'y', false, 20),
         (3, 'x', false, 30)
RETURNING me, c;
/* # Output #
 me | c
----+---
  3 | t
  4 | f
  5 | f
(3 rows) */

TABLE self_concious_T;
/* # Output #
 me | a | b | c | d
----+---+---+---+----
  1 | 1 | x | t | 10
  2 | 2 | y | t | 40
  3 | 5 | x | t |
  4 | 4 | y | f | 20
  5 | 3 | x | f | 30
(5 rows) */
```

## Chapter 4

### 22. Arrays vs. 1NF, array semantics, array literals

- `{x1,...,xn}`: array of elements

```sql
DROP TABLE IF EXISTS "Trees";
CREATE TABLE "Trees" (tree int PRIMARY KEY,
                      parents int[],
                      labels text[]);

INSERT INTO "Trees"(tree, parents, labels) VALUES
  (1, array[NULL,1,2,2,1,5], array['a','b','d','e','c','f']),
  (2, array[4,1,1,6,4,NULL,6], array['d','f','a','b','e','g','c']),
  (3, array[NULL,1,NULL,1,3], string_to_array('a;b;d;c;e',';'));

TABLE "Trees";
/* # Output #
 tree |      parents       |     labels
------+--------------------+-----------------
    1 | {NULL,1,2,2,1,5}   | {a,b,d,e,c,f}
    2 | {4,1,1,6,4,NULL,6} | {d,f,a,b,e,g,c}
    3 | {NULL,1,NULL,1,3}  | {a,b,d,c,e}
(3 rows) */
```

### 23. Array construction/indexing/slicing, searching in arrays

```sql
SELECT array_append(array[1,2,3], 4);         -- {1,2,3,4}
SELECT array[1,2,3] || 4;                     -- {1,2,3,4}
SELECT array_prepend(4, array[1,2,3]);        -- {4,1,2,3}
SELECT 4 || array[1,2,3];                     -- {4,1,2,3}
SELECT array_cat(array[1,2,3], array[4,5,6]); -- {1,2,3,4,5,6}
SELECT array[1,2,3] || array[4,5,6];          -- {1,2,3,4,5,6}

SELECT (array[4])[1];           -- 4
SELECT (array[4])[NULL];        -- NULL
SELECT (array[NULL])[1];        -- NULL
SELECT (array[1,2,3,4,5])[2:4]; -- {2,3,4}
SELECT (array[1,2,3,4,5])[2:];  -- {2,3,4,5}
SELECT (array[1,2,3,4,5])[:4];  -- {1,2,3,4}

SELECT array_length(array[1,2,3], 1); -- 3
SELECT cardinality(array[1,2,3]);     -- 3

SELECT array_position(array[3,4,5], 4);     -- 2
SELECT array_position(array[3,4,5], 1);     -- NULL
SELECT array_positions(array[3,4,5,4], 4);  -- {2,4}
SELECT array_positions(array[3,4,5,4], 1);  -- {}
SELECT array_replace(array[1,2,3], 1, 4);   -- {4,2,3}
```

```sql
SELECT bool_and(cardinality(t.parents) = cardinality(t.labels))
FROM "Trees" AS t;
/* # Output #
 bool_and
----------
 t
(1 row) */

SELECT t.tree, array_positions(t.labels, 'f') AS "f nodes"
FROM "Trees" AS t
WHERE 'f' = ANY(t.labels);
/* # Output #
 tree | f nodes
------+---------
    1 | {6}
    2 | {2}
(2 rows) */

SELECT t.tree, t.labels[array_position(t.parents,NULL)] AS root
FROM "Trees" AS t;
/* # Output #
 tree | root
------+------
    1 | a
    2 | g
    3 | a
(3 rows) */

SELECT t.tree AS forest
FROM "Trees" AS t
WHERE cardinality(array_positions(t.parents,NULL)) > 1;
/* # Output #
 forest
--------
      3
(1 row) */
```

### 24. Array programming via unnest(), array_agg, WITH ORDINALITY

```sql
SELECT t.elem
FROM unnest(array[1,2,3]) AS t(elem); -- items order lost
/* # Output #
 elem
------
    1
    2
    3
(3 rows) */

SELECT array_agg(t.elem) AS xs
FROM (VALUES (1), (2), (3)) AS t(elem);
/* # Output #
   xs
---------
 {1,2,3}
(1 row) */

SELECT t.*
FROM unnest(array[6,5,4])
     WITH ORDINALITY AS t(elem,idx);  -- keep items order on "idx" column
/* # Output #
 elem | idx
------+-----
    6 |   1
    5 |   2
    4 |   3
(3 rows) */

SELECT array_agg(t.elem ORDER BY t.idx DESC) AS xs
FROM (VALUES (6,1), (5,2), (4,3)) AS t(elem,idx);
/* # Output #
   xs
---------
 {4,5,6}
(1 row) */
```

```sql
SELECT node.parent, node.label
FROM "Trees" AS t,
     unnest(t.parents, t.labels) AS node(parent,label)
WHERE t.tree = 2;
/* # Output #
 parent | label
--------+-------
      4 | d
      1 | f
      1 | a
      6 | b
      4 | e
        | g
      6 | c
(7 rows) */

SELECT node.*
FROM "Trees" AS t,
     unnest(t.parents, t.labels) WITH ORDINALITY AS node(parent,label,idx)
WHERE t.tree = 2;
/* # Output #
 parent | label | idx
--------+-------+-----
      4 | d     |   1
      1 | f     |   2
      1 | a     |   3
      6 | b     |   4
      4 | e     |   5
        | g     |   6
      6 | c     |   7
(7 rows) */

SELECT t.tree,
       array_agg(node.parent ORDER BY node.idx) AS parents,
       array_agg(upper(node.label) ORDER BY node.idx) AS labels
FROM "Trees" AS t,
     unnest(t.parents, t.labels) WITH ORDINALITY AS node(parent,label,idx)
GROUP BY t.tree;
/* # Output #
 tree |      parents       |     labels
------+--------------------+-----------------
    1 | {NULL,1,2,2,1,5}   | {A,B,D,E,C,F}
    2 | {4,1,1,6,4,NULL,6} | {D,F,A,B,E,G,C}
    3 | {NULL,1,NULL,1,3}  | {A,B,D,C,E}
(3 rows) */

SELECT t.tree, t.parents[node.idx] AS "parent of c"
FROM "Trees" AS t,
     unnest(t.labels) WITH ORDINALITY AS node(label,idx)
WHERE node.label = 'c';
/* # Output #
 tree | parent of c
------+-------------
    1 |           1
    2 |           6
    3 |           1
(3 rows) */

SELECT t.*
FROM "Trees" AS t,
     unnest(t.parents) AS node(parent)
WHERE node.parent IS NULL
GROUP BY t.tree
HAVING COUNT(*) > 1;
/* # Output #
 tree |      parents      |   labels
------+-------------------+-------------
    3 | {NULL,1,NULL,1,3} | {a,b,d,c,e}
(1 row) */
```

### 25. Set-returning/table-generating functions, ROWS FROM (zip)

```sql
SELECT generate_series(1,10,3); -- (from, to, increment)
/* # Output #
 generate_series
-----------------
               1
               4
               7
              10
(4 rows) */

SELECT generate_series(0,-2, -1);
/* # Output #
 generate_series
-----------------
               0
              -1
              -2
(3 rows) */

SELECT idx, arr[idx]
FROM (VALUES (string_to_array('abcde', NULL))) AS _(arr),
     generate_subscripts(arr, 1) AS idx;
/* # Output #
 idx | arr
-----+-----
   1 | a
   2 | b
   3 | c
   4 | d
   5 | e
(5 rows) */
```

```sql
SELECT i, xs[i]
FROM (VALUES (string_to_array('Star Wars', ' '))) AS _(xs),
     generate_subscripts(xs, 1) AS i;
/* # Output #
 i |  xs
---+------
 1 | Star
 2 | Wars
(2 rows) */

SELECT t.word
FROM regexp_split_to_table('Luke, I am Your Father', '\s+') AS t(word);
/* # Output #
  word
--------
 Luke,
 I
 am
 Your
 Father
(5 rows) */

SELECT upper(t.c) AS character, t.pos
FROM unnest(string_to_array('abcde', NULL))
     WITH ORDINALITY AS t(c,pos);
/* # Output #
 character | pos
-----------+-----
 A         |   1
 B         |   2
 C         |   3
 D         |   4
 E         |   5
(5 rows) */

SELECT starwars.*
FROM unnest(array[4,5,1,2,3,6,7,8,9],
            array['A New Hope',
                  'The Empire Strikes Back',
                  'The Phantom Menace',
                  'Attack of the Clones',
                  'Revenge of the Sith',
                  'Return of the Jedi',
                  'The Force Awakens',
                  'The Last Jedi',
                  'The Rise of Skywalker'])
     WITH ORDINALITY AS starwars(episode,film,watch)
ORDER BY watch;
/* # Output #
 episode |          film           | watch
---------+-------------------------+-------
       4 | A New Hope              |     1
       5 | The Empire Strikes Back |     2
       1 | The Phantom Menace      |     3
       2 | Attack of the Clones    |     4
       3 | Revenge of the Sith     |     5
       6 | Return of the Jedi      |     6
       7 | The Force Awakens       |     7
       8 | The Last Jedi           |     8
       9 | The Rise of Skywalker   |     9
(9 rows) */
```
