from modules.YoutubeCommentScraper import YoutubeCommentScraper
from modules.Cleaner import Cleaner
from modules.AIModel import SentimentClassifier
from reports.Visualize import _CloudKeyword
from datetime import datetime
class SocialMediaListenTool:
      def __init__(self,url):
            self.url = url
            self.cleaner = Cleaner()
            self.scraper = YoutubeCommentScraper()
            self._aimodel = SentimentClassifier()
            self.cloud = _CloudKeyword()

      def CommentScraper(self,scroll_time =30):
            self.scraper._get_url(self.url)
            self.scraper._scroll(scroll_time) 
            self.comment = self.scraper.extract_comments()
            self.scraper._save_to_csv(self.comment)
            print("Đã lưu kết quả raw")

      def CleanerData(self, data_folder='data'):
           print("--- Bắt đầu quy trình làm sạch dữ liệu ---")
           try:
                  processed_df = self.cleaner.process_csv(folder_path=data_folder, text_column_name='comment')

                  if processed_df is not None and not processed_df.empty:
                        self.df = processed_df 
                        
                        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        output_path = f"{data_folder}/clean_comments_{current_time}.csv"
                        
                        # 4. Lưu file sạch
                        self.df.to_csv(output_path, index=False, encoding='utf-8-sig')
                        print(f">> Thành công! Đã lưu file sạch tại: {output_path}")
                  else:
                        print("Cảnh báo: Không có dữ liệu nào được làm sạch (File rỗng hoặc không tìm thấy file).")
                        
           except Exception as e:
            print("Lỗi kịch bản khi làm sạch:", e)

      def _model(self):
            self._aimodel._loadModel()
            try:
                  self._aimodel.predict()
                  print("Model đã dự đoán hoàn thành")
            except Exception as e :
                  print("Lỗi",e)    

      def _cloud(self):
            try:
             self.cloud.keyword()
            except Exception as e:
             print("Lỗi",e)
      def run(self):
           try:
                self.CommentScraper()
                try:
                     self.CleanerData()
                     try:
                          self._model()
                     except Exception as e:
                              print("Lỗi khi chạy mô hình")
                              return None
                     try:
                          self._cloud()
                     except Exception as e:
                          print("Lỗi khi biểu diễn keyword")
                          return None
                except Exception as e:
                 print("Lỗi khi làm sạch dữ liệu")
                 return None
           except Exception as e:
                print("Lỗi khi cào comment")
                return None

if __name__ == "__main__":
      #FILL URL YOUTUBE AT HERE 
      url = 'https://www.youtube.com/watch?v=XQkze4rQMsU'
      tool = SocialMediaListenTool(url)
      tool.run()
      

