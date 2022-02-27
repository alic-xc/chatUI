from helpers.services import connect_get_user


class AuthenticateMixin:
    """ """
    def dispatch(self, request, *args, **kwargs):

        try:
            var = request.session['session_token']
            response = connect_get_user(request)
            if response['success']:
                self.user = response['data']

            else:
                raise Exception("Unable to connect to the server")

            return super().dispatch(request, *args, **kwargs)

        except Exception as err:
            print(err)
            pass

        from app.views import logout
        return logout(request)


class UserContextMixin:
    """ """
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['user'] = self.user
        except:
            context['user'] = None

        return context


class FilterMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context