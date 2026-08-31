import math
from typing import Dict, Any

class ElectricalCalculators:
    @staticmethod
    def three_phase_current(power_mva: float, voltage_kv: float, pf: float = 0.85) -> Dict[str, Any]:
        """Calculates three-phase full-load current."""
        if voltage_kv <= 0:
            return {"error": "Voltage must be greater than zero."}
            
        current_amps = (power_mva * 1000) / (math.sqrt(3) * voltage_kv * pf)
        
        return {
            "formula": "I = S / (√3 × V × PF)",
            "inputs": {"Power (MVA)": power_mva, "Voltage (kV)": voltage_kv, "Power Factor": pf},
            "result": round(current_amps, 2),
            "units": "A",
            "assumptions": "Balanced three-phase system."
        }
        
    @staticmethod
    def transformer_impedance(voltage_kv: float, mva_base: float, percent_z: float) -> Dict[str, Any]:
        """Calculates transformer base impedance and actual impedance in Ohms."""
        if mva_base <= 0 or percent_z <= 0:
            return {"error": "MVA base and %Z must be greater than zero."}
            
        z_base = (voltage_kv ** 2) / mva_base
        z_actual = z_base * (percent_z / 100)
        
        return {
            "formula": "Z_base = V² / S, Z_actual = Z_base × (%Z / 100)",
            "inputs": {"Voltage (kV)": voltage_kv, "Base (MVA)": mva_base, "% Impedance": percent_z},
            "result": round(z_actual, 4),
            "units": "Ohms",
            "assumptions": "Calculated on the specified voltage side."
        }
