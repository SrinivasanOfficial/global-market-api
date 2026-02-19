from fastapi import APIRouter
import common

stocksRouter = APIRouter(tags=["Stocks"])

BASE_PATH = "https://finance.yahoo.com/markets/"


@stocksRouter.get("/stocks/most-active")
def stocksMostActive():
    htmlResponse = common.getContentFromUrl(f"{BASE_PATH}stocks/most-active/")
    divContainer = htmlResponse.find("div", class_="table-container")
    if not divContainer:
        return {"success": "false", "message": "Problem occurred while fetching Stocks Most Active", "data": []}
    tables = htmlResponse.find("table")
    if not tables:
        return {"success": "false", "message": "Problem occurred while fetching Stocks Most Active", "data": []}

    result = []

    # get headers from th
    headers = []
    for th in tables.find_all("th"):
        text = th.get_text(strip=True)
        if text:
            headers.append(text)
    print("headers", headers)

    # loop tr and map td with headers
    for tr in tables.find_all("tr"):
        tds = tr.find_all("td")

        if tds:
            row_obj = {}
            headerId = 0
            for i, td in enumerate(tds):
                value = td.get_text(strip=True)
                if value:   # match header safely
                    row_obj[headers[headerId]] = td.find(
                        "span").get_text(strip=True) if i == 3 else value
                    headerId = headerId + 1
                else:
                    continue

            result.append(row_obj)

    return {"success": "true", "message": "Most Active Stocks fetched successfully", "data": result}


@stocksRouter.get("/stocks/trending")
def stocksTrending():
    htmlResponse = common.getContentFromUrl(f"{BASE_PATH}stocks/trending/")
    tables = htmlResponse.find("table", class_="yf-1w0dr5b bd")
    if not tables:
        return {"success": "false", "message": "Problem occurred while fetching Stocks Most Active", "data": []}

    result = []

    # get headers from th
    headers = []
    for th in tables.find_all("th"):
        text = th.get_text(strip=True)
        if text:
            headers.append(text)
    print("headers", headers)

    # loop tr and map td with headers
    for tr in tables.find_all("tr"):
        tds = tr.find_all("td")

        if tds:
            row_obj = {}
            headerId = 0
            for i, td in enumerate(tds):
                value = td.get_text(strip=True)
                if value:   # match header safely
                    row_obj[headers[headerId]] = td.find(
                        "span").get_text(strip=True) if i == 3 else value
                    # row_obj[headers[headerId]] = value
                    headerId = headerId + 1
                else:
                    continue

            result.append(row_obj)

    return {"success": "true", "message": "Trending Now Stocks fetched successfully", "data": result}


@stocksRouter.get("/stocks/top-gainers")
def stocksTrending():
    htmlResponse = common.getContentFromUrl(f"{BASE_PATH}stocks/gainers/")
    tables = htmlResponse.find("table", class_="yf-1w0dr5b bd")
    if not tables:
        return {"success": "false", "message": "Problem occurred while fetching Stocks Top Gainers", "data": []}

    result = []

    # get headers from th
    headers = []
    for th in tables.find_all("th"):
        text = th.get_text(strip=True)
        if text:
            headers.append(text)
    print("headers", headers)

    # loop tr and map td with headers
    for tr in tables.find_all("tr"):
        tds = tr.find_all("td")

        if tds:
            row_obj = {}
            headerId = 0
            for i, td in enumerate(tds):
                value = td.get_text(strip=True)
                if value:   # match header safely
                    row_obj[headers[headerId]] = td.find(
                        "span").get_text(strip=True) if i == 3 else value
                    # row_obj[headers[headerId]] = value
                    headerId = headerId + 1
                else:
                    continue

            result.append(row_obj)

    return {"success": "true", "message": "Top Gainers Stocks fetched successfully", "data": result}
