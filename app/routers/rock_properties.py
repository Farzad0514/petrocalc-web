"""
Rock properties calculations API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Import petrocalc from pip-installed package
try:
    from petrocalc import rock_properties
except ImportError:
    raise ImportError("petrocalc package not found. Please install it using: pip install petrocalc")

router = APIRouter()


# Request Models
class PorosityFromLogsRequest(BaseModel):
    neutron_porosity: float
    density_porosity: float
    shale_volume: float = 0.0


class PorosityFromDensityLogRequest(BaseModel):
    bulk_density: float
    matrix_density: float
    fluid_density: float


class WaterSaturationArchieRequest(BaseModel):
    formation_resistivity: float
    water_resistivity: float
    porosity: float
    cementation_factor: float = 2.0
    saturation_exponent: float = 2.0
    tortuosity_factor: float = 1.0


class PermeabilityFromPorosityKozenyCarmanRequest(BaseModel):
    porosity: float
    grain_diameter: float
    shape_factor: float = 180


class PermeabilityTimurCorrelationRequest(BaseModel):
    porosity: float
    irreducible_water_saturation: float


class RockCompressibilityRequest(BaseModel):
    porosity: float
    pressure: float
    compressibility_coefficient: float = 3e-6


class RelativePermeabilityOilCoreyRequest(BaseModel):
    water_saturation: float
    irreducible_water_saturation: float
    residual_oil_saturation: float
    oil_endpoint: float = 1.0
    oil_exponent: float = 2.0


class RelativePermeabilityWaterCoreyRequest(BaseModel):
    water_saturation: float
    irreducible_water_saturation: float
    residual_oil_saturation: float
    water_endpoint: float = 1.0
    water_exponent: float = 2.0


class CapillaryPressureBrooksCoreyRequest(BaseModel):
    water_saturation: float
    irreducible_water_saturation: float
    entry_pressure: float
    pore_size_distribution: float


class FormationFactorRequest(BaseModel):
    porosity: float
    cementation_factor: float = 2.0
    tortuosity_factor: float = 1.0


class NetToGrossRatioRequest(BaseModel):
    net_thickness: float
    gross_thickness: float


class BulkVolumeOilRequest(BaseModel):
    gross_rock_volume: float
    net_to_gross: float
    porosity: float
    oil_saturation: float


class HydrocarbonPoreVolumeRequest(BaseModel):
    bulk_volume: float
    porosity: float
    hydrocarbon_saturation: float


# API Endpoints
@router.post("/porosity_from_logs")
async def calculate_porosity_from_logs(request: PorosityFromLogsRequest):
    """Calculate effective porosity from neutron and density logs."""
    try:
        result = rock_properties.porosity_from_logs(
            request.neutron_porosity,
            request.density_porosity,
            request.shale_volume
        )
        return {
            "effective_porosity_fraction": result,
            "neutron_porosity_fraction": request.neutron_porosity,
            "density_porosity_fraction": request.density_porosity,
            "shale_volume_fraction": request.shale_volume
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/porosity_from_density_log")
async def calculate_porosity_from_density_log(request: PorosityFromDensityLogRequest):
    """Calculate porosity from density log using standard formula."""
    try:
        result = rock_properties.porosity_from_density_log(
            request.bulk_density,
            request.matrix_density,
            request.fluid_density
        )
        return {
            "porosity_fraction": result,
            "bulk_density_g_per_cm3": request.bulk_density,
            "matrix_density_g_per_cm3": request.matrix_density,
            "fluid_density_g_per_cm3": request.fluid_density
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/water_saturation_archie")
async def calculate_water_saturation_archie(request: WaterSaturationArchieRequest):
    """Calculate water saturation using Archie's equation."""
    try:
        result = rock_properties.water_saturation_archie(
            request.formation_resistivity,
            request.water_resistivity,
            request.porosity,
            request.cementation_factor,
            request.saturation_exponent,
            request.tortuosity_factor
        )
        return {
            "water_saturation_fraction": result,
            "formation_resistivity_ohm_m": request.formation_resistivity,
            "water_resistivity_ohm_m": request.water_resistivity,
            "porosity_fraction": request.porosity,
            "cementation_factor": request.cementation_factor,
            "saturation_exponent": request.saturation_exponent,
            "tortuosity_factor": request.tortuosity_factor
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/permeability_from_porosity_kozeny_carman")
async def calculate_permeability_kozeny_carman(request: PermeabilityFromPorosityKozenyCarmanRequest):
    """Calculate permeability using Kozeny-Carman equation."""
    try:
        result = rock_properties.permeability_from_porosity_kozeny_carman(
            request.porosity,
            request.grain_diameter,
            request.shape_factor
        )
        return {
            "permeability_md": result,
            "porosity_fraction": request.porosity,
            "grain_diameter_mm": request.grain_diameter,
            "shape_factor": request.shape_factor
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/permeability_timur_correlation")
async def calculate_permeability_timur(request: PermeabilityTimurCorrelationRequest):
    """Calculate permeability using Timur correlation."""
    try:
        result = rock_properties.permeability_timur_correlation(
            request.porosity,
            request.irreducible_water_saturation
        )
        return {
            "permeability_md": result,
            "porosity_fraction": request.porosity,
            "irreducible_water_saturation_fraction": request.irreducible_water_saturation
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rock_compressibility")
async def calculate_rock_compressibility(request: RockCompressibilityRequest):
    """Calculate rock compressibility."""
    try:
        result = rock_properties.rock_compressibility(
            request.porosity,
            request.pressure,
            request.compressibility_coefficient
        )
        return {
            "rock_compressibility_per_psi": result,
            "porosity_fraction": request.porosity,
            "pressure_psia": request.pressure,
            "compressibility_coefficient_per_psi": request.compressibility_coefficient
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/relative_permeability_oil_corey")
async def calculate_relative_permeability_oil_corey(request: RelativePermeabilityOilCoreyRequest):
    """Calculate oil relative permeability using Corey correlation."""
    try:
        result = rock_properties.relative_permeability_oil_corey(
            request.water_saturation,
            request.irreducible_water_saturation,
            request.residual_oil_saturation,
            request.oil_endpoint,
            request.oil_exponent
        )
        return {
            "oil_relative_permeability": result,
            "water_saturation_fraction": request.water_saturation,
            "irreducible_water_saturation_fraction": request.irreducible_water_saturation,
            "residual_oil_saturation_fraction": request.residual_oil_saturation,
            "oil_endpoint": request.oil_endpoint,
            "oil_exponent": request.oil_exponent
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/relative_permeability_water_corey")
async def calculate_relative_permeability_water_corey(request: RelativePermeabilityWaterCoreyRequest):
    """Calculate water relative permeability using Corey correlation."""
    try:
        result = rock_properties.relative_permeability_water_corey(
            request.water_saturation,
            request.irreducible_water_saturation,
            request.residual_oil_saturation,
            request.water_endpoint,
            request.water_exponent
        )
        return {
            "water_relative_permeability": result,
            "water_saturation_fraction": request.water_saturation,
            "irreducible_water_saturation_fraction": request.irreducible_water_saturation,
            "residual_oil_saturation_fraction": request.residual_oil_saturation,
            "water_endpoint": request.water_endpoint,
            "water_exponent": request.water_exponent
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/capillary_pressure_brooks_corey")
async def calculate_capillary_pressure_brooks_corey(request: CapillaryPressureBrooksCoreyRequest):
    """Calculate capillary pressure using Brooks-Corey correlation."""
    try:
        result = rock_properties.capillary_pressure_brooks_corey(
            request.water_saturation,
            request.irreducible_water_saturation,
            request.entry_pressure,
            request.pore_size_distribution
        )
        return {
            "capillary_pressure_psi": result,
            "water_saturation_fraction": request.water_saturation,
            "irreducible_water_saturation_fraction": request.irreducible_water_saturation,
            "entry_pressure_psi": request.entry_pressure,
            "pore_size_distribution_index": request.pore_size_distribution
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/formation_factor")
async def calculate_formation_factor(request: FormationFactorRequest):
    """Calculate formation resistivity factor."""
    try:
        result = rock_properties.formation_factor(
            request.porosity,
            request.cementation_factor,
            request.tortuosity_factor
        )
        return {
            "formation_factor": result,
            "porosity_fraction": request.porosity,
            "cementation_factor": request.cementation_factor,
            "tortuosity_factor": request.tortuosity_factor
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/net_to_gross_ratio")
async def calculate_net_to_gross_ratio(request: NetToGrossRatioRequest):
    """Calculate net-to-gross ratio."""
    try:
        result = rock_properties.net_to_gross_ratio(
            request.net_thickness,
            request.gross_thickness
        )
        return {
            "net_to_gross_ratio": result,
            "net_thickness_ft": request.net_thickness,
            "gross_thickness_ft": request.gross_thickness
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bulk_volume_oil")
async def calculate_bulk_volume_oil(request: BulkVolumeOilRequest):
    """Calculate bulk volume of oil in reservoir."""
    try:
        result = rock_properties.bulk_volume_oil(
            request.gross_rock_volume,
            request.net_to_gross,
            request.porosity,
            request.oil_saturation
        )
        return {
            "bulk_volume_oil_acre_ft": result,
            "gross_rock_volume_acre_ft": request.gross_rock_volume,
            "net_to_gross_ratio": request.net_to_gross,
            "porosity_fraction": request.porosity,
            "oil_saturation_fraction": request.oil_saturation
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/hydrocarbon_pore_volume")
async def calculate_hydrocarbon_pore_volume(request: HydrocarbonPoreVolumeRequest):
    """Calculate hydrocarbon pore volume."""
    try:
        result = rock_properties.hydrocarbon_pore_volume(
            request.bulk_volume,
            request.porosity,
            request.hydrocarbon_saturation
        )
        return {
            "hydrocarbon_pore_volume_acre_ft": result,
            "bulk_volume_acre_ft": request.bulk_volume,
            "porosity_fraction": request.porosity,
            "hydrocarbon_saturation_fraction": request.hydrocarbon_saturation
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
