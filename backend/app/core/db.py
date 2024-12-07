import json

import asyncpg
import redis
from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)


class Database:
    def __init__(self):
        self._pool = None

    async def connect(self):
        self._pool = await asyncpg.create_pool(
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            min_size=1, max_size=10, timeout=60)

    async def disconnect(self):
        await self._pool.close()

    async def fetch(self, query: str, *args):
        async with self._pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        async with self._pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def execute(self, query: str, *args):
        async with self._pool.acquire() as connection:
            return await connection.execute(query, *args)


# class RedisDatabase:
#     def __init__(self):
#         self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
#
#     def get_user_token(self, user_id):
#         return self.r.get(f"{user_id}:session")
#
#     def set_user_token(self, user_id, token):
#         return self.r.set(f"{user_id}:session", token)
#
#     def get_top_5_tickers(self):
#         stored_data = self.r.get('funding:top:5:tickets')
#
#         if stored_data:
#             data = stored_data.decode('utf-8')
#             return json.loads(data)
#         return None
#
#     def get_top_5_tickers_by_volume(self):
#         stored_data = self.r.get('funding:top:5:tickets:volume')
#
#         if stored_data:
#             data = stored_data.decode('utf-8')
#             return json.loads(data)
#         return None


database = Database()
# redis_database = RedisDatabase()
