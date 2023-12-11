import logging


def setup_logger(
    name: str, log_file: str, level: int = logging.INFO, console_logging: bool = False
):
    """
    Set up a logger for a given application.

    Parameters:
    - name: Name of the logger.
    - log_file: File path for the log file.
    - level: Logging level, e.g., logging.INFO.
    - console_logging: If True, also log to the console.
    """

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(level)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)

    if console_logging:
        # Create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
