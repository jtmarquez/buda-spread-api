from fastapi.openapi.utils import get_openapi


def generate_openapi_schema(routes):
    return get_openapi(
        title="Buda Spread API",
        version="0.1.0",
        description="An API for monitoring spreads in the Buda exchange platform",
        routes=routes,
    )
