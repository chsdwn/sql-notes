# postgres-playground

## Instructions to Run Locally

- Install and start Docker
- `docker compose up -d`: start postgres container on background
- `docker ps`: list all running containers
- `docker exec -it <container_id> psql -U postgres -W postgres`: run psql
