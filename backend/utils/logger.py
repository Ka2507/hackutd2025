"""
Logging configuration for ProdPlex.

Sets up structured logging with both file and console handlers.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(
    name: str = "prodigypm",
    level: int = logging.INFO
) -> logging.Logger:
    """
    Setup and configure logger with file and console handlers.
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if logger.handlers:
        return logger
    
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - '
        '%(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / (
        f"prodigypm_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    return logger


logger = setup_logger()
