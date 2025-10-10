## Responsibility
1. Users, Companies, Projects, Sections
2. Links users with companies
3. Auth
4. Permissions

---
## Migrations  
revision: alembic -c identity/alembic.ini revision --autogenerate -m "comment"
upgrade: alembic -c identity/alembic.ini upgrade head
