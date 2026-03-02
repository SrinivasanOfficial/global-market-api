from fastapi import APIRouter
import common
import requests
from typing import Literal

marketsRouter = APIRouter(tags=["Markets"])

BASE_PATH = "https://finance.yahoo.com/markets/"


def getMarketUrl(urlParam: str):
    url = ""
    match urlParam:
        case "top-gainers":
            url = "gainers/?start=0&count=50"
        case "top-losers":
            url = "losers/?start=0&count=50"
        case _:
            url = urlParam

    return url


@marketsRouter.get("/markets/{url}")
def allStockData(
    url: str,
    sort: str | None = None,
    limit: int | None = None,
    order: Literal["asc", "desc"] = "desc",
):
    fullUrl = f"{BASE_PATH}{getMarketUrl(url)}"
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

        finalResult = result.copy()

        # ✅ Case-insensitive sort
        if sort and result:

            # Convert all keys to lowercase map
            valid_keys = {key.lower(): key for key in finalResult[0].keys()}

            # Convert user input to lowercase
            sort_lower = sort.lower()

            if sort_lower in valid_keys:
                actual_key = valid_keys[sort_lower]

                reverse = True if order == "desc" else False
                finalResult = sorted(
                    finalResult, key=lambda x: x[actual_key], reverse=reverse)

        # ✅ Apply limit if provided
        if limit:
            finalResult = finalResult[:limit]

        return {"success": "true", "message": "Data fetched successfully", "data": finalResult}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@marketsRouter.get("/markets/options/{url}")
def allStockData(
    url: str,
    sort: str | None = None,
    limit: int | None = None,
    order: Literal["asc", "desc"] = "desc",
):
    fullUrl = f"{BASE_PATH}options/{getMarketUrl(url)}"
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
                        row_obj[headers[headerId]] = td.get_text(strip=True)
                        headerId = headerId + 1
                    else:
                        continue

                result.append(row_obj)

        finalResult = result.copy()

        # ✅ Case-insensitive sort
        if sort and result:

            # Convert all keys to lowercase map
            valid_keys = {key.lower(): key for key in finalResult[0].keys()}

            # Convert user input to lowercase
            sort_lower = sort.lower()

            if sort_lower in valid_keys:
                actual_key = valid_keys[sort_lower]

                reverse = True if order == "desc" else False
                finalResult = sorted(
                    finalResult, key=lambda x: x[actual_key], reverse=reverse)

        # ✅ Apply limit if provided
        if limit:
            finalResult = finalResult[:limit]

        return {"success": "true", "message": "Data fetched successfully", "data": finalResult}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
