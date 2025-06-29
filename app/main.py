"""
PetroCalc Web Application

A modern web interface for petroleum engineering calculations.
Built with FastAPI and modern frontend technologies.

Supports both pip-installed and local petrocalc packages.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

from app.config import get_config
from app.routers import drilling, fluids, reservoir, production, economics, completion, flow, pressure, rock_properties, thermodynamics

# Get configuration
config = get_config()

# Create FastAPI app
app = FastAPI(
    title="PetroCalc Web",
    description="A comprehensive web application for petroleum engineering calculations",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Include routers only if petrocalc is available
if config.is_petrocalc_available():
    app.include_router(drilling.router, prefix="/api/drilling", tags=["drilling"])
    app.include_router(fluids.router, prefix="/api/fluids", tags=["fluids"])
    app.include_router(reservoir.router, prefix="/api/reservoir", tags=["reservoir"])
    app.include_router(production.router, prefix="/api/production", tags=["production"])
    app.include_router(economics.router, prefix="/api/economics", tags=["economics"])
    app.include_router(completion.router, prefix="/api/completion", tags=["completion"])
    app.include_router(flow.router, prefix="/api/flow", tags=["flow"])
    app.include_router(pressure.router, prefix="/api/pressure", tags=["pressure"])
    app.include_router(rock_properties.router, prefix="/api/rock_properties", tags=["rock_properties"])
    app.include_router(thermodynamics.router, prefix="/api/thermodynamics", tags=["thermodynamics"])
else:
    print("⚠️  API endpoints disabled - petrocalc not available")
    print(config.get_import_instructions())


@app.get("/api/status")
async def get_status():
    """Get application and petrocalc status."""
    return JSONResponse(content={
        "app_status": "running",
        "petrocalc_available": config.is_petrocalc_available(),
        "config": config.get_status_info(),
        "installation_instructions": config.get_import_instructions() if not config.is_petrocalc_available() else None
    })


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with navigation to different calculation modules."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "petrocalc_available": config.is_petrocalc_available(),
        "config_info": config.get_status_info()
    })


@app.get("/drilling", response_class=HTMLResponse)
async def drilling_page(request: Request):
    """Drilling calculations page."""
    return templates.TemplateResponse("drilling.html", {"request": request})


@app.get("/fluids", response_class=HTMLResponse)
async def fluids_page(request: Request):
    """Fluid properties page."""
    return templates.TemplateResponse("fluids.html", {"request": request})


@app.get("/reservoir", response_class=HTMLResponse)
async def reservoir_page(request: Request):
    """Reservoir engineering page."""
    return templates.TemplateResponse("reservoir.html", {"request": request})


@app.get("/production", response_class=HTMLResponse)
async def production_page(request: Request):
    """Production engineering page."""
    return templates.TemplateResponse("production.html", {"request": request})


@app.get("/economics", response_class=HTMLResponse)
async def economics_page(request: Request):
    """Economics calculations page."""
    return templates.TemplateResponse("economics.html", {"request": request})


@app.get("/completion", response_class=HTMLResponse)
async def completion_page(request: Request):
    """Completion engineering page."""
    return templates.TemplateResponse("completion.html", {"request": request})


@app.get("/flow", response_class=HTMLResponse)
async def flow_page(request: Request):
    """Flow calculations page."""
    return templates.TemplateResponse("flow.html", {"request": request})


@app.get("/pressure", response_class=HTMLResponse)
async def pressure_page(request: Request):
    """Pressure calculations page."""
    return templates.TemplateResponse("pressure.html", {"request": request})


@app.get("/rock_properties", response_class=HTMLResponse)
async def rock_properties_page(request: Request):
    """Rock properties page."""
    return templates.TemplateResponse("rock_properties.html", {"request": request})


@app.get("/thermodynamics", response_class=HTMLResponse)
async def thermodynamics_page(request: Request):
    """Thermodynamics calculations page."""
    return templates.TemplateResponse("thermodynamics.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
