from flask import Blueprint, jsonify, request
import uuid

v1_bp = Blueprint('v1', __name__, url_prefix='/api/v1')

transactions = {}

DEPRECATION_DATE = 'Thu, 07 May 2026 00:00:00 GMT'
SUNSET_DATE = 'Thu, 31 Dec 2026 23:59:59 GMT'


def add_deprecation_headers(response):
    response.headers['Deprecation'] = DEPRECATION_DATE
    response.headers['Sunset'] = SUNSET_DATE
    response.headers['Link'] = '</api/v2/payments>; rel="successor-version"'
    response.headers['Warning'] = '299 - "API v1 is deprecated. Please migrate to v2."'
    return response


@v1_bp.route('/payments', methods=['POST'])
def create_payment_v1():
    data = request.get_json()

    amount = data.get('amount')
    currency = data.get('currency', 'USD')

    if amount is None:
        response = jsonify({
            'error': 'amount is required'
        })
        response.status_code = 400
        return add_deprecation_headers(response)

    transaction_id = str(uuid.uuid4())

    transactions[transaction_id] = {
        'amount': amount,
        'currency': currency
    }

    response = jsonify({
        'status': 'success',
        'message': f'Successfully processed payment of {amount} {currency}',
        'transaction_id': transaction_id
    })

    response.status_code = 200

    return add_deprecation_headers(response)


@v1_bp.route('/payments/<transaction_id>', methods=['GET'])
def get_payment_v1(transaction_id):
    if transaction_id not in transactions:
        response = jsonify({
            'error': 'Transaction not found'
        })
        response.status_code = 404
        return add_deprecation_headers(response)

    response = jsonify({
        'status': 'success',
        'transaction_id': transaction_id,
        'note': 'Status lookup is limited in v1. Migrate to v2 for full transaction details.'
    })

    return add_deprecation_headers(response)