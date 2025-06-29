"""
Drilling calculations API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# Import petrocalc from pip-installed package
try:
    from petrocalc import drilling
except ImportError:
    raise ImportError("petrocalc package not found. Please install it using: pip install petrocalc")

router = APIRouter()


class MudWeightRequest(BaseModel):
    mud_weight: float
    unit: str = "ppg"


class HydrostaticPressureRequest(BaseModel):
    mud_weight: float
    depth: float
    unit: str = "ppg"


class AnnularVelocityRequest(BaseModel):
    flow_rate: float
    hole_diameter: float
    pipe_diameter: float


class PipeVelocityRequest(BaseModel):
    flow_rate: float
    pipe_inner_diameter: float


class ReynoldsNumberRequest(BaseModel):
    velocity: float
    diameter: float
    density: float
    viscosity: float


@router.post("/mud-weight-to-pressure-gradient")
async def mud_weight_to_pressure_gradient(request: MudWeightRequest):
    """Convert mud weight to pressure gradient."""
    try:
        result = drilling.mud_weight_to_pressure_gradient(
            request.mud_weight, 
            request.unit
        )
        return {
            "mud_weight": request.mud_weight,
            "unit": request.unit,
            "pressure_gradient": result,
            "pressure_gradient_unit": "psi/ft"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/hydrostatic-pressure")
async def hydrostatic_pressure(request: HydrostaticPressureRequest):
    """Calculate hydrostatic pressure at depth."""
    try:
        result = drilling.hydrostatic_pressure(
            request.mud_weight,
            request.depth,
            request.unit
        )
        return {
            "mud_weight": request.mud_weight,
            "depth": request.depth,
            "unit": request.unit,
            "hydrostatic_pressure": result,
            "pressure_unit": "psi"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/annular-velocity")
async def annular_velocity(request: AnnularVelocityRequest):
    """Calculate annular velocity."""
    try:
        result = drilling.annular_velocity(
            request.flow_rate,
            request.hole_diameter,
            request.pipe_diameter
        )
        return {
            "flow_rate": request.flow_rate,
            "hole_diameter": request.hole_diameter,
            "pipe_diameter": request.pipe_diameter,
            "annular_velocity": result,
            "velocity_unit": "ft/min"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pipe-velocity")
async def pipe_velocity(request: PipeVelocityRequest):
    """Calculate pipe velocity."""
    try:
        result = drilling.pipe_velocity(
            request.flow_rate,
            request.pipe_inner_diameter
        )
        return {
            "flow_rate": request.flow_rate,
            "pipe_inner_diameter": request.pipe_inner_diameter,
            "pipe_velocity": result,
            "velocity_unit": "ft/min"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reynolds-number")
async def reynolds_number(request: ReynoldsNumberRequest):
    """Calculate Reynolds number."""
    try:
        result = drilling.reynolds_number(
            request.velocity,
            request.diameter,
            request.density,
            request.viscosity
        )
        return {
            "velocity": request.velocity,
            "diameter": request.diameter,
            "density": request.density,
            "viscosity": request.viscosity,
            "reynolds_number": result,
            "unit": "dimensionless"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
