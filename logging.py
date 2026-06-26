import json
import logging
import re
import time
from functools import wraps
from typing import Any, Dict

class PIIAndStructuredFormatter(logging.Formatter):
    def __init__(self, fmt: str = None, datefmt: str = None):
        super().__init__(fmt, datefmt)
        # أنماط الحماية لبيانات الـ PII والـ Secrets
        self.email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.api_key_regex = re.compile(r'(?i)(api[_-]?key|secret|password|token)["\s]*[:=]["\s]*([a-zA-Z0-9_\-]{8,})')

    def redact_pii(self, text: str) -> str:
        if not isinstance(text, str):
            return text
        text = self.email_regex.sub("[REDACTED_EMAIL]", text)
        text = self.api_key_regex.sub(r'=": [REDACTED_SECRET]"', text)
        return text

    def format(self, record: logging.LogRecord) -> str:
        # بناء الـ Structured JSON Schema للمؤسسات
        log_data: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": self.redact_pii(record.getMessage()),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # دمج أي معلومات إضافية مرسلة عبر الـ extra
        if hasattr(record, "tenant_id"):
            log_data["tenant_id"] = record.tenant_id
        if hasattr(record, "latency_ms"):
            log_data["latency_ms"] = record.latency_ms
            
        return json.dumps(log_data)

def setup_logging(env: str = "development") -> logging.Logger:
    logger = logging.getLogger("EnterpriseRAG")
    logger.setLevel(logging.DEBUG if env == "development" else logging.INFO)
    logger.handlers.clear()
    
    # Stream Handler للمخرجات الحية
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(PIIAndStructuredFormatter())
    logger.addHandler(stream_handler)
    
    # File Handler لحفظ السجلات في بيئة الإنتاج
    os.makedirs("logs", exist_ok=True)
    file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
    file_handler.setFormatter(PIIAndStructuredFormatter())
    logger.addHandler(file_handler)
    
    return logger

# إنشاء نسخة لوجر جاهزة للاستخدام
from app.core.config import get_settings
settings = get_settings()
logger = setup_logging(settings.ENVIRONMENT)

# Decorators لحساب الأداء والـ Metrics
def log_execution_time(target_logger: logging.Logger):
    def decorator(func):
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                latency = (time.perf_counter() - start_time) * 1000
                target_logger.info(f"Executed sync function: {func.__name__}", extra={"latency_ms": round(latency, 2)})
                return result
            except Exception as e:
                latency = (time.perf_counter() - start_time) * 1000
                target_logger.error(f"Failed sync function: {func.__name__} - Error: {str(e)}", extra={"latency_ms": round(latency, 2)})
                raise e
        return sync_wrapper
    return decorator

def log_async_execution_time(target_logger: logging.Logger):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                latency = (time.perf_counter() - start_time) * 1000
                target_logger.info(f"Executed async function: {func.__name__}", extra={"latency_ms": round(latency, 2)})
                return result
            except Exception as e:
                latency = (time.perf_counter() - start_time) * 1000
                target_logger.error(f"Failed async function: {func.__name__} - Error: {str(e)}", extra={"latency_ms": round(latency, 2)})
                raise e
        return async_wrapper
    return decorator
