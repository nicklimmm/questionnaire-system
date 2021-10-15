from fastapi import FastAPI
from routers import questions, users, choices, responses
from database.session import engine
from database import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(questions.router)
app.include_router(users.router)
app.include_router(choices.router)
app.include_router(responses.router)


@app.get("/")
def index():
    return {"msg": "Welcome"}
