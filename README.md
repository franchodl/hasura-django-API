# Hasura + Django + Postgres

A project which pairs up the best features of Hasura with Django ❤️

## Get Started
Running these 2 commands will get your project up and running (as long as you have Docker installed).

Just run `./up.sh` or `docker-compose up` from the project directory.

Afterwards:
- Your Hasura Console dashboard will be exposed at: http://localhost:8080/console
  - You can start creating / exposing tables for your API here: http://localhost:8080/console/data/schema/public
  - You can test with your GraphQL endpoint here: http://localhost:8080/graphql
- Your REST API (for Django stuff) will be accessible over: http://localhost:8000
  - Django admin panel will be accessible from: 


### Enter the Hasura console

The password is set by the environment variable <HASURA_GRAPHQL_ADMIN_SECRET>


## Troubleshooting

### ERROR: for postgres  Cannot start service postgres: Ports are not available: exposing port TCP 0.0.0.0:5432 -> 0.0.0.0:0: listen tcp 0.0.0.0:5432: bind: address already in use

You need to kill any other process in that port:
`sudo lsof -i:5432`
`sudo kill -15 <process id>`

Specifically kill postgres process: `sudo service postgresql stop`

### ModuleNotFoundError: No module names 'yaml'
Run `pip3 install pyyaml` (outside of any virtual environment).

### "ERROR: permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock"

If you installed Docker it with sudo, add your user to the docker group, or give access to any user to use the docker files (note everyone in your machine will be able to use it): `sudo chmod 666 /var/run/docker.sock`

