import os
from typing import List, Optional, Literal
from pydantic import Field, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

class EnterpriseSettings(BaseSettings):
    # Core Infrastructure Routing
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True
    PROJECT_NAME: str = "Enterprise RAG Platform"
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Storage & Data Strategy
    DEFAULT_DOMAINS: List[str] = ["medical", "financial", "legal", "general"]
    ENABLE_HEADER_TENANCY: bool = True
    ROUTING_STRATEGY: str = "domain_specific"
    
    # Advanced Vector DB & Hybrid Search Connections
    QDRANT_URL: str = Field(default="http://localhost:6333")
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_PREFER_GRPC: bool = True
    
    OPENSEARCH_HOST: str = "localhost"
    OPENSEARCH_PORT: int = 9200
    OPENSEARCH_USER: str = "admin"
    OPENSEARCH_PASSWORD: str = "admin"
    
    # LLM and Multi-Token Specs
    LLM_PROVIDER: Literal["ollama", "openai", "vllm", "azure"] = "ollama"
    LLM_MODEL: str = "qwen2.5-coder:7b"
    EMBEDDING_PROVIDER: str = "ollama"
    EMBEDDING_MODEL: str = "bge-m3"
    EMBEDDING_DIMENSION: int = Field(default=1024)
    
    # Asynchronous Middleware & Cache
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    KAFKA_BOOTSTRAP_SERVERS: List[str] = ["localhost:9092"]
    
    # Chunking Architecture & Multi-Tenant Pipeline Specs
    CHUNK_SIZE: int = Field(default=512, gt=0)
    CHUNK_OVERLAP: int = Field(default=64, ge=0)
    PARENT_CHUNK_SIZE: int = Field(default=2048, gt=0)
    AWS_S3_BUCKET_NAME: str = "enterprise-rag-chunks"
    
    # Compliance & Security Shield
    PII_REDACTION_ENABLED: bool = True
    AUDIT_LOG_RETENTION_DAYS: int = 365
    MAX_COST_LIMIT_USD: float = 100.0

    @field_validator("EMBEDDING_DIMENSION", mode="before")
    @classmethod
    def resolve_dimensions(cls, v: Optional[int], info: ValidationInfo) -> int:
        if v is not None:
            return v
        provider = info.data.get("EMBEDDING_PROVIDER", "ollama")
        model = info.data.get("EMBEDDING_MODEL", "")
        if "bge-m3" in model:
            return 1024
        if "text-embedding-3-small" in model:
            return 1536
        return 768

    @field_validator("CHUNK_OVERLAP")
    @classmethod
    def validate_overlap(cls, v: int, info: ValidationInfo) -> int:
        chunk_size = info.data.get("CHUNK_SIZE", 512)
        if v >= chunk_size:
            raise ValueError("CHUNK_OVERLAP must be strictly less than CHUNK_SIZE")
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

def get_settings() -> EnterpriseSettings:
    return EnterpriseSettings()
