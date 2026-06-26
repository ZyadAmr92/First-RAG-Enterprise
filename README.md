# First-RAG-Enterprise
A production-ready, highly configurable Enterprise RAG Platform featuring multi-tenancy, hybrid search (Qdrant + OpenSearch), structured JSON logging with PII redaction, and enterprise observability
# Enterprise RAG Platform (Core Architecture)

A production-ready, highly scalable, and secure Retrieval-Augmented Generation (RAG) Platform engineered for enterprise deployment. The platform features strict configuration management, multi-tenant safety, multi-provider LLM support, hybrid search capabilities, and robust asynchronous structured logging.

## 🚀 Key Features Built-in

- **Enterprise Configuration Engine**: Powered by `Pydantic-Settings` with strict validation for chunk configurations, custom multi-token metrics, and dynamic embedding dimension resolvers.
- **Advanced Structured JSON Logging**: Emits production-grade JSON logs optimized for Logstash/Datadog/Grafana integration.
- **Automated PII Redaction Layer**: Intercepts and masks sensitive user data (Emails, Credit Cards, API Keys) out-of-the-box using safe regex filters before writing logs.
- **Performance & Observability Decorators**: Built-in context-aware latency tracking for sync and async operations (Retrieval, Ingestion, Generation).
- **Enterprise-Grade Strategy Ready**: Out-of-the-box specifications for:
  - Hybrid Search (`Qdrant` for Vector + `OpenSearch` for Keyword matching).
  - Multi-Tenancy segregation via secure headers.
  - Distributed caching via `Redis` with TTL controls.
  - Event-driven processing compatibility via `Kafka`.

## 🏗️ Core Architecture & Component Blueprint

- **LLM Layer**: Configured for flexible switching between enterprise options (`OpenAI`, `Anthropic`, `Azure`) and local edge execution models (`Ollama` with `qwen2.5-coder`, `vLLM`).
- **Chunking Pipeline**: Strict validation logic supporting advanced semantic hierarchies (Parent-Child chunking models).
- **Resilience**: Configured with automated background backup routines, token budgeting, and custom USD cost controls per environment.

## 📁 Environment Setup


```text
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
qdrant-client>=1.7.0
opensearch-py>=2.4.0
redis>=5.0.0
kafka-python>=2.0.2
asyncio>=3.4.3


   # Core DB Configuration

QDRANT_URL="http://localhost:6333"
QDRANT_API_KEY="your_secure_api_key_here"
OPENSEARCH_HOST="localhost"
OPENSEARCH_PORT=9200

# LLM Controls
LLM_PROVIDER="ollama"
LLM_MODEL="qwen2.5-coder:7b"

# Optional Providers
OPENAI_API_KEY="your-openai-key-if-provider-is-openai"



EXAMPLE:
from app.core.config import get_settings
from app.core.logging import logger, log_execution_time

settings = get_settings()
print(f"Loaded platform for Environment: {settings.ENVIRONMENT}")

@log_execution_time(logger)
async def sample_retrieval_pipeline(query: str):
    logger.info("Initiating secure retrieval process...", extra={"tenant_id": "client_alpha"})
    # Platform automatically handles PII redaction and records execution metrics
    return "Retrieved Data Chunk"
