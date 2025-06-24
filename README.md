# Phân tích cảm xúc quan đáng giá sản phẩm của khách hàng
## Tổng quan
Dự án này thực hiện phân tích cảm xúc trên dữ liệu văn bản tiếng Việt, phân loại các đánh giá thành ba loại cảm xúc: Tích cực (POS), Tiêu cực (NEG) và Trung lập (NEU). Bộ dữ liệu được phân tích, tiền xử lý và chuẩn bị cho việc huấn luyện mô hình học máy.

## Bộ dữ liệu
- **Nguồn**: Dữ liệu được lưu trữ trong file `data/data.csv`.
- **Các cột**:
  - `content`: Nội dung văn bản của các đánh giá.
  - `label`: Nhãn cảm xúc (POS, NEG, NEU).
  - `start`: Điểm đánh giá (từ 1 đến 5 sao).
  - `text_length`: Độ dài của văn bản.
  - `word_count`: Số từ trong văn bản.
- **Kích thước**: Ban đầu có 31,436 mẫu, giảm xuống còn 26,472 mẫu sau khi làm sạch.
- **Các bước làm sạch**:
  - Loại bỏ các giá trị bị thiếu trong cột `content`.
  - Loại bỏ các hàng trùng lặp dựa trên cột `content`.
  - Loại bỏ các văn bản quá ngắn (<3 ký tự).

## Tiền xử lý
- **Tiền xử lý văn bản**:
  - Chuyển đổi văn bản sang chữ thường.
  - Thay thế các mã "teen code" phổ biến trong tiếng Việt (ví dụ: "2day" → "hôm nay", "ko" → "không").
  - Loại bỏ dấu câu.
  - Loại bỏ khoảng trắng thừa.
- **Kỹ thuật tạo đặc trưng**:
  - Tính toán `text_length` và `word_count` để phân tích.
  - Phân tích phân bố cảm xúc và mối quan hệ giữa `start` và `label`.

## Phụ thuộc
Xem file `requirements.txt` để biết danh sách các gói Python cần thiết.

## Cài đặt
1. Sao chép kho lưu trữ:
   ```bash
   git clone <url-kho-lưu-trữ>
   ```
2. Cài đặt các gói phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```
3. Đảm bảo file dữ liệu (`data/data.csv`) được đặt trong thư mục đúng.

## Sử dụng
- Mở notebook `VNS.ipynb` trong Jupyter để khám phá các bước phân tích dữ liệu và tiền xử lý.
- Notebook bao gồm:
  - Tải và khám phá dữ liệu.
  - Trực quan hóa phân bố cảm xúc.
  - Phân tích độ dài văn bản và số từ theo cảm xúc.
  - Tiền xử lý văn bản để chuẩn bị cho việc huấn luyện mô hình.

## Công việc tương lai
- Triển khai các mô hình học máy (ví dụ: Naive Bayes, SVM, Random Forest, Logistic Regression) để phân loại cảm xúc.
- Thực hiện trích xuất đặc trưng bằng TF-IDF hoặc CountVectorizer.
- Đánh giá mô hình bằng các chỉ số như độ chính xác, độ chính xác từng lớp, độ phủ và F1-score.

## Giấy phép
Dự án này được cấp phép theo Giấy phép MIT.
