import os
from typing import Annotated
import dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.controllers import auth, shifts, users, roles, teams, organizations
from app.custom_exceptions import authorization, notfound, taken
from app.db import engine
from app.models import Base
from fastapi.middleware.cors import CORSMiddleware
from app.utils.ws_connection_manager import ConnectionManager


dotenv.load_dotenv()

# Jos et halua luoda tauluja, ei jätä enviin esim. tyhjä string.
if os.getenv("CREATE_DB_TABLES") == "true":
    # Create tables in the database
    Base.metadata.create_all(bind=engine)


# Create routers
app = FastAPI()
app.include_router(auth.router)
app.include_router(shifts.router)
app.include_router(users.router)
app.include_router(teams.router)
app.include_router(roles.router)
app.include_router(organizations.router)


# Määritellän sallitut originit. Devausvaiheessa periaatteesa sallia kaikki allow_origins['*']
origins = [
    "http://localhost:5173"  # Frontendin origin
    "https://localhost:5173" # Frontendin suojattu yhteys origin
    # Kaikki muut originit
]
# Lisätään originit sallituiden listalle
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins or ["*"] for any origin
    allow_credentials=True,  # Allow cookies and other credentials in requests
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers, or specify certain headers
)


# Custom exceptions handlers
@app.exception_handler(authorization.UnauthorizedAccessException)
async def handle_credentials_exception(request, exception):
    raise HTTPException(detail=str(exception), status_code=401)

@app.exception_handler(authorization.UnauthorizedActionException)
async def handle_credentials_exception(request, exception):
    raise HTTPException(detail=str(exception), status_code=403)

@app.exception_handler(notfound.NotFoundException)
async def handle_credentials_exception(request, exception):
    raise HTTPException(detail=str(exception), status_code=404)

@app.exception_handler(taken.TakenException)
async def handle_credentials_exception(request, exception):
    raise HTTPException(detail=str(exception), status_code=409)


# Websocket realtimeä varten
# Koodit haettu https://fastapi.tiangolo.com/advanced/websockets/#handling-disconnections-and-multiple-clients
# Ja chatgpt
# Websocket toimii /ws endpointissa. Jos halutaan, voidaan lisätä muitakin websocketteja eri endpointtiin,
# tai jopa /{id} kanssa.
manager = ConnectionManager()

@app.websocket("/ws/{org_id}")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast received messages
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# :D
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index():
    return """
        <html>
          <head>
            <style>
              .button {
                background-color: #04AA6D;
                display: block;
                border: none;
                max-width: 500px;
                font-size: 28px;
                text-align: center;
                color: #FFFFFF;
                padding: 20px;
                transition-duration: 0.4s;
                text-decoration: none;
              }
              .button:hover {
                background: #03793D;
              }
            </style>
          </head>
          <body style="align-items: centered">
            <a class="button" href="/docs">Open Fastapi Swagger UI</a>
          </body>
        </html>
    """


def get_app():
    return app

MainApp = Annotated[FastAPI, get_app]