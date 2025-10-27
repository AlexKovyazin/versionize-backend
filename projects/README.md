## Responsibility
1. Projects
2. Sections

---
## Migrations  
Alembic calls from versionize-backend root:  
revision: `alembic -c projects/alembic.ini revision --autogenerate -m "comment"`  
upgrade: `alembic -c projects/alembic.ini upgrade head`
