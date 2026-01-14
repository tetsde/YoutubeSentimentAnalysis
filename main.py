"""
Social Media Listen Tool - Main Entry Point
Automated YouTube comment analysis pipeline:
Scrape → Clean → Sentiment Analysis → Visualization
"""

from modules.YoutubeCommentScraper import YoutubeCommentScraper
from modules.Cleaner import Cleaner
from modules.AIModel import SentimentClassifier
from reports.Visualize import _CloudKeyword
from config import DATA_DIR, SCRAPER, DATA_PROCESSING
from utils import setup_logger, get_timestamp, ensure_dir_exists


class SocialMediaListenTool:
    """
    Main orchestrator for YouTube sentiment analysis pipeline
    """
    
    def __init__(self, url: str):
        """
        Initialize the tool with YouTube URL
        
        Args:
            url: YouTube video URL to analyze
        """
        self.url = url
        self.logger = setup_logger(__name__)
        
        # Initialize components
        self.scraper = YoutubeCommentScraper(headless=SCRAPER["headless"])
        self.cleaner = Cleaner()
        self.model = SentimentClassifier()
        self.visualizer = _CloudKeyword()
        
        # Ensure directories exist
        ensure_dir_exists(str(DATA_DIR))
        ensure_dir_exists("result")
    
    def scrape_comments(self, scroll_time: int = None) -> bool:
        """
        Scrape YouTube comments
        
        Args:
            scroll_time: Number of scroll iterations (default from config)
            
        Returns:
            True if successful, False otherwise
        """
        if scroll_time is None:
            scroll_time = SCRAPER["scroll_time"]
        
        self.logger.info(f"🔄 Starting comment scraping from: {self.url}")
        
        try:
            self.scraper._get_url(self.url)
            self.scraper._scroll(scroll_time)
            comments = self.scraper.extract_comments()
            self.scraper._save_to_csv(comments)
            
            self.logger.info("✅ Comment scraping completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error during scraping: {e}")
            return False
    
    def clean_data(self) -> bool:
        """
        Clean scraped comment data
        
        Returns:
            True if successful, False otherwise
        """
        self.logger.info("🧹 Starting data cleaning process...")
        
        try:
            df = self.cleaner.process_csv(
                folder_path=str(DATA_DIR),
                text_column_name=DATA_PROCESSING["text_column"]
            )
            
            if df is None or df.empty:
                self.logger.warning("⚠️  No data to clean")
                return False
            
            # Save cleaned data
            timestamp = get_timestamp()
            output_path = DATA_DIR / f"clean_comments_{timestamp}.csv"
            df.to_csv(output_path, index=False, 
                     encoding=DATA_PROCESSING["output_encoding"])
            
            self.logger.info(f"✅ Cleaned data saved: {output_path.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error during cleaning: {e}")
            return False
    
    def run_model(self) -> bool:
        """
        Run sentiment analysis model
        
        Returns:
            True if successful, False otherwise
        """
        self.logger.info("🤖 Starting sentiment analysis...")
        
        try:
            # Load model
            if not self.model._loadModel():
                self.logger.error("❌ Failed to load model")
                return False
            
            # Predict (auto-finds latest clean file)
            result = self.model.predict()
            
            if result is None:
                self.logger.error("❌ Prediction failed")
                return False
            
            self.logger.info("✅ Sentiment analysis completed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error during prediction: {e}")
            return False
    
    def visualize_results(self) -> bool:
        """
        Generate visualization from analysis results
        
        Returns:
            True if successful, False otherwise
        """
        self.logger.info("📊 Generating visualizations...")
        
        try:
            self.visualizer.keyword()
            self.logger.info("✅ Visualization completed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error during visualization: {e}")
            return False
    
    def run(self) -> None:
        """
        Execute complete pipeline: Scrape → Clean → Analyze → Visualize
        """
        self.logger.info("="*60)
        self.logger.info("🚀 SOCIAL MEDIA LISTEN TOOL - PIPELINE STARTED")
        self.logger.info("="*60)
        
        # Step 1: Scrape
        if not self.scrape_comments():
            self.logger.error("Pipeline stopped: Scraping failed")
            return
        
        # Step 2: Clean
        if not self.clean_data():
            self.logger.error("Pipeline stopped: Data cleaning failed")
            return
        
        # Step 3: Model
        if not self.run_model():
            self.logger.error("Pipeline stopped: Model prediction failed")
            return
        
        # Step 4: Visualize
        if not self.visualize_results():
            self.logger.error("Pipeline stopped: Visualization failed")
            return
        
        self.logger.info("="*60)
        self.logger.info("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        self.logger.info("="*60)


if __name__ == "__main__":
    # Configure YouTube URL here
    YOUTUBE_URL = 'https://www.youtube.com/watch?v=zSNgmQx-QqU&list=RDzSNgmQx-QqU&start_radio=1'
    
    # Run pipeline
    tool = SocialMediaListenTool(YOUTUBE_URL)
    tool.run()
