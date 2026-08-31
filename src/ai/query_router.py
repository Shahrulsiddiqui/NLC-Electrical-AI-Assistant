class QueryRouter:
    @staticmethod
    def route_query(query: str) -> str:
        query_lower = query.lower()
        if "calculate" in query_lower or "current" in query_lower:
            return "CALCULATION"
        if "tripped" in query_lower or "check" in query_lower or "fault" in query_lower:
            return "TROUBLESHOOTING"
        if "procedure" in query_lower or "step" in query_lower:
            return "PROCEDURE"
        return "DOCUMENT_LOOKUP"
