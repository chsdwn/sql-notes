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
