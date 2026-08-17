# =====================================================
# AIOps Logging Module
# =====================================================

import logging
import os

# Create logs directory automatically
os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/aiops.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("AIOps")