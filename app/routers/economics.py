"""
Economics calculations API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

# Import petrocalc from pip-installed package
try:
    from petrocalc import economics
except ImportError:
    raise ImportError("petrocalc package not found. Please install it using: pip install petrocalc")

router = APIRouter()


# Request Models
class NPVRequest(BaseModel):
    cash_flows: List[float]
    discount_rate: float
    initial_investment: float = 0


class IRRRequest(BaseModel):
    cash_flows: List[float]
    initial_investment: float
    tolerance: float = 0.001


class DiscountedPaybackRequest(BaseModel):
    cash_flows: List[float]
    discount_rate: float
    initial_investment: float


class ProfitabilityIndexRequest(BaseModel):
    cash_flows: List[float]
    discount_rate: float
    initial_investment: float


class OilRevenueRequest(BaseModel):
    production_rate: float
    oil_price: float
    royalty_rate: float = 0.125
    operating_cost_per_barrel: float = 15


class GasRevenueRequest(BaseModel):
    production_rate: float
    gas_price: float
    royalty_rate: float = 0.125
    operating_cost_per_mcf: float = 1.5


class DrillingCostRequest(BaseModel):
    well_depth: float
    hole_diameter: float
    day_rate: float = 25000
    drilling_days_per_1000ft: float = 2.5


class CompletionCostRequest(BaseModel):
    well_depth: float
    completion_type: str = "conventional"
    number_of_stages: int = 1


class AbandonmentCostRequest(BaseModel):
    well_depth: float
    offshore: bool = False


class BreakEvenOilPriceRequest(BaseModel):
    initial_investment: float
    annual_production: float
    operating_cost_per_barrel: float
    royalty_rate: float = 0.125
    discount_rate: float = 0.1
    project_life: int = 20


# API Endpoints
@router.post("/net_present_value")
async def calculate_npv(request: NPVRequest):
    """Calculate Net Present Value (NPV) of a project."""
    try:
        result = economics.net_present_value(
            request.cash_flows,
            request.discount_rate,
            request.initial_investment
        )
        return {
            "net_present_value": result,
            "cash_flows": request.cash_flows,
            "discount_rate": request.discount_rate,
            "initial_investment": request.initial_investment
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/internal_rate_of_return")
async def calculate_irr(request: IRRRequest):
    """Calculate Internal Rate of Return (IRR)."""
    try:
        result = economics.internal_rate_of_return(
            request.cash_flows,
            request.initial_investment,
            request.tolerance
        )
        return {
            "internal_rate_of_return": result,
            "internal_rate_of_return_percent": result * 100,
            "cash_flows": request.cash_flows,
            "initial_investment": request.initial_investment,
            "tolerance": request.tolerance
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/discounted_payback_period")
async def calculate_discounted_payback(request: DiscountedPaybackRequest):
    """Calculate discounted payback period."""
    try:
        result = economics.discounted_payback_period(
            request.cash_flows,
            request.discount_rate,
            request.initial_investment
        )
        return {
            "discounted_payback_period_years": result,
            "cash_flows": request.cash_flows,
            "discount_rate": request.discount_rate,
            "initial_investment": request.initial_investment
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/profitability_index")
async def calculate_profitability_index(request: ProfitabilityIndexRequest):
    """Calculate Profitability Index (PI)."""
    try:
        result = economics.profitability_index(
            request.cash_flows,
            request.discount_rate,
            request.initial_investment
        )
        return {
            "profitability_index": result,
            "cash_flows": request.cash_flows,
            "discount_rate": request.discount_rate,
            "initial_investment": request.initial_investment
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/oil_revenue")
async def calculate_oil_revenue(request: OilRevenueRequest):
    """Calculate annual oil revenue."""
    try:
        result = economics.oil_revenue_calculation(
            request.production_rate,
            request.oil_price,
            request.royalty_rate,
            request.operating_cost_per_barrel
        )
        return {
            "annual_net_revenue": result,
            "production_rate_bbl_per_day": request.production_rate,
            "oil_price_per_bbl": request.oil_price,
            "royalty_rate": request.royalty_rate,
            "operating_cost_per_barrel": request.operating_cost_per_barrel,
            "annual_production_bbl": request.production_rate * 365
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/gas_revenue")
async def calculate_gas_revenue(request: GasRevenueRequest):
    """Calculate annual gas revenue."""
    try:
        result = economics.gas_revenue_calculation(
            request.production_rate,
            request.gas_price,
            request.royalty_rate,
            request.operating_cost_per_mcf
        )
        return {
            "annual_net_revenue": result,
            "production_rate_mscf_per_day": request.production_rate,
            "gas_price_per_mscf": request.gas_price,
            "royalty_rate": request.royalty_rate,
            "operating_cost_per_mcf": request.operating_cost_per_mcf,
            "annual_production_mscf": request.production_rate * 365
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/drilling_cost")
async def estimate_drilling_cost(request: DrillingCostRequest):
    """Estimate drilling cost for a well."""
    try:
        result = economics.drilling_cost_estimation(
            request.well_depth,
            request.hole_diameter,
            request.day_rate,
            request.drilling_days_per_1000ft
        )
        return {
            "drilling_cost": result,
            "well_depth_ft": request.well_depth,
            "hole_diameter_inches": request.hole_diameter,
            "day_rate": request.day_rate,
            "drilling_days_per_1000ft": request.drilling_days_per_1000ft,
            "estimated_drilling_days": (request.well_depth / 1000) * request.drilling_days_per_1000ft
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/completion_cost")
async def estimate_completion_cost(request: CompletionCostRequest):
    """Estimate completion cost for a well."""
    try:
        result = economics.completion_cost_estimation(
            request.well_depth,
            request.completion_type,
            request.number_of_stages
        )
        return {
            "completion_cost": result,
            "well_depth_ft": request.well_depth,
            "completion_type": request.completion_type,
            "number_of_stages": request.number_of_stages
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/abandonment_cost")
async def estimate_abandonment_cost(request: AbandonmentCostRequest):
    """Estimate well abandonment cost."""
    try:
        result = economics.abandonment_cost_estimation(
            request.well_depth,
            request.offshore
        )
        return {
            "abandonment_cost": result,
            "well_depth_ft": request.well_depth,
            "offshore": request.offshore
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/break_even_oil_price")
async def calculate_break_even_oil_price(request: BreakEvenOilPriceRequest):
    """Calculate break-even oil price for a project."""
    try:
        result = economics.break_even_oil_price(
            request.initial_investment,
            request.annual_production,
            request.operating_cost_per_barrel,
            request.royalty_rate,
            request.discount_rate,
            request.project_life
        )
        return {
            "break_even_oil_price_per_bbl": result,
            "initial_investment": request.initial_investment,
            "annual_production_bbl": request.annual_production,
            "operating_cost_per_barrel": request.operating_cost_per_barrel,
            "royalty_rate": request.royalty_rate,
            "discount_rate": request.discount_rate,
            "project_life_years": request.project_life
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
