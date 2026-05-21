# Week 4 - API Specification và OpenAPI

## Mục tiêu bài thực hành

- Viết OpenAPI YAML cho API quản lý sách (5 endpoints)
- Render tài liệu tự động bằng Swagger UI
- Chia sẻ link tài liệu API

---

# Cấu trúc project

```text
week4/
├── app.py
├── books.py
├── openapi.yaml
├── requirements.txt
├── README.md
└── static/
    └── swagger.html
```

---

# Cấu trúc file

| File | Chức năng |
|---|---|
| `openapi.yaml` | OpenAPI 3.0.3 specification |
| `app.py` | Flask server + Swagger UI renderer |
| `books.py` | Xử lý logic Book API |
| `requirements.txt` | Danh sách dependencies |
| `static/swagger.html` | Giao diện Swagger UI |

---

# Công nghệ sử dụng

- Python 3.12
- Flask
- OpenAPI 3.0.3
- Swagger UI

---

# 5 endpoints của Book API

| Method | Endpoint | Chức năng |
|---|---|---|
| GET | `/books` | Lấy danh sách sách |
| POST | `/books` | Tạo sách mới |
| GET | `/books/{book_id}` | Lấy chi tiết sách |
| PUT | `/books/{book_id}` | Cập nhật sách |
| DELETE | `/books/{book_id}` | Xóa sách |

---

# Ví dụ dữ liệu sách

```json
{
  "id": 1,
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "price": 29.99
}
```

---

# Cách chạy project

Từ thư mục gốc project:

## Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python week4/app.py
```

---

# Swagger UI

Swagger UI được dùng để tự động render tài liệu API từ file OpenAPI YAML.

Sau khi chạy server, mở:

```text
http://127.0.0.1:5007/docs
```

Swagger UI sẽ hiển thị:

- Danh sách endpoints
- Request body
- Response schemas
- Parameters
- HTTP methods
- Try it out / Execute API trực tiếp

---

# Link tài liệu Swagger UI

## Local Development

Swagger UI:

```text
http://127.0.0.1:5007/docs
```

OpenAPI YAML:

```text
http://127.0.0.1:5007/openapi.yaml
```

---

# Demo sử dụng Swagger UI

## 1. Lấy danh sách sách

Endpoint:

```http
GET /books
```

Nhấn:

```text
Try it out → Execute
```

Swagger sẽ tự gửi request và hiển thị response JSON.

---

## 2. Tạo sách mới

Endpoint:

```http
POST /books
```

Ví dụ request body:

```json
{
  "title": "Flask API",
  "author": "John Doe",
  "price": 19.99
}
```

Response:

```json
{
  "id": 2,
  "title": "Flask API",
  "author": "John Doe",
  "price": 19.99
}
```

---

# OpenAPI Specification

File:

```text
openapi.yaml
```

định nghĩa:

- `paths`
- `components`
- `schemas`
- `parameters`
- `requestBody`
- `responses`

theo chuẩn OpenAPI 3.0.3.

---

# Swagger UI hoạt động như thế nào

```text
openapi.yaml
        ↓
Swagger UI đọc specification
        ↓
Render thành giao diện tài liệu API
```

Swagger UI giúp:

- Tài liệu hóa API tự động
- Giảm viết README thủ công
- Hỗ trợ frontend/backend integration
- Test API trực tiếp trên browser

---

# Deploy lên Vercel

Cấu hình deploy:

```text
vercel.json
api/index.py
requirements.txt
```

---

# Các bước deploy

## 1. Push code lên GitHub

```bash
git add .
git commit -m "add week4 openapi swagger demo"
git push origin main
```

---

## 2. Import repo vào Vercel

- Vào Vercel Dashboard
- Chọn:

```text
Add New Project
```

- Import GitHub repository

---

## 3. Environment Variables

Thêm các biến môi trường:

```env
FLASK_ENV=production
FLASK_DEBUG=0
JWT_SECRET=<secret-manh>
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

---

## 4. Deploy

Nhấn:

```text
Deploy
```

---

# Link sau khi deploy

Swagger UI:

```text
https://<your-vercel-domain>/docs
```

OpenAPI YAML:

```text
https://<your-vercel-domain>/openapi.yaml
```

---

# Tài liệu tham khảo

- OpenAPI Specification: https://swagger.io/specification/
- Swagger UI: https://swagger.io/tools/swagger-ui/
- Flask Documentation: https://flask.palletsprojects.com/