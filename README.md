Need to also create a data directory in the root of the project with the following empty subdirectories: data and presto.

Can deploy via docker-compose up -d --build

For Superset, you might need to set a password
docker exec -it superset-app superset fab create-admin   --username admin   --firstname Admin   --lastname User   --email admin@example.com   --password admin

**Best Practice to Upgrade**

docker exec -it superset-app superset db upgrade

docker exec -it superset-app superset db upgrade



<img width="1212" height="848" alt="Screenshot 2025-07-23 at 10 34 03 AM" src="https://github.com/user-attachments/assets/e6628031-a400-4294-98ba-16f3068c42c4" />
