import time
from sys import prefix

from fastapi import FastAPI, Request

from app.v1.router import auth, user, sale, cart

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


"""
Configuración personalizada de OpenAPI:
- Sacar los comentarios del siguiente código en el caso de querer que 
para ciertas APIs necesiten el ingreso de Token Bearer luego que la obtenemos del API
'/token' que se ha creado líneas arriba.
"""

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
    # Descomentar la siguiente línea en caso que se quiera aplicar el uso de Token Bearer para todas las APIs
    # Dejar el for y su contenido comentado
    #openapi_schema["security"] = [{"bearerAuth": []}]
    for route in openapi_schema["paths"]:
        if "/all_users" in route:
            openapi_schema["paths"][route]["get"]["security"] = [{"bearerAuth": []}]
        if "/user/{id}" in route:
            openapi_schema["paths"][route]["get"]["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
"""