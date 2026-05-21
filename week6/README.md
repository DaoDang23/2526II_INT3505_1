# Week 6 - Authentication và Authorization

## Mục tiêu

- Triển khai JWT Authentication
- Tìm hiểu Authorization bằng roles
- Thực hiện security audit cho API

---

# Cấu trúc project

week6/

- app.py
- auth.py
- security.py
- requirements.txt
- README.md

---

# Kiến thức chính

## JWT Authentication

JWT gồm:

- Header
- Payload
- Signature

Dùng để xác thực người dùng stateless.

---

# JWT vs OAuth2

| JWT | OAuth2 |
|---|---|
| Xác thực token | Framework authorization |
| Đơn giản | Phức tạp hơn |
| Phù hợp app nhỏ | Phù hợp hệ thống lớn |

---

# Bearer Token

Client gửi:

```http
Authorization: Bearer <token>