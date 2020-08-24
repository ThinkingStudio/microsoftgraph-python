import uuid
from urllib.parse import urlencode
import requests
from ts_microsoftgraph.reponse_parser import parse
import json

class Auth(object):
    def __init__(self, client_id: str, tenant_id: str, secret: str, scope=".default", account=None, redirect_uri="https://login.microsoftonline.com/common/oauth2/nativeclient", save_cache_handler=None, load_cache_handler=None, state_id=None):
        self._authority = "https://login.microsoftonline.com/" + tenant_id
        self._client_id = client_id
        self._secret = secret
        self._scope = scope
        self._save_cache_handler = save_cache_handler
        self._load_cache_handler = load_cache_handler
        self._state = str(uuid.uuid1()) if state_id is None else state_id
        self._redirect_uri = redirect_uri
        self._token = None
        self._account = account

    def authorization_url(self):
        params = {
            'client_id': self._client_id,
            'redirect_uri': self._redirect_uri,
            'scope': self._scope,
            'response_type': 'code',
            'response_mode': 'query',
            'state': self._state
        }
        return self._authority + "/oauth2/v2.0/authorize?" + urlencode(params)

    def exchange_code(self, code):
        data = {
            'client_id': self._client_id,
            'redirect_uri': self._redirect_uri,
            'client_secret': self._secret,
            'code': code,
            'grant_type': 'authorization_code',
        }
        response = requests.post(self._authority + "/oauth2/v2.0/token", data=data)
        self._set_token(parse(response))

    def _refresh_token(self, token):
        data = {
            'client_id': self._client_id,
            'redirect_uri': self._redirect_uri,
            'client_secret': self._secret,
            'refresh_token': token['access_token'],
            'grant_type': 'refresh_token',
            'scope': self._scope #'https://graph.microsoft.com/mail.read'
        }
        print(data)
        response = requests.post(self._authority + "/oauth2/v2.0/token", data=data)
        self._set_token(parse(response))

    def _set_token(self, token):
        if self._save_cache_handler is not None:
            self._save_cache_handler(str(token))
        self._token = token

    def get_token(self):
        if self._load_cache_handler is not None:
            t = json.loads(self._load_cache_handler())
            self._refresh_token(t)
        return self._token


