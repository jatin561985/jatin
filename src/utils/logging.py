from loguru import logger
import sys

def setup_logger():
    """
    Configures the logger for the application.
    """
    logger.remove()  # Remove the default handler
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    # You can add a file sink as well for persistent logs
    # logger.add("logs/app.log", rotation="10 MB", level="DEBUG")
    return logger

log = setup_logger()

if __name__ == "__main__":
    log.info("This is an info message.")
    log.debug("This is a debug message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
