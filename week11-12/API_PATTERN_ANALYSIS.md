# API_PATTERN_ANALYSIS.md

# API Design Pattern Analysis - Stripe vs GitHub

## Muc tieu

Tai lieu nay phan tich cac API design pattern duoc su dung trong Stripe va GitHub. Day la hai he thong API rat pho bien va la vi du tot cho:

* RESTful resource design
* Query va filtering
* Webhook integration
* Event-driven architecture
* Security pattern
* Pagination strategy
* API scalability

---

# 1. Stripe API Analysis

## Tong quan

Stripe la nen tang thanh toan online cung cap API cho:

* payment
* customer
* invoice
* subscription
* webhook
* billing

Stripe API duoc xem la mot trong nhung REST API de dung nhat hien nay.

---

# Resource-oriented REST

Stripe to chuc API theo resource:

| Resource       | Endpoint            |
| -------------- | ------------------- |
| Customer       | /v1/customers       |
| Payment Intent | /v1/payment_intents |
| Subscription   | /v1/subscriptions   |
| Invoice        | /v1/invoices        |

CRUD duoc mapping ro rang qua HTTP method:

| HTTP Method | Y nghia      |
| ----------- | ------------ |
| GET         | Lay resource |
| POST        | Tao resource |
| DELETE      | Xoa resource |

Vi du tao customer:

```bash
curl https://api.stripe.com/v1/customers \
  -u sk_test_xxx: \
  -d email="user@example.com"
```

---

# Query Pattern

Stripe ho tro:

* filtering
* pagination
* expand object
* search

Vi du:

```bash
GET /v1/payment_intents?limit=10
```

Pagination cua Stripe dung:

* limit
* starting_after
* ending_before

Day la cursor-based pagination.

Loi ich:

* nhanh voi dataset lon
* khong bi duplicate khi data thay doi
* phu hop realtime transaction

---

# Event-driven Architecture

Stripe dung event-driven architecture rat manh.

Khi co:

* payment success
* refund
* invoice paid
* subscription canceled

Stripe se tao event.

Vi du:

```json
{
  "type": "payment_intent.succeeded"
}
```

Event duoc dung cho:

* analytics
* notification
* accounting
* webhook integration

---

# Webhook Pattern

Webhook la core integration cua Stripe.

Client dang ky webhook URL:

```txt
https://example.com/webhook
```

Stripe se POST event den URL nay.

Header quan trong:

```txt
Stripe-Signature
```

Server receiver phai verify signature.

Loi ich:

* tranh fake request
* tranh modified payload
* xac thuc event dung tu Stripe

---

# Idempotency Pattern

Stripe dung:

```txt
Idempotency-Key
```

cho POST request.

Muc dich:

Neu client retry request do timeout/network error thi Stripe khong tao duplicate payment.

Day la pattern rat quan trong trong financial API.

---

# Security Pattern

Stripe dung:

* HTTPS only
* API key
* webhook signature
* rate limit
* audit log

Tat ca request deu dung TLS.

---

# 2. GitHub API Analysis

## Tong quan

GitHub API cung cap:

* repository management
* issue tracking
* pull request
* webhook
* actions

GitHub co ca:

* REST API
* GraphQL API

---

# REST Resource Design

GitHub dung resource ro rang:

| Resource     | Endpoint |
| ------------ | -------- |
| Repository   | /repos   |
| Issue        | /issues  |
| Pull Request | /pulls   |
| User         | /users   |

Vi du:

```bash
GET /repos/octocat/Hello-World
```

---

# Query Pattern

GitHub search API rat manh.

Vi du:

```bash
GET /search/repositories?q=python
```

Support:

* sort
* filter
* page
* per_page

GitHub REST pagination dung:

* Link header
* page
* per_page

---

# GraphQL Pattern

GitHub GraphQL API cho phep:

* client tu dinh nghia response shape
* lay nested data trong mot request
* giam over-fetching

Vi du:

* repository
* owner
* issues
* contributors

co the lay trong mot request GraphQL.

GraphQL phu hop voi:

* frontend phuc tap
* dashboard
* mobile app

---

# Webhook Pattern

GitHub webhook duoc dung cho:

* push event
* pull_request event
* issue event

Vi du:

```txt
X-Hub-Signature-256
```

duoc dung de verify request.

Webhook rat pho bien trong:

* CI/CD
* automation
* deployment pipeline

---

# Rate Limiting

GitHub dung rate limit theo token.

Response header:

```txt
X-RateLimit-Limit
X-RateLimit-Remaining
X-RateLimit-Reset
```

Loi ich:

* bao ve infrastructure
* tranh abuse API

---

# So sanh Stripe va GitHub

| Feature                | Stripe           | GitHub              |
| ---------------------- | ---------------- | ------------------- |
| REST API               | Co               | Co                  |
| GraphQL                | Khong phai core  | Co                  |
| Webhook                | Rat manh         | Rat manh            |
| Event-driven           | Core pattern     | Core pattern        |
| Cursor Pagination      | Co               | Mot phan            |
| Page Pagination        | It dung          | Pho bien            |
| Signature Verification | Stripe-Signature | X-Hub-Signature-256 |
| Idempotency            | Co               | Khong pho bien      |
| Rate Limit             | Co               | Co                  |

---

# Bai hoc rut ra cho project week11-12

Project week11-12 ap dung cac pattern tu Stripe va GitHub:

| Pattern                | Project                    |
| ---------------------- | -------------------------- |
| CRUD                   | Product API                |
| Query                  | Search/filter/sort         |
| HATEOAS                | _links field               |
| Event-driven           | Notification + order event |
| Webhook                | Subscription + delivery    |
| Signature verification | X-Webhook-Signature        |
| Pagination             | page + limit               |

---

# Khi nao dung REST, gRPC, GraphQL

## REST

Nen dung khi:

* API public
* resource ro rang
* can Swagger/curl/Postman
* webhook integration

Project week11-12 dung REST vi:

* don gian
* de debug
* phu hop CRUD

---

## gRPC

Nen dung khi:

* service-to-service
* latency thap
* binary protocol
* streaming

Khong qua phu hop cho demo webhook public.

---

## GraphQL

Nen dung khi:

* frontend can flexible query
* nested data phuc tap
* tranh over-fetching

Vi du dashboard ecommerce.

---

# Ket luan

Stripe va GitHub deu cho thay:

* REST van rat manh cho public API
* webhook la integration pattern cuc ky quan trong
* event-driven architecture giup mo rong he thong
* signature verification la bat buoc cho webhook security
* pagination va query design anh huong lon den scalability

Project week11-12 da ket hop cac pattern nay de tao mot he thong API nho nhung day du:

* CRUD
* Query
* HATEOAS
* Event-driven
* Webhook
* OpenAPI documentation
