from enum import Enum

class RiskLevel(Enum):
    LOW = "Educational/General"
    NORMAL = "Engineering Analysis"
    HIGH = "Safety-Critical/Operational"

class SafetyClassifier:
    HIGH_RISK_KEYWORDS = ["close", "open", "trip", "energize", "isolate", "permit", "setting"]
    
    @classmethod
    def classify_query(cls, query: str) -> RiskLevel:
        query_lower = query.lower()
        if any(word in query_lower for word in cls.HIGH_RISK_KEYWORDS):
            return RiskLevel.HIGH
        if "why" in query_lower or "explain" in query_lower:
            return RiskLevel.NORMAL
        return RiskLevel.LOW
        
    @staticmethod
    def get_safety_disclaimer(risk_level: RiskLevel) -> str:
        if risk_level == RiskLevel.HIGH:
            return "⚠️ CRITICAL: I cannot authorize plant operations or verify protection settings. Refer to approved plant SOPs and consult authorized control-room personnel."
        return ""
