# API Versioning & Lifecycle Management Demo
## Chạy project

### Cài thư viện

pip install -r requirements.txt

### Chạy server

python server.py

### Chạy client

python client.py

---

## Các chiến lược versioning

### 1. URL Path Versioning

/api/v1/payments
/api/v2/payments

Ưu điểm:
- Dễ test
- Dễ nhìn
- Dễ cache

Nhược điểm:
- URL dài hơn

---

### 2. Header Versioning

API-Version: 2

Ưu điểm:
- URL sạch
- RESTful hơn

Nhược điểm:
- Khó test bằng browser

---
### 3. Query Parameter Versioning

/payments?version=2

Ưu điểm:
- Linh hoạt

Nhược điểm:
- Dễ bị bỏ sót

---

## Breaking Changes từ v1 -> v2

### v1

{
  "amount": 100
}

### v2

{
  "amount": 100,
  "user_id": "usr_123",
  "payment_method": "CREDIT_CARD"
}

---

## Deprecation Policy

v1 sẽ bị sunset vào 31/12/2026.

Headers:

Deprecation
Sunset
Warning
Link

---

## Migration Plan

### Step 1
Đổi endpoint:

/api/v1/payments
→
/api/v2/payments

### Step 2
Cập nhật request body.

### Step 3
Cập nhật parsing response.

### Step 4
Thêm Idempotency-Key.

### Step 5
Cập nhật status code checking.