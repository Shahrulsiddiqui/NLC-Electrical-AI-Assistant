import math
from typing import Dict, Any

class ElectricalCalculations:
    @staticmethod
    def three_phase_current(power_mva: float, voltage_kv: float) -> Dict[str, Any]:
        """Calculates three-phase full-load current."""
        if voltage_kv <= 0:
            raise ValueError("Voltage must be greater than zero.")
            
        current_amps = (power_mva * 1e6) / (math.sqrt(3) * voltage_kv * 1000)
        
        return {
            "formula": "I = S / (√3 × V)",
            "inputs": {"S (MVA)": power_mva, "V (kV)": voltage_kv},
            "result_amps": round(current_amps, 2),
            "units": "A"
        }
