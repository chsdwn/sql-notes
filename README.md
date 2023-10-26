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
