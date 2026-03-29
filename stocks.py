from fastapi import APIRouter
import common
import requests
from typing import Literal

stocksRouter = APIRouter(tags=["Stocks"])

BASE_PATH = "https://finance.yahoo.com/markets/"


@stocksRouter.get("/stocks/most-active-old")
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


def getStockUrl(urlParam: str):
    url = ""
    match urlParam:
        case "most-active":
            url = "most-active/?start=0&count=50"
        # case "trending-now":
            # url = "trending/"
        case "top-gainers":
            url = "gainers/?start=0&count=50"
        case "top-losers":
            url = "losers/?start=0&count=50"
        case _:
            url = urlParam + "/?start=0&count=50"

    return url


@stocksRouter.get("/stocks/{url}")
def allStockData(
    url: str,
    sort: str | None = None,
    limit: int | None = None,
    order: Literal["asc", "desc"] = "desc",
):
    fullUrl = f"{BASE_PATH}stocks/{getStockUrl(url)}"
    print(fullUrl)

    try:
        htmlResponse = common.getContentFromUrl(fullUrl)
        divContainer = htmlResponse.find("div", class_="table-container")
        if not divContainer:
            return {"success": "false", "message": "Problem occurred while fetching Data", "data": []}
        tables = htmlResponse.find("table")
        if not tables:
            return {"success": "false", "message": "Problem occurred while fetching Data", "data": []}

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

        for val in result:
            if 'Price' in val:
                priceVal = val['Price']
                val['Price'] = float(priceVal)
            if 'Change' in val:
                priceVal = val['Change']
                val['Change'] = float(priceVal)
            if 'Change %' in val:
                priceVal = val['Change %'].replace("%", "").strip()
                val['Change %'] = float(priceVal)
            if 'Volume' in val:
                priceVal = val['Volume'][:-1]
                val['Volume'] = float(priceVal)
            if 'Market Cap' in val:
                priceVal = val['Market Cap'][:-1]
                val['Market Cap'] = float(priceVal)

        finalResult = result.copy()

        # ✅ Case-insensitive sort
        if sort and result:

            # Convert all keys to lowercase map
            valid_keys = {key.lower(): key for key in finalResult[0].keys()}

            # Convert user input to lowercase
            sort_lower = sort.lower()

            if sort_lower in valid_keys:
                actual_key = valid_keys[sort_lower]
                print('actual_key', actual_key)

                reverse = True if order == "desc" else False
                finalResult = sorted(
                    finalResult, key=lambda x: x[actual_key], reverse=True)

        # ✅ Apply limit if provided
        if limit:
            finalResult = finalResult[:limit]

        return {"success": "true", "message": "Data fetched successfully", "data": finalResult}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
