# Week10 - Production API Security & Monitoring

## Nội dung thực hành

- Logging JSON
- Monitoring với Prometheus
- Rate limiting
- Circuit breaker
- Security headers
- Docker deploy

---

# Cấu trúc project

```text
src/
├── app.py
├── server.py
├── config/
├── middleware/
└── routes/
```

---

# Cài đặt

```bash
cd week10

python -m pip install -r requirements.txt
```

---

# Chạy project

```bash
python src/server.py
```

Server chạy tại:

```text
http://127.0.0.1:5012
```

---

# Endpoints

## Health Check

```http
GET /health
```

---

## Metrics

```http
GET /metrics
```

---

## Get Users

```http
GET /api/users
```

---

## Create User

```http
POST /api/users
```

Body:

```json
{
  "name": "David"
}
```

---

# Logging

File log:

```text
logs/app.log
logs/audit.log
```

---

# Rate Limiting

Giới hạn:

```text
60 requests / minute
```

Nếu vượt giới hạn:

```json
{
  "error": "Too many requests"
}
```

---

# Circuit Breaker

Sau nhiều request lỗi liên tiếp:

```json
{
  "error": "Service temporarily unavailable"
}
```

---

# Docker

Build:

```bash
docker-compose up -d
```

---

# Test Rate Limit

```bash
for i in {1..65}; do
  curl http://127.0.0.1:5012/api/users
done
```

---

# Test Circuit Breaker

```bash
for i in {1..6}; do
  curl -X POST http://127.0.0.1:5012/api/users \
    -H "Content-Type: application/json" \
    -d '{}'
done
```