from fastapi import APIRouter

from documents.src.adapters.db.session import Session
from documents.src.adapters.db.orm import OrmDocument
from documents.src.domain.schemas.document import DocumentIn, DocumentOut

router = APIRouter(tags=["Documents"])


@router.post("", status_code=201)
def create_document(data: DocumentIn):
    with Session() as session:
        db_document = OrmDocument(**data.model_dump())
        session.add(db_document)
        session.commit()
        session.refresh(db_document)

    return DocumentOut.model_validate(db_document)
