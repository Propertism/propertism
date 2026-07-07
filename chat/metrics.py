import threading

class InfrastructureMetrics:
    """
    Thread-safe registry for realBOT infrastructure counters.
    """
    _lock = threading.Lock()
    _metrics = {
        "app_startup_count": 0,
        "active_sessions_count": 0,
        "conversation_count": 0,
        "health_requests": 0,
        "failed_requests": 0,
        "configuration_errors": 0,
    }

    @classmethod
    def increment(cls, key, count=1):
        with cls._lock:
            if key in cls._metrics:
                cls._metrics[key] += count

    @classmethod
    def get_all(cls):
        with cls._lock:
            # Dynamically resolve database counts
            try:
                from chat.models import RealBotSession
                cls._metrics["conversation_count"] = RealBotSession.objects.count()
            except Exception:
                pass
            return cls._metrics.copy()
