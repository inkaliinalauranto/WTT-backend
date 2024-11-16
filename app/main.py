import os
import dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.controllers import test, auth, work, users, roles, teams
from app.db import engine
from app.models import Base
from fastapi.middleware.cors import CORSMiddleware


dotenv.load_dotenv()

# Jos et halua luoda tauluja, ei jätä enviin esim. tyhjä string.
if os.getenv("CREATE_DB_TABLES") == "true":
    # Create tables in the database
    Base.metadata.create_all(bind=engine)


# Create routers
app = FastAPI()
app.include_router(test.router)
app.include_router(auth.router)
app.include_router(work.router)
app.include_router(users.router)
app.include_router(teams.router)
app.include_router(roles.router)


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
