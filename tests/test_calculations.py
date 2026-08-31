import pytest
from src.engineering.calculations import ElectricalCalculators

def test_three_phase_current_calculation():
    # 10 MVA, 11 kV, 0.85 PF -> I = 10000 / (sqrt(3) * 11 * 0.85) = 618.04 A
    result = ElectricalCalculators.three_phase_current(power_mva=10.0, voltage_kv=11.0, pf=0.85)
    
    assert "error" not in result
    assert result["result"] == 618.04
    assert result["units"] == "A"

def test_three_phase_current_zero_voltage():
    result = ElectricalCalculators.three_phase_current(power_mva=10.0, voltage_kv=0.0)
    assert "error" in result

def test_transformer_impedance_calculation():
    # 11 kV, 10 MVA, 5% Z -> Z_base = 121 / 10 = 12.1 Ohms, Z_actual = 12.1 * 0.05 = 0.605 Ohms
    result = ElectricalCalculators.transformer_impedance(voltage_kv=11.0, mva_base=10.0, percent_z=5.0)
    
    assert "error" not in result
    assert result["result"] == 0.605
    assert result["units"] == "Ohms"
