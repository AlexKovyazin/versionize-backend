## Responsibility
1. Users, Companies, Projects, Sections
2. Links users with companies
3. Auth
4. Permissions

---
# Specific
   Because of using mono repository, for the convenience of local development, 
   the working directory is set to the parent directory of each service. 
   Therefore, if you run particular service in a container, its files wil be located in `/usr/src/<service_name>`, 
   but working directory will be set to `/usr/src`.  
   In this regard, there are some specifics of running commands.

---
## Migrations  
revision: `alembic -c identity/alembic.ini revision --autogenerate -m "comment"`  
upgrade: `alembic -c identity/alembic.ini upgrade head`

---
## Tests
Tests should be run with poetry from service directory as:
`cd identity && poetry run pytest`
