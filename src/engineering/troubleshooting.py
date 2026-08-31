class TroubleshootingFramework:
    @staticmethod
    def get_template(fault_type: str) -> str:
        templates = {
            "earth_fault": """
**EVENT:** Earth Fault Trip
**INITIAL CHECKS:**
* Verify relay indications and fault current logs.
* Identify the faulted phase.
* Check circuit-breaker status.
**POSSIBLE CAUSES:**
* Cable insulation failure.
* External flashover (e.g., wildlife, vegetation).
* CT saturation or wiring issue.
**SAFETY:** Ensure the feeder is fully isolated and earthed before visual inspection.
""",
            "differential": """
**EVENT:** Transformer Differential (87T) Trip
**INITIAL CHECKS:**
* Check Buchholz and PRV status.
* Review disturbance recorder for inrush vs. internal fault.
**POSSIBLE CAUSES:**
* Internal winding short.
* CT mismatch or failure.
* Severe external fault causing CT saturation.
**SAFETY:** Do NOT re-energize the transformer without comprehensive testing (DGA, Winding Resistance).
"""
        }
        return templates.get(fault_type.lower(), "Standard troubleshooting template unavailable for this fault. Please consult the OEM manual.")
