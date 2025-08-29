import uuid

from documents.src.domain.schemas.document import DocumentIn
from documents.tests.fixtures.factories import create_document_in_data


# TODO rewrite to make it pure unit test
async def test_document_service_create(fake_documents_service):
    """ Test creating a document through documents service. """

    section_id = uuid.uuid4()
    first_variation_data = create_document_in_data(
        name="Document of a specific section",
        note="First variation",
        section_id=section_id
    )
    second_variation_data = create_document_in_data(
        name="Document of a specific section",
        note="Second variation",
        section_id=section_id
    )
    first_document = await fake_documents_service.create(
        DocumentIn(**first_variation_data)
    )
    second_document = await fake_documents_service.create(
        DocumentIn(**second_variation_data)
    )

    assert first_document.md5 is not None
    assert first_document.version == 0
    assert first_document.variation == 1
    assert second_document.md5 is not None
    assert second_document.version == 1
    assert second_document.variation == 2