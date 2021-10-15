# Questionnaire System REST API

A questionnaire system to manage and collect responses from users. Allows basic CRUD interactions, allowing users to answer each question, view the questions that they have answered, and edit their answers even after submitting them.

## Tools Used

- FastAPI
- SQLite3
- pytest

## Prerequisites

1. Python >= 3.8.10, pip >= 20.0.2
1. Install dependencies by running `pip install requirements.txt` in terminal

## Run API

Run the code below in terminal

```bash
cd app
uvicorn main:app --reload --host '0.0.0.0' --port 8000
```

## Documentation

Documentation is available at [0.0.0.0:8000/docs](0.0.0.0:8000/docs) (API must be running beforehand)

## Run tests

```bash
cd app
python -m pytest
```

## Assumptions

- A user can answer the same question more than once
- Questions and choices cannot be modified after creation
- Only 3 question types are available: textbox, checkbox, and radio
