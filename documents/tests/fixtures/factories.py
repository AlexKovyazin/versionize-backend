import uuid


def create_document_in_data(**overrides):
    """Factory for DocumentIn test data."""

    defaults = {
        "name": "Test Document",  # TODO use Faker for doc names
        "note": "Test note",
        "company_id": str(uuid.uuid4()),
        "project_id": str(uuid.uuid4()),
        "section_id": str(uuid.uuid4()),
        "responsible_id": str(uuid.uuid4()),
    }
    defaults.update(overrides)
    return defaults
