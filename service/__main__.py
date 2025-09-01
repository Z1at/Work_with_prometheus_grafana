from fastapi import FastAPI, Request
from uvicorn import run
from endpoints import list_of_routes
from configs import *
from utils import get_hostname
from dotenv import load_dotenv

from prometheus_client import Counter, generate_latest
from fastapi.responses import Response


def bind_routes(application: FastAPI, settings: DefaultSettings) -> None:
    """
    Bind all routes to application
    """

    for route in list_of_routes:
        application.include_router(route, prefix=settings.PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Create an application and dependable objects
    """

    description = "Микросервис, который позволяет выполнять работу с таблицой из базы данных"

    tags_metadata = [
        {
            "name": "Fastapi application",
            "description": "Work with Postgres via fastapi application"
        }
    ]

    application = FastAPI(
        description=description,
        docs_url="/fastapi_swagger",
        openapi_url="/fastapi_openapi",
        version="1.0.0",
        openapi_tags=tags_metadata
    )
    settings = get_settings()
    bind_routes(application, settings)
    application.state.settings = settings
    return application


app = get_app()

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status_code']
)


@app.middleware("http")
async def collect_metrics(request: Request, call_next):
    method = request.method
    endpoint = request.url.path

    try:
        response = await call_next(request)
        status_code = str(response.status_code)

        # Записываем метрики
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=status_code).inc()

        return response

    except Exception as e:
        # Обрабатываем ошибки
        status_code = "500"
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
        raise


@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )


if __name__ == "__main__":
    load_dotenv()
    settings_for_application = get_settings()
    run(
        "__main__:app",
        host=get_hostname(settings_for_application.APP_HOST),
        port=settings_for_application.APP_PORT,
    )
