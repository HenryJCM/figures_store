import time
from sys import prefix

from fastapi import FastAPI, Request

from app.v1.router import auth, user, sale, cart, brand, product

# instanciamos la clase FastAPI
app = FastAPI(prefix="api/v1")

@app.get('/')
async def root():
    return {"name": "Figures Store v1"}

@app.middleware('http')
async def add_custom_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-hi-name"] = "Hi, welcome"

    return response

@app.middleware('http')
async def add_process_time_header(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    response.headers["X-process-Time"] = str(process_time)
    print("Tiempo de procedimiento: {}".format(process_time))

    return response

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(cart.router)
app.include_router(sale.router)
app.include_router(brand.router)
app.include_router(product.router)


"""
Configuración personalizada de OpenAPI:
"""

from fastapi.openapi.utils import get_openapi
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="API description",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    openapi_schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi