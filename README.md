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
