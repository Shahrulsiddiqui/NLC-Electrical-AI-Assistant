from src.safety.guardrails import SafetyClassifier, RiskLevel

def test_safety_critical_operational_query():
    query = "Should I close this 11 kV breaker right now?"
    risk = SafetyClassifier.classify_query(query)
    
    assert risk == RiskLevel.HIGH
    disclaimer = SafetyClassifier.get_safety_disclaimer(risk)
    assert "SAFETY NOTICE" in disclaimer

def test_safety_educational_query():
    query = "Explain transformer differential protection."
    risk = SafetyClassifier.classify_query(query)
    
    assert risk == RiskLevel.NORMAL or risk == RiskLevel.LOW
    disclaimer = SafetyClassifier.get_safety_disclaimer(risk)
    assert disclaimer == ""
