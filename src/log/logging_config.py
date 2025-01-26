import logging

def _configure_handler(logger: logging.Logger, level: int) -> None:
    """
    Helper function to configure a handler for a logger.
    
    Args:
        logger: The logger to configure.
        level: Logging level.
        format_str: Format string for the log messages.
        date_format: Date format for the log messages.
    """
    handler = logging.StreamHandler()
    date_format = '%m-%d %H:%M'
    format_str = '%(name).2s %(levelname).1s - %(filename)s:%(lineno)d - %(message)s'
    
    formatter = logging.Formatter(format_str, date_format)
    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)

def setup_root_logging(level: int = logging.INFO) -> None:
    """
    Configure the root logger with the specified logging level and format.
    
    Args:
        level: Logging level (default: logging.INFO).
    """
    
    root_logger = logging.getLogger()
    _configure_handler(root_logger, level)

    logging.captureWarnings(True)  # Redirect warnings to the logging system

    # Hide potentially noisy third-party logs
    for log_name in ["httpx", "httpcore", "telegram", "apscheduler"]:
        logging.getLogger(log_name).setLevel(logging.WARNING)

def setup_logging(
    name: str,
    level: int = logging.INFO,
) -> None:
    """
    Configure logging settings for the application.
    
    Args:
        name: Name of the logger.
        level: Logging level (default: logging.INFO).
    """
    logger = logging.getLogger(name)
    logger.propagate = False  # Prevent the logger from sending messages to the root logger, avoiding duplicates.

    # Configure the specific logger
    _configure_handler(logger, level)
