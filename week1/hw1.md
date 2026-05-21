# Bài Tập Về Nhà – Buổi 1
## Tìm và phân tích 3 API công khai

---

## 1. GitHub API

### Giới thiệu
GitHub API cho phép ứng dụng bên ngoài truy cập dữ liệu trên GitHub như thông tin người dùng, repository, issue, pull request...

### Đường dẫn (Endpoint)
```
GET https://api.github.com/users/{username}
```

### Ví dụ Request
```
GET https://api.github.com/users/octocat
```

### Ví dụ Response
```json
{
  "login": "octocat",
  "name": "The Octocat",
  "public_repos": 8,
  "followers": 10000,
  "bio": "A mysterious octocat"
}
```

### Phân tích thuộc tính

| Thuộc tính        | Giá trị              |
|-------------------|----------------------|
| Loại API          | REST API             |
| Giao thức         | HTTPS                |
| Định dạng dữ liệu | JSON                 |
| Xác thực          | Không cần (public)   |
| Phiên bản         | v3                   |

### Ứng dụng
- Xây dựng dashboard quản lý project trên GitHub
- Công cụ thống kê, phân tích repository
- Tích hợp đăng nhập bằng tài khoản GitHub

---

## 2. OpenWeatherMap API

### Giới thiệu
OpenWeatherMap API cung cấp dữ liệu thời tiết theo thời gian thực cho bất kỳ thành phố nào trên thế giới: nhiệt độ, độ ẩm, tốc độ gió...

### Đường dẫn (Endpoint)
```
GET https://api.openweathermap.org/data/2.5/weather
```

### Ví dụ Request
```
GET https://api.openweathermap.org/data/2.5/weather?q=Hanoi&appid={API_KEY}&units=metric
```

### Ví dụ Response
```json
{
  "name": "Hanoi",
  "main": {
    "temp": 32.5,
    "humidity": 78
  },
  "weather": [
    { "description": "mây rải rác" }
  ],
  "wind": {
    "speed": 3.2
  }
}
```

### Phân tích thuộc tính

| Thuộc tính        | Giá trị                    |
|-------------------|----------------------------|
| Loại API          | REST API                   |
| Giao thức         | HTTPS                      |
| Định dạng dữ liệu | JSON                       |
| Xác thực          | API Key (query parameter)  |
| Phiên bản         | v2.5                       |

### Ứng dụng
- App dự báo thời tiết cho người dùng
- Hệ thống cảnh báo thời tiết tự động
- Dashboard nông nghiệp, vận tải theo dõi thời tiết

---

## 3. Bybit API

### Giới thiệu
Bybit API cung cấp dữ liệu thị trường tiền điện tử theo thời gian thực: giá, khối lượng giao dịch 24h, biến động giá...

### Đường dẫn (Endpoint)
```
GET https://api.bybit.com/v5/market/tickers
```

### Ví dụ Request
```
GET https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT
```

### Ví dụ Response
```json
{
  "result": {
    "list": [
      {
        "symbol": "BTCUSDT",
        "lastPrice": "60000",
        "volume24h": "12345",
        "price24hPcnt": "0.0215"
      }
    ]
  }
}
```

### Phân tích thuộc tính

| Thuộc tính        | Giá trị                  |
|-------------------|--------------------------|
| Loại API          | REST API                 |
| Giao thức         | HTTPS                    |
| Định dạng dữ liệu | JSON                     |
| Xác thực          | Không cần (public endpoint) |
| Phiên bản         | v5                       |

### Ứng dụng
- Bot giao dịch tự động (trading bot)
- App theo dõi giá tiền điện tử
- Phân tích dữ liệu thị trường crypto
