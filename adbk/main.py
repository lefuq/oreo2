from fastapi import FastAPI
from .database import database
from .roots import abonents, phones, mails

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(abonents.router, prefix='/abonents')
app.include_router(phones.router, prefix='/phones')
app.include_router(mails.router, prefix='/mails')
