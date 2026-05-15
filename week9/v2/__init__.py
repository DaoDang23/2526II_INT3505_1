from flask import Blueprint, jsonify, request
import uuid
import time

v2_bp = Blueprint('v2', __name__, url_prefix='/api/v2')

transactions = {}
idempotency_cache = {}

VALID_PAYMENT_METHODS = [
    'CREDIT_CARD',
    'DEBIT_CARD',
    'E_WALLET',
    'BANK_TRANSFER'
]

VALID_CURRENCIES = ['USD', 'EUR', 'VND', 'GBP']


@v2_bp.route('/payments', methods=['POST'])
def create_payment_v2():
    data = request.get_json()

    errors = []

    amount = data.get('amount')
    user_id = data.get('user_id')
    payment_method = data.get('payment_method')
    currency = data.get('currency', 'USD')

    if amount is None:
        errors.append('amount is required')

    if user_id is None:
        errors.append('user_id is required')

    if payment_method is None:
        errors.append('payment_method is required')

    if payment_method and payment_method not in VALID_PAYMENT_METHODS:
        errors.append(
            f'payment_method must be one of: {VALID_PAYMENT_METHODS}'
        )

    if currency not in VALID_CURRENCIES:
        errors.append(
            f'currency must be one of: {VALID_CURRENCIES}'
        )

    if errors:
        response = jsonify({
            'error': 'Validation Failed',
            'details': errors
        })

        response.status_code = 400
        return response

    idempotency_key = request.headers.get('Idempotency-Key')

    if idempotency_key and idempotency_key in idempotency_cache:
        cached_response = idempotency_cache[idempotency_key]

        response = jsonify(cached_response)
        response.status_code = 200
        response.headers['X-Idempotency-Cache'] = 'HIT'

        return response

    transaction_id = str(uuid.uuid4())

    payment_data = {
        'transaction_id': transaction_id,
        'status': 'COMPLETED',
        'amount': amount,
        'currency': currency,
        'payment_method': payment_method,
        'user_id': user_id,
        'timestamp': int(time.time())
    }

    transactions[transaction_id] = payment_data

    response_body = {
        'data': payment_data,
        'meta': {
            'api_version': 'v2',
            'idempotency_key': idempotency_key
        }
    }

    if idempotency_key:
        idempotency_cache[idempotency_key] = response_body

    response = jsonify(response_body)
    response.status_code = 201
    response.headers['X-Idempotency-Cache'] = 'MISS'

    return response


@v2_bp.route('/payments/<transaction_id>', methods=['GET'])
def get_payment_v2(transaction_id):
    if transaction_id not in transactions:
        return jsonify({
            'error': 'Transaction not found'
        }), 404

    return jsonify({
        'data': {
            'transaction_id': transaction_id,
            'status': 'COMPLETED',
            'note': 'This is a simulated status response.'
        },
        'meta': {
            'api_version': 'v2'
        }
    })


@v2_bp.route('/payments-header-version', methods=['GET'])
def header_versioning_demo():
    api_version = request.headers.get('API-Version', '1')

    if api_version == '2':
        return jsonify({
            'strategy': 'Header Versioning',
            'version': 'v2',
            'message': 'Using API-Version header'
        })

    return jsonify({
        'strategy': 'Header Versioning',
        'version': 'v1',
        'message': 'Default version'
    })


@v2_bp.route('/payments-query-version', methods=['GET'])
def query_versioning_demo():
    version = request.args.get('version', '1')

    return jsonify({
        'strategy': 'Query Parameter Versioning',
        'version': f'v{version}'
    })