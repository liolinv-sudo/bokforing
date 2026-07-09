from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Mitt bokföringsprogram</h1>

    <p>
    <a href="#">Kvitton</a>
    </p>

    <p>
    <a href="#">Verifikationer</a>
    </p>

    <p>
    <a href="#">Kontoplan</a>
    </p>

    <p>
    <a href="#">Rapporter</a>
    </p>
    """
