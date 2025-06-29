"""
Flow calculations API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Tuple

# Import petrocalc from pip-installed package
try:
    from petrocalc import flow
except ImportError:
    raise ImportError("petrocalc package not found. Please install it using: pip install petrocalc")

router = APIRouter()


# Request Models
class MoodyFrictionFactorRequest(BaseModel):
    reynolds_number: float
    relative_roughness: float


class PressureDropHorizontalPipeRequest(BaseModel):
    flow_rate: float
    pipe_diameter: float
    pipe_length: float
    fluid_density: float
    fluid_viscosity: float
    pipe_roughness: float = 0.0006


class GasFlowRateWeymouthRequest(BaseModel):
    upstream_pressure: float
    downstream_pressure: float
    pipe_diameter: float
    pipe_length: float
    gas_gravity: float
    temperature: float
    efficiency: float = 1.0


class OilFlowRateHazenWilliamsRequest(BaseModel):
    pressure_drop: float
    pipe_diameter: float
    pipe_length: float
    hazen_williams_coefficient: float = 120


class CriticalFlowVelocityRequest(BaseModel):
    liquid_density: float
    gas_density: float
    surface_tension: float


class TerminalSettlingVelocityRequest(BaseModel):
    particle_diameter: float
    particle_density: float
    fluid_density: float
    fluid_viscosity: float


class FlowThroughOrificeRequest(BaseModel):
    upstream_pressure: float
    downstream_pressure: float
    orifice_diameter: float
    fluid_density: float
    discharge_coefficient: float = 0.6


class MultiphaseFlowPressureDropRequest(BaseModel):
    liquid_superficial_velocity: float
    gas_superficial_velocity: float
    pipe_diameter: float
    pipe_inclination: float
    liquid_density: float
    gas_density: float
    liquid_viscosity: float
    gas_viscosity: float
    surface_tension: float


class PumpHeadCalculationRequest(BaseModel):
    flow_rate: float
    total_dynamic_head: float
    pump_efficiency: float = 0.75


# API Endpoints
@router.post("/moody_friction_factor")
async def calculate_moody_friction_factor(request: MoodyFrictionFactorRequest):
    """Calculate friction factor using Moody chart correlation."""
    try:
        result = flow.moody_friction_factor(
            request.reynolds_number,
            request.relative_roughness
        )
        return {
            "friction_factor": result,
            "reynolds_number": request.reynolds_number,
            "relative_roughness": request.relative_roughness
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pressure_drop_horizontal_pipe")
async def calculate_pressure_drop_horizontal_pipe(request: PressureDropHorizontalPipeRequest):
    """Calculate pressure drop in horizontal pipe due to friction."""
    try:
        result = flow.pressure_drop_horizontal_pipe(
            request.flow_rate,
            request.pipe_diameter,
            request.pipe_length,
            request.fluid_density,
            request.fluid_viscosity,
            request.pipe_roughness
        )
        return {
            "pressure_drop_psi": result,
            "flow_rate_bbl_per_day": request.flow_rate,
            "pipe_diameter_inches": request.pipe_diameter,
            "pipe_length_ft": request.pipe_length,
            "fluid_density_lb_per_ft3": request.fluid_density,
            "fluid_viscosity_cp": request.fluid_viscosity,
            "pipe_roughness_ft": request.pipe_roughness
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/gas_flow_rate_weymouth")
async def calculate_gas_flow_rate_weymouth(request: GasFlowRateWeymouthRequest):
    """Calculate gas flow rate using Weymouth equation."""
    try:
        result = flow.gas_flow_rate_weymouth(
            request.upstream_pressure,
            request.downstream_pressure,
            request.pipe_diameter,
            request.pipe_length,
            request.gas_gravity,
            request.temperature,
            request.efficiency
        )
        return {
            "gas_flow_rate_mscf_per_day": result,
            "upstream_pressure_psia": request.upstream_pressure,
            "downstream_pressure_psia": request.downstream_pressure,
            "pipe_diameter_inches": request.pipe_diameter,
            "pipe_length_miles": request.pipe_length,
            "gas_gravity": request.gas_gravity,
            "temperature_rankine": request.temperature,
            "efficiency": request.efficiency
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/oil_flow_rate_hazen_williams")
async def calculate_oil_flow_rate_hazen_williams(request: OilFlowRateHazenWilliamsRequest):
    """Calculate oil flow rate using Hazen-Williams equation."""
    try:
        result = flow.oil_flow_rate_hazen_williams(
            request.pressure_drop,
            request.pipe_diameter,
            request.pipe_length,
            request.hazen_williams_coefficient
        )
        return {
            "flow_rate_bbl_per_day": result,
            "pressure_drop_psi": request.pressure_drop,
            "pipe_diameter_inches": request.pipe_diameter,
            "pipe_length_ft": request.pipe_length,
            "hazen_williams_coefficient": request.hazen_williams_coefficient
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/critical_flow_velocity")
async def calculate_critical_flow_velocity(request: CriticalFlowVelocityRequest):
    """Calculate critical velocity for liquid carryover in gas flow."""
    try:
        result = flow.critical_flow_velocity(
            request.liquid_density,
            request.gas_density,
            request.surface_tension
        )
        return {
            "critical_velocity_ft_per_sec": result,
            "liquid_density_lb_per_ft3": request.liquid_density,
            "gas_density_lb_per_ft3": request.gas_density,
            "surface_tension_dynes_per_cm": request.surface_tension
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/terminal_settling_velocity")
async def calculate_terminal_settling_velocity(request: TerminalSettlingVelocityRequest):
    """Calculate terminal settling velocity of particles in fluid."""
    try:
        result = flow.terminal_settling_velocity(
            request.particle_diameter,
            request.particle_density,
            request.fluid_density,
            request.fluid_viscosity
        )
        return {
            "terminal_velocity_ft_per_sec": result,
            "particle_diameter_ft": request.particle_diameter,
            "particle_density_lb_per_ft3": request.particle_density,
            "fluid_density_lb_per_ft3": request.fluid_density,
            "fluid_viscosity_cp": request.fluid_viscosity
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/flow_through_orifice")
async def calculate_flow_through_orifice(request: FlowThroughOrificeRequest):
    """Calculate flow rate through an orifice."""
    try:
        result = flow.flow_through_orifice(
            request.upstream_pressure,
            request.downstream_pressure,
            request.orifice_diameter,
            request.fluid_density,
            request.discharge_coefficient
        )
        return {
            "flow_rate_bbl_per_day": result,
            "upstream_pressure_psi": request.upstream_pressure,
            "downstream_pressure_psi": request.downstream_pressure,
            "orifice_diameter_inches": request.orifice_diameter,
            "fluid_density_lb_per_ft3": request.fluid_density,
            "discharge_coefficient": request.discharge_coefficient
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/multiphase_flow_pressure_drop")
async def calculate_multiphase_flow_pressure_drop(request: MultiphaseFlowPressureDropRequest):
    """Calculate pressure drop in multiphase flow using simplified correlation."""
    try:
        pressure_gradient, liquid_holdup = flow.multiphase_flow_pressure_drop(
            request.liquid_superficial_velocity,
            request.gas_superficial_velocity,
            request.pipe_diameter,
            request.pipe_inclination,
            request.liquid_density,
            request.gas_density,
            request.liquid_viscosity,
            request.gas_viscosity,
            request.surface_tension
        )
        return {
            "pressure_gradient_psi_per_ft": pressure_gradient,
            "liquid_holdup": liquid_holdup,
            "liquid_superficial_velocity_ft_per_sec": request.liquid_superficial_velocity,
            "gas_superficial_velocity_ft_per_sec": request.gas_superficial_velocity,
            "pipe_diameter_ft": request.pipe_diameter,
            "pipe_inclination_degrees": request.pipe_inclination,
            "liquid_density_lb_per_ft3": request.liquid_density,
            "gas_density_lb_per_ft3": request.gas_density,
            "liquid_viscosity_cp": request.liquid_viscosity,
            "gas_viscosity_cp": request.gas_viscosity,
            "surface_tension_dynes_per_cm": request.surface_tension
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pump_head_calculation")
async def calculate_pump_head(request: PumpHeadCalculationRequest):
    """Calculate required pump power."""
    try:
        result = flow.pump_head_calculation(
            request.flow_rate,
            request.total_dynamic_head,
            request.pump_efficiency
        )
        return {
            "required_pump_power_hp": result,
            "flow_rate_bbl_per_day": request.flow_rate,
            "total_dynamic_head_ft": request.total_dynamic_head,
            "pump_efficiency": request.pump_efficiency
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
