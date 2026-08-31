from enum import Enum

class QueryType(Enum):
    DOCUMENT_LOOKUP = "DOCUMENT_LOOKUP"
    TROUBLESHOOTING = "TROUBLESHOOTING"
    CALCULATION = "CALCULATION"
    PROCEDURE = "PROCEDURE"
    GENERAL = "GENERAL"

class QueryRouter:
    @staticmethod
    def route_query(query: str) -> QueryType:
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["calculate", "current", "voltage drop", "power factor"]):
            return QueryType.CALCULATION
            
        if any(word in query_lower for word in ["tripped", "check", "fault", "alarm", "cause"]):
            return QueryType.TROUBLESHOOTING
            
        if any(word in query_lower for word in ["procedure", "step", "how to"]):
            return QueryType.PROCEDURE
            
        if any(word in query_lower for word in ["what is", "explain", "difference"]):
            return QueryType.GENERAL
            
        return QueryType.DOCUMENT_LOOKUP
