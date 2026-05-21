# Week 5 - Data Modeling và Resource Design

## Mục tiêu bài thực hành

- Thiết kế resource tree cho domain thư viện
- Xây dựng API tìm kiếm sách
- Thực hiện phân trang dữ liệu
- Tài liệu API bằng Swagger UI

---

# Cấu trúc project

week5/

- app.py
- models.py
- routes.py
- utils.py
- requirements.txt
- README.md

---

# Data Model

## Books

- id
- title
- author
- category
- available

## Members

- id
- name

## Borrow Records

- id
- member_id
- book_id

---

# Resource Tree

/member/{id}/borrowed-books

Ví dụ:

/members/1/borrowed-books

---

# Pagination Strategy

Project sử dụng page-based pagination:

Example:

/books?page=1&limit=2

Ưu điểm:
- Dễ dùng
- Dễ implement
- Phù hợp dữ liệu nhỏ

Nhược điểm:
- Không tối ưu với dữ liệu lớn
- Có thể bị duplicate khi dữ liệu thay đổi liên tục

---

# Search Endpoint

/books/search?keyword=python

Cho phép tìm kiếm theo title.

---

# API Endpoints

## Books

GET /books

GET /books/search

GET /books/{id}

## Members

GET /members

GET /members/{id}/borrowed-books

---

