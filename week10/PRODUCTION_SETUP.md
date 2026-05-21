# Production Setup Guide

## 1. Install Docker

Cài Docker Desktop:

https://www.docker.com/products/docker-desktop/

---

## 2. Build container

```bash
docker-compose up --build
```

---

## 3. Run container

```bash
docker-compose up -d
```

---

## 4. Monitoring

Metrics endpoint:

```text
http://127.0.0.1:5012/metrics
```

---

## 5. Logs

Application logs:

```text
logs/app.log
```

Audit logs:

```text
logs/audit.log
```

---

## 6. Security

Project đã bật:

- CSP headers
- X-Frame-Options
- Rate limiting
- Audit logs
- Circuit breaker

---