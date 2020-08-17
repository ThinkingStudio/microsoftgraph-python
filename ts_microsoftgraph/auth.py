import msal


class Auth(object):
    def __init__(self, client_id: str, tenant_id: str, secret: str, scope=".default"):
        authority = "https://login.microsoftonline.com/" + tenant_id
        app = msal.ConfidentialClientApplication( client_id, authority=authority, client_credential=secret)
        result = app.acquire_token_silent(scopes=[scope], account=None)
        if not result:
            # No suitable token exists in cache. Let's get a new one from AAD
            result = app.acquire_token_for_client(scopes=[scope])
        if "access_token" in result:
            self._token = result
        else:
            raise EnvironmentError(result.get("error") + ":" + result.get("error_description") + ":" + result.get("correlation_id"))

    def get_token(self):
        return self._token
