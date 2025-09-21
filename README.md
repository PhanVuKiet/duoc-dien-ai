# Dược Điển AI 💊

**Trợ lý Dược sĩ lâm sàng AI thông minh, chuyên nghiệp và đáng tin cậy.**

## Giới thiệu

Dược Điển AI là một ứng dụng web được xây dựng nhằm hỗ trợ các chuyên gia y tế, dược sĩ và sinh viên ngành y dược trong việc tra cứu thông tin thuốc và phân tích đơn thuốc một cách nhanh chóng và chuyên sâu. Ứng dụng tận dụng sức mạnh của các mô hình ngôn ngữ lớn (LLMs) từ Google để cung cấp thông tin dược lý chính xác và các cảnh báo dược lâm sàng quan trọng.

## Dùng thử ứng dụng

Bạn có thể trải nghiệm trực tiếp Dược Điển AI tại địa chỉ:

**[https://duoc-dien-ai.streamlit.app/](https://duoc-dien-ai.streamlit.app/)**

## Tính năng chính

-   **Tra cứu Dược điển thông minh**:
    -   Nhận diện hoạt chất gốc từ tên biệt dược hoặc tên thương mại.
    -   Cung cấp thông tin chi tiết về thuốc theo cấu trúc 10 mục chuyên sâu (cơ chế, dược động học, chỉ định, chống chỉ định, liều dùng...).

-   **Phân tích Đơn thuốc AI**:
    -   Phân tích toàn diện đơn thuốc dựa trên bối cảnh bệnh nhân (bệnh lý nền, dị ứng).
    -   Cảnh báo các tương tác thuốc-thuốc, tương tác thuốc-bệnh có ý nghĩa lâm sàng.
    -   Kiểm tra chống chỉ định, trùng lặp trị liệu và nguy cơ "thác kê đơn".

-   **Hệ thống Tài khoản cá nhân**:
    -   Lưu trữ lịch sử tra cứu.
    -   Tạo và quản lý các bộ sưu tập thuốc theo chủ đề (ví dụ: Tim mạch, Tiểu đường).

-   **Phiên bản PRO**:
    -   Mở rộng giới hạn sử dụng các tính năng.
    -   Truy cập các chức năng nâng cao như phân tích tóm tắt các thử nghiệm lâm sàng mới nhất từ PubMed.

## Kiến trúc & Công nghệ

Ứng dụng được xây dựng trên một ngăn xếp công nghệ hiện đại và mạnh mẽ:

-   **Giao diện người dùng (Frontend)**: [Streamlit](https://streamlit.io/)
-   **Ngôn ngữ lập trình**: Python 3.11
-   **Mô hình AI**: [Google Gemini](https://ai.google.dev/)
-   **Xác thực & Cơ sở dữ liệu**: [Firebase (Authentication & Realtime Database)](https://firebase.google.com/)
-   **Quản lý Mã PRO**: [Google Sheets API](https://developers.google.com/sheets/api)
-   **Triển khai (Deployment)**: Streamlit Community Cloud
-   **Quản lý phiên bản**: Git & Github

## Hướng dẫn Cài đặt & Chạy trên máy cá nhân

Để chạy dự án này trên máy tính của bạn, hãy làm theo các bước sau:

#### 1. Yêu cầu cần có
-   Cài đặt [Python 3.11](https://www.python.org/downloads/).
-   Cài đặt [Git](https://git-scm.com/downloads).

#### 2. Sao chép (Clone) mã nguồn
Mở terminal và chạy lệnh sau:
```bash
git clone [https://github.com/TEN_NGUOI_DUNG_CUA_BAN/duoc-dien-ai.git](https://github.com/TEN_NGUOI_DUNG_CUA_BAN/duoc-dien-ai.git)
cd duoc-dien-ai\
```
#### 3. Cài đặt các thư viện cần thiết
Mở terminal và chạy lệnh sau:
```bash
pip install -r requirements.txt
cd duoc-dien-ai
```
#### 4. Cấu hình các biến môi trường (Rất quan trọng)
Tạo một thư mục tên là .streamlit bên trong thư mục gốc của dự án. Bên trong thư mục .streamlit, tạo một file tên là secrets.toml.
Sao chép toàn bộ nội dung dưới đây và dán vào file secrets.toml của bạn, sau đó điền các thông tin bí mật tương ứng mà bạn đã tạo ở các bước trước.
```bash
# File: .streamlit/secrets.toml

##### 1. API KEY CỦA GOOGLE AI STUDIO
GOOGLE_API_KEY = "AIzaSy..."

##### 2. CẤU HÌNH KẾT NỐI FIREBASE
[firebase]
apiKey = "AIzaSy..."
authDomain = "ten-du-an.firebaseapp.com"
databaseURL = "[https://ten-du-an-default-rtdb.vung-mien.firebasedatabase.app](https://ten-du-an-default-rtdb.vung-mien.firebasedatabase.app)"
projectId = "ten-du-an"
storageBucket = "ten-du-an.appspot.com"
messagingSenderId = "..."
appId = "..."

##### 3. CẤU HÌNH KẾT NỐI GOOGLE SHEETS
[connections.gsheets]
# ID của trang tính Google Sheets chứa mã PRO
spreadsheet_id = "..."

# Nội dung từ file JSON của Service Account
[connections.gsheets.credentials]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = """-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"""
client_email = "...@...iam.gserviceaccount.com"
client_id = "..."
auth_uri = "[https://accounts.google.com/o/oauth2/auth](https://accounts.google.com/o/oauth2/auth)"
token_uri = "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)"
auth_provider_x509_cert_url = "[https://www.googleapis.com/oauth2/v1/certs](https://www.googleapis.com/oauth2/v1/certs)"
client_x509_cert_url = "[https://www.googleapis.com/robot/v1/metadata/x509/](https://www.googleapis.com/robot/v1/metadata/x509/)..."

##### 4. CẤU HÌNH TÊN MODEL AI
[models]
lookup = "gemini-2.5-flash-lite"
pro = "gemini-2.5-pro"
prescription = "gemini-2.5-pro"

##### 5. API KEY PHỤ (NẾU CÓ)
[api_keys]
pubmed = "..."
```

#### 5. Deploy app

