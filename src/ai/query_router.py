from enum import Enum

class QueryType(Enum):
    CALCULATION = "CALCULATION"
    DOCUMENT_LOOKUP = "DOCUMENT_LOOKUP"
    TROUBLESHOOTING = "TROUBLESHOOTING"
    GENERAL_ENGINEERING = "GENERAL_ENGINEERING"
    UNKNOWN = "UNKNOWN"

class QueryRouter:
    @classmethod
    def route_query(cls, query: str) -> QueryType:
        query_lower = query.lower()
        
        if any(kw in query_lower for kw in ["calculate", "formula", "value of", "compute"]):
            return QueryType.CALCULATION
        elif any(kw in query_lower for kw in ["tripped", "fault on", "alarm", "diagnose"]):
            return QueryType.TROUBLESHOOTING
        elif any(kw in query_lower for kw in ["according to manual", "in the sop", "document says"]):
            return QueryType.DOCUMENT_LOOKUP
        elif any(kw in query_lower for kw in ["what is", "explain", "how does"]):
            return QueryType.GENERAL_ENGINEERING
            
        return QueryType.UNKNOWN
