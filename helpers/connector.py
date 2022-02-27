from django.conf import settings
import requests


def api_connector(request, endpoint, method, params):
    """ Function to handle request to the api. """
    try:
        """ Check if a user token is available else use API_TOKEN to authenticate """
        token = request.session['session_token']
        headers = {"Content-Type": "application/json", "Authorization": "Token " + token }

    except KeyError as err:
        headers = {"Content-Type": "application/json"}

    try:
        """ """
        requests_method = getattr(requests, method)
        url = str(settings.API_END_POINT + endpoint)
        response = requests_method(url=url, headers=headers, json=params)

        if response.status_code in settings.SUCCESS_CODES:
            return {
                'success': True,
                'data': response.json(),
                'status_code': response.status_code
            }
        elif response.status_code == 204:
            return {
                'success': True,
                'data': 'Action performed successfully',
                'status_code': response.status_code

            }
        else:
            return {
                'success': False,
                'data': response.json(),
                'status_code': response.status_code
            }

    except Exception as err:
        return {
            'success': False,
            'data': 'An error occurred while trying to connect to the server',
            'status_code': 500,
        }


def file_connector(request, endpoint, file, method=None):
    token = request.session['session_token']
    headers = {"Authorization": "Bearer " + token}
    url = str(settings.API_END_POINT + endpoint)
    if not method:
        response = requests.patch(url, files=file, headers=headers)
    else:
        response = requests.put(url, files=file, headers=headers)

    if response.status_code in settings.SUCCESS_CODES:
        return {
            'success': True,
            'data': response.json()
        }
    else:
        try:
            return {
                'success': False,
                'data': response.json()
            }
        except Exception as error:
            return {
                'success': False,
                'data': error
            }
