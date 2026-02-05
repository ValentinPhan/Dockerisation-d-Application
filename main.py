import logging
import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", None)

# Création de l'app
app = FastAPI(title="FastAPI Upload Demo", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    global storage_client
    try:
        logger.info("Client storage initialisé avec succès")
    except Exception as e:
        logger.error(f"Impossible d'initialiser le client storage: {e}")
        # Ne pas faire planter l'app au démarrage
        storage_client = None


@app.get("/")
def read_root():
    logger.info("Accès à la route /")
    return {"message": "Hello World!", "status": "running"}


@app.get("/upload_from_file", response_class=HTMLResponse)
def upload_from_file():
    logger.info("Accès à la route /upload_from_file")
    return """
    <html>
        <head>
            <title>Upload Image</title>
        </head>
        <body>
            <h1>Uploader une image vers Google Cloud Storage</h1>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept="image/*">
                <input type="submit">
            </form>
        </body>
    </html>
    """


@app.get("/health")
def health_check():
    logger.info("Accès à la route /health")
    return {"status": "healthy"}


@app.get("/users")
def get_users():
    logger.info("Accès à la route /users")
    # Simuler une liste d'utilisateurs
    return [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
    ]


@app.post("/users")
def create_user(user_data: dict):
    logger.info("Accès à la route /users")
    # Simuler la création d'un utilisateur
    return {"message": "User created", "user": user_data}


@app.get("/slow")
def slow_endpoint():
    logger.info("Accès à la route /slow")
    import time

    time.sleep(2)  # Simuler une opération lente
    return {"message": "This was slow!"}


@app.get("/error")
def error_endpoint():
    logger.info("Accès à la route /error")
    raise Exception("This is a test error!")


if __name__ == "__main__":
    import uvicorn

    logger.info("Démarrage de l'application FastAPI")
    uvicorn.run(app, host="0.0.0.0", port=8000)
