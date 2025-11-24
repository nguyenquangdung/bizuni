# Hướng dẫn chuyển từ text thô sang trang HTML đẹp (theo template Bài 1/Bài 5)

## 1) Chuẩn bị nội dung
- Gom các ghi chú, bullet hoặc đoạn văn từ file text thô.
- Chia thành các phần chính (H1/H2) và tiểu mục (H3/H4) để tạo mục lục rõ ràng.
- Đánh dấu các phần cần nhấn mạnh (lưu ý, cảnh báo, trích dẫn) để chuyển thành các "note box" hoặc blockquote.

## 2) Tạo khung HTML cơ bản
- Dùng skeleton đã có trong `Bai-5.html`:
  - Khai báo `<!DOCTYPE html>`, thẻ `<html lang="vi">`, `<meta charset>` và `<meta viewport>`.
  - Nhúng Tailwind CDN: `<script src="https://cdn.tailwindcss.com"></script>` và cấu hình font Inter + Merriweather.
  - Giữ cấu trúc header sticky + main content + sidebar (nếu cần TOC) để có bố cục nhất quán.
- Sao chép các lớp tiện ích dùng sẵn:
  - `.content-area` cho typography chính, `.note-box` cho khối lưu ý, `.table-wrap` cho bảng.
  - Các đoạn JavaScript cuối file để sinh TOC tự động và kích hoạt icon Lucide.

## 3) Đưa nội dung vào khung
- Mở phần `<!-- Nội dung -->` và thay thế các tiêu đề/h3/h4 theo dàn ý ở bước 1.
- Mỗi ý ngắn nên để dạng `<ul><li>...</li></ul>`; các luận điểm dài dùng `<p>`.
- Nếu có bảng so sánh, quấn trong `<div class="table-wrap">` rồi dùng `<table><thead><tbody>`.
- Các lưu ý quan trọng bọc trong `<div class="note-box">Nội dung lưu ý...</div>`.

## 4) Tối ưu hiển thị
- Kiểm tra heading có dạng số thứ tự để TOC tự sinh đẹp (ví dụ `1. Tổng quan`, `2. Chiến lược ...`).
- Giữ câu ngắn, xuống dòng hợp lý; tránh copy nguyên văn text thô chưa dọn sạch.
- Dùng các lớp màu đã có (màu cam `topas.orange`, nền `topas.bg`) thay vì tự đặt inline style.
- Nếu muốn thêm mục lục nổi trên mobile, giữ nút "Mục lục" và modal đã có ở cuối file.

## 5) Xuất bản/kiểm tra
- Lưu file thành `Bai-x.html` mới hoặc thay thế bài hiện có.
- Mở file bằng trình duyệt để soát lỗi font, spacing, liên kết mục lục.
- Nếu cần chỉnh nhanh, chỉ sửa phần nội dung; hạn chế động vào phần cấu hình Tailwind/JS.

> Mẹo nhanh: copy nguyên thân trang từ `Bai-5.html`, dán vào file mới, rồi thay phần trong `<div id="article-content"> ... </div>` bằng nội dung đã chuẩn hóa. Phần còn lại giữ nguyên để đảm bảo layout đồng nhất.
