# README.md

# Week11-12 - Advanced API Design Patterns with Flask

## Gioi thieu

Project nay mo phong mot backend ecommerce + notification system dung Flask.

Muc tieu la demo nhieu API design pattern trong cung mot he thong:

* CRUD
* Query pattern
* HATEOAS
* Event-driven architecture
* Webhook integration
* OpenAPI documentation

Project lay cam hung tu cach thiet ke API cua:

* Stripe
* GitHub

---

# Muc tieu bai hoc

## Kien thuc can dat

* Hieu CRUD, Query, HATEOAS, Event-driven va Webhook pattern
* Phan biet REST, gRPC va GraphQL
* Hieu cach webhook duoc dung trong he thong thuc te
* Hieu event-driven architecture trong backend

---

## Ky nang can lam duoc

* Thiet ke API theo resource
* Them query/filter/sort/pagination
* Tao response HATEOAS
* Publish event sau business action
* Dang ky webhook endpoint
* Gui webhook signed request
* Viet OpenAPI docs

---

# Cau truc thu muc

```txt
week11-12/
├── README.md
├── API_PATTERN_ANALYSIS.md
├── requirements.txt
├── .env.example
└── src/
    ├── app.py
    ├── server.py
    ├── openapi.py
    ├── storage.py
    ├── routes/
    │   ├── catalog_routes.py
    │   ├── activity_routes.py
    │   └── integration_routes.py
    ├── services/
    │   ├── dispatcher.py
    │   └── outbound_webhook.py
    └── utils/
        └── links.py
```

---

# Chuc nang chinh

## Product Catalog API

CRUD cho product:

* create product
* get product
* update product
* delete product

Co:

* filter
* search
* sort
* pagination

---

## HATEOAS

Moi resource tra ve:

```json
"_links": {
  "self": {},
  "update": {},
  "delete": {}
}
```

Client co the discover action tiep theo.

---

# Event-driven Pattern

Khi:

* tao notification
* tao order

server publish event.

Vi du:

```txt
notification.created
order.created
```

Event duoc luu vao event log.

---

# Webhook Pattern

Client dang ky webhook URL.

Khi co event:

* notification.created
* order.created

server gui HTTP POST den external service.

Moi request co:

```txt
X-Webhook-Signature
```

---

# Cai dat

## Tao virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Cai dependencies

```bash
pip install -r requirements.txt
```

---

# Tao file environment

Windows:

```powershell
copy .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

---

# Chay server

```bash
python src/server.py
```

Server mac dinh:

```txt
http://127.0.0.1:5013
```

---

# Swagger UI

Swagger docs:

```txt
http://127.0.0.1:5013/docs
```

OpenAPI JSON:

```txt
http://127.0.0.1:5013/openapi.json
```

---

# API Endpoint

| Method | Endpoint                      | Pattern      |
| ------ | ----------------------------- | ------------ |
| GET    | /                             | HATEOAS      |
| GET    | /docs                         | Swagger      |
| GET    | /openapi.json                 | OpenAPI      |
| POST   | /api/catalog/items            | CRUD         |
| GET    | /api/catalog/items            | Query        |
| GET    | /api/catalog/items/{id}       | CRUD         |
| PUT    | /api/catalog/items/{id}       | CRUD         |
| DELETE | /api/catalog/items/{id}       | CRUD         |
| POST   | /api/activities/notifications | Event-driven |
| POST   | /api/activities/orders        | Event-driven |
| GET    | /api/activities/events        | Event log    |
| POST   | /api/integrations/webhooks    | Webhook      |
| GET    | /api/integrations/webhooks    | Webhook      |
| GET    | /api/integrations/deliveries  | Webhook      |

---

# Query Pattern Demo

Endpoint:

```txt
GET /api/catalog/items
```

Support:

| Parameter | Meaning         |
| --------- | --------------- |
| category  | filter category |
| search    | search by name  |
| min_price | minimum         |
| max_price | maximum         |
| sort      | sort field      |
| page      | current page    |
| limit     | items per page  |

Vi du:

```bash
curl "http://127.0.0.1:5013/api/catalog/items?search=python&sort=-price&page=1&limit=5"
```

---

# Tao Product

```bash
curl -X POST http://127.0.0.1:5013/api/catalog/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Architecture",
    "category": "book",
    "price": 40
  }'
```

---

# Dang ky Webhook

Dung webhook.site:

```bash
curl -X POST http://127.0.0.1:5013/api/integrations/webhooks \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://webhook.site/your-id",
    "events": ["notification.created"],
    "secret": "demo-secret"
  }'
```

---

# Trigger Notification Event

```bash
curl -X POST http://127.0.0.1:5013/api/activities/notifications \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Payment success",
    "recipient": "user_01"
  }'
```

---

# Delivery Log

```bash
GET /api/integrations/deliveries
```

---

# REST vs gRPC vs GraphQL

## REST

Dung khi:

* public API
* resource-oriented
* webhook integration

---

## gRPC

Dung khi:

* internal microservices
* low latency
* streaming

---

## GraphQL

Dung khi:

* frontend can flexible query
* nested data complexity cao

---

# Gioi han cua demo

* in-memory storage
* khong co database that
* khong retry webhook failed
* khong auth
* khong async queue

Project tap trung vao:

* API design pattern
* event flow
* webhook architecture
* HATEOAS
* query strategy
