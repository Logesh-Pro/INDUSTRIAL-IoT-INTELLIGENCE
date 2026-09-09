import os
import platform
import time

import psutil

from backend.config.settings import settings


START_TIME = time.time()


class SystemService:

    def get_status(self):
        uptime = int(time.time() - START_TIME)

        memory = psutil.virtual_memory()

        return {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "cpu_usage_percent": psutil.cpu_percent(interval=0.2),
            "memory_usage_percent": memory.percent,
            "memory_total_mb": round(memory.total / (1024 * 1024)),
            "memory_available_mb": round(memory.available / (1024 * 1024)),
            "process_id": os.getpid(),
            "uptime_seconds": uptime
        }
