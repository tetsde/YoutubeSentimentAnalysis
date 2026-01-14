"""
Configuration file for Social Media Listen Tool
Centralized constants to avoid hard-coding throughout the project
"""

from pathlib import Path

# ==================== PATHS ====================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RESULT_DIR = BASE_DIR / "result"
MODULES_DIR = BASE_DIR / "modules"
REPORTS_DIR = BASE_DIR / "reports"

# Model paths
MODEL_FILE = MODULES_DIR / "model.pkl"
STOPWORDS_FILE = DATA_DIR / "stopwords.txt"

# ==================== SCRAPER SETTINGS ====================
SCRAPER = {
    "headless": True,
    "window_size": "1920,1080",
    "scroll_time": 30,
    "scroll_delay_min": 2,
    "scroll_delay_max": 4,
    "wait_timeout": 15,
}

# ==================== DATA PROCESSING ====================
DATA_PROCESSING = {
    "text_column": "comment",
    "output_encoding": "utf-8-sig",
    "timestamp_format": "%Y-%m-%d_%H-%M-%S",
}

# ==================== MODEL SETTINGS ====================
MODEL = {
    "alpha": 1.0,  # Laplace smoothing for MultinomialNB
    "min_df": 1,   # Minimum document frequency for CountVectorizer
}

# Label mapping
SENTIMENT_LABELS = {
    0: "Positive",
    1: "Neutral", 
    2: "Negative"
}

# ==================== VISUALIZATION ====================
VISUALIZATION = {
    "figure_size": (20, 8),
    "dpi": 100,
    "wordcloud_width": 1200,
    "wordcloud_height": 600,
    "max_words": 150,
    "hspace": 0.3,
    "wspace": 0.3,
}

# Color palette
COLORS = {
    "positive": "#10B981",
    "negative": "#EF4444",
    "neutral": "#6B7280",
    "background": "#1F2937",
    "text": "#F9FAFB",
    "accent": "#3B82F6"
}

# ==================== FILE PATTERNS ====================
FILE_PATTERNS = {
    "raw_comments": "raw_comments*.csv",
    "clean_comments": "clean_comments*.csv",
    "test_results": "test_results*.csv",
}

# ==================== LOGGING ====================
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S",
}
