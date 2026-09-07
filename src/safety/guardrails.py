from enum import Enum
import re

class RiskLevel(Enum):
    EDUCATIONAL = 1
    ANALYTICAL = 2
    DIAGNOSTIC = 3
    PROCEDURAL = 4
    OPERATIONAL = 5
    SAFETY_CRITICAL = 6

class SafetyClassifier:
    CRITICAL_PATTERNS = [
        r"\b(energize|de-energize|isolate)\b",
        r"\b(close|open)\s+(breaker|switch|isolator)\b",
        r"\b(bypass|reset)\s+(protection|relay|interlock)\b",
        r"\b(change|modify)\s+(setting|parameter)\b",
        r"\b(restore\s+supply|synchronize\s+generator)\b"
    ]

    @classmethod
    def classify_query(cls, query: str) -> RiskLevel:
        query_lower = query.lower()
        for pattern in cls.CRITICAL_PATTERNS:
            if re.search(pattern, query_lower):
                return RiskLevel.SAFETY_CRITICAL
        
        if any(word in query_lower for word in ["trip", "fault", "alarm", "check"]):
            return RiskLevel.DIAGNOSTIC
            
        return RiskLevel.EDUCATIONAL

    @classmethod
    def get_safety_disclaimer(cls, risk_level: RiskLevel) -> str:
        if risk_level == RiskLevel.SAFETY_CRITICAL:
            return "⚠️ **SAFETY WARNING:** This assistant cannot authorize switching operations. Verify the applicable approved switching procedure, consult plant SOPs, and obtain required permits (LOTO) before operating any equipment."
        elif risk_level == RiskLevel.DIAGNOSTIC:
            return "ℹ️ **DIAGNOSTIC NOTICE:** Information provided is for preliminary analysis. Do not reset protection relays or re-energize equipment without a qualified engineering inspection."
        return ""
