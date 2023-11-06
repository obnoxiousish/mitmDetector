import uvicorn

from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from hashlib import sha256

templates = Jinja2Templates(directory="templates")


async def buildHash():
    newHash = sha256()
    newHash.update(b"127.0.0.1:8000") # This has to be your websites domain!
    return newHash.hexdigest()


async def compareHash(submittedHash, expectedHash):
    if submittedHash == expectedHash:
        return True


async def homepage(request):
    return templates.TemplateResponse("index.html", {"request": request})


async def detectMITM(request):
    returnJson = {
        "message": None,
        "isMitm": None,
    }

    requestJson = await request.json()

    expectedHash = await buildHash()
    submittedHash = requestJson["hostHash"]

    print(f'Comparing: {submittedHash} to {expectedHash}')

    if await compareHash(submittedHash=submittedHash, expectedHash=expectedHash):
        returnJson["message"] = "not a MITM"
        returnJson["isMitm"] = False
    else:
        returnJson["message"] = "a MITM"
        returnJson["isMitm"] = True

    return JSONResponse(returnJson)


routes = [
    Route("/", endpoint=homepage, methods=["GET"]),
    Route("/detectMITM", endpoint=detectMITM, methods=["POST"]),
    Mount("/static", StaticFiles(directory="static"), name="static"),
]

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
