from fastapi import FastAPI

from src.routes import phones,users,emails

app = FastAPI()

app.include_router(users.router, prefix='/api')
app.include_router(emails.router,prefix='/api')
app.include_router(phones.router,prefix='/api')


@app.get('/')
def read_root():
    return {'Message':"it's ok!!!"}


