import requests
from django.conf import settings
from requests.exceptions import ConnectionError

api_url = settings.CUSTOMER_CABINET_URL
api_token = settings.CUSTOMER_CABINET_TOKEN


def get_customer_insurance_data(data):
    result = {
        'customer': data.customer.iin,
        'insurance': data.contract.insurance.code,
        'insurer': data.contract.insurer.title,
        'program': data.program.title,
        'card_number': data.number,
        'begin_date': data.begin_date.strftime("%Y-%m-%d"),
        'end_date': data.end_date.strftime("%Y-%m-%d"),
        'limit': data.program.service_limit,
        'invoice_sum': data.get_invoice_sum()
    }
    return result


def create_customer_insurance(data):
    url_customer_api = 'http://{}/api/customer_management/customer_insurance/create'.format(api_url)
    customer_insurance_data = get_customer_insurance_data(data)
    try:
        result = requests.post(url_customer_api, data=customer_insurance_data,
                               headers={'Authorization': 'Token ' + api_token}, timeout=1)
        print(result.json())
        return result
    except ConnectionError:
        pass


def update_customer_insurance(card_number, data):
    url_customer_api = 'http://{}/api/customer_management/customer_insurance/{}/update'.format(api_url, card_number)
    customer_insurance_data = get_customer_insurance_data(data)
    try:
        result = requests.put(url_customer_api, data=customer_insurance_data,
                              headers={'Authorization': 'Token ' + api_token}, timeout=1)
        return result
    except ConnectionError:
        pass


def destroy_customer_insurance(card_number):
    url_customer_api = 'http://{}/api/customer_management/customer_insurance/{}/destroy'.format(api_url, card_number)
    try:
        result = requests.delete(url_customer_api, headers={'Authorization': 'Token ' + api_token}, timeout=1)
        return result
    except ConnectionError:
        pass
