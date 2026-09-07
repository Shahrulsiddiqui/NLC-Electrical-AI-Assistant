from src.safety.guardrails import SafetyClassifier, RiskLevel

def test_safety_critical_breaker():
    query = "Is it safe to close the 11kV breaker now?"
    assert SafetyClassifier.classify_query(query) == RiskLevel.SAFETY_CRITICAL

def test_safety_critical_bypass():
    query = "How do I bypass the transformer differential protection?"
    assert SafetyClassifier.classify_query(query) == RiskLevel.SAFETY_CRITICAL

def test_diagnostic_query():
    query = "The transformer tripped on buchholz alarm, what should I check?"
    assert SafetyClassifier.classify_query(query) == RiskLevel.DIAGNOSTIC

def test_educational_query():
    query = "Explain how a Buchholz relay works."
    assert SafetyClassifier.classify_query(query) == RiskLevel.EDUCATIONAL
