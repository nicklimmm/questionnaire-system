from typing import List, Optional
from database.models import Response

from crud.responses import crud_responses
from database.session import get_db
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from schemas import responses as schema
from sqlalchemy.orm.session import Session

router = APIRouter(prefix="/responses", tags=["responses"])


@router.get("/", response_model=List[schema.Response])
def get_responses(question_id: Optional[int] = None, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud_responses.get_all(db, question_id, user_id)


@router.get("/{id}", response_model=schema.Response)
def get_response(id: int, db: Session = Depends(get_db)):
    db_response = crud_responses.get(db, id)
    if db_response is None:
        raise HTTPException(
            status_code=404,
            detail=f"Response with id of {id} not found"
        )
    return db_response


@router.post("/", response_model=schema.Response)
def add_response(response: schema.ResponseCreate, db: Session = Depends(get_db)):
    db_response = crud_responses.create(db, response)

    if type(db_response) == Response:
        return db_response

    # Invalid creation
    else:
        raise HTTPException(
            status_code=400,
            detail=db_response["msg"]
        )


@router.patch("/{id}", response_model=schema.Response)
def edit_response(id: int, response: schema.ResponseUpdate, db: Session = Depends(get_db)):
    db_response = crud_responses.update(db, id, response)
    if db_response is None:
        raise HTTPException(
            status_code=404,
            detail=f"Response with id of {id} not found"
        )

    elif type(db_response) == Response:
        return db_response

    # Invalid edit
    else:
        raise HTTPException(
            status_code=400,
            detail=db_response["msg"]
        )


@router.delete("/{id}", response_model=schema.Response)
def delete_question(id: int, db: Session = Depends(get_db)):
    db_response = crud_responses.delete(db, id)
    if db_response is None:
        raise HTTPException(
            status_code=404,
            detail=f"Response with id of {id} not found"
        )
    return db_response
