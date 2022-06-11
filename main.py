import configs
import logging

# =============================================================================
# ------------------------------ LOGGING CONFIG -------------------------------
# =============================================================================

logger: logging.Logger = logging.getLogger()

LOGGING_CONFIGS: dict = configs.LOGGING["DEV"] \
    if configs.LOGGING["DEV_ENV"] else configs.LOGGING["PROD"]

LOGGING_LEVEL: int = logging.DEBUG \
    if configs.LOGGING["DEV_ENV"] else logging.INFO

logging.basicConfig(filename=LOGGING_CONFIGS["PATH"],
                    level=LOGGING_LEVEL,
                    format=LOGGING_CONFIGS["MESSAGE"],
                    datefmt='%d-%m %H:%M:%S')

# =============================================================================
# ------------------------------- MAIN FUNCTION -------------------------------
# =============================================================================

if __name__ == "__main__":
    pass
