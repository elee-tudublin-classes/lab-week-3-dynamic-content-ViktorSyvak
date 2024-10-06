# import dependencies
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime # importing the python datetime package


import httpx
from contextlib import asynccontextmanager
import json
from starlette.config import Config

# Load the environment variables from .env
config = Config(".env")



@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient()
    yield
    await app.requests_client.aclose()


# create app instance
app = FastAPI(lifespan=lifespan)

# set location for templates
templates = Jinja2Templates(directory="app/view_templates")


# handle http get requests for the site root /
# return the index.html page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):

    # get current date and time
    serverTime: datetime = datetime.now().strftime("%d/%m/%y %H:%M:%S")

    # note passing of parameters to the page
    return templates.TemplateResponse("index.html", {"request": request,
                                    "serverTime": serverTime})

# handle http get requests for the site 
# return the advice.html page
@app.get("/advice", response_class=HTMLResponse)
async def advice(request: Request):

    # Define a request_client instance
    requests_client = request.app.requests_client

    # Connect to the API URL and await the response
    response = await requests_client.get(config("https://api.nasa.gov/planetary/apod?api_key=")
                        + config("9BSUDPNmDFCoj4HECskPeOqB8EFe1fVuk5aSIqb8"))
    
# Send the json data from the response in the TemplateResponse data parameter 
    return templates.TemplateResponse("advice.html", {"request": request, "data": response.json() })


# handle http get requests for the site 
# return the apod.html page
@app.get("/apod", response_class=HTMLResponse)
async def apod(request: Request):
    return templates.TemplateResponse("apod.html", {"request": request})


# handle http get requests for the site 
# return the params.html page
@app.get("/params", response_class=HTMLResponse)
async def params(request: Request, name : str  | None = ""):
    return templates.TemplateResponse("params.html", {"request": request, "name": name})

# return the dependencies.html page
@app.get("/dependencies", response_class=HTMLResponse)
async def dependencies(request: Request):
    return templates.TemplateResponse("dependencies.html", {"request": request})


#return the nav.html page 
app.get("/nav", response_class=HTMLResponse)
async def nav(request: Request):
    return templates.TemplateResponse("nav.html", {"request": request})



app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)