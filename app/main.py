from fastapi import FastAPI, Depends
from routers import questions, choices, responses
from database.session import SessionLocal, engine
from database import models


models.Base.metadata.create_all(bind=engine)

# Dependency


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


app = FastAPI()


app.include_router(questions.router)
app.include_router(choices.router)
app.include_router(responses.router)


@app.get("/")
def index():
    return {"msg": "Welcome"}
