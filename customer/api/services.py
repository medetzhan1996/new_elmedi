import requests
from requests.exceptions import ConnectionError
from django.conf import settings

api_url = settings.CUSTOMER_CABINET_URL
api_token = settings.CUSTOMER_CABINET_TOKEN


def get_customer_data(data):
    result = {
        'first_name': data.first_name,
        'last_name': data.last_name,
        'surname': data.surname,
        'iin': data.iin,
        'national': data.national,
        'address': data.address,
        'place_work': data.place_work,
        'telephone_number': data.telephone_number,
        'profession': data.profession
    }
    return result


def create_customer(data):
    url_customer_api = 'http://{}/api/customer_management/customer/create'.format(api_url)
    customer_data = get_customer_data(data)
    try:
        result = requests.post(url_customer_api, data=customer_data,
                               headers={'Authorization': 'Token ' + api_token}, timeout=1)
        return result
    except ConnectionError:
        pass


def update_customer(iin, data):
    url_customer_api = 'http://{}/api/customer_management/customer/{}/update'.format(api_url, iin)
    customer_data = get_customer_data(data)
    try:
        result = requests.put(url_customer_api, data=customer_data,
                              headers={'Authorization': 'Token ' + api_token}, timeout=1)
        return result
    except ConnectionError:
        pass


def destroy_customer(iin):
    url_customer_api = 'http://{}/api/customer_management/customer/{}/destroy'.format(api_url, iin)
    try:
        result = requests.delete(url_customer_api,
                                 headers={'Authorization': 'Token ' + api_token}, timeout=1)
        return result
    except ConnectionError:
        pass
