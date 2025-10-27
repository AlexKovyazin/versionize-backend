## Responsibility
1. Projects
2. Sections

---
# Specific
   Because of using mono repository, for the convenience of local development, 
   the working directory is set to the parent directory of each service. 
   Therefore, if you run particular service in a container, its files wil be located in `/usr/src/<service_name>`, 
   but working directory will be set to `/usr/src`.  
   In this regard, there are some specifics of running commands.

---
## Migrations  
Alembic calls from versionize-backend root:  
revision: `alembic -c projects/alembic.ini revision --autogenerate -m "comment"`  
upgrade: `alembic -c projects/alembic.ini upgrade head`

---
## Tests
Tests should be run with poetry from service directory as:
`cd projects && poetry run pytest`
