import logging
import sys

def setup_logging(log_level: str = "INFO"):
    """
    Sets up structured logging for the application.
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

logger = logging.getLogger("ai_resume_analyzer")
