from functools import wraps
from django.contrib import messages
from django.forms.utils import ErrorDict
from .connector import api_connector


def user_login_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            var = request.session['session_token']
            return function(request, *args, **kwargs)
        except KeyError as err:
            messages.error(request, 'We noticed an unusual activity with your account.'
                                    ' Please login again to validate account')
            from app.views import logout
            return logout(request)

    return wrap


def connect_user_registration(request, params):
    """ """
    url = '/users/'
    response = api_connector(request, url, 'post', params)
    return response


def connect_login_api(request, params):
    """ """
    url = '/login/'
    response = api_connector(request, url, 'post', params)
    return response


def connect_get_user(request):
    """ Get authenticated user """
    url = '/users/'
    response = api_connector(request, url, 'get', None)
    return response


def connect_create_room_api(request, params):
    """ """
    url = '/chat_room/'
    response = api_connector(request, url, 'post', params)
    return response


def connect_room_messages(request, room_name):
    """ """
    url = '/chat/?room=%s' % room_name
    response = api_connector(request, url, 'get', None)
    return response


def connect_room_api(request, user_id):
    """ """
    url = '/chat_room/?user=%s' % user_id
    response = api_connector(request, url, 'get', None)
    return response


def connect_update_chat(request, message_id):
    url = '/chat/%s/' % message_id
    params = {'read_status': True}
    response = api_connector(request, url, 'patch', params)
    return response


def error_handler(request, errors):
    if type(errors) == str:
        messages.error(request, errors)
    elif type(errors) == dict or type(errors) == ErrorDict:
        print(errors)
        for error in errors.keys():
            if type(errors[error]) == list:
                for item in errors[error]:
                    messages.error(request, item)
            else:
                messages.error(request, "%s - %s" % (error, errors[error]))
    elif type(errors) == list:
        for error in errors:
            if type(error) == dict:
                for item in error.keys():
                    messages.error(request, "%s - %s" %(item, error[item]))
            else:
                messages.error(request, error)

    else:
        messages.error(request, "System error, please try again.")
    return errors