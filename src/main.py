from redis import asyncio as aioredis
from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers
from fastapi.staticfiles import StaticFiles
from src.chat.router import router as chat_router
from src.auth.models import User
from .operations.router import router as router_operation
from .tasks.router import router as send_mail_router
from fastapi.middleware.cors import CORSMiddleware
from .auth.base_config import auth_backend, current_user
from .auth.manager import get_user_manager
from .auth.schemas import UserRead, UserCreate
from .page.router import router as template_router

app = FastAPI(
    title='Trading app'
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get('/protected_route')
def protected_route(user: User = Depends(current_user)):
    return f'Hello {user.email}'


app.include_router(router_operation)
app.include_router(send_mail_router)
app.include_router(template_router)
app.include_router(chat_router)


@app.get('/unprotected_route')
def unprotected_route():
    return 'Hello anonymous'


origins = [
    "http://127.0.0.1:8000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"], )


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
