import pandas as pd
import json
import os
import math
from datetime import datetime
import glob
class SentimentClassifier:
    def __init__(self):
        self.pos_word = {}
        self.neu_word = {}
        self.neg_word = {}
        self.dictionary = set()
        
        self.pos_sentences = 0
        self.neu_sentences = 0
        self.neg_sentences = 0
        
        self.pos_words_count = 0
        self.neu_words_count = 0
        self.neg_words_count = 0
    def _token(self,text):
        return str(text).lower().split()
    def _train(self,data):
        print(f'Đang học từ {data}')
        feature = str(input("Nhập feature:"))
        label = str(input("Nhập label: "))
        try:
            try: 
                df = pd.read_csv(data)
                X = df[f"{feature}"]
                Y = df [f"{label}"]
                try:
                    for sentences, label in zip(X,Y):
                        words = self._token([[sentences]])
                        if label == 0:
                            self.pos_sentences += 1 
                            for word in words:
                                self.pos_word[word] = self.pos_word.get(word,0) + 1 
                                self.pos_words_count += 1
                        elif label ==2 :
                            self.neg_sentences +=1
                            for word in words:
                                self.neg_word[word] = self.neg_word.get(word,0) + 1 
                                self.neg_words_count += 1 
                        elif label == 1:
                            self.neu_sentences += 1 
                            for word in words:
                                self.neu_word[word] = self.neu_word.get(word,0) + 1 
                                self.neu_words_count +=1
                    self.dictionary = set(list(self.pos_word) + list(self.neu_word) + list(self.neg_word))
                    print("Kết quả training:")
                    print(f"- Tổng số câu đã học: {self.pos_sentences + self.neg_sentences + self.neu_sentences}")
                    self._saveModel()
                    print("- Xem kết quả chi tiết tại file model.json")
                except Exception as e:
                       print("Lỗi khi huấn luyện mô hình",e)       
            except FileNotFoundError:
                print("Không tìm thấy file")
        except Exception as e:
            print("Lỗi khi nhận dữ liệu học")
    def _saveModel(self,filepath="modules/model.json"):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True) 
            data = {
                'positive_words': self.pos_word,
                'negative_words': self.neg_word,
                'neutral_words': self.neu_word,
                'dictionary': list(self.dictionary),
                'neutral_sentences': self.neu_sentences,
                'positive_sentences': self.pos_sentences,
                'negative_sentences': self.neg_sentences,
                'number_of_positive_words': self.pos_words_count,
                'number_of_negative_words': self.neg_words_count,
                'number_of_neutral_words': self.neu_words_count,
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Đã lưu model vào {filepath}")
        except Exception as e:
            print(f"Lỗi khi lưu model: {e}")
    def _loadModel(self,filepath="modules/model.json"):
        try:
            os.makedirs(os.path.dirname(filepath),exist_ok=True)
            with open(filepath, "r", encoding="utf-8") as f:
                result = json.load(f)
            self.pos_word = result["positive_words"]
            self.neg_word = result["negative_words"]
            self.neu_word = result["neutral_words"]
            self.dictionary = set(result["dictionary"]) 

            self.neu_sentences = result["neutral_sentences"]
            self.pos_sentences = result["positive_sentences"]
            self.neg_sentences = result["negative_sentences"]

            self.pos_words_count = result["number_of_positive_words"]
            self.neg_words_count = result["number_of_negative_words"]
            self.neu_words_count = result["number_of_neutral_words"]
            print("Đã load model thành công!")
        except FileNotFoundError:
            print("Chưa có file model. Vui lòng train trước.")
        except Exception as e:
            print(f"Lỗi khi load model: {e}")

    def predict(self, input_folder='data', save_path="result/result.csv"):
        data_to_predict = []
        if isinstance(input_folder, list):
         print(f"--- Nhận dữ liệu trực tiếp từ list ({len(input_folder)} dòng) ---")
         data_to_predict = input_folder
         data_to_predict = [str(x) for x in data_to_predict]
        elif isinstance(input_folder, str):
            try:
                search_pattern = os.path.join(input_folder, "clean_comments*.csv")
                list_of_files = glob.glob(search_pattern)
                    
                if not list_of_files:
                    print(f"Lỗi: Không tìm thấy file trong folder '{input_folder}'")
                    return None
                        
                latest_file = max(list_of_files, key=os.path.getmtime)
                print(f"--- Đang thực hiện dự đoán trên file: {latest_file} ---")
                    
                df = pd.read_csv(latest_file)
                if 'comment' not in df.columns:
                    print("Lỗi: File không có cột 'comment'.")
                    return None
                data_to_predict = df['comment'].astype(str).tolist()
                
            except Exception as e:
                print(f"Lỗi khi đọc file: {e}")
                return None
        else:
            print("Lỗi: Input không hợp lệ (phải là list hoặc đường dẫn folder)")
            return None
        

        total_sentences = self.pos_sentences + self.neu_sentences + self.neg_sentences
        if total_sentences == 0:
            print("Mô hình chưa được huấn luyện (total_sentences = 0).")
            return None

        vocab_size = len(self.dictionary)
        results = []

        log_prior_pos = math.log(self.pos_sentences / total_sentences)
        log_prior_neg = math.log(self.neg_sentences / total_sentences)
        log_prior_neu = math.log(self.neu_sentences / total_sentences)

        denom_pos = self.pos_words_count + vocab_size
        denom_neg = self.neg_words_count + vocab_size
        denom_neu = self.neu_words_count + vocab_size

        print(f"Bắt đầu dự đoán {len(data_to_predict)} dòng...")

        try:
            
            for text in data_to_predict:

                words = self._token(text) 
                
                curr_log_prob_pos = log_prior_pos
                curr_log_prob_neg = log_prior_neg
                curr_log_prob_neu = log_prior_neu

                for word in words:
                    curr_log_prob_pos += math.log((self.pos_word.get(word, 0) + 1) / denom_pos)
                    curr_log_prob_neg += math.log((self.neg_word.get(word, 0) + 1) / denom_neg)
                    curr_log_prob_neu += math.log((self.neu_word.get(word, 0) + 1) / denom_neu)

                probs = {
                    0: curr_log_prob_pos, # Positive
                    2: curr_log_prob_neg, # Negative
                    1: curr_log_prob_neu  # Neutral
                }
                
                predicted_label = max(probs, key=probs.get)

                label_map = {2: 'Negative', 0: 'Neutral', 1: 'Positive'}
                
                results.append({
                    "text": text,
                    "label_id": predicted_label,
                    "sentiment": label_map.get(predicted_label, predicted_label)
                })
            

            output_dir = os.path.dirname(save_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            root, ext = os.path.splitext(save_path)
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            final_save_path = f"{root}_{current_time}{ext}"

            result_df = pd.DataFrame(results)
            result_df.to_csv(final_save_path, index=False, encoding='utf-8-sig')
            
            print(f">> Hoàn tất! Đã lưu kết quả dự đoán tại: {final_save_path}")
            return results

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình dự đoán: {e}")
            return None 
    def evaluate_fast(self, test_path='data/test1.csv'):
        print(f"--- Đang đánh giá trên file: {test_path} ---")
        try:
            test_df = pd.read_csv(test_path)
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file {test_path}")
            return

        x_test = test_df['text'].tolist() 
        y_test = test_df['label'].tolist()
        
        results = self.predict(x_test, save_path="result/test_results.csv")
        
        if results is None:
            print("Không thể đánh giá do quá trình dự đoán gặp lỗi.")
            return

        correct = 0
        for i in range(len(results)):
            pred = results[i].get('label_id') 
            actual = y_test[i]
            
            if int(pred) == int(actual):
                correct += 1
                
        print(f"Accuracy: {(correct/len(results))*100:.2f}%")
if __name__ == "__main__":
    model = SentimentClassifier()
    model._loadModel()
    model.evaluate_fast()