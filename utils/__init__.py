from config import Config
import logging


# Set up logging
logger = logging.getLogger()
log_level = Config["log_level"]
logger.setLevel(log_level)