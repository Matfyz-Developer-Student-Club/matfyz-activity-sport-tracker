# How to build development environment

1. Go to the project root
2. Create the storage for environment variables on development environment with following structure
```shell
FLASK_APP=mast/__init__.py
FLASK_ENV=production
DATABASE_URL=postgresql://<username>:<password>@db:5432/mast_db_dev
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
ADMIN_PASSWD=
EMAIL_USER=
EMAIL_PASS=
```

3. Create a storage for environment variables intent to be placed in the Postgres container with following structure - name: env.prod.db
```shell
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
```

4. Run the following commands
```shell
# Stops and removes previously initiated compose
$ docker-compose down -v
# Builds and starts the containers from compose in detached mode, hence in the background
$ docker-compose -f docker-compose.prod.yml up -d --build 
# Creates the new database
$ docker-compose -f docker-compose.prod.yml exec mathletics python manage.py create_db 
# Creates an admin user
$ docker-compose -f docker-compose.prod.yml exec mathletics python manage.py seed_db
```

4. Follow the link: https://localhost:1337
