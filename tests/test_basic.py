"""
Test file for basic functionality of all modules.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import petrocalc

def test_drilling_module():
    """Test basic drilling calculations"""
    print("Testing drilling module...")
    
    # Test mud weight to pressure gradient
    gradient = petrocalc.drilling.mud_weight_to_pressure_gradient(12.0, "ppg")
    print(f"Mud weight 12 ppg = {gradient:.3f} psi/ft")
    assert abs(gradient - 0.624) < 0.001
    
    # Test hydrostatic pressure
    pressure = petrocalc.drilling.hydrostatic_pressure(12.0, 10000, "ppg")
    print(f"Hydrostatic pressure at 10,000 ft with 12 ppg mud = {pressure:.0f} psi")
    assert abs(pressure - 6240) < 1
    
    print("✓ Drilling module tests passed\n")


def test_reservoir_module():
    """Test basic reservoir calculations"""
    print("Testing reservoir module...")
    
    # Test oil formation volume factor
    bo = petrocalc.reservoir.oil_formation_volume_factor_standing(
        gas_oil_ratio=500, gas_gravity=0.7, oil_gravity=35, 
        temperature=180, pressure=2500
    )
    print(f"Oil FVF = {bo:.3f} res bbl/STB")
    assert 1.0 < bo < 2.0
    
    # Test bubble point pressure
    pb = petrocalc.reservoir.bubble_point_pressure_standing(
        gas_oil_ratio=500, gas_gravity=0.7, oil_gravity=35, temperature=180
    )
    print(f"Bubble point pressure = {pb:.0f} psia")
    assert pb > 0
    
    print("✓ Reservoir module tests passed\n")


def test_production_module():
    """Test basic production calculations"""
    print("Testing production module...")
    
    # Test Vogel IPR
    rate = petrocalc.production.vogel_ipr(
        reservoir_pressure=3000, bottomhole_pressure=2000, maximum_oil_rate=1000
    )
    print(f"Oil production rate = {rate:.0f} STB/day")
    assert 0 < rate < 1000
    
    # Test productivity index
    pi = petrocalc.production.productivity_index(
        flow_rate=500, reservoir_pressure=3000, bottomhole_pressure=2500
    )
    print(f"Productivity index = {pi:.2f} STB/day/psi")
    assert pi > 0
    
    print("✓ Production module tests passed\n")


def test_fluids_module():
    """Test basic fluid properties"""
    print("Testing fluids module...")
    
    # Test water formation volume factor
    bw = petrocalc.fluids.water_formation_volume_factor(
        temperature=180, pressure=2500, salinity=50000
    )
    print(f"Water FVF = {bw:.4f} res bbl/STB")
    assert 0.9 < bw < 1.2
    
    # Test gas compressibility factor
    z = petrocalc.fluids.gas_compressibility_factor_standing(
        pressure=2000, temperature=640, gas_gravity=0.7
    )
    print(f"Gas compressibility factor = {z:.3f}")
    assert 0.2 < z < 2.0
    
    print("✓ Fluids module tests passed\n")


def test_rock_properties_module():
    """Test basic rock properties"""
    print("Testing rock properties module...")
    
    # Test porosity from density log
    phi = petrocalc.rock_properties.porosity_from_density_log(
        bulk_density=2.3, matrix_density=2.65, fluid_density=1.0
    )
    print(f"Porosity from density log = {phi:.2f}")
    assert 0 <= phi <= 1
    
    # Test water saturation using Archie's equation
    sw = petrocalc.rock_properties.water_saturation_archie(
        formation_resistivity=10, water_resistivity=0.1, porosity=0.2
    )
    print(f"Water saturation = {sw:.2f}")
    assert 0 <= sw <= 1
    
    print("✓ Rock properties module tests passed\n")


def test_economics_module():
    """Test basic economic calculations"""
    print("Testing economics module...")
    
    # Test NPV calculation
    cash_flows = [100000, 150000, 120000, 90000]
    npv = petrocalc.economics.net_present_value(
        cash_flows=cash_flows, discount_rate=0.1, initial_investment=400000
    )
    print(f"NPV = ${npv:,.0f}")
    
    # Test break-even oil price
    breakeven = petrocalc.economics.break_even_oil_price(
        initial_investment=1000000, annual_production=50000, 
        operating_cost_per_barrel=25
    )
    print(f"Break-even oil price = ${breakeven:.2f}/bbl")
    assert breakeven > 0
    
    print("✓ Economics module tests passed\n")


def main():
    """Run all tests"""
    print("=" * 50)
    print("PETROCALC LIBRARY TEST SUITE")
    print("=" * 50)
    print()
    
    try:
        test_drilling_module()
        test_reservoir_module()
        test_production_module()
        test_fluids_module()
        test_rock_properties_module()
        test_economics_module()
        
        print("=" * 50)
        print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
        print("PetroCalc library is ready for use.")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
