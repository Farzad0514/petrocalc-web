"""
Fluids calculations API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# Import petrocalc from pip-installed package
try:
    from petrocalc import fluids
except ImportError:
    raise ImportError("petrocalc package not found. Please install it using: pip install petrocalc")

router = APIRouter()


class WaterFormationVolumeFactorRequest(BaseModel):
    temperature: float
    pressure: float
    salinity: float = 0


class WaterCompressibilityRequest(BaseModel):
    temperature: float
    pressure: float
    salinity: float = 0


class GasFormationVolumeFactorRequest(BaseModel):
    temperature: float
    pressure: float
    z_factor: float = 1.0


class WaterViscosityRequest(BaseModel):
    temperature: float
    pressure: float
    salinity: float = 0


@router.post("/water-formation-volume-factor")
async def water_formation_volume_factor(request: WaterFormationVolumeFactorRequest):
    """Calculate water formation volume factor."""
    try:
        result = fluids.water_formation_volume_factor(
            request.temperature,
            request.pressure,
            request.salinity
        )
        return {
            "temperature": request.temperature,
            "pressure": request.pressure,
            "salinity": request.salinity,
            "water_fvf": result,
            "unit": "res bbl/STB"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/water-compressibility")
async def water_compressibility(request: WaterCompressibilityRequest):
    """Calculate water compressibility."""
    try:
        result = fluids.water_compressibility(
            request.temperature,
            request.pressure,
            request.salinity
        )
        return {
            "temperature": request.temperature,
            "pressure": request.pressure,
            "salinity": request.salinity,
            "water_compressibility": result,
            "unit": "1/psi"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/gas-formation-volume-factor")
async def gas_formation_volume_factor(request: GasFormationVolumeFactorRequest):
    """Calculate gas formation volume factor."""
    try:
        result = fluids.gas_formation_volume_factor(
            request.temperature,
            request.pressure,
            request.z_factor
        )
        return {
            "temperature": request.temperature,
            "pressure": request.pressure,
            "z_factor": request.z_factor,
            "gas_fvf": result,
            "unit": "res ft³/scf"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/water-viscosity")
async def water_viscosity(request: WaterViscosityRequest):
    """Calculate water viscosity."""
    try:
        result = fluids.water_viscosity(
            request.temperature,
            request.pressure,
            request.salinity
        )
        return {
            "temperature": request.temperature,
            "pressure": request.pressure,
            "salinity": request.salinity,
            "water_viscosity": result,
            "unit": "cp"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
