import uuid

from src.domain.document import DocumentIn
from tests.fixtures.factories import create_document_in_data


async def test_document_creation(fake_documents_service):
    """
    Test creating single document.

    Checking that all manually set attributes are correct.
    """

    name = "Test Document"
    note = "Test note"
    company_id = uuid.uuid4()
    project_id = uuid.uuid4()
    section_id = uuid.uuid4()
    responsible_id = uuid.uuid4()

    data = create_document_in_data(
        name=name,
        note=note,
        company_id=company_id,
        project_id=project_id,
        section_id=section_id,
        responsible_id=responsible_id
    )

    document = await fake_documents_service.create(
        DocumentIn(**data),
        file_content=b"test",
    )

    # check attrs that was set manually
    assert document.name == name
    assert document.note == note
    assert document.company_id == company_id
    assert document.project_id == project_id
    assert document.section_id == section_id
    assert document.responsible_id == responsible_id

    # check generated values
    assert document.md5 is not None
    assert document.version == 1
    assert document.variation == 0


async def test_document_versions(fake_documents_service):
    """
    Test documents versionizing.

    Creating multiple documents of the same section without raise_variation flag.
    """

    section_id = uuid.uuid4()
    first_variation_data = create_document_in_data(
        name="Document of a specific section",
        note="First version, zero variation",
        section_id=section_id
    )
    second_variation_data = create_document_in_data(
        name="Document of a specific section",
        note="Second version, zero variation",
        section_id=section_id
    )

    first_document = await fake_documents_service.create(
        DocumentIn(**first_variation_data),
        raise_variation=False,
        file_content=b"test1",
    )
    second_document = await fake_documents_service.create(
        DocumentIn(**second_variation_data),
        raise_variation=False,
        file_content=b"test2",
    )

    assert first_document.version == 1
    assert first_document.variation == 0
    assert second_document.version == 2
    assert second_document.variation == 0


async def test_document_variations(fake_documents_service):
    """
    Test documents variations.

    Creating multiple documents of the same section with raise_variation flag.
    """

    section_id = uuid.uuid4()
    first_variation_data = create_document_in_data(
        name="Document of a specific section",
        note="First variation, zero variation",
        section_id=section_id
    )
    second_variation_data = create_document_in_data(
        name="Document of a specific section",
        note="Second variation, first variation",
        section_id=section_id
    )

    first_document = await fake_documents_service.create(
        DocumentIn(**first_variation_data),
        raise_variation=True,
        file_content=b"test1",
    )
    second_document = await fake_documents_service.create(
        DocumentIn(**second_variation_data),
        raise_variation=True,
        file_content=b"test2",
    )

    assert first_document.version == 1
    assert first_document.variation == 0
    assert second_document.version == 2
    assert second_document.variation == 1
