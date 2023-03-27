# Commoning Biomedicine

![Architecture](./diagrams/architecture.png)

## Requirements

- Python 3.10 (optional, development should be done in the provided Docker environment)
- Docker Desktop (or Docker Compose)

## Build and run

Note: update the environment variables in `env` folder before running the following commands:

```shell
cd <project-folder>
docker-compose build
docker-compose up  # or "docker-compose up -d" to run in detached mode
```
Go to [http://localhost:8081](http://localhost:8081)

## Installation on a DigitalOcean Droplet and nginx (Optional)

![Demo Architecture](diagrams/demo-architecture.png)

If you don't have a DigitalOcean account yet, create one using my referral [link](https://m.do.co/c/5b9c0bd05e4e).

1. Create a Domain and add an `A record` pointing to your Droplet.
2. Inside your Droplet, create an SSL certificate:

```shell
certbot --nginx -d <domain>
```

3. Edit the nginx configuration (usually /etc/nginx/sites-available/default) and update the `location /` block just below the domain created by certbot (look for `server_name <domain>; # managed by Certbot`):
   
```
	location / {
            proxy_pass http://127.0.0.1:8081$request_uri;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
	}
```

4. Reload nginx:

```shell
service nginx reload
```

## Scaling

To scale up, add --scale web=N parameter. For example:

```shell
docker-compose up --scale web=3
```

## Add translations

```shell
poetry run python manage.py makemessages -l <language_code>
# edit and translate locale/<language_code>/LC_MESSAGES/django.po
```

## Development

Go in the web container by doing

`docker exec -it combio_web bash`

You can then run the following commands.

### CSS / Tailwind
1. `python manage.py tailwind start` - starts the tailwind watcher, which recompiles the css file on every change
2. `python manage.py collectstatic --no-input` - creates the static files, necessary to update the css file used by the templates

### Loading Dummy Test Data
1. `python manage.py loaddummydata` - loads dummy test data

### Elasticsearch Index update
1. `python manage.py search_index --rebuild` - rebuilds the elasticsearch index

### Create Superuser
1. `python manage.py createsuperuser` - creates a super user, necessary to access the admin area at /admin

### Make Commands

Use the `Makefile` included for running different development tasks:

1. `make install` - installs the packages needed for development.
2. `make build` - build application.
3. `make start` - start application.
4. `make format` - runs `autoflake`, `isort` and `black` for fixing coding style.
5. `make lint` - runs `autoflake`, `isort`, `black`, `flake8` and `mypy` checks.
6. `make test` - run unit tests.
7. `make migrations` - generate migration scripts, if applicable.
8. `make migrate` - run migrations, if applicable.
9. `make superuser` - create superuser.
10. `make messages` - update messages.
11. `make compilemessages` - compile messages.
12. `make dumpdata` - backup data.
13. `make loaddata` - load data from backup.

