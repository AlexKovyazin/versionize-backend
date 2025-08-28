from documents.src.settings import settings


def get_db_url(sync=False):
    return (
        f"postgresql{'' if sync else '+asyncpg'}://"
        f"{settings.db_username.get_secret_value()}:"
        f"{settings.db_password.get_secret_value()}@"
        f"{settings.db_host.get_secret_value()}:"
        f"{settings.db_port.get_secret_value()}/"
        f"{settings.db_database.get_secret_value()}"
    )
