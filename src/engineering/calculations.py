import math

class ElectricalCalculators:
    @staticmethod
    def three_phase_current(power_mva: float, voltage_kv: float, pf: float) -> dict:
        if voltage_kv <= 0 or pf <= 0:
            return {"result": "Error: Invalid inputs", "units": "", "formula": ""}
        current = (power_mva * 1000) / (math.sqrt(3) * voltage_kv * pf)
        return {
            "result": round(current, 2), 
            "units": "A", 
            "formula": "I = S / (√3 × V × PF)"
        }

    @staticmethod
    def transformer_impedance(voltage_kv: float, base_mva: float, z_percent: float) -> dict:
        if base_mva <= 0:
            return {"result": "Error: Invalid base", "units": "", "formula": ""}
        z_ohms = (z_percent / 100) * ((voltage_kv ** 2) / base_mva)
        return {
            "result": round(z_ohms, 4), 
            "units": "Ω", 
            "formula": "Z(Ω) = (Z% / 100) × (V² / S)"
        }

    @staticmethod
    def three_phase_power(voltage_kv: float, current_a: float, pf: float) -> dict:
        if voltage_kv <= 0 or current_a < 0 or pf <= 0:
            return {"result": "Error: Invalid inputs", "units": "", "formula": ""}
        p_mw = (math.sqrt(3) * voltage_kv * current_a * pf) / 1000
        return {
            "result": round(p_mw, 2), 
            "units": "MW", 
            "formula": "P = (√3 × V × I × PF) / 1000"
        }
