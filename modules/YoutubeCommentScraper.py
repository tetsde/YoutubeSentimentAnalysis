from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager


class YoutubeCommentScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
    def _setup_driver(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
    def _get_url(self,url):
        try: 
         self._setup_driver()
         self.driver.get(url)
         print("Truy cập thành công trang", self.driver.title)
        except Exception as e :
          print("Lỗi khi truy cập",e)        
    def _scroll(self, scroll_time=50):
        print("Bắt đầu quy trình cuộn trang...")
        
        try:
            
            wait = WebDriverWait(self.driver, 15)
            comment_section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contents")))

            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", comment_section)
            
            print("Đã tìm thấy khung bình luận, đang chờ tải dữ liệu...")
            time.sleep(3) 

    
            last_height = self.driver.execute_script("return document.documentElement.scrollHeight")

            for i in range(scroll_time):
                print(f"Đang tải thêm comment... (Lần {i+1}/{scroll_time})")
                
                self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                
                time.sleep(random.randint(2, 4))

                new_height = self.driver.execute_script("return document.documentElement.scrollHeight")

                if new_height == last_height:
                    time.sleep(2)
                    new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
                    
                    if new_height == last_height:
                        print("Đã đến đáy trang hoặc không còn comment mới.")
                        break
                
                last_height = new_height

        except Exception as e:
            print(f"Lỗi trong quá trình cuộn (Có thể video tắt comment): {e}")

        print("Hoàn tất quy trình cuộn.")
    def extract_comments(self, timeout=10):
        print("Đang trích xuất comment")
        comment_list = []
        wait = WebDriverWait(self.driver, timeout)

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contents")))

            comments = self.driver.find_elements(By.CSS_SELECTOR, "ytd-comment-thread-renderer")
            if not comments:
                print("Không tìm thấy thẻ cũ, thử selector thay thế...")
                comments = self.driver.find_elements(By.CSS_SELECTOR, "ytd-comment-renderer, ytd-comment-view-model")

            print(f"Đã tìm thấy {len(comments)} thẻ comment")

            for comment in comments:
                try:
                    author_elem = comment.find_element(By.CSS_SELECTOR, "#author-text, #header-author")
                    content_elem = comment.find_element(By.CSS_SELECTOR, "#content-text, #content")
                    author_name = author_elem.text.strip()
                    content_text = " ".join(content_elem.text.split())  # collapse whitespace/newlines
                    comment_list.append({"name": author_name, "comment": content_text})
                except Exception as e:
                    print(f"Ignored comment due to: {e}")
                    continue

            return comment_list

        except Exception as e:
            print("Timeout: vùng chứa comments không xuất hiện",e)
            return []
        except Exception as e:
            print(f"Lỗi: {e}")
            return []

    def _save_to_csv(self, data, output_path="data/raw_comments.csv"):
        if not data:
            print("Không có dữ liệu để lưu")
            return
        try:
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            df = pd.DataFrame(data)
            root, ext = os.path.splitext(output_path)
            
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            final_path = f"{root}_{current_time}{ext}"

           
            df.to_csv(final_path, index=False, encoding='utf-8-sig')
            
            print(f"Đã lưu {len(data)} dòng vào {final_path}")
            
            return final_path 

        except Exception as e:
            print("Lỗi khi lưu file:", e)
    def close(self):
        if self.driver:
            print("Đang đóng trình duyệt...")
            self.driver.quit()       
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
   
if __name__ == "__main__":
    TARGET_URL = 'https://www.youtube.com/watch?v=fZpSRs81V80'
    try:
        scraper = YoutubeCommentScraper()
        scraper._get_url(TARGET_URL)
        scraper._scroll(scroll_time=10) 
        data = scraper.extract_comments()
        scraper._save_to_csv(data, "data/youtube_comments.csv")
            
    except Exception as e:
        print(f"Chương trình gặp lỗi: {e}")