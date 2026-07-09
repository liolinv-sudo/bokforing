from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


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

    <p>Här kommer vi att kunna:</p>

    <ul>
        <li>Ladda upp kvitton</li>
        <li>Läsa information från kvitton</li>
        <li>Skapa bokföringsposter</li>
    </ul>

    <p><a href="/">← Tillbaka</a></p>
    """
