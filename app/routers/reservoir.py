"""
Reservoir engineering calculations API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# Import petrocalc from pip-installed package
try:
    from petrocalc import reservoir
except ImportError:
    raise ImportError("petrocalc package not found. Please install it using: pip install petrocalc")

router = APIRouter()


class OilFormationVolumeFactorRequest(BaseModel):
    gas_oil_ratio: float
    gas_gravity: float
    oil_gravity: float
    temperature: float
    pressure: float


class SolutionGasOilRatioRequest(BaseModel):
    pressure: float
    temperature: float
    gas_gravity: float
    oil_gravity: float


@router.post("/oil-formation-volume-factor")
async def oil_formation_volume_factor(request: OilFormationVolumeFactorRequest):
    """Calculate oil formation volume factor using Standing's correlation."""
    try:
        result = reservoir.oil_formation_volume_factor_standing(
            request.gas_oil_ratio,
            request.gas_gravity,
            request.oil_gravity,
            request.temperature,
            request.pressure
        )
        return {
            "gas_oil_ratio": request.gas_oil_ratio,
            "gas_gravity": request.gas_gravity,
            "oil_gravity": request.oil_gravity,
            "temperature": request.temperature,
            "pressure": request.pressure,
            "oil_fvf": result,
            "unit": "res bbl/STB"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solution-gas-oil-ratio")
async def solution_gas_oil_ratio(request: SolutionGasOilRatioRequest):
    """Calculate solution gas-oil ratio using Standing's correlation."""
    try:
        result = reservoir.solution_gas_oil_ratio_standing(
            request.pressure,
            request.temperature,
            request.gas_gravity,
            request.oil_gravity
        )
        return {
            "pressure": request.pressure,
            "temperature": request.temperature,
            "gas_gravity": request.gas_gravity,
            "oil_gravity": request.oil_gravity,
            "solution_gor": result,
            "unit": "scf/STB"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
