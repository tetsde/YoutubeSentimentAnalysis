import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from wordcloud import WordCloud
import os
import glob
from pyvi import ViTokenizer
from typing import Optional, Tuple
import numpy as np


class _CloudKeyword:
    """
    Modern visualization class for sentiment analysis results
    Features: Word Cloud + Donut Chart + Statistics
    """
    
    # Visual Constants
    FIGURE_SIZE = (20, 8)
    WORDCLOUD_WIDTH = 1200
    WORDCLOUD_HEIGHT = 600
    DPI = 100
    
    # Color Palette (Modern & Professional)
    COLORS = {
        'positive': '#10B981',    # Emerald green
        'negative': '#EF4444',    # Red
        'neutral': '#6B7280',     # Gray
        'background': '#1F2937',  # Dark blue-gray
        'text': '#F9FAFB',        # Off-white
        'accent': '#3B82F6'       # Blue
    }
    
    SENTIMENT_COLORS = ['#10B981', '#6B7280', '#EF4444']  # Positive, Neutral, Negative
    
    def __init__(self, stopwords_path: str = 'data/stopwords.txt'):
        """
        Initialize visualization with stopwords
        
        Args:
            stopwords_path: Path to stopwords file
        """
        self.stopwords_set = self._load_stopwords(stopwords_path)
        self._setup_style()
    
    def _load_stopwords(self, path: str) -> set:
        """Load stopwords from file"""
        if not os.path.exists(path):
            print(f"⚠️  Cảnh báo: File {path} không tồn tại. Sẽ không lọc stopwords.")
            return set()
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                words = f.read().splitlines()
            print(f"✅ Đã load {len(words)} stopwords")
            return set(words)
        except Exception as e:
            print(f"❌ Không thể đọc file stopwords: {e}")
            return set()
    
    def _setup_style(self):
        """Setup matplotlib style for modern look"""
        plt.style.use('dark_background')
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['DejaVu Sans', 'Arial'],
            'font.size': 11,
            'axes.titlesize': 16,
            'axes.titleweight': 'bold',
            'axes.labelsize': 12,
            'axes.facecolor': self.COLORS['background'],
            'figure.facecolor': '#111827',
            'text.color': self.COLORS['text'],
            'axes.labelcolor': self.COLORS['text'],
            'xtick.color': self.COLORS['text'],
            'ytick.color': self.COLORS['text'],
            'axes.unicode_minus': False,
        })
    
    def _find_latest_result(self, data_path: str = 'result') -> Optional[str]:
        """Find the latest result CSV file"""
        search_pattern = os.path.join(data_path, '*results*.csv')
        list_of_files = glob.glob(search_pattern)
        
        if not list_of_files:
            print("❌ Không tìm thấy file kết quả")
            return None
        
        latest_file = max(list_of_files, key=os.path.getmtime)
        print(f"📁 Phân tích file: {os.path.basename(latest_file)}")
        return latest_file
    
    def _create_wordcloud(self, text: str, max_words: int = 150) -> WordCloud:
        """
        Create modern word cloud with gradient colors
        
        Args:
            text: Tokenized text data
            max_words: Maximum number of words to display
        """
        # Custom color function for gradient effect
        def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
            # Gradient from green to blue to red
            colors = ['#10B981', '#3B82F6', '#8B5CF6', '#EC4899', '#EF4444']
            return np.random.choice(colors)
        
        wordcloud = WordCloud(
            width=self.WORDCLOUD_WIDTH,
            height=self.WORDCLOUD_HEIGHT,
            background_color='#1F2937',
            colormap='viridis',
            stopwords=self.stopwords_set,
            max_words=max_words,
            relative_scaling=0.5,
            min_font_size=10,
            collocations=False,
            color_func=color_func
        ).generate(text)
        
        return wordcloud
    
    def _create_statistics_text(self, df: pd.DataFrame) -> str:
        """Create statistics summary text (no emoji for encoding)"""
        total = len(df)
        label_counts = df['Label'].value_counts()
        
        stats = f"""
THONG KE PHAN TICH
{'='*30}

Tong so mau: {total:,}

Phan bo cam xuc:
  Tich cuc:  {label_counts.get(0, 0):,} ({label_counts.get(0, 0)/total*100:.1f}%)
  Trung lap: {label_counts.get(1, 0):,} ({label_counts.get(1, 0)/total*100:.1f}%)
  Tieu cuc:  {label_counts.get(2, 0):,} ({label_counts.get(2, 0)/total*100:.1f}%)

Tu vung: {len(set(' '.join(df['Text']).split())):,} tu duy nhat
        """
        return stats
    
    def keyword(self, max_words: int = 150, data_path: str = 'result', 
                save_path: Optional[str] = None) -> None:
        """
        Generate visualization with word cloud and sentiment distribution
        
        Args:
            max_words: Maximum words in word cloud
            data_path: Path to result folder
            save_path: Optional path to save figure
        """
        # Find latest result file
        latest_file = self._find_latest_result(data_path)
        if not latest_file:
            return
        
        try:
            # Load data
            df = pd.read_csv(latest_file)
            print(f"📊 Đã load {len(df)} dòng dữ liệu")
            
            # Check required columns
            required_cols = ['Text', 'Label', 'Sentiment']
            if not all(col in df.columns for col in required_cols):
                print(f"❌ File thiếu cột cần thiết: {required_cols}")
                return
            
            # Prepare text data with ViTokenizer
            print("Dang tokenize voi ViTokenizer...")
            tokenized_texts = []
            for text in df['Text'].astype(str):
                tokenized = ViTokenizer.tokenize(text)
                tokenized_texts.append(tokenized)
            
            tokenized_text = " ".join(tokenized_texts)
            print(f"Da tokenize {len(tokenized_texts)} cau, {len(tokenized_text.split())} tu")
            
            # Create visualizations
            self._create_visualization(df, tokenized_text, max_words, save_path)
            
        except Exception as e:
            print(f"❌ Lỗi khi phân tích dữ liệu: {e}")
            import traceback
            traceback.print_exc()
    
    def _create_visualization(self, df: pd.DataFrame, text: str, 
                            max_words: int, save_path: Optional[str]) -> None:
        """Create the main visualization figure"""
        # Create figure with 3 subplots
        fig = plt.figure(figsize=self.FIGURE_SIZE, dpi=self.DPI)
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        # 1. Word Cloud (large, spans 2 rows)
        ax1 = fig.add_subplot(gs[:, :2])
        wordcloud = self._create_wordcloud(text, max_words)
        ax1.imshow(wordcloud, interpolation='bilinear')
        ax1.set_title('Word Cloud - Tu khoa pho bien', 
                     fontsize=18, fontweight='bold', pad=20,
                     color=self.COLORS['text'])
        ax1.axis('off')
        
        # 2. Donut Chart (top right)
        ax2 = fig.add_subplot(gs[0, 2])
        self._plot_donut_chart(ax2, df)
        
        # 3. Statistics (bottom right)
        ax3 = fig.add_subplot(gs[1, 2])
        self._plot_statistics(ax3, df)
        
        # Add main title
        fig.suptitle('PHAN TICH CAM XUC - SENTIMENT ANALYSIS', 
                    fontsize=22, fontweight='bold', y=0.98,
                    color=self.COLORS['text'])
        
        # Save or show
        if save_path:
            plt.savefig(save_path, dpi=self.DPI, bbox_inches='tight', 
                       facecolor=fig.get_facecolor())
            print(f"💾 Đã lưu visualization tại: {save_path}")
        
        plt.tight_layout()
        plt.show()
    
    def _plot_donut_chart(self, ax, df: pd.DataFrame) -> None:
        """Plot modern donut chart for sentiment distribution"""
        label_counts = df['Label'].value_counts().sort_index()
        
        # Dynamic labels and colors based on actual data
        label_map = {0: 'Tich cuc', 1: 'Trung lap', 2: 'Tieu cuc'}
        color_map = {0: '#10B981', 1: '#6B7280', 2: '#EF4444'}
        
        labels = [label_map[label] for label in label_counts.index]
        colors = [color_map[label] for label in label_counts.index]
        
        # Create donut chart
        wedges, texts, autotexts = ax.pie(
            label_counts.values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops={'edgecolor': '#111827', 'linewidth': 2},
            textprops={'color': self.COLORS['text'], 'fontsize': 11}
        )
        
        # Make it donut (add white circle in center)
        centre_circle = plt.Circle((0, 0), 0.70, fc='#1F2937', linewidth=0)
        ax.add_artist(centre_circle)
        
        # Style autopct
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')
        
        ax.set_title('Phan bo cam xuc', fontsize=14, fontweight='bold', 
                    pad=15, color=self.COLORS['text'])
    
    def _plot_statistics(self, ax, df: pd.DataFrame) -> None:
        """Plot statistics text panel"""
        stats_text = self._create_statistics_text(df)
        
        ax.text(0.5, 0.5, stats_text, 
               transform=ax.transAxes,
               fontsize=10,
               verticalalignment='center',
               horizontalalignment='center',
               fontfamily='monospace',
               color=self.COLORS['text'],
               bbox=dict(boxstyle='round,pad=1', 
                        facecolor='#374151', 
                        edgecolor=self.COLORS['accent'],
                        linewidth=2))
        ax.axis('off')


if __name__ == "__main__":
    print("="*50)
    print("SENTIMENT VISUALIZATION - MODERN UI")
    print("="*50)
    
    cloud = _CloudKeyword()
    cloud.keyword(max_words=150)