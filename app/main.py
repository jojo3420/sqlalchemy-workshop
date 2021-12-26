import uvicorn
from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from devtools import debug

# from app import models
# from app import api
from app import database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://localhost",
        " https://0101-49-166-116-160.ap.ngrok.io",
    ],
    allow_credentials=True,
    allow_methods=["OPTION", "GET", "POST", "DELETE"],
    allow_headers={"*"},
)


@app.on_event("startup")
def startup():
    from app.database import engine
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    database.Base.metadata.create_all(bind=engine)


@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return "hello world"


# app.include_router(api.router)

if __name__ == "__main__":
    uvicorn.run("telbot.main:app", reload=True)
