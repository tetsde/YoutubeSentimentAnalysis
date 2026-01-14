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
        """
        Process latest raw_comments CSV file
        - Clean text
        - Keep only text column (drop name column)
        - Rename to 'text' for consistency
        """
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
            
            # Detect text column name
            if text_column_name is None:
                # Auto-detect: usually 'comment' or 'text'
                if 'comment' in df.columns:
                    text_column_name = 'comment'
                elif 'text' in df.columns:
                    text_column_name = 'text'
                else:
                    # Use last column (usually comment is the last)
                    text_column_name = df.columns[-1]
            
            print(f"📝 Đang clean cột: {text_column_name}")
            
            # Remove empty rows
            df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
            df.replace('nan', np.nan, inplace=True)
            df.dropna(subset=[text_column_name], inplace=True)
            
            print(f"Số dòng sau khi xoá rỗng (NaN): {len(df)}")

            # Clean text column
            if text_column_name in df.columns:
                df[text_column_name] = df[text_column_name].apply(self.clean_single_text)
                df = df[df[text_column_name] != '']
            else:
                print(f"Cảnh báo: Cột '{text_column_name}' không tồn tại trong file.")
                return None
            
            # ✅ CRITICAL: Keep only text column, drop others (like 'name')
            df = df[[text_column_name]].copy()
            
            # ✅ Rename to 'text' for consistency
            df.rename(columns={text_column_name: 'text'}, inplace=True)
            
            print(f"✅ Output: {len(df)} dòng, chỉ cột 'text'")
            
            return df

        except Exception as e:
            print(f"Lỗi khi xử lý file: {e}")
            import traceback
            traceback.print_exc()
            return None


if __name__ == "__main__":
    model = Cleaner()

    cleaned_df = model.process_csv("data", text_column_name='comment')
    
    if cleaned_df is not None:
        print(cleaned_df.head())
        cleaned_df.to_csv("data/train_clean.csv", index=False)