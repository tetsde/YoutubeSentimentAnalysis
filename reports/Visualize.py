import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os 
from pyvi import ViTokenizer
import glob
class _CloudKeyword:
    def __init__(self,STOPWORDS='data/stopwords.txt'):
         self.stopwords_set = self._LoadstopWord(STOPWORDS)   
    def _LoadstopWord(self,path):
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    words = f.read().splitlines() 
                return set(words)
            except Exception as e:
                print(f"Không thể đọc file stopwords: {e}")
                return set() 
        else:
            print(f"Cảnh báo: File {path} không tồn tại. Sẽ không lọc stopwords.")
            return set()
    def keyword(self, max_words=100,data_path='result'):
        search_pattern = os.path.join(data_path,'result*.csv')
        list_of_files = glob.glob(search_pattern)
        if not list_of_files:
            print("Không tìm thấy file")
            return None
        lastest_file = max(list_of_files,key=os.path.getmtime)
        print(f'Tiến hành phân tích{lastest_file}')

        try:
            df = pd.read_csv(lastest_file)
            label_counts = df['label_id'].value_counts()
            text_data = " ".join(title for title in df['text'])
            tokenized_text = ViTokenizer.tokenize(text_data)
            print(f"Số từ đã phân tích{len(text_data)}")
            try: 
                    worcdcloud = WordCloud(
                    width=800,
                    height=400,
                    background_color='white',
                    colormap='viridis',
                    stopwords=self.stopwords_set,
                    max_words = max_words).generate(tokenized_text)
                    try:
                        fig,ax = plt.subplots(1,2,figsize =(20,6))
                        ax[0].imshow(worcdcloud,interpolation='bilinear')
                        ax[0].set_title("1. Đám mây từ khoá",fontweight='bold')
                        ax[0].axis('off')

                        ax[1].pie(label_counts,labels=label_counts.index ,autopct='%1.1f%%', startangle=90)
                        ax[1].set_title("2. Tỷ trọng ngôn từ\n" \
                        "Tích cực (0)\n" \
                        "Tiêu cực (2)\n" \
                        "Trung lập (1)\n" \
                        "Accuracy: 77.63% ",fontweight='bold')
                        plt.tight_layout()
                        plt.show()
                    except Exception as e:
                        print("Lỗi khi khởi tạo biểu đồ")
            except Exception as e:
                print("Lỗi khi khởi tạo dữ liệu")
        except Exception as e:
            print("Lỗi",e)
if __name__ == "__main__":
    cloud = _CloudKeyword()
    cloud.keyword()
        