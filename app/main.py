# import dependencies
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# create app instance
app = FastAPI()

# set location for templates
templates = Jinja2Templates(directory="app/view_templates")

# handle http get requests for the site root /
# return the index.html page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

    # get current date and time
    serverTime: datetime = datetime.now().strftime("%d/%m/%y %H:%M:%S")

# handle http get requests for the site 
# return the advice.html page
@app.get("/advice", response_class=HTMLResponse)
async def advice(request: Request):
    return templates.TemplateResponse("advice.html", {"request": request})

# handle http get requests for the site 
# return the apod.html page
@app.get("/apod", response_class=HTMLResponse)
async def apod(request: Request):
    return templates.TemplateResponse("apod.html", {"request": request})


# handle http get requests for the site 
# return the params.html page
@app.get("/params", response_class=HTMLResponse)
async def params(request: Request):
    return templates.TemplateResponse("params.html", {"request": request})

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