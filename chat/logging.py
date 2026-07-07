import logging
from chat.middleware import correlation_context

class CorrelationFilter(logging.Filter):
    """
    Logging filter that injects the request correlation_id into the log record.
    """
    def filter(self, record):
        record.correlation_id = correlation_context.get() or '-'
        return True
