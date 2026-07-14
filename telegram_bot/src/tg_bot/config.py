import logging
import sys
from pathlib import Path

# region Set up logging
# Create dir if not exist
LOGS_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE_PATH = LOGS_DIR / "bot.log"

# Define format for logs
LOG_FORMAT = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Setup the Root Logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Stream logs in terminal
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(LOG_FORMAT)
root_logger.addHandler(stdout_handler)

# Stream logs to a file
file_handler = logging.FileHandler(LOG_FILE_PATH, encoding="utf-8")
file_handler.setFormatter(LOG_FORMAT)
root_logger.addHandler(file_handler)
