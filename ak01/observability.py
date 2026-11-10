from __future__ import annotations

import logging
import time
from contextlib import contextmanager

logger = logging.getLogger("ak01")


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


@contextmanager
def operation(name: str, **fields):
    started = time.perf_counter()
    logger.info("operation.start %s %s", name, fields)
    try:
        yield
    except Exception:
        logger.exception("operation.error %s %s", name, fields)
        raise
    finally:
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info("operation.end %s elapsed_ms=%.2f %s", name, elapsed_ms, fields)
