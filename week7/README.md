2526II_INT3505_1 / week7 /
Mục tiêu của phần thực hành này là dựng backend Python từ OpenAPI spec và kết nối MongoDB để thao tác CRUD cho resource Product.

Cấu trúc
openapi.yaml: đặc tả API cho Product (dùng Flasgger trong code)

requirements.txt: danh sách thư viện Python (Flask, PyMongo, Flasgger,...)

src/server.py: entrypoint chạy server

src/app.py: cấu hình Flask, Flasgger, routes

src/config/db.py: kết nối MongoDB

src/models/product.py: helper xác thực/serialize Product

src/controllers/product_controller.py: logic CRUD

src/routes/product_routes.py: định tuyến API và Swagger docs

Chạy local
1. Cài dependencies:

Đảm bảo bạn đã kích hoạt môi trường ảo (venv), sau đó chạy:

Bash
python -m pip install -r requirements.txt
2. Tạo file môi trường:

Tạo file .env từ mẫu có sẵn:

Bash
cp .env.example .env
(Đảm bảo thông số MONGO_URI và PORT=5009 trong file .env đã chính xác).

3. Khởi động MongoDB local, rồi chạy backend:

Sử dụng lệnh chạy dạng module để tránh lỗi đường dẫn:

Bash
python -m src.server
4. Mở Swagger UI:

Truy cập đường dẫn sau để kiểm tra tài liệu API:
http://127.0.0.1:5009/apidocs/

API
GET /products: Lấy danh sách tất cả sản phẩm

POST /products: Tạo sản phẩm mới

GET /products/{productId}: Lấy chi tiết một sản phẩm

PUT /products/{productId}: Cập nhật thông tin sản phẩm

DELETE /products/{productId}: Xóa sản phẩm

Ví dụ payload (JSON)
JSON
{
  "name": "Mechanical Keyboard",
  "description": "Compact keyboard with hot-swappable switches",
  "price": 79.99,
  "category": "peripherals",
  "stock": 25,
  "imageUrl": "https://example.com/product.png"
}