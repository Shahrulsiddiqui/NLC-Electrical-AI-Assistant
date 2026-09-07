class TroubleshootingFramework:
    TEMPLATES = {
        "Earth_Fault": "### 🌍 Earth Fault Analysis\n**Possible Causes:**\n* Insulation breakdown\n* Moisture ingress\n* Physical cable damage\n\n**Required Checks:**\n1. Isolate the affected circuit.\n2. Perform Megger/IR test on cables.\n3. Check relay targets and event logger.\n\n**Safety Note:** Do not re-energize until IR values are within statutory limits.",
        
        "Differential": "### ⚡ Transformer Differential (87T)\n**Possible Causes:**\n* Internal winding fault\n* CT saturation or ratio mismatch\n* Heavy inrush current\n\n**Required Checks:**\n1. Verify Buchholz gas accumulation.\n2. Check PRV status.\n3. Test winding resistance and DGA.\n\n**Safety Note:** A differential trip requires comprehensive internal inspection before charging.",
        
        "Buchholz": "### 🛢️ Buchholz Relay Alarm/Trip\n**Possible Causes:**\n* Low oil level\n* Insulation degradation generating gas\n* Severe internal short circuit\n\n**Required Checks:**\n1. Check for visible oil leaks.\n2. Collect gas from relay (test combustibility).\n3. Perform DGA (Dissolved Gas Analysis) on main tank oil.\n\n**Safety Note:** Do not reset trip without analyzing the trapped gas."
    }

    @classmethod
    def get_template(cls, fault_type: str) -> str:
        return cls.TEMPLATES.get(fault_type, "Diagnostic template not found. Refer to official plant SOPs.")
