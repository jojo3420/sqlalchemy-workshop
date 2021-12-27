import uvicorn
from fastapi import FastAPI, status, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from devtools import debug
from sqlalchemy.orm import Session

from app import models
from app import database

# from app import api
# from sqlalchemy import or_, and_


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["OPTION", "GET", "POST", "DELETE"],
    allow_headers={"*"},
)


@app.on_event("startup")
def startup():
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    models.Base.metadata.create_all(bind=database.engine)


@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {'msg': "hello world"}


@app.get('/users')
def read_users(conn: Session = Depends(database.get_conn)):
    debug('/users')
    return conn.query(models.User).all()


# app.include_router(api.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
