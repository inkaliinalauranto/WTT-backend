from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.controllers import test
from app.services.db import Base, engine

# Create tables in the database
Base.metadata.create_all(bind=engine)


# Create routers
app = FastAPI()
app.include_router(test.router)


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



