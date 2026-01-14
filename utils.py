"""
Utility functions for Social Media Listen Tool
Common helpers to avoid code duplication
"""

import os
import glob
import logging
from datetime import datetime
from typing import Optional
from pathlib import Path

from config import DATA_PROCESSING, FILE_PATTERNS


def get_timestamp() -> str:
    """
    Get current timestamp in standardized format
    
    Returns:
        Formatted timestamp string (YYYY-MM-DD_HH-MM-SS)
    """
    return datetime.now().strftime(DATA_PROCESSING["timestamp_format"])


def find_latest_file(folder: str, pattern: str) -> Optional[str]:
    """
    Find the most recent file matching pattern in folder
    
    Args:
        folder: Directory to search in
        pattern: Glob pattern to match
        
    Returns:
        Path to latest file or None if not found
    """
    search_pattern = os.path.join(folder, pattern)
    list_of_files = glob.glob(search_pattern)
    
    if not list_of_files:
        return None
    
    return max(list_of_files, key=os.path.getmtime)


def ensure_dir_exists(directory: str) -> None:
    """
    Create directory if it doesn't exist
    
    Args:
        directory: Path to directory
    """
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Setup logger with standardized format
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    handler = logging.StreamHandler()
    handler.setLevel(getattr(logging, level))
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


def get_file_basename(filepath: str) -> str:
    """
    Get filename without path
    
    Args:
        filepath: Full file path
        
    Returns:
        Filename only
    """
    return os.path.basename(filepath)


def validate_csv_columns(df, required_columns: list) -> bool:
    """
    Check if DataFrame has required columns
    
    Args:
        df: pandas DataFrame
        required_columns: List of column names
        
    Returns:
        True if all columns exist, False otherwise
    """
    return all(col in df.columns for col in required_columns)
