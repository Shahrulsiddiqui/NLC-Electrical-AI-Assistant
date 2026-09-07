from src.engineering.calculations import ElectricalCalculators

def test_three_phase_current():
    # 10 MVA, 11 kV, 0.85 PF
    res = ElectricalCalculators.three_phase_current(10.0, 11.0, 0.85)
    assert res["result"] == 617.49
    assert res["units"] == "A"

def test_three_phase_current_zero_voltage():
    # Should catch division by zero
    res = ElectricalCalculators.three_phase_current(10.0, 0.0, 0.85)
    assert "Error" in str(res["result"])

def test_transformer_impedance():
    # 11 kV, 10 MVA, 5% Z
    res = ElectricalCalculators.transformer_impedance(11.0, 10.0, 5.0)
    assert res["result"] == 0.605

def test_three_phase_power():
    # 11 kV, 500 A, 0.85 PF
    res = ElectricalCalculators.three_phase_power(11.0, 500.0, 0.85)
    assert res["result"] == 8.10
