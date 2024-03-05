from fastapi import FastAPI
from user import api as UserAPI
from tortoise.contrib.fastapi import register_tortoise



app = FastAPI()
app.include_router(UserAPI.app,tags=["API"])






register_tortoise(
    app,
    db_url="postgres://postgres:12345@127.0.0.1/crudinfastapi",
    modules={'models':['user.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)