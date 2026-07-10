from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import os
#from sqlalchemy import create_engine, text
from sqlalchemy import (
    create_engine,
    text,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    MetaData
)
from fastapi import Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

metadata = MetaData()

receipts = Table(
    "receipts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("filename", String(255)),
    Column("uploaded_at", DateTime)
)


metadata.create_all(engine)

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

    with engine.begin() as conn:
        conn.execute(
          receipts.insert().values(
            filename=fil.filename
        )
    )
        

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

@app.get("/lista")
def lista():

    with engine.connect() as conn:
        rows = conn.execute(
            receipts.select()
        ).fetchall()

    html = """
    <h1>Kvitton</h1>

    <table border="1" cellpadding="5">
        <tr>
            <th>ID</th>
            <th>Filnamn</th>
            <th>Uppladdad</th>
        </tr>
    """

    for row in rows:
        html += f"""
        <tr>
            <td>{row.id}</td>
            <td>{row.filename}</td>
            <td>{row.uploaded_at}</td>
        </tr>
        """

    html += "</table>"

    return HTMLResponse(html)


@app.get("/upgrade-db")
def upgrade_db():

    with engine.begin() as conn:
        conn.execute(text(
            """
            ALTER TABLE receipts
            ADD COLUMN IF NOT EXISTS uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """
        ))

    return {"status": "ok"}
