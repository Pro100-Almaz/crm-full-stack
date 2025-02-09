import aio_pika
import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.core.db import database


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

RABBITMQ_URL = f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@localhost/"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    print("I have all cors origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins= ["*"], #settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup():
    await database.connect()

    # app.state.rabbit_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    # app.state.rabbit_channel = await app.state.rabbit_connection.channel()
    # await app.state.rabbit_channel.declare_queue("my_queue", durable=True)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
