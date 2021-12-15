import json
import traceback

import requests

api_domain = 'https://odoo-staging.rinznetwork.com'


def odoo_request(*args, **kwargs):
    res = requests.request(
        *args, **kwargs
    )
    print(res.text)
    if res.status_code == 200:
        response = res.json()
        print(response)
        if response and response.get('status'):
            return res.cookies

        raise Exception(response.get('msg'))

    raise Exception


def get_cookies(user: str, password: str):
    AUTH_URL = f'{api_domain}/api/v1/login/'
    headers = {'Content-type': 'application/json'}

    data = {
        'params': {
            'login': user,
            'password': password,
            'db': 'paydi'
        }
    }

    return odoo_request(url=AUTH_URL, method="POST", data=json.dumps(data), headers=headers)


class OdooApi(object):

    # Get response cookies
    # This hold information for authenticated user

    def __init__(self, user, password):
        self.cookies = get_cookies(user, password)
        print(self.cookies)
        self.user = user
        self.password = password

    def get(self, url, params):
        return odoo_request(
            url=url,
            method='GET',
            params=params,
            cookies=self.cookies
        )


# Example 2
USERS_URL = f'{api_domain}/api/v1/object/res.partner.bank'

# Use query param to fetch only id and name
params = {'query': '{acc_number, bank_name, acc_holder_name}', 'filter': '[["partner_id", "=", 35]]'}

odoo_api = OdooApi(user='mms@paydi.vn', password='admin')

result = odoo_api.get(USERS_URL, params)

print(result)
