"""
Comprehensive example demonstrating PetroCalc library capabilities.

This script shows how to use the PetroCalc library for various petroleum engineering calculations.
Requires: pip install petrocalc
"""

import sys
import math

try:
    import petrocalc
except ImportError:
    print("❌ Error: petrocalc package not found!")
    print("Please install petrocalc using: pip install petrocalc")
    sys.exit(1)

def drilling_example():
    """Demonstrate drilling engineering calculations"""
    print("=" * 60)
    print("DRILLING ENGINEERING CALCULATIONS")
    print("=" * 60)
    
    # Well parameters
    depth = 12000  # ft
    hole_diameter = 8.5  # inches
    pipe_od = 5.0  # inches
    mud_weight = 12.5  # ppg
    flow_rate = 450  # gpm
    
    print(f"Well Depth: {depth:,} ft")
    print(f"Hole Diameter: {hole_diameter} inches")
    print(f"Mud Weight: {mud_weight} ppg")
    print(f"Flow Rate: {flow_rate} gpm")
    print()
    
    # Pressure calculations
    pressure_gradient = petrocalc.drilling.mud_weight_to_pressure_gradient(mud_weight, "ppg")
    hydrostatic_pressure = petrocalc.drilling.hydrostatic_pressure(mud_weight, depth, "ppg")
    
    print(f"Pressure gradient: {pressure_gradient:.3f} psi/ft")
    print(f"Hydrostatic pressure: {hydrostatic_pressure:,.0f} psi")
    
    # Hydraulic calculations
    ann_velocity = petrocalc.drilling.annular_velocity(flow_rate, hole_diameter, pipe_od)
    critical_flow = petrocalc.drilling.critical_flow_rate(hole_diameter, pipe_od, 0.1, 12.5, 21.0)
    
    print(f"Annular velocity: {ann_velocity:.1f} ft/min")
    print(f"Critical flow rate for hole cleaning: {critical_flow:.0f} gpm")
    
    # Buoyancy factor
    mud_density_lbft3 = mud_weight * 8.33  # Convert ppg to lb/ft³
    buoyancy = petrocalc.drilling.buoyancy_factor(mud_density_lbft3)
    print(f"Buoyancy factor: {buoyancy:.3f}")
    print()


def reservoir_example():
    """Demonstrate reservoir engineering calculations"""
    print("=" * 60)
    print("RESERVOIR ENGINEERING CALCULATIONS")
    print("=" * 60)
    
    # Fluid properties
    api_gravity = 32  # degrees API
    gas_gravity = 0.7  # air = 1.0
    temperature = 180  # °F
    pressure = 2500  # psia
    gor = 550  # scf/STB
    
    print(f"API Gravity: {api_gravity}°")
    print(f"Gas Gravity: {gas_gravity}")
    print(f"Temperature: {temperature}°F")
    print(f"Pressure: {pressure:,} psia")
    print(f"Gas-Oil Ratio: {gor} scf/STB")
    print()
    
    # PVT calculations
    oil_fvf = petrocalc.reservoir.oil_formation_volume_factor_standing(
        gor, gas_gravity, api_gravity, temperature, pressure
    )
    bubble_point = petrocalc.reservoir.bubble_point_pressure_standing(
        gor, gas_gravity, api_gravity, temperature
    )
    oil_viscosity = petrocalc.reservoir.oil_viscosity_beggs_robinson(
        api_gravity, temperature, pressure, gor
    )
    
    print(f"Oil Formation Volume Factor: {oil_fvf:.3f} res bbl/STB")
    print(f"Bubble Point Pressure: {bubble_point:.0f} psia")
    print(f"Oil Viscosity: {oil_viscosity:.2f} cp")
    
    # Decline curve analysis
    initial_rate = 1200  # bbl/day
    decline_rate = 0.12  # annual
    time_years = 5
    
    current_rate = petrocalc.reservoir.arps_decline_curve(initial_rate, time_years, decline_rate)
    cumulative = petrocalc.reservoir.cumulative_production_arps(initial_rate, time_years, decline_rate)
    
    print(f"\nDecline Curve Analysis:")
    print(f"Initial rate: {initial_rate:,} bbl/day")
    print(f"After {time_years} years: {current_rate:.0f} bbl/day")
    print(f"Cumulative production: {cumulative:,.0f} bbls")
    print()


def production_example():
    """Demonstrate production engineering calculations"""
    print("=" * 60)
    print("PRODUCTION ENGINEERING CALCULATIONS")
    print("=" * 60)
    
    # Well performance
    reservoir_pressure = 3200  # psia
    max_rate = 1500  # STB/day
    
    print(f"Reservoir Pressure: {reservoir_pressure:,} psia")
    print(f"Maximum Oil Rate: {max_rate:,} STB/day")
    print()
    
    # IPR curve points
    print("Inflow Performance Relationship (IPR):")
    print("Pwf (psia)    Rate (STB/day)")
    print("-" * 30)
    
    for pwf in range(0, reservoir_pressure + 1, 500):
        rate = petrocalc.production.vogel_ipr(reservoir_pressure, pwf, max_rate)
        print(f"{pwf:8,}    {rate:10.0f}")
    
    # Productivity index
    test_rate = 800  # STB/day
    test_pwf = 2000  # psia
    pi = petrocalc.production.productivity_index(test_rate, reservoir_pressure, test_pwf)
    
    print(f"\nProductivity Index: {pi:.2f} STB/day/psi")
    
    # Gas well deliverability
    aof = 10000  # Mscf/day
    pr_gas = 3500  # psia
    pwf_gas = 2500  # psia
    
    gas_rate = petrocalc.production.gas_well_deliverability_rawlins_schellhardt(
        aof, pwf_gas, pr_gas
    )
    print(f"Gas production rate: {gas_rate:,.0f} Mscf/day")
    print()


def fluid_properties_example():
    """Demonstrate fluid properties calculations"""
    print("=" * 60)
    print("FLUID PROPERTIES CALCULATIONS")
    print("=" * 60)
    
    temperature = 180  # °F
    pressure = 2500  # psia
    
    # Water properties
    bw = petrocalc.fluids.water_formation_volume_factor(temperature, pressure, 100000)
    water_visc = petrocalc.fluids.water_viscosity(temperature, pressure, 100000)
    water_comp = petrocalc.fluids.water_compressibility(temperature, pressure, 100000)
    
    print("Water Properties:")
    print(f"Formation Volume Factor: {bw:.4f} res bbl/STB")
    print(f"Viscosity: {water_visc:.2f} cp")
    print(f"Compressibility: {water_comp:.2e} 1/psi")
    print()
    
    # Gas properties
    gas_gravity = 0.7
    temperature_r = temperature + 459.67  # Convert to Rankine
    z_factor = petrocalc.fluids.gas_compressibility_factor_standing(pressure, temperature_r, gas_gravity)
    gas_fvf = petrocalc.fluids.gas_formation_volume_factor(temperature_r, pressure, z_factor)
    gas_density = petrocalc.fluids.gas_density(pressure, temperature_r, 28.97 * gas_gravity, z_factor)
    
    print("Gas Properties:")
    print(f"Compressibility Factor: {z_factor:.3f}")
    print(f"Formation Volume Factor: {gas_fvf:.6f} res ft³/scf")
    print(f"Density: {gas_density:.3f} lb/ft³")
    print()


def economics_example():
    """Demonstrate economic calculations"""
    print("=" * 60)
    print("ECONOMIC ANALYSIS")
    print("=" * 60)
    
    # Project parameters
    initial_investment = 2500000  # $
    oil_price = 75  # $/bbl
    gas_price = 4.5  # $/Mscf
    oil_production = [800, 700, 600, 500, 450, 400, 350, 300, 250, 200]  # bbl/day by year
    operating_cost = 25  # $/bbl
    discount_rate = 0.12
    
    print(f"Initial Investment: ${initial_investment:,}")
    print(f"Oil Price: ${oil_price}/bbl")
    print(f"Operating Cost: ${operating_cost}/bbl")
    print(f"Discount Rate: {discount_rate:.1%}")
    print()
    
    # Calculate annual cash flows
    cash_flows = []
    for i, daily_rate in enumerate(oil_production):
        annual_revenue = petrocalc.economics.oil_revenue_calculation(
            daily_rate, oil_price, operating_cost_per_barrel=operating_cost
        )
        cash_flows.append(annual_revenue)
        print(f"Year {i+1}: {daily_rate} bbl/day → ${annual_revenue:,.0f}")
    
    print()
    
    # Economic indicators
    npv = petrocalc.economics.net_present_value(cash_flows, discount_rate, initial_investment)
    irr = petrocalc.economics.internal_rate_of_return(cash_flows, initial_investment)
    payback = petrocalc.economics.discounted_payback_period(cash_flows, discount_rate, initial_investment)
    pi = petrocalc.economics.profitability_index(cash_flows, discount_rate, initial_investment)
    
    print("Economic Indicators:")
    print(f"Net Present Value: ${npv:,.0f}")
    print(f"Internal Rate of Return: {irr:.1%}")
    print(f"Discounted Payback Period: {payback:.1f} years")
    print(f"Profitability Index: {pi:.2f}")
    
    # Break-even analysis
    breakeven_price = petrocalc.economics.break_even_oil_price(
        initial_investment, sum(oil_production) * 365 / len(oil_production), operating_cost
    )
    print(f"Break-even Oil Price: ${breakeven_price:.2f}/bbl")
    print()


def rock_properties_example():
    """Demonstrate rock properties calculations"""
    print("=" * 60)
    print("ROCK PROPERTIES CALCULATIONS")
    print("=" * 60)
    
    # Log analysis
    neutron_porosity = 0.25
    density_porosity = 0.22
    bulk_density = 2.35  # g/cm³
    formation_resistivity = 15  # ohm-m
    water_resistivity = 0.08  # ohm-m
    
    # Calculate porosity
    effective_porosity = petrocalc.rock_properties.porosity_from_logs(neutron_porosity, density_porosity)
    density_porosity_calc = petrocalc.rock_properties.porosity_from_density_log(bulk_density, 2.65, 1.0)
    
    print("Porosity Calculations:")
    print(f"From neutron-density logs: {effective_porosity:.3f}")
    print(f"From density log: {density_porosity_calc:.3f}")
    
    # Water saturation
    water_saturation = petrocalc.rock_properties.water_saturation_archie(
        formation_resistivity, water_resistivity, effective_porosity
    )
    
    print(f"Water saturation (Archie): {water_saturation:.3f}")
    
    # Permeability estimation
    permeability_timur = petrocalc.rock_properties.permeability_timur_correlation(
        effective_porosity, water_saturation
    )
    
    print(f"Permeability (Timur): {permeability_timur:.1f} md")
    
    # Relative permeability
    oil_rel_perm = petrocalc.rock_properties.relative_permeability_oil_corey(
        0.3, 0.2, 0.25
    )
    water_rel_perm = petrocalc.rock_properties.relative_permeability_water_corey(
        0.3, 0.2, 0.25
    )
    
    print(f"Oil relative permeability: {oil_rel_perm:.3f}")
    print(f"Water relative permeability: {water_rel_perm:.3f}")
    print()


def main():
    """Run all examples"""
    print("🛢️  PETROCALC LIBRARY - COMPREHENSIVE EXAMPLES")
    print("=" * 80)
    print()
    
    drilling_example()
    reservoir_example()
    production_example()
    fluid_properties_example()
    rock_properties_example()
    economics_example()
    
    print("=" * 80)
    print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
    print("This demonstrates the comprehensive capabilities of the PetroCalc library.")
    print("=" * 80)


if __name__ == "__main__":
    main()
