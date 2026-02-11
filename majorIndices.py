from fastapi import APIRouter
import common
import re

router = APIRouter(tags=["Indices"])


@router.get("/major-indices")
def get_users():
    htmlResponse = common.getContentFromUrl(
        'https://www.investing.com/indices/major-indices')
    tables = htmlResponse.find("table", class_="datatable-v2_table__93S4Y")
    if not tables:
        return {"success": "false", "message": "Problem occurred while fetching Major Indices", "data": []}

    result = []

    # get headers from th
    headers = []
    for th in tables.find_all("th"):
        text = th.get_text(strip=True)
        if text:
            headers.append(text)

    # loop tr and map td with headers
    for tr in tables.find_all("tr"):
        tds = tr.find_all("td")

        if tds:
            row_obj = {}
            headerId = 0
            for i, td in enumerate(tds):
                value = td.get_text(strip=True)
                if value:   # match header safely
                    row_obj[headers[headerId]] = value
                    headerId = headerId + 1
                else:
                    continue

            result.append(row_obj)

    return {"success": "true", "message": "Major indices fetched successfully", "data": result}


@router.get("/country-list")
def getCountryList():
    htmlResponse = common.getContentFromUrl(
        'https://www.investing.com/indices/world-indices')
    countryNamesList = htmlResponse.find(
        "select", class_="js-indice-country-filter")
    if not countryNamesList:
        return {"success": "false", "message": "Problem occurred while fetching Country List", "data": []}

    result = []
    for id, opt in enumerate(countryNamesList.find_all("option")):
        if id > 0 and opt:
            value = opt.get("value")      # get value attribute
            text = opt.get_text(strip=True)
            result.append({"name": text, "url": value})
    return result


@router.get("/countrywise-indices")
def worldIndices(url: str):
    getUrl = f"https://www.investing.com{url}?include-major-indices=true&include-additional-indices=true&include-primary-sectors=true&include-other-indices=true"
    htmlResponse = common.getContentFromUrl(getUrl)
    tables = htmlResponse.find("table", class_="datatable-v2_table__93S4Y")
    if not tables:
        return {"success": "false", "message": "Problem occurred while fetching Major Indices", "data": []}

    result = []

    # get headers from th
    headers = []
    for th in tables.find_all("th"):
        text = th.get_text(strip=True)
        if text:
            headers.append(text)

    # loop tr and map td with headers
    for tr in tables.find_all("tr"):
        tds = tr.find_all("td")

        if tds:
            row_obj = {}
            headerId = 0
            for i, td in enumerate(tds):
                value = td.get_text(strip=True)
                if value:   # match header safely
                    row_obj[headers[headerId]] = value
                    headerId = headerId + 1
                else:
                    continue

            result.append(row_obj)

    return {"success": "true", "message": "Major indices Countrywise fetched successfully", "data": result}


@router.get("/global-indices")
def globalIndices():
    htmlResponse = common.getContentFromUrl(
        'https://www.investing.com/indices/global-indices')
    tables = htmlResponse.find("table", class_="closedTbl")
    if not tables:
        return {"success": "false", "message": "Problem occurred while fetching Global Major Indices", "data": []}

    result = []

    # get headers from th
    headers = []
    for th in tables.find_all("th"):
        text = th.get_text(strip=True)
        if text:
            headers.append(text)

    # loop tr and map td with headers
    for tr in tables.find_all("tr"):
        tds = tr.find_all("td")

        if tds:
            row_obj = {}
            headerId = 0
            for i, td in enumerate(tds):
                value = td.get_text(strip=True)
                if value:   # match header safely
                    row_obj[headers[headerId]] = value
                    headerId = headerId + 1
                else:
                    continue

            result.append(row_obj)

    return {"success": "true", "message": "Major indices fetched successfully", "data": result}


@router.get("/majorindices_bk")
def get_users():
    htmlResponse = common.getContentFromUrl(
        'https://www.investing.com/indices/major-indices')
    tables = htmlResponse.find("table")
    if not tables:
        return {"error": "No tables found with id='test'"}

    result = []
    headers = [th.get_text(strip=True) for th in tables.find_all("th")]

    for idx, table in enumerate(tables):
        rows = []

        for tr in table.find_all("tr")[1:]:
            cells = tr.find_all("td")

            row = {}

            for i, cell in enumerate(cells):
                key = headers[i] if i < len(headers) else f"col_{i}"
                if key:
                    b_tag = cell.find("span")
                    row[key] = (
                        b_tag.get_text(
                            strip=True) if b_tag else cell.get_text(strip=True)
                    )

            rows.append(row)
            if rows:
                result.append(
                    {"table_index": idx, "table_id": "test", "data": rows})

    return result
