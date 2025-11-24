# Hướng dẫn chuyển text thô thành HTML chuẩn (theo format Bài 1)

## 1) Chuẩn bị nội dung (đủ 100% thông tin)
- Gom toàn bộ đoạn văn, bullet, ví dụ từ file text thô. **Không được bỏ sót ý hoặc con số**.
- Chia thành các khối logic rõ ràng:
  - H2 cho phần chính (I, II, III...).
  - H3/H4 cho tiểu mục (1, 2, 3...).
- Đánh dấu trước các phần cần làm nổi bật (lưu ý, cảnh báo, ví dụ, bảng số liệu) để lên layout sau.

## 2) Dùng khung HTML của Bài 1 (layout đẹp, có TOC)
- Sao chép toàn bộ khung từ `Bai-1.html` hoặc file mới nhất đã chuẩn:
  - Header sticky, nút về trang chủ, nút "Bài kế tiếp".
  - Bố cục 2 cột: sidebar TOC (desktop) + main content.
  - Hero gồm badge, tiêu đề, mô tả, thông tin giảng viên/ngày.
- Giữ nguyên cấu hình Tailwind + font (Inter, Merriweather), màu `topas` và script Lucide.
- Giữ block JS cuối file để tự sinh TOC desktop/mobile và toggle drawer.

## 3) Đưa nội dung vào `<div id="article-content">` (đủ 100%)
- Chuyển toàn bộ text vào các thẻ `<p>`, `<ul>/<ol>`, `<table>` **không lược bỏ chữ**.
- Với phần quan trọng/so sánh, bọc trong card: `bg-white border border-slate-200 rounded-xl p-5 shadow-sm`.
- Lưu ý/cảnh báo dùng nền cam nhạt: `bg-orange-50 border-orange-200`.
- Bảng số liệu quấn trong `<div class="table-wrap">` để tránh tràn.
- Nếu có ví dụ nhiều bước, chia grid 2 cột (`grid grid-cols-1 md:grid-cols-2 gap-4`) giống cách trình bày Bài 1.

## 4) Kiểm tra bố cục và TOC
- Đảm bảo tất cả H2/H3 xuất hiện đúng thứ tự để TOC tự sinh chuẩn.
- Kiểm tra spacing: thêm `space-y-*`, `mt-*`, `mb-*` để nội dung thoáng như Bài 1.
- Đảm bảo các bullet/bảng giữ nguyên số liệu, ví dụ, ký hiệu (%, ≈, →...).

## 5) Soát lần cuối và xuất bản
- Đọc lại toàn bộ bài, so sánh với file text gốc để chắc chắn **100% ý, 100% ví dụ** đã có.
- Mở file HTML trong trình duyệt: kiểm tra font, TOC, liên kết anchor, header sticky.
- Lưu đúng tên `Bai-x.html` và link điều hướng (trang chủ/bài tiếp) nếu có.

> Mẹo nhanh: dán nguyên khung `Bai-1.html`, thay toàn bộ nội dung trong `<div id="article-content"> ... </div>` bằng text đã chuẩn hóa. Không chỉnh phần cấu hình/JS để giữ format đồng nhất.
