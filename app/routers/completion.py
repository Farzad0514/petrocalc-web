"""
Well completion and stimulation calculations API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Import petrocalc from pip-installed package
try:
    from petrocalc import completion
except ImportError:
    raise ImportError("petrocalc package not found. Please install it using: pip install petrocalc")

router = APIRouter()


# Request Models
class PerforationFlowEfficiencyRequest(BaseModel):
    perforation_diameter: float
    wellbore_diameter: float
    shots_per_foot: float
    penetration_depth: float
    phasing_angle: float = 60


class HydraulicFracturingRequest(BaseModel):
    formation_permeability: float
    fracture_half_length: float
    fracture_conductivity: float
    reservoir_pressure: float
    bottomhole_pressure: float
    drainage_area: float


class ProppantConcentrationRequest(BaseModel):
    proppant_mass: float
    fracture_volume: float
    proppant_density: float = 2.65


class FractureWidthRequest(BaseModel):
    injection_rate: float
    fluid_viscosity: float
    fracture_height: float
    youngs_modulus: float
    poisson_ratio: float = 0.25


class AcidizingVolumeRequest(BaseModel):
    wellbore_radius: float
    penetration_depth: float
    porosity: float
    acid_concentration: float = 15


# API Endpoints
@router.post("/perforation_flow_efficiency")
async def calculate_perforation_flow_efficiency(request: PerforationFlowEfficiencyRequest):
    """Calculate perforation flow efficiency."""
    try:
        result = completion.perforation_flow_efficiency(
            request.perforation_diameter,
            request.wellbore_diameter,
            request.shots_per_foot,
            request.penetration_depth,
            request.phasing_angle
        )
        return {
            "flow_efficiency": result,
            "perforation_diameter_inches": request.perforation_diameter,
            "wellbore_diameter_inches": request.wellbore_diameter,
            "shots_per_foot": request.shots_per_foot,
            "penetration_depth_inches": request.penetration_depth,
            "phasing_angle_degrees": request.phasing_angle
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/hydraulic_fracturing_productivity")
async def calculate_hydraulic_fracturing_productivity(request: HydraulicFracturingRequest):
    """Calculate productivity improvement from hydraulic fracturing."""
    try:
        # Note: This would use an actual function from the completion module
        # For now, implementing a simplified calculation
        k = request.formation_permeability
        xf = request.fracture_half_length
        kf_wf = request.fracture_conductivity
        
        # Simplified productivity ratio calculation
        productivity_ratio = 1 + (kf_wf / (k * xf)) * 0.5
        
        return {
            "productivity_ratio": productivity_ratio,
            "formation_permeability_md": request.formation_permeability,
            "fracture_half_length_ft": request.fracture_half_length,
            "fracture_conductivity_md_ft": request.fracture_conductivity,
            "reservoir_pressure_psia": request.reservoir_pressure,
            "bottomhole_pressure_psia": request.bottomhole_pressure,
            "drainage_area_acres": request.drainage_area
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/proppant_concentration")
async def calculate_proppant_concentration(request: ProppantConcentrationRequest):
    """Calculate proppant concentration in fracturing fluid."""
    try:
        concentration = (request.proppant_mass / request.proppant_density) / request.fracture_volume
        concentration_ppa = concentration * 8.34  # Convert to pounds per gallon added
        
        return {
            "proppant_concentration_lb_per_gal": concentration_ppa,
            "proppant_mass_lb": request.proppant_mass,
            "fracture_volume_gal": request.fracture_volume,
            "proppant_density_sg": request.proppant_density
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/fracture_width")
async def calculate_fracture_width(request: FractureWidthRequest):
    """Calculate fracture width during injection."""
    try:
        # PKN model approximation
        q = request.injection_rate / 60  # Convert to bbl/sec
        mu = request.fluid_viscosity
        h = request.fracture_height
        e_prime = request.youngs_modulus / (1 - request.poisson_ratio**2)
        
        # Simplified fracture width calculation
        width = ((12 * mu * q) / (h * e_prime))**(1/3)
        
        return {
            "fracture_width_inches": width,
            "injection_rate_bbl_per_min": request.injection_rate,
            "fluid_viscosity_cp": request.fluid_viscosity,
            "fracture_height_ft": request.fracture_height,
            "youngs_modulus_psi": request.youngs_modulus,
            "poisson_ratio": request.poisson_ratio
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/acidizing_volume")
async def calculate_acidizing_volume(request: AcidizingVolumeRequest):
    """Calculate acid volume required for matrix acidizing."""
    try:
        import math
        
        rw = request.wellbore_radius
        r_penetration = rw + request.penetration_depth / 12  # Convert inches to ft
        phi = request.porosity
        
        # Volume of rock to be acidized
        rock_volume = math.pi * (r_penetration**2 - rw**2)  # ft³ per ft of height
        
        # Acid volume (simplified - assumes 15% porosity treatment)
        acid_volume = rock_volume * phi * 7.48  # Convert to gallons per ft of height
        
        return {
            "acid_volume_gal_per_ft": acid_volume,
            "wellbore_radius_ft": request.wellbore_radius,
            "penetration_depth_inches": request.penetration_depth,
            "porosity_fraction": request.porosity,
            "acid_concentration_percent": request.acid_concentration
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
