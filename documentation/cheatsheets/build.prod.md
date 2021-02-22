# How to build production environment

1. Go to the project root
2. Create the storage for environment variables on development environment with following structure
```shell
FLASK_APP=roco/__init__.py
FLASK_ENV=production
DATABASE_URL=postgresql://<username>:<password>@db:5432/mast_db_prod
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
ADMIN_PASSWD= # Set some
EMAIL_USER= #set mathletics email
EMAIL_PASS= #set mathletics email password
```

3. Run the following commands
```shell
# Stops and removes previously initiated compose
$ docker-compose down -w
# Builds and starts the containers from compose in detached mode, hence in the background
$ docker-compose -f docker-compose.prod.yml up -d --build 
# Creates a new database
$ docker-compose -f docker-compose.prod.yml exec rfc_app python manage.py create_db
# Creates the new admin user
$ docker-compose -f docker-compose.prod.yml exec rfc_app python manage.py seed_db
```

4. Follow the link: https://localhost:1337