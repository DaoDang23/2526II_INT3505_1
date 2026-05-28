# Week11-12 - API Design Patterns with Flask

## Gioi thieu

Project nay mo phong mot backend task management + webhook integration de thuc hanh cac API Design Pattern pho bien.

He thong ket hop nhieu pattern trong cung mot API:

* CRUD pattern cho task management
* Query pattern cho search/filter/sort/pagination
* HATEOAS pattern cho navigation link
* Event-driven pattern cho event log
* Webhook pattern cho external integration
* Swagger/OpenAPI de test API truc quan

---

# Muc tieu bai hoc

## Kien thuc can dat

* Hieu CRUD, Query, HATEOAS, Event-driven va Webhook pattern
* Biet khi nao nen dung REST, GraphQL hoac gRPC
* Hieu cach webhook duoc dung trong Stripe va GitHub
* Hieu event-driven architecture co ban

## Ky nang can lam duoc

* Thiet ke API theo nhieu pattern ket hop
* Tao API co query/filter/pagination
* Them HATEOAS vao response
* Publish event khi co business action
* Dang ky va gui webhook den he thong ngoai
* Viet API documentation bang OpenAPI

---

# Cach chay project

## Tao moi truong

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

## Cai thu vien

```bash
pip install -r requirements.txt
```

## Chay server

```bash
python src/server.py
```

Server mac dinh:

```txt
http://127.0.0.1:5013
```

Swagger UI:

```txt
http://127.0.0.1:5013/docs
```

OpenAPI JSON:

```txt
http://127.0.0.1:5013/openapi.json
```

---

# Cau truc thu muc

```txt
week11-12/
├── README.md
├── API_PATTERN_ANALYSIS.md
├── requirements.txt
├── .env.example
├── docker-compose.yaml
├── docker/
│   └── Dockerfile
└── src/
    ├── app.py
    ├── server.py
    ├── docs.py
    ├── database.py
    ├── helpers/
    │   └── links.py
    ├── routes/
    │   ├── task_routes.py
    │   ├── activity_routes.py
    │   ├── integration_routes.py
    │   └── project_routes.py
    └── services/
        ├── dispatcher.py
        └── integration_service.py
```

---

# Chuc nang chinh

## CRUD Pattern

Task API su dung CRUD pattern.

### Tao task

```http
POST /api/tasks
```

### Lay danh sach task

```http
GET /api/tasks
```

### Lay chi tiet task

```http
GET /api/tasks/{task_id}
```

### Cap nhat task

```http
PUT /api/tasks/{task_id}
```

### Xoa task

```http
DELETE /api/tasks/{task_id}
```

---

# Query Pattern

API ho tro:

* search theo title
* filter theo status
* sort theo created_at
* pagination

Vi du:

```http
GET /api/tasks?status=done&search=api&page=1&limit=5
```

---

# HATEOAS Pattern

Moi task response deu co `_links`.

Vi du:

```json
{
  "id": "123",
  "title": "Learn Flask",
  "_links": {
    "self": "/api/tasks/123",
    "update": "/api/tasks/123",
    "delete": "/api/tasks/123",
    "collection": "/api/tasks"
  }
}
```

Muc dich:

* Giup client discover API
* Giam hardcode URL
* API tu mo ta hanh dong hop le

---

# Event-driven Pattern

Khi tao task hoac project, server publish event.

Vi du:

* task.created
* task.updated
* project.created

Event duoc luu trong event log.

Lay event log:

```http
GET /api/events
```

---

# Webhook Pattern

Client co the dang ky webhook endpoint.

### Dang ky webhook

```http
POST /api/integrations/webhooks
```

Payload:

```json
{
  "url": "https://webhook.site/your-id",
  "events": ["task.created", "project.created"]
}
```

Khi co event moi:

* server gui HTTP POST toi URL
* webhook duoc ky bang HMAC SHA256
* ket qua duoc luu vao delivery log

Lay delivery log:

```http
GET /api/integrations/deliveries
```

---

# Swagger/OpenAPI

Test API truc tiep:

```txt
http://127.0.0.1:5013/docs
```

---

# REST vs GraphQL vs gRPC

## REST

Dung khi:

* API public
* resource ro rang
* de test bang browser/Postman

Project nay dung REST.

## GraphQL

Dung khi:

* frontend can query linh hoat
* can tranh over-fetching

## gRPC

Dung khi:

* service-to-service communication
* can latency thap
* can streaming

---

# Phan tich Stripe va GitHub

```txt
API_PATTERN_ANALYSIS.md
```

Noi dung gom:

* CRUD pattern
* Webhook pattern
* Event-driven architecture
* Pagination
* Signature verification
* Rate limiting

---

# Bien moi truong

`.env.example`

```env
PORT=5013
FLASK_DEBUG=0
WEBHOOK_TIMEOUT=3
```

---

# Docker

Build image:

```bash
docker build -t week11-api -f docker/Dockerfile .
```

Run container:

```bash
docker-compose up -d
```

---

# Han che cua demo

* Du lieu dang luu in-memory
* Chua dung database that
* Chua co authentication
* Chua co retry queue cho webhook
* Chua co background worker

