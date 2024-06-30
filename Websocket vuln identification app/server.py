from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    response = templates.TemplateResponse("index.html", {"request": request})
    #response.set_cookie(key="PHPSESSID", value="446c748a552c7777d2e9e81a9756c154", samesite='none', secure=True)
    return response
