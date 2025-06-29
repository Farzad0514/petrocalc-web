"""
Thermodynamics calculations API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Import petrocalc from pip-installed package
try:
    from petrocalc import thermodynamics
except ImportError:
    raise ImportError("petrocalc package not found. Please install it using: pip install petrocalc")

router = APIRouter()


# Request Models
class HeatCapacityOilRequest(BaseModel):
    oil_gravity: float
    temperature: float


class HeatCapacityGasRequest(BaseModel):
    gas_gravity: float
    temperature: float
    pressure: float = 14.7


class HeatCapacityWaterRequest(BaseModel):
    temperature: float
    pressure: float = 14.7


class ThermalConductivityOilRequest(BaseModel):
    oil_gravity: float
    temperature: float


class ThermalConductivityGasRequest(BaseModel):
    gas_gravity: float
    temperature: float
    pressure: float = 14.7


class ThermalExpansionCoefficientOilRequest(BaseModel):
    oil_gravity: float
    temperature: float


class HeatTransferCoefficientForcedConvectionRequest(BaseModel):
    velocity: float
    pipe_diameter: float
    fluid_density: float
    fluid_viscosity: float
    thermal_conductivity: float
    heat_capacity: float


class HeatLossInsulatedPipeRequest(BaseModel):
    inner_temperature: float
    outer_temperature: float
    pipe_inner_radius: float
    pipe_outer_radius: float
    insulation_outer_radius: float
    pipe_thermal_conductivity: float
    insulation_thermal_conductivity: float
    length: float


class TemperatureDropFlowingWellRequest(BaseModel):
    depth: float
    flow_rate: float
    geothermal_gradient: float = 0.015
    surface_temperature: float = 70


class JouleThomsonCoefficientGasRequest(BaseModel):
    temperature: float
    pressure: float
    gas_gravity: float


class HeatOfVaporizationOilRequest(BaseModel):
    oil_gravity: float
    temperature: float


class BubblePointTemperatureRequest(BaseModel):
    pressure: float
    oil_gravity: float
    gas_gravity: float
    gas_oil_ratio: float


# API Endpoints
@router.post("/heat_capacity_oil")
async def calculate_heat_capacity_oil(request: HeatCapacityOilRequest):
    """Calculate heat capacity of crude oil."""
    try:
        result = thermodynamics.heat_capacity_oil(
            request.oil_gravity,
            request.temperature
        )
        return {
            "heat_capacity_btu_per_lb_f": result,
            "oil_gravity_api": request.oil_gravity,
            "temperature_fahrenheit": request.temperature
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/heat_capacity_gas")
async def calculate_heat_capacity_gas(request: HeatCapacityGasRequest):
    """Calculate heat capacity of natural gas at constant pressure."""
    try:
        result = thermodynamics.heat_capacity_gas(
            request.gas_gravity,
            request.temperature,
            request.pressure
        )
        return {
            "heat_capacity_btu_per_lb_f": result,
            "gas_gravity": request.gas_gravity,
            "temperature_fahrenheit": request.temperature,
            "pressure_psia": request.pressure
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/heat_capacity_water")
async def calculate_heat_capacity_water(request: HeatCapacityWaterRequest):
    """Calculate heat capacity of water."""
    try:
        result = thermodynamics.heat_capacity_water(
            request.temperature,
            request.pressure
        )
        return {
            "heat_capacity_btu_per_lb_f": result,
            "temperature_fahrenheit": request.temperature,
            "pressure_psia": request.pressure
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/thermal_conductivity_oil")
async def calculate_thermal_conductivity_oil(request: ThermalConductivityOilRequest):
    """Calculate thermal conductivity of crude oil."""
    try:
        result = thermodynamics.thermal_conductivity_oil(
            request.oil_gravity,
            request.temperature
        )
        return {
            "thermal_conductivity_btu_per_hr_ft_f": result,
            "oil_gravity_api": request.oil_gravity,
            "temperature_fahrenheit": request.temperature
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/thermal_conductivity_gas")
async def calculate_thermal_conductivity_gas(request: ThermalConductivityGasRequest):
    """Calculate thermal conductivity of natural gas."""
    try:
        result = thermodynamics.thermal_conductivity_gas(
            request.gas_gravity,
            request.temperature,
            request.pressure
        )
        return {
            "thermal_conductivity_btu_per_hr_ft_f": result,
            "gas_gravity": request.gas_gravity,
            "temperature_fahrenheit": request.temperature,
            "pressure_psia": request.pressure
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/thermal_expansion_coefficient_oil")
async def calculate_thermal_expansion_coefficient_oil(request: ThermalExpansionCoefficientOilRequest):
    """Calculate thermal expansion coefficient of oil."""
    try:
        result = thermodynamics.thermal_expansion_coefficient_oil(
            request.oil_gravity,
            request.temperature
        )
        return {
            "thermal_expansion_coefficient_per_f": result,
            "oil_gravity_api": request.oil_gravity,
            "temperature_fahrenheit": request.temperature
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/heat_transfer_coefficient_forced_convection")
async def calculate_heat_transfer_coefficient_forced_convection(request: HeatTransferCoefficientForcedConvectionRequest):
    """Calculate heat transfer coefficient for forced convection in pipes."""
    try:
        result = thermodynamics.heat_transfer_coefficient_forced_convection(
            request.velocity,
            request.pipe_diameter,
            request.fluid_density,
            request.fluid_viscosity,
            request.thermal_conductivity,
            request.heat_capacity
        )
        return {
            "heat_transfer_coefficient_btu_per_hr_ft2_f": result,
            "velocity_ft_per_sec": request.velocity,
            "pipe_diameter_ft": request.pipe_diameter,
            "fluid_density_lb_per_ft3": request.fluid_density,
            "fluid_viscosity_cp": request.fluid_viscosity,
            "thermal_conductivity_btu_per_hr_ft_f": request.thermal_conductivity,
            "heat_capacity_btu_per_lb_f": request.heat_capacity
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/heat_loss_insulated_pipe")
async def calculate_heat_loss_insulated_pipe(request: HeatLossInsulatedPipeRequest):
    """Calculate heat loss from insulated pipe."""
    try:
        result = thermodynamics.heat_loss_insulated_pipe(
            request.inner_temperature,
            request.outer_temperature,
            request.pipe_inner_radius,
            request.pipe_outer_radius,
            request.insulation_outer_radius,
            request.pipe_thermal_conductivity,
            request.insulation_thermal_conductivity,
            request.length
        )
        return {
            "heat_loss_btu_per_hr": result,
            "inner_temperature_fahrenheit": request.inner_temperature,
            "outer_temperature_fahrenheit": request.outer_temperature,
            "pipe_inner_radius_ft": request.pipe_inner_radius,
            "pipe_outer_radius_ft": request.pipe_outer_radius,
            "insulation_outer_radius_ft": request.insulation_outer_radius,
            "pipe_thermal_conductivity_btu_per_hr_ft_f": request.pipe_thermal_conductivity,
            "insulation_thermal_conductivity_btu_per_hr_ft_f": request.insulation_thermal_conductivity,
            "length_ft": request.length
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/temperature_drop_flowing_well")
async def calculate_temperature_drop_flowing_well(request: TemperatureDropFlowingWellRequest):
    """Calculate temperature at depth in flowing well."""
    try:
        result = thermodynamics.temperature_drop_flowing_well(
            request.depth,
            request.flow_rate,
            request.geothermal_gradient,
            request.surface_temperature
        )
        return {
            "temperature_at_depth_fahrenheit": result,
            "depth_ft": request.depth,
            "flow_rate_bbl_per_day": request.flow_rate,
            "geothermal_gradient_f_per_ft": request.geothermal_gradient,
            "surface_temperature_fahrenheit": request.surface_temperature
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/joule_thomson_coefficient_gas")
async def calculate_joule_thomson_coefficient_gas(request: JouleThomsonCoefficientGasRequest):
    """Calculate Joule-Thomson coefficient for natural gas."""
    try:
        result = thermodynamics.joule_thomson_coefficient_gas(
            request.temperature,
            request.pressure,
            request.gas_gravity
        )
        return {
            "joule_thomson_coefficient_f_per_psi": result,
            "temperature_fahrenheit": request.temperature,
            "pressure_psia": request.pressure,
            "gas_gravity": request.gas_gravity
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/heat_of_vaporization_oil")
async def calculate_heat_of_vaporization_oil(request: HeatOfVaporizationOilRequest):
    """Calculate heat of vaporization for crude oil."""
    try:
        result = thermodynamics.heat_of_vaporization_oil(
            request.oil_gravity,
            request.temperature
        )
        return {
            "heat_of_vaporization_btu_per_lb": result,
            "oil_gravity_api": request.oil_gravity,
            "temperature_fahrenheit": request.temperature
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bubble_point_temperature")
async def calculate_bubble_point_temperature(request: BubblePointTemperatureRequest):
    """Calculate bubble point temperature."""
    try:
        result = thermodynamics.bubble_point_temperature(
            request.pressure,
            request.oil_gravity,
            request.gas_gravity,
            request.gas_oil_ratio
        )
        return {
            "bubble_point_temperature_fahrenheit": result,
            "pressure_psia": request.pressure,
            "oil_gravity_api": request.oil_gravity,
            "gas_gravity": request.gas_gravity,
            "gas_oil_ratio_scf_per_stb": request.gas_oil_ratio
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
