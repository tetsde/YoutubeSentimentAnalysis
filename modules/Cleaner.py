import re
import pandas as pd
import numpy as np
import glob
import os
class Cleaner:
    def __init__(self):
        pass

    def url_clean(self, text):
        return re.sub(r'http\S+|www\.\S+', '', text)

    def punct_clean(self, text):
        return re.sub(r'[^\w\s]', ' ', text)

    def mention_clean(self, text):
        return re.sub(r'@[\w.]+', '', text)

    def _standardize_whitespace(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def clean_single_text(self, text):
        if not isinstance(text, str): 
            return ''
        
        text = str(text).lower() 
        text = self.url_clean(text)
        text = self.mention_clean(text) 
        text = self.punct_clean(text)
        text = self._standardize_whitespace(text)
        return text
    def process_csv(self, folder_path="data", text_column_name=None):
        search_pattern = os.path.join(folder_path, "raw_comments*.csv")
        
        list_of_files = glob.glob(search_pattern)
        
        if not list_of_files:
            print(f"Lỗi: Không tìm thấy file nào bắt đầu bằng 'raw_comments' trong folder '{folder_path}'")
            return None

        latest_file = max(list_of_files, key=os.path.getmtime)
        
        print(f"--- Đang xử lý file mới nhất: {latest_file} ---")

        try:
            
            df = pd.read_csv(latest_file)
            print(f"Số dòng ban đầu: {len(df)}")

            df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
            df.replace('nan', np.nan, inplace=True)
            
            if text_column_name:
                df.dropna(subset=[text_column_name], inplace=True)
            else:
                df.dropna(how='all', inplace=True)
            
            print(f"Số dòng sau khi xoá rỗng (NaN): {len(df)}")

            if text_column_name:
                if text_column_name in df.columns:
                    df[text_column_name] = df[text_column_name].apply(self.clean_single_text)
                    df = df[df[text_column_name] != '']
                else:
                    print(f"Cảnh báo: Cột '{text_column_name}' không tồn tại trong file.")
            else:
                for col in df.select_dtypes(include=['object']).columns:
                    df[col] = df[col].apply(self.clean_single_text)

            return df

        except Exception as e:
            print(f"Lỗi khi xử lý file: {e}")
            return None
if __name__ == "__main__":
    model = Cleaner()

    cleaned_df = model.process_csv("data/train.csv", text_column_name='text')
    
    if cleaned_df is not None:
        print(cleaned_df.head())
        cleaned_df.to_csv("data/train_clean.csv", index=False)