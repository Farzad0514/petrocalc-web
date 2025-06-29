"""
Pressure calculations and analysis API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Import petrocalc from pip-installed package
try:
    from petrocalc import pressure
except ImportError:
    raise ImportError("petrocalc package not found. Please install it using: pip install petrocalc")

router = APIRouter()


# Request Models
class FormationPressureGradientRequest(BaseModel):
    formation_water_density: float
    salinity: float = 100000
    temperature: float = 150


class OverburdenPressureGradientRequest(BaseModel):
    depth: float
    surface_density: float = 18.0


class FracturePressureGradientRequest(BaseModel):
    overburden_gradient: float
    pore_pressure_gradient: float
    poisson_ratio: float = 0.25


class EquivalentMudWeightRequest(BaseModel):
    pressure: float
    depth: float


class KickToleranceRequest(BaseModel):
    casing_shoe_depth: float
    formation_pressure: float
    fracture_pressure: float
    current_mud_weight: float


class KillMudWeightRequest(BaseModel):
    original_mud_weight: float
    shut_in_drillpipe_pressure: float
    true_vertical_depth: float


class InitialCirculatingPressureRequest(BaseModel):
    shut_in_drillpipe_pressure: float
    slow_pump_rate_pressure: float


class FinalCirculatingPressureRequest(BaseModel):
    slow_pump_rate_pressure: float
    original_mud_weight: float
    kill_mud_weight: float


class MaxAllowableAnnularSurfacePressureRequest(BaseModel):
    fracture_pressure: float
    mud_weight: float
    shoe_depth: float


class PitGainCalculationRequest(BaseModel):
    kick_volume: float
    formation_gas_gradient: float = 0.1
    mud_gradient: float = 0.45


class PumpPressureScheduleRequest(BaseModel):
    initial_circulating_pressure: float
    final_circulating_pressure: float
    total_pump_strokes: float
    current_stroke: float


class LostCirculationPressureRequest(BaseModel):
    formation_pressure: float
    hydrostatic_pressure: float
    safety_margin: float = 50


# API Endpoints
@router.post("/formation_pressure_gradient")
async def calculate_formation_pressure_gradient(request: FormationPressureGradientRequest):
    """Calculate formation pressure gradient."""
    try:
        result = pressure.formation_pressure_gradient(
            request.formation_water_density,
            request.salinity,
            request.temperature
        )
        return {
            "pressure_gradient_psi_per_ft": result,
            "formation_water_density_lb_per_ft3": request.formation_water_density,
            "salinity_ppm": request.salinity,
            "temperature_fahrenheit": request.temperature
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/overburden_pressure_gradient")
async def calculate_overburden_pressure_gradient(request: OverburdenPressureGradientRequest):
    """Calculate overburden pressure gradient."""
    try:
        result = pressure.overburden_pressure_gradient(
            request.depth,
            request.surface_density
        )
        return {
            "overburden_gradient_psi_per_ft": result,
            "depth_ft": request.depth,
            "surface_density_lb_per_ft3": request.surface_density
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/fracture_pressure_gradient")
async def calculate_fracture_pressure_gradient(request: FracturePressureGradientRequest):
    """Calculate fracture pressure gradient using Eaton's method."""
    try:
        result = pressure.fracture_pressure_gradient(
            request.overburden_gradient,
            request.pore_pressure_gradient,
            request.poisson_ratio
        )
        return {
            "fracture_gradient_psi_per_ft": result,
            "overburden_gradient_psi_per_ft": request.overburden_gradient,
            "pore_pressure_gradient_psi_per_ft": request.pore_pressure_gradient,
            "poisson_ratio": request.poisson_ratio
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/equivalent_mud_weight")
async def calculate_equivalent_mud_weight(request: EquivalentMudWeightRequest):
    """Calculate equivalent mud weight from pressure and depth."""
    try:
        result = pressure.equivalent_mud_weight(
            request.pressure,
            request.depth
        )
        return {
            "equivalent_mud_weight_ppg": result,
            "pressure_psi": request.pressure,
            "depth_ft": request.depth
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/kick_tolerance")
async def calculate_kick_tolerance(request: KickToleranceRequest):
    """Calculate kick tolerance for well control."""
    try:
        result = pressure.kick_tolerance(
            request.casing_shoe_depth,
            request.formation_pressure,
            request.fracture_pressure,
            request.current_mud_weight
        )
        return {
            "kick_tolerance_ppg": result,
            "casing_shoe_depth_ft": request.casing_shoe_depth,
            "formation_pressure_psi": request.formation_pressure,
            "fracture_pressure_psi": request.fracture_pressure,
            "current_mud_weight_ppg": request.current_mud_weight
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/kill_mud_weight")
async def calculate_kill_mud_weight(request: KillMudWeightRequest):
    """Calculate kill mud weight for well control."""
    try:
        result = pressure.kill_mud_weight(
            request.original_mud_weight,
            request.shut_in_drillpipe_pressure,
            request.true_vertical_depth
        )
        return {
            "kill_mud_weight_ppg": result,
            "original_mud_weight_ppg": request.original_mud_weight,
            "shut_in_drillpipe_pressure_psi": request.shut_in_drillpipe_pressure,
            "true_vertical_depth_ft": request.true_vertical_depth
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/initial_circulating_pressure")
async def calculate_initial_circulating_pressure(request: InitialCirculatingPressureRequest):
    """Calculate initial circulating pressure for well control."""
    try:
        result = pressure.initial_circulating_pressure(
            request.shut_in_drillpipe_pressure,
            request.slow_pump_rate_pressure
        )
        return {
            "initial_circulating_pressure_psi": result,
            "shut_in_drillpipe_pressure_psi": request.shut_in_drillpipe_pressure,
            "slow_pump_rate_pressure_psi": request.slow_pump_rate_pressure
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/final_circulating_pressure")
async def calculate_final_circulating_pressure(request: FinalCirculatingPressureRequest):
    """Calculate final circulating pressure for well control."""
    try:
        result = pressure.final_circulating_pressure(
            request.slow_pump_rate_pressure,
            request.original_mud_weight,
            request.kill_mud_weight
        )
        return {
            "final_circulating_pressure_psi": result,
            "slow_pump_rate_pressure_psi": request.slow_pump_rate_pressure,
            "original_mud_weight_ppg": request.original_mud_weight,
            "kill_mud_weight_ppg": request.kill_mud_weight
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/maximum_allowable_annular_surface_pressure")
async def calculate_maximum_allowable_annular_surface_pressure(request: MaxAllowableAnnularSurfacePressureRequest):
    """Calculate maximum allowable annular surface pressure."""
    try:
        result = pressure.maximum_allowable_annular_surface_pressure(
            request.fracture_pressure,
            request.mud_weight,
            request.shoe_depth
        )
        return {
            "maasp_psi": result,
            "fracture_pressure_psi": request.fracture_pressure,
            "mud_weight_ppg": request.mud_weight,
            "shoe_depth_ft": request.shoe_depth
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pit_gain_calculation")
async def calculate_pit_gain(request: PitGainCalculationRequest):
    """Calculate pit gain during gas kick migration."""
    try:
        result = pressure.pit_gain_calculation(
            request.kick_volume,
            request.formation_gas_gradient,
            request.mud_gradient
        )
        return {
            "pit_gain_bbls": result,
            "kick_volume_bbls": request.kick_volume,
            "formation_gas_gradient_psi_per_ft": request.formation_gas_gradient,
            "mud_gradient_psi_per_ft": request.mud_gradient
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pump_pressure_schedule")
async def calculate_pump_pressure_schedule(request: PumpPressureScheduleRequest):
    """Calculate pump pressure for kill operation."""
    try:
        result = pressure.pump_pressure_schedule(
            request.initial_circulating_pressure,
            request.final_circulating_pressure,
            request.total_pump_strokes,
            request.current_stroke
        )
        return {
            "required_pump_pressure_psi": result,
            "initial_circulating_pressure_psi": request.initial_circulating_pressure,
            "final_circulating_pressure_psi": request.final_circulating_pressure,
            "total_pump_strokes": request.total_pump_strokes,
            "current_stroke": request.current_stroke
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/lost_circulation_pressure")
async def calculate_lost_circulation_pressure(request: LostCirculationPressureRequest):
    """Calculate pressure at which lost circulation may occur."""
    try:
        result = pressure.lost_circulation_pressure(
            request.formation_pressure,
            request.hydrostatic_pressure,
            request.safety_margin
        )
        return {
            "lost_circulation_pressure_psi": result,
            "formation_pressure_psi": request.formation_pressure,
            "hydrostatic_pressure_psi": request.hydrostatic_pressure,
            "safety_margin_psi": request.safety_margin
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
