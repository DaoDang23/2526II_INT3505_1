import requests
import uuid
import json

BASE_URL = 'http://localhost:5000'


print('\n========== HOME ==========' )
resp = requests.get(f'{BASE_URL}/')
print(resp.json())


print('\n========== HEALTH ==========' )
resp = requests.get(f'{BASE_URL}/health')
print(resp.json())


print('\n========== V1 PAYMENT ==========' )
resp = requests.post(
    f'{BASE_URL}/api/v1/payments',
    json={
        'amount': 100,
        'currency': 'USD'
    }
)

print(resp.status_code)
print(resp.json())
print(dict(resp.headers))

v1_transaction_id = resp.json()['transaction_id']


print('\n========== V1 LOOKUP ==========' )
resp = requests.get(
    f'{BASE_URL}/api/v1/payments/{v1_transaction_id}'
)
print(resp.json())


print('\n========== V2 PAYMENT ==========' )
idempotency_key = f'req_{uuid.uuid4()}'

payload = {
    'amount': 250,
    'currency': 'USD',
    'user_id': 'usr_123456',
    'payment_method': 'CREDIT_CARD'
}

headers = {
    'Idempotency-Key': idempotency_key
}

resp = requests.post(
    f'{BASE_URL}/api/v2/payments',
    json=payload,
    headers=headers
)

print(resp.status_code)
print(json.dumps(resp.json(), indent=2))
print(dict(resp.headers))


print('\n========== V2 IDEMPOTENCY RETRY ==========' )
resp = requests.post(
    f'{BASE_URL}/api/v2/payments',
    json=payload,
    headers=headers
)

print(resp.status_code)
print(json.dumps(resp.json(), indent=2))
print(dict(resp.headers))

v2_transaction_id = resp.json()['data']['transaction_id']


print('\n========== V2 LOOKUP ==========' )
resp = requests.get(
    f'{BASE_URL}/api/v2/payments/{v2_transaction_id}'
)
print(json.dumps(resp.json(), indent=2))


print('\n========== HEADER VERSIONING ==========' )
resp = requests.get(
    f'{BASE_URL}/api/v2/payments-header-version',
    headers={
        'API-Version': '2'
    }
)
print(resp.json())


print('\n========== QUERY VERSIONING ==========' )
resp = requests.get(
    f'{BASE_URL}/api/v2/payments-query-version?version=2'
)
print(resp.json())