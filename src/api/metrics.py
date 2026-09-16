from threading import Lock
from time import perf_counter


class ApiMetrics:

    def __init__(self):
        self._lock = Lock()
        self._started_at = perf_counter()
        self._requests = 0
        self._successful_requests = 0
        self._failed_requests = 0
        self._total_latency_ms = 0.0

    def record(self, latency_ms: float, successful: bool) -> None:
        with self._lock:
            self._requests += 1
            self._total_latency_ms += latency_ms

            if successful:
                self._successful_requests += 1
            else:
                self._failed_requests += 1

    def snapshot(self) -> dict[str, float | int]:
        with self._lock:
            average_latency_ms = (
                self._total_latency_ms / self._requests
                if self._requests
                else 0.0
            )

            return {
                "uptime_seconds": round(
                    perf_counter() - self._started_at,
                    2,
                ),
                "requests_total": self._requests,
                "requests_successful": self._successful_requests,
                "requests_failed": self._failed_requests,
                "average_latency_ms": round(
                    average_latency_ms,
                    2,
                ),
            }


api_metrics = ApiMetrics()
