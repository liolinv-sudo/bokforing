from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import os
from sqlalchemy import create_engine, text
import os

app = FastAPI()

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Mitt bokföringsprogram</h1>

    <p><a href="/kvitton">Kvitton</a></p>
    <p><a href="#">Verifikationer</a></p>
    <p><a href="#">Kontoplan</a></p>
    <p><a href="#">Rapporter</a></p>
    """


@app.get("/kvitton", response_class=HTMLResponse)
def kvitton():
    return """
    <h1>Kvitton</h1>

    <form action="/ladda-upp" method="post" enctype="multipart/form-data">
        <input type="file" name="fil">
        <button type="submit">Ladda upp</button>
    </form>

    <p><a href="/">← Tillbaka</a></p>
    """


@app.post("/ladda-upp", response_class=HTMLResponse)
async def ladda_upp(fil: UploadFile = File(...)):

    path = os.path.join(UPLOAD_FOLDER, fil.filename)

    with open(path, "wb") as buffer:
        buffer.write(await fil.read())

    return f"""
    <h1>Kvittot är uppladdat</h1>

    <p>Fil: {fil.filename}</p>

    <p><a href="/kvitton">Tillbaka till kvitton</a></p>
    """

@app.get("/dbtest")
def dbtest():

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        value = result.scalar()

    return {"database": "ok", "result": value}
