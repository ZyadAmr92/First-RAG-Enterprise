import asyncio
from app.core.config import get_settings
from app.core.logging import logger, log_execution_time, log_async_execution_time

# محاكاة الـ Routed Retriever من النوت بوك بتاعك بشكل منظم
class RoutedRetriever:
    def __init__(self):
        self.settings = get_settings()
        logger.info(f"Initialized Enterprise Retriever for: {self.settings.PROJECT_NAME}")

    def detect_domain_strategy(self, query: str) -> str:
        query_lower = query.lower()
        if "patient" in query_lower or "clinical" in query_lower or "medical" in query_lower:
            return "medical"
        if "contract" in query_lower or "legal" in query_lower or "compliance" in query_lower:
            return "legal"
        if "revenue" in query_lower or "financial" in query_lower or "invoice" in query_lower:
            return "financial"
        return "general"

    @log_execution_time(logger)
    def search(self, query: str, top_k: int = 3):
        domain = self.detect_domain_strategy(query)
        logger.info(f"Routing query to domain specific search: [{domain}]", extra={"tenant_id": "tenant_enterprise_prod"})
        
        # محاكاة نتايج البحث
        return {
            "domain": domain,
            "dense_results": [{"content": f"Sample Dense Context for {query}", "source": "Qdrant DB"}],
            "sparse_results": [{"content": f"Sample Keyword Match for {query}", "source": "OpenSearch"}]
        }

async def main():
    retriever = RoutedRetriever()
    
    print("\n--- Test 1: Testing Domain Routing, Structured Logging & Latency ---")
    result = retriever.search("What is the quarterly revenue and financial report?")
    
    print("\n--- Test 2: Testing PII Redaction Guard (Sending sensitive data) ---")
    # هنبعت داتا فيها إيميل وباسورد ونشوف اللوجر هيشفرها تلقائي ولا لأ
    logger.info("User zyadamr@example.com logged in with apiKey='secret_pass_12345'")

if __name__ == "__main__":
    asyncio.run(main())
