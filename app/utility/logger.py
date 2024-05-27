from loguru import logger
import sys

# Remove default handler to avoid duplicate logs
logger.remove()

# Add new handler with the desired configuration
logger.add(
	sys.stdout,
	level="INFO",
	format="[<green>{time:DD/MMM/YYYY HH:mm:ss}</green>] <level>{level}</level> [<cyan>{name}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan>] <level>{message}</level>",
)
