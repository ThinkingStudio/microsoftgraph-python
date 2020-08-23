import msal
import uuid

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

    def get_token(self):
        cache = self._load_cache()
        result = self._build_msal_app(cache=cache).acquire_token_silent(scopes=[self._scope],account=self._account)
        if "access_token" in result:
            self._token = result
        else:
            raise EnvironmentError(result.get("error") + ":" + result.get("error_description") + ":" + result.get("correlation_id"))
        self._save_cache(cache)
        return self._token

    def get_service_token(self):
        cache = self._load_cache()
        result = self._build_msal_app(cache=cache).acquire_token_silent(scopes=[self._scope], account=self._account)
        if not result:
            # No suitable token exists in cache. Let's get a new one from AAD
            result = self._build_msal_app(cache=cache).acquire_token_for_client(scopes=[self._scope])
        if "access_token" in result:
            self._token = result
        else:
            raise EnvironmentError(result.get("error") + ":" + result.get("error_description") + ":" + result.get("correlation_id"))
        self._save_cache(cache)
        return self._token

    def get_auth_url(self):
        return self._build_msal_app(cache=None).get_authorization_request_url(
            [self._scope],
            state=self._state,
            redirect_uri=self._redirect_uri)

    def get_user_token(self, code):
        cache = self._load_cache()
        result = self._build_msal_app(cache=cache).acquire_token_silent(scopes=[self._scope],account=self._account)
        if not result:
            result = self._build_msal_app(cache=cache).acquire_token_by_authorization_code(
                code,
                scopes=[self._scope],
                redirect_uri=self._redirect_uri)
        if "access_token" in result:
            self._token = result
        else:
            raise EnvironmentError(result.get("error") + ":" + result.get("error_description") + ":" + result.get("correlation_id"))
        self._save_cache(cache)
        return self._token

    def _load_cache(self):
        cache = msal.SerializableTokenCache()
        source = None
        if self._load_cache_handler is not None:
            source = self._load_cache_handler()
        if source is not None:
            cache.deserialize(source)
        return cache

    def _save_cache(self, cache):
        if cache.has_state_changed:
            if self._save_cache_handler is not None:
                self._save_cache_handler(cache.serialize())

    def _build_msal_app(self, cache=None):
        return msal.ConfidentialClientApplication(
            self._client_id,
            authority=self._authority,
            client_credential=self._secret,
            token_cache=cache)

    def _get_token_from_cache(self, scope=None):
        cache = self._load_cache()  # This web app maintains one cache per session
        cca = self._build_msal_app(cache)
        accounts = cca.get_accounts()
        if accounts:  # So all account(s) belong to the current signed-in user
            result = cca.acquire_token_silent(scope, account=accounts[0])
            self._save_cache(cache)
            return result