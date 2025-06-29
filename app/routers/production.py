"""
Production engineering calculations API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

# Import petrocalc from pip-installed package
try:
    from petrocalc import production
except ImportError:
    raise ImportError("petrocalc package not found. Please install it using: pip install petrocalc")

router = APIRouter()


# Request Models
class VogelIPRRequest(BaseModel):
    reservoir_pressure: float
    bottomhole_pressure: float
    maximum_oil_rate: float


class ProductivityIndexRequest(BaseModel):
    flow_rate: float
    reservoir_pressure: float
    bottomhole_pressure: float


class DarcyRadialFlowRequest(BaseModel):
    permeability: float
    thickness: float
    pressure_drop: float
    viscosity: float
    formation_volume_factor: float
    wellbore_radius: float
    drainage_radius: float


class SkinFactorRequest(BaseModel):
    actual_productivity_index: float
    ideal_productivity_index: float


class GasWellDeliverabilityRequest(BaseModel):
    absolute_open_flow_potential: float
    flowing_bottomhole_pressure: float
    reservoir_pressure: float
    flow_exponent: float = 0.5


class ChokeFlowRateGasRequest(BaseModel):
    upstream_pressure: float
    downstream_pressure: float
    choke_diameter: float
    gas_gravity: float
    temperature: float
    discharge_coefficient: float = 0.85


class MultiphaseFlowRequest(BaseModel):
    liquid_rate: float
    gas_rate: float
    pipe_diameter: float
    pipe_inclination: float
    liquid_density: float
    gas_density: float
    liquid_viscosity: float
    gas_viscosity: float


class WellTestHornerRequest(BaseModel):
    pressure_data: List[float]
    time_data: List[float]
    production_time: float
    flow_rate: float
    porosity: float
    viscosity: float
    total_compressibility: float
    formation_volume_factor: float
    thickness: float


# API Endpoints
@router.post("/vogel_ipr")
async def calculate_vogel_ipr(request: VogelIPRRequest):
    """Calculate oil production rate using Vogel's IPR correlation."""
    try:
        result = production.vogel_ipr(
            request.reservoir_pressure,
            request.bottomhole_pressure,
            request.maximum_oil_rate
        )
        return {
            "flow_rate_stb_per_day": result,
            "reservoir_pressure_psia": request.reservoir_pressure,
            "bottomhole_pressure_psia": request.bottomhole_pressure,
            "maximum_oil_rate_stb_per_day": request.maximum_oil_rate
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/productivity_index")
async def calculate_productivity_index(request: ProductivityIndexRequest):
    """Calculate productivity index for a well."""
    try:
        result = production.productivity_index(
            request.flow_rate,
            request.reservoir_pressure,
            request.bottomhole_pressure
        )
        return {
            "productivity_index_stb_per_day_per_psi": result,
            "flow_rate_stb_per_day": request.flow_rate,
            "reservoir_pressure_psia": request.reservoir_pressure,
            "bottomhole_pressure_psia": request.bottomhole_pressure
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/darcy_radial_flow")
async def calculate_darcy_radial_flow(request: DarcyRadialFlowRequest):
    """Calculate flow rate using Darcy's equation for radial flow."""
    try:
        result = production.darcy_radial_flow(
            request.permeability,
            request.thickness,
            request.pressure_drop,
            request.viscosity,
            request.formation_volume_factor,
            request.wellbore_radius,
            request.drainage_radius
        )
        return {
            "flow_rate_stb_per_day": result,
            "permeability_md": request.permeability,
            "thickness_ft": request.thickness,
            "pressure_drop_psi": request.pressure_drop,
            "viscosity_cp": request.viscosity,
            "formation_volume_factor": request.formation_volume_factor,
            "wellbore_radius_ft": request.wellbore_radius,
            "drainage_radius_ft": request.drainage_radius
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/skin_factor")
async def calculate_skin_factor(request: SkinFactorRequest):
    """Calculate skin factor from productivity indices."""
    try:
        result = production.skin_factor(
            request.actual_productivity_index,
            request.ideal_productivity_index
        )
        return {
            "skin_factor": result,
            "actual_productivity_index": request.actual_productivity_index,
            "ideal_productivity_index": request.ideal_productivity_index
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/gas_well_deliverability")
async def calculate_gas_well_deliverability(request: GasWellDeliverabilityRequest):
    """Calculate gas well deliverability using Rawlins-Schellhardt equation."""
    try:
        result = production.gas_well_deliverability_rawlins_schellhardt(
            request.absolute_open_flow_potential,
            request.flowing_bottomhole_pressure,
            request.reservoir_pressure,
            request.flow_exponent
        )
        return {
            "gas_flow_rate_mscf_per_day": result,
            "absolute_open_flow_potential_mscf_per_day": request.absolute_open_flow_potential,
            "flowing_bottomhole_pressure_psia": request.flowing_bottomhole_pressure,
            "reservoir_pressure_psia": request.reservoir_pressure,
            "flow_exponent": request.flow_exponent
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/choke_flow_rate_gas")
async def calculate_choke_flow_rate_gas(request: ChokeFlowRateGasRequest):
    """Calculate gas flow rate through a choke."""
    try:
        result = production.choke_flow_rate_gas(
            request.upstream_pressure,
            request.downstream_pressure,
            request.choke_diameter,
            request.gas_gravity,
            request.temperature,
            request.discharge_coefficient
        )
        return {
            "gas_flow_rate_mscf_per_day": result,
            "upstream_pressure_psia": request.upstream_pressure,
            "downstream_pressure_psia": request.downstream_pressure,
            "choke_diameter_inches": request.choke_diameter,
            "gas_gravity": request.gas_gravity,
            "temperature_rankine": request.temperature,
            "discharge_coefficient": request.discharge_coefficient
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/multiphase_flow_beggs_brill")
async def calculate_multiphase_flow(request: MultiphaseFlowRequest):
    """Calculate pressure gradient using Beggs-Brill correlation."""
    try:
        pressure_gradient, liquid_holdup = production.multiphase_flow_beggs_brill(
            request.liquid_rate,
            request.gas_rate,
            request.pipe_diameter,
            request.pipe_inclination,
            request.liquid_density,
            request.gas_density,
            request.liquid_viscosity,
            request.gas_viscosity
        )
        return {
            "pressure_gradient_psi_per_ft": pressure_gradient,
            "liquid_holdup": liquid_holdup,
            "liquid_rate_bbl_per_day": request.liquid_rate,
            "gas_rate_mscf_per_day": request.gas_rate,
            "pipe_diameter_inches": request.pipe_diameter,
            "pipe_inclination_degrees": request.pipe_inclination,
            "liquid_density_lb_per_ft3": request.liquid_density,
            "gas_density_lb_per_ft3": request.gas_density,
            "liquid_viscosity_cp": request.liquid_viscosity,
            "gas_viscosity_cp": request.gas_viscosity
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/well_test_horner")
async def analyze_well_test_horner(request: WellTestHornerRequest):
    """Analyze well test data using Horner plot method."""
    try:
        permeability, skin = production.well_test_analysis_horner(
            request.pressure_data,
            request.time_data,
            request.production_time,
            request.flow_rate,
            request.porosity,
            request.viscosity,
            request.total_compressibility,
            request.formation_volume_factor,
            request.thickness
        )
        return {
            "permeability_md": permeability,
            "skin_factor": skin,
            "production_time_hours": request.production_time,
            "flow_rate_stb_per_day": request.flow_rate,
            "porosity": request.porosity,
            "viscosity_cp": request.viscosity,
            "total_compressibility_per_psi": request.total_compressibility,
            "formation_volume_factor": request.formation_volume_factor,
            "thickness_ft": request.thickness
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
