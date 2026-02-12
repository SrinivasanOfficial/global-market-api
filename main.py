from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi.responses import HTMLResponse
from bs4 import BeautifulSoup

from majorIndices import router as indices_routes


app = FastAPI()


app = FastAPI()

# ✅ Allow your frontend domains (Render frontend URL, localhost, etc.)
origins = [
    "http://localhost:5173",   # React/Vite local
    "http://localhost:4200",   # Angular local
    "http://127.0.0.1:5173",
    "http://127.0.0.1:4200",
    "https://global-market-api.onrender.com/"  # Render deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # You can also use ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(indices_routes)


@app.get("/")
def home():
    return "welcome to Home page"


@app.get("/displayPage")
def displayPage():
    url = "https://www.investing.com/indices/world-indices"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    return HTMLResponse(content=f"<pre>{response.text}</pre>")


@app.get("/geturl")
def getUrl():
    url = "https://tradingeconomics.com/commodities"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table", class_="table-striped")

    if not tables:
        return {"error": "No tables found with id='test'"}

    result = []

    for idx, table in enumerate(tables):
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        rows = []

        for tr in table.find_all("tr")[1:]:
            cells = tr.find_all("td")

            row = {}

            for i, cell in enumerate(cells):
                key = headers[i] if i < len(headers) else f"col_{i}"
                b_tag = cell.find("b")
                row[key] = (
                    b_tag.get_text(
                        strip=True) if b_tag else cell.get_text(strip=True)
                )

            rows.append(row)

        result.append({"table_index": idx, "table_id": "test", "rows": rows})

    return result
