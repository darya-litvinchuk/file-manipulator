import logging

from .config import get_settings

logging.basicConfig(
    level=get_settings().logger_level,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S",
)
logger = logging.getLogger(__name__)
