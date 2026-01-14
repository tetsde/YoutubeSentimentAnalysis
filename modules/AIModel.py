import pandas as pd
import json
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pickle
import os
import glob
from typing import Optional

class SentimentClassifier:
    """
    Sentiment Analysis model using sklearn's MultinomialNB
    Supports 3 classes: Positive (0), Neutral (1), Negative (2)
    """
    
    def __init__(self):
        # sklearn components
        self.vectorizer = CountVectorizer(
            lowercase=True,
            token_pattern=r'\b\w+\b',  # word tokenization
            min_df=1,  # minimum document frequency
        )
        self.model = MultinomialNB(alpha=1.0)  # Laplace smoothing
        
        # Training statistics
        self.is_trained = False
        self.n_samples = 0
        self.class_distribution = {}
    
    def _token(self, text):
        """Simple tokenizer for compatibility"""
        if isinstance(text, str):
            return text.lower().split()
        return []
    
    def _train(self, data):
        """
        Train the model with data from CSV file
        
        Args:
            data (str): Path to training CSV file
        """
        print(f'Đang học từ {data}')
        feature = str(input("Nhập feature:"))
        label = str(input("Nhập label: "))
        
        try:
            # Load data
            df = pd.read_csv(data)
            
            # Convert label to int and filter invalid values
            df['label'] = pd.to_numeric(df['label'], errors='coerce')
            df = df.dropna(subset=['label'])
            df['label'] = df['label'].astype(int)
            
            X = df[feature]
            Y = df[label]
            
            # Vectorize text data
            print("Đang vectorize dữ liệu...")
            X_vectorized = self.vectorizer.fit_transform(X)
            
            # Train model
            print("Đang train model...")
            self.model.fit(X_vectorized, Y)
            
            # Update statistics
            self.is_trained = True
            self.n_samples = len(Y)
            self.class_distribution = Y.value_counts().to_dict()
            
            print("\nKết quả training:")
            print(f"- Tổng số câu đã học: {self.n_samples}")
            print(f"- Phân bố nhãn:")
            for label_id, count in sorted(self.class_distribution.items()):
                label_name = {0: 'Positive', 1: 'Neutral', 2: 'Negative'}.get(label_id, 'Unknown')
                print(f"  + {label_name} ({label_id}): {count} câu")
            print(f"- Vocabulary size: {len(self.vectorizer.vocabulary_)}")
            
            # Save model
            self._saveModel()
            print("- Xem kết quả chi tiết tại file model.pkl")
            
        except FileNotFoundError:
            print("Không tìm thấy file")
        except Exception as e:
            print(f"Lỗi khi huấn luyện mô hình: {e}")
            import traceback
            traceback.print_exc()
    
    def _saveModel(self):
        """Save model using pickle"""
        try:
            model_data = {
                'vectorizer': self.vectorizer,
                'model': self.model,
                'is_trained': self.is_trained,
                'n_samples': self.n_samples,
                'class_distribution': self.class_distribution
            }
            
            with open('modules/model.pkl', 'wb') as f:
                pickle.dump(model_data, f)
            
            print("Đã lưu model vào modules/model.pkl")
        except Exception as e:
            print(f"Lỗi khi lưu model: {e}")
    
    def _loadModel(self):
        """Load model from pickle file"""
        try:
            with open('modules/model.pkl', 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.model = model_data['model']
            self.is_trained = model_data.get('is_trained', True)
            self.n_samples = model_data.get('n_samples', 0)
            self.class_distribution = model_data.get('class_distribution', {})
            
            print("Đã load model thành công!")
            return True
        except FileNotFoundError:
            print("Không tìm thấy file model. Vui lòng train model trước.")
            return False
        except Exception as e:
            print(f"Lỗi khi load model: {e}")
            return False
    
    def _find_latest_clean_file(self, data_folder: str = 'data') -> Optional[str]:
        """
        Find the latest clean_comments CSV file in data folder
        
        Args:
            data_folder: Folder containing clean_comments files
            
        Returns:
            Path to latest file or None if not found
        """
        search_pattern = os.path.join(data_folder, 'clean_comments*.csv')
        list_of_files = glob.glob(search_pattern)
        
        if not list_of_files:
            print(f"⚠️  Không tìm thấy file clean_comments trong folder: {data_folder}")
            return None
        
        latest_file = max(list_of_files, key=os.path.getmtime)
        print(f"📁 Tìm thấy file clean mới nhất: {os.path.basename(latest_file)}")
        return latest_file
    
    def predict(self, data: Optional[str] = None, folder: str = "result"):
        """
        Predict sentiment for input data
        Auto-detects latest clean_comments file if data is None
        
        Args:
            data: Path to CSV file, list of texts, or None (auto-detect latest)
            folder: Output folder for results
            
        Returns:
            DataFrame with predictions or None if error
        """
        if not self.is_trained:
            print("Mô hình chưa được huấn luyện (is_trained = False).")
            return None
        
        results = []
        
        try:
            # Auto-detect latest clean file if data is None
            if data is None:
                data = self._find_latest_clean_file()
                if data is None:
                    print("❌ Không thể tìm thấy file dữ liệu để dự đoán")
                    return None
            
            # Load data
            if isinstance(data, list):
                print(f"--- Nhận dữ liệu từ list ({len(data)} dòng) ---")
                X = data
            else:
                print(f"📊 Đang phân tích file: {os.path.basename(data)}")
                df = pd.read_csv(data)
                X = df.iloc[:, 0].tolist()  # First column (comment/text)
                print(f"✅ Đã load {len(X)} dòng dữ liệu")
            
            # Vectorize input
            print(f"Bắt đầu dự đoán {len(X)} dòng...")
            X_vectorized = self.vectorizer.transform(X)
            
            # Predict
            predictions = self.model.predict(X_vectorized)
            
            # Map labels to sentiment names
            label_map = {0: 'Positive', 1: 'Neutral', 2: 'Negative'}
            
            # Create results
            for text, pred_label in zip(X, predictions):
                sentiment = label_map.get(pred_label, 'Unknown')
                results.append({
                    'Text': text,
                    'Label': int(pred_label),
                    'Sentiment': sentiment
                })
            
            # Save results
            result_df = pd.DataFrame(results)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_path = f"{folder}/test_results_{timestamp}.csv"
            
            os.makedirs(folder, exist_ok=True)
            result_df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f">> Hoàn tất! Đã lưu kết quả dự đoán tại: {output_path}")
            
            return result_df
            
        except Exception as e:
            print(f"Lỗi khi dự đoán: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def evaluate_fast(self, data_test):
        """
        Evaluate model accuracy on test dataset
        
        Args:
            data_test: Path to test CSV file
        """
        print(f"Đang đánh giá model trên {data_test}...")
        
        try:
            # Predict
            result_df = self.predict(data_test)
            
            if result_df is None:
                print("Không thể đánh giá do quá trình dự đoán gặp lỗi.")
                return
            
            # Load true labels
            df_test = pd.read_csv(data_test)
            
            # Convert labels to int
            df_test.iloc[:, 1] = pd.to_numeric(df_test.iloc[:, 1], errors='coerce')
            df_test = df_test.dropna(subset=[df_test.columns[1]])
            df_test.iloc[:, 1] = df_test.iloc[:, 1].astype(int)
            
            y_true = df_test.iloc[:, 1].tolist()
            y_pred = result_df['Label'].tolist()
            
            # Calculate accuracy
            accuracy = accuracy_score(y_true, y_pred)
            print(f"Accuracy: {accuracy * 100:.2f}%")
            
        except Exception as e:
            print(f"Lỗi khi đánh giá: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # Initialize model
    model = SentimentClassifier()
    
    # Train model
    model._train("data/train_clean.csv")
    
    # Load model
    model._loadModel()
    
    # Evaluate
    model.evaluate_fast("data/test1.csv")