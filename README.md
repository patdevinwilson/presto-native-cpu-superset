Need to also create a data directory in the root of the project with the following empty subdirectories: data and presto.

Can deploy via docker-compose up -d.

For Superset, you made to set a password
docker exec -it superset-app superset fab create-admin   --username admin   --firstname Admin   --lastname User   --email admin@example.com   --password admin

**Best Practice to Upgrade**
docker exec -it superset-app superset db upgrade

docker exec -it superset-app superset db upgrade
