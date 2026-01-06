#  Social Media Listen Tool - YouTube Sentiment Analysis


![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.10%2B-green)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-red)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng nổi bật](#tính-năng-nổi-bật)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Cài đặt](#cài-đặt)
- [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
- [Quy trình hoạt động](#quy-trình-hoạt-động)
- [Kết quả mẫu](#kết-quả-mẫu)
- [Đóng góp](#đóng-góp)
- [License](#license)
- [Liên hệ](#liên-hệ)

---

##  Giới thiệu

**Social Media Listen Tool** là công cụ phân tích cảm xúc (Sentiment Analysis) tự động trên YouTube, giúp bạn thấu hiểu **"Voice of Customer"** (Tiếng nói khách hàng) một cách nhanh chóng và chính xác.

### Tính năng chính

Công cụ tự động hóa toàn bộ quy trình:
1. Thu thập dữ liệu thô (YouTube Comments)
2. Làm sạch và tiền xử lý dữ liệu
3. Phân tích cảm xúc bằng Machine Learning
4. Trực quan hóa kết quả và tạo báo cáo

---

##  Tính năng nổi bật

###  1. Advanced Auto Crawler
- Sử dụng **Selenium WebDriver** để giả lập hành vi người dùng thực
- Tự động cuộn trang (Auto-scroll) để xử lý cơ chế **Lazy Loading** của YouTube
- Đảm bảo cào được lượng bình luận tối đa với tùy chỉnh thời gian scroll
- Trích xuất đầy đủ thông tin: Tên người dùng, nội dung bình luận, thời gian

###  2. Smart Data Cleaning
Dữ liệu mạng xã hội thường rất "bẩn". Hệ thống tích hợp bộ lọc mạnh mẽ để xử lý đặc thù tiếng Việt:
- Loại bỏ emoji, icon, ký tự đặc biệt và HTML tags
- Chuẩn hóa văn bản về dạng lowercase
- Xử lý teencode và từ viết tắt phổ biến
- Loại bỏ stop words tiếng Việt
- Xử lý trùng lặp và dữ liệu rỗng

### 🧠. AI Sentiment Analysis Engine
- Thuật toán **Naive Bayes** được tùy chỉnh cho tiếng Việt
- Model đã được huấn luyện sẵn với dữ liệu tiếng Việt
- Phân loại cảm xúc: **Positive**, **Negative**, **Neutral**
- Độ chính xác cao trên dữ liệu thực tế

###  4. Visual Insights & Reporting
- **Sentiment Distribution:** Biểu đồ tròn thể hiện tỷ lệ Tích cực/Tiêu cực/Trung lập
- **WordCloud:** "Đám mây từ khóa" làm nổi bật chủ đề hot nhất
- Export kết quả ra CSV để phân tích tiếp
- Báo cáo chi tiết với các metrics quan trọng

---

## 🛠️ Công nghệ sử dụng

| Lĩnh vực | Công nghệ | Version |
|----------|-----------|---------|
| **Ngôn ngữ** | Python | 3.9+ |
| **Web Scraping** | Selenium | ≥4.10.0 |
| **Browser Driver** | WebDriver Manager | ≥4.0.0 |
| **Data Processing** | Pandas, NumPy | ≥2.0.0, ≥1.24.0 |
| **Machine Learning** | Scikit-learn, Custom Naive Bayes | ≥1.2.0 |
| **NLP** | RegEx, Custom Text Processing | - |
| **Visualization** | Matplotlib, WordCloud | ≥3.7.0, ≥1.9.0 |
| **Utilities** | tqdm, Pillow | ≥4.65.0, ≥9.5.0 |

---

## 📁 Cấu trúc dự án

```
SocialMediaListenTool/
├── 📂 chrome/                    # Chrome browser files (338 files)
├── 📂 chromedriver/              # ChromeDriver for Selenium
├── 📂 data/                      # Dữ liệu và tài nguyên
│   ├── raw_comments.csv          # 📄 Dữ liệu thô sau khi cào
│   ├── clean_comments.csv        # 📄 Dữ liệu đã làm sạch
│   ├── stopwords.txt             # 📄 Danh sách stop words tiếng Việt
│   ├── train_clean.csv           # 📄 Dữ liệu huấn luyện model
│   └── test1.csv                 # 📄 Dữ liệu test
├── 📂 modules/                   # Các module chính
│   ├── YoutubeCommentScraper.py  # 🕷️ Module cào comments YouTube
│   ├── Cleaner.py                # 🧹 Module làm sạch dữ liệu
│   ├── AIModel.py                # 🤖 Module phân tích cảm xúc (Naive Bayes)
│   ├── model.json                # 💾 Model weights đã được train
│   └── test.py                   # 🧪 Test module
├── 📂 reports/                   # Báo cáo và visualization
│   └── Visualize.py              # 📊 Module tạo WordCloud và charts
├── 📂 result/                    # Kết quả phân tích
│   └── result.csv                # 📈 Kết quả dự đoán cảm xúc
├── main.py                       # 🚀 File chạy chính
├── requirements.txt              # 📦 Danh sách dependencies
└── README.md                     # 📖 File này
```

---

## Cài đặt

### 1️⃣ Prerequisites (Yêu cầu)

- **Python 3.9 trở lên**
- **Google Chrome** (phiên bản mới nhất)
- **Git** (optional)

### 2️⃣ Clone Repository

```bash
git clone https://github.com/tetsde/SocialMediaListenTool.git
cd SocialMediaListenTool
```

### 3️⃣ Tạo Virtual Environment (Khuyến nghị)

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 4️⃣ Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Kiểm tra cài đặt

```bash
python -c "import selenium; import pandas; print('✅ All packages installed successfully!')"
```

---

## 🚀 Hướng dẫn sử dụng

### 🎬 Quick Start

#### **Cách 1: Sử dụng file main.py có sẵn**

1. Mở file `main.py` và thay đổi URL YouTube:

```python
if __name__ == "__main__":
    url = 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID'  # ⬅️ Thay đổi URL tại đây
    tool = SocialMediaListenTool(url)
    tool.CommentScraper(scroll_time=50)  # Scroll 50 lần, có thể thay đổi
    tool.CleanerData()
    tool._model()
    tool._cloud(data="result/result.csv")
```

2. Chạy chương trình:

```bash
python main.py
```

#### **Cách 2: Sử dụng Python Interactive**

```python
from modules.YoutubeCommentScraper import YoutubeCommentScraper
from modules.Cleaner import Cleaner
from modules.AIModel import SentimentClassifier
from reports.Visualize import _CloudKeyword
import pandas as pd

# 1. Khởi tạo tool
url = 'https://www.youtube.com/watch?v=R43ld7VhvN4'
tool = SocialMediaListenTool(url)

# 2. Cào dữ liệu (scroll 30 giây)
tool.CommentScraper(scroll_time=30)

# 3. Làm sạch dữ liệu
tool.CleanerData()

# 4. Phân tích cảm xúc
tool._model()

# 5. Tạo WordCloud
tool._cloud(data="result/result.csv")
```

---

## ⚙️ Quy trình hoạt động

```
┌─────────────────────┐
│  1. INPUT           │
│  YouTube Video URL  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  2. SCRAPING        │
│  • Auto scroll      │
│  • Extract comments │
│  • Save raw CSV     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  3. CLEANING        │
│  • Remove emojis    │
│  • Normalize text   │
│  • Remove stopwords │
│  • Save clean CSV   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  4. AI ANALYSIS     │
│  • Load AI model    │
│  • Predict sentiment│
│  • Save results     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  5. VISUALIZATION   │
│  • Generate charts  │
│  • Create wordcloud │
│  • Export reports   │
└─────────────────────┘
```

---

## 📊 Kết quả mẫu

### 📁 Output Files

Sau khi chạy xong, bạn sẽ có các file sau:

1. **`data/raw_comments.csv`** - Dữ liệu thô
   ```
   username,comment,timestamp
   User123,Sản phẩm này quá tuyệt vời! 😍,2 giờ trước
   TechReviewer,Camera hơi tệ,1 ngày trước
   ```

2. **`data/clean_comments.csv`** - Dữ liệu đã làm sạch
   ```
   comment
   sản phẩm này quá tuyệt vời
   camera hơi tệ
   ```

3. **`result/result.csv`** - Kết quả phân tích
   ```
   comment,sentiment,confidence
   sản phẩm này quá tuyệt vời,positive,0.92
   camera hơi tệ,negative,0.87
   ```

4. **`reports/wordcloud.png`** - Word Cloud visualization

### 📈 Sample Statistics

```
📊 Phân tích hoàn thành!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Tổng comments: 1,234
😊 Positive:      657 (53.2%)
😐 Neutral:       321 (26.0%)
😞 Negative:      256 (20.8%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 Top keywords: camera, pin, thiết kế, giá, chất lượng
```

---

## 🎯 Tùy chỉnh nâng cao

### Thay đổi thời gian scroll

```python
tool.CommentScraper(scroll_time=100)  # Scroll 100 giây để lấy nhiều comments hơn
```

### Xử lý file CSV khác

```python
tool.CleanerData(csv_path='path/to/your/file.csv')
```

### Sử dụng model với dữ liệu riêng

```python
tool._model(data_path='data/your_clean_data.csv')
```

---

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh! Nếu bạn muốn cải thiện dự án:

1. Fork repository này
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

---

## ⚠️ Lưu ý

- ⏰ Thời gian cào dữ liệu phụ thuộc vào tốc độ mạng và số lượng comments
- 🌐 Cần kết nối Internet ổn định
- 💻 Chrome browser sẽ tự động mở và đóng, không can thiệp trong quá trình chạy
- 📊 Kết quả phân tích phụ thuộc vào chất lượng dữ liệu đầu vào
- 🔒 Tuân thủ Terms of Service của YouTube khi sử dụng

---

## 📝 License

Dự án này được phát hành dưới giấy phép **MIT License**.

---

## 📧 Liên hệ

Nếu có bất kỳ câu hỏi hoặc góp ý, vui lòng liên hệ:

- **Email:** tphn26.work@mgmail.com
- **GitHub:** [@tetsde](https://github.com/tetsde)

---

## 🙏 Acknowledgments

- Cảm ơn cộng đồng Python và các thư viện open-source
- Dữ liệu huấn luyện từ các nguồn công khai tiếng Việt
- Selenium WebDriver team

---

<div align="center">
  
**⭐ Nếu dự án hữu ích, đừng quên cho 1 star nhé! ⭐**

Made with ❤️ by [Hoài Nam]

</div>
