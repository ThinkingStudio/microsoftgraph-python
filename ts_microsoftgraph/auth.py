import uuid
from enum import Enum
from urllib.parse import urlencode
import requests
from ts_microsoftgraph.reponse_parser import parse
import json

"""
Calendars.Read	Read user calendars	Allows the app to read events in user calendars.	No	Yes
Calendars.Read.Shared	Read user and shared calendars 	Allows the app to read events in all calendars that the user can access, including delegate and shared calendars. 	No	No
Calendars.ReadWrite	Have full access to user calendars	Allows the app to create, read, update, and delete events in user calendars.	No	Yes
Calendars.ReadWrite.Shared	Read and write user and shared calendars 	Allows the app to create, read, update and delete events in all calendars the user has permissions to access. This includes delegate and shared calendars.	No	No

Contacts.Read	Read user contacts 	Allows the app to read user contacts.	No	Yes
Contacts.Read.Shared	Read user and shared contacts	Allows the app to read contacts that the user has permissions to access, including the user's own and shared contacts. 	No	No
Contacts.ReadWrite	Have full access to user contacts	Allows the app to create, read, update, and delete user contacts.	No	Yes
Contacts.ReadWrite.Shared	Read and write user and shared contacts	Allows the app to create, read, update and delete contacts that the user has permissions to, including the user's own and shared contacts.	No	No

Mail.Read	Read user mail 	Allows the app to read email in user mailboxes. 	No	Yes
Mail.ReadBasic	Read user basic mail	Allows the app to read email in the signed-in user's mailbox, except for body, bodyPreview, uniqueBody, attachments, extensions, and any extended properties. Does not include permissions to search messages.	No	No
Mail.ReadWrite	Read and write access to user mail 	Allows the app to create, read, update, and delete email in user mailboxes. Does not include permission to send mail.	No	Yes
Mail.Read.Shared	Read user and shared mail	Allows the app to read mail that the user can access, including the user's own and shared mail. 	No	No
Mail.ReadWrite.Shared	Read and write user and shared mail 	Allows the app to create, read, update, and delete mail that the user has permission to access, including the user's own and shared mail. Does not include permission to send mail.	No	No
Mail.Send	Send mail as a user 	Allows the app to send mail as users in the organization. 	No	Yes
Mail.Send.Shared	Send mail on behalf of others 	Allows the app to send mail as the signed-in user, including sending on-behalf of others. 	No	No
MailboxSettings.Read	Read user mailbox settings 	Allows the app to the read user's mailbox settings. Does not include permission to send mail.	No	Yes
MailboxSettings.ReadWrite	Read and write user mailbox settings 	Allows the app to create, read, update, and delete user's mailbox settings. Does not include permission to directly send mail, but allows the app to create rules that can forward or redirect messages.	No	Yes

Notes.Read	Read user OneNote notebooks	Allows the app to read the titles of OneNote notebooks and sections and to create new pages, notebooks, and sections on behalf of the signed-in user.	No	Yes
Notes.Create	Create user OneNote notebooks	Allows the app to read the titles of OneNote notebooks and sections and to create new pages, notebooks, and sections on behalf of the signed-in user.	No	Yes
Notes.ReadWrite	Read and write user OneNote notebooks	Allows the app to read, share, and modify OneNote notebooks on behalf of the signed-in user.	No	Yes
Notes.Read.All	Read all OneNote notebooks that user can access	Allows the app to read OneNote notebooks that the signed-in user has access to in the organization.	No	No
Notes.ReadWrite.All	Read and write all OneNote notebooks that user can access	Allows the app to read, share, and modify OneNote notebooks that the signed-in user has access to in the organization.	No	No
Notes.ReadWrite.CreatedByApp	Limited notebook access (deprecated)	Deprecated Do not use. No privileges are granted by this permission.	No	No

email	View users' email address	Allows the app to read your users' primary email address.	No	No
offline_access	Access user's data anytime	Allows the app to read and update user data, even when they are not currently using the app.	No	No
openid	Sign users in	Allows users to sign in to the app with their work or school accounts and allows the app to see basic user profile information.	No	No
profile	View users' basic profile	Allows the app to see your users' basic profile (name, picture, user name).	No	No

"""


class AuthScope(Enum):
    DEFAULT = 0
    CALENDARS_READ = 1
    CALENDARS_READ_SHARED = 2
    CALENDARS_READWRITE	 = 3
    CALENDARS_READWRITE_SHARED	 = 4
    CONTACTS_READ = 5
    CONTACTS_READ_SHARED = 6
    CONTACTS_READWRITE = 7
    CONTACTS_READWRITE_SHARED = 8
    MAIL_READ = 9
    MAIL_READBASIC = 10
    MAIL_READWRITE = 11
    MAIL_READ_SHARED = 12
    MAIL_READWRITE_SHARED = 13
    MAIL_SEND = 14
    MAIL_SEND_SHARED = 15
    MAILBOXSETTINGS_READ = 16
    MAILBOXSETTINGS_READWRITE = 17
    NOTES_READ = 18
    NOTES_CREATE = 19
    NOTES_READWRITE = 20
    NOTES_READ_ALL = 21
    NOTES_READWRITE_ALL = 22
    NOTES_READWRITE_CREATEDBYAPP = 23
    EMAIL = 24
    OFFLINE_ACCESS = 25
    OPENID = 26
    PROFILE = 27


class AuthScopeList(object):
    def __init__(self):
        self._lut = {
            AuthScope.DEFAULT : ".default",
            AuthScope.CALENDARS_READ : "Calendars.Read",
            AuthScope.CALENDARS_READ_SHARED :"Calendars.Read.Shared",
            AuthScope.CALENDARS_READWRITE	 :"Calendars.ReadWrite",
            AuthScope.CALENDARS_READWRITE_SHARED	 :"Calendars.ReadWrite.Shared",
            AuthScope.CONTACTS_READ :"Contacts.Read",
            AuthScope.CONTACTS_READ_SHARED :"Contacts.Read.Shared",
            AuthScope.CONTACTS_READWRITE :"Contacts.ReadWrite",
            AuthScope.CONTACTS_READWRITE_SHARED :"Contacts.ReadWrite.Shared",
            AuthScope.MAIL_READ :"Mail.Read",
            AuthScope.MAIL_READBASIC : "Mail.ReadBasic",
            AuthScope.MAIL_READWRITE : "Mail.ReadWrite",
            AuthScope.MAIL_READ_SHARED : "Mail.Read.Shared",
            AuthScope.MAIL_READWRITE_SHARED : "Mail.ReadWrite.Shared",
            AuthScope.MAIL_SEND : "Mail.Send",
            AuthScope.MAIL_SEND_SHARED : "Mail.Send.Shared",
            AuthScope.MAILBOXSETTINGS_READ : "MailboxSettings.Read",
            AuthScope.MAILBOXSETTINGS_READWRITE : "MailboxSettings.ReadWrite",
            AuthScope.NOTES_READ : "Notes.Read",
            AuthScope.NOTES_CREATE : "Notes.Create",
            AuthScope.NOTES_READWRITE : "Notes.ReadWrite",
            AuthScope.NOTES_READ_ALL : "Notes.Read.All",
            AuthScope.NOTES_READWRITE_ALL : "Notes.ReadWrite.All",
            AuthScope.NOTES_READWRITE_CREATEDBYAPP : "Notes.ReadWrite.CreatedByApp",
            AuthScope.EMAIL : "email",
            AuthScope.OFFLINE_ACCESS : "offline_access",
            AuthScope.OPENID : "openid",
            AuthScope.PROFILE : "profile"
        }
        self._flags = list()

    def add_scope(self, scope_enum: AuthScope):
        self._flags.append(self._lut[scope_enum])

    def __str__(self):
        return ",".join(self._flags)

    def as_list(self):
        return self._flags


class Auth(object):
    def __init__(self,
                 client_id: str,
                 tenant_id: str,
                 secret: str,
                 scope=None,
                 account=None,
                 redirect_uri="https://login.microsoftonline.com/common/oauth2/nativeclient",
                 save_cache_handler=None,
                 load_cache_handler=None,
                 state_id=None
                 ):
        """
        Auth object
        :param client_id: required MS client_id provided by Azure
        :param tenant_id: required MS tenant_id provided by Azure
        :param secret: required MS tenant_id provided by Azure
        :param scope: a single or set of scopes - you can use a single string, a list of strings, or an AuthScope or an AuthScopeList for this
        :param account: this is a long UID value representing your Azure account ID
        :param redirect_uri: the URI that handles your auth code - the default value is "https://login.microsoftonline.com/common/oauth2/nativeclient"
        :param save_cache_handler: this is a function that handles a single parameter which is the JSON token. This needs to be serialised and saved
        :param load_cache_handler: this is a function that takes no parameters, but should return a string representing the JSON file (it will be parsed)
        :param state_id: see OAUTH2 details on the state_id - it's for CSRF protection
        """
        if type(scope) is str:
            self._scope = scope
        elif type(scope) is AuthScopeList:
            self._scope = scope.as_list()
        elif type(scope) is AuthScope:
            asl = AuthScopeList()
            asl.add_scope(scope)
            self._scope = str(scope)
        elif type(scope) is list:
            self._scope = scope #",".join(scope)
        else:
            self._scope = ".default"

        self._authority = "https://login.microsoftonline.com/" + tenant_id
        self._client_id = client_id
        self._secret = secret
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
            'response_type': 'code',
            'response_mode': 'query',
            'state': self._state
        }
        return self._authority + "/oauth2/v2.0/authorize?" + urlencode(params)

    def exchange_code(self, code):
        data = {
            'client_id': self._client_id,
            'redirect_uri': self._redirect_uri,
            'scope': self._scope,
            'client_secret': self._secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
        print(data)
        response = requests.post(self._authority + "/oauth2/v2.0/token", data=data)
        self._set_token(parse(response))

    def refresh_token(self):
        token = self.get_token()
        data = {
            'grant_type': 'refresh_token',
            'client_id': self._client_id,
            'redirect_uri': self._redirect_uri,
            'client_secret': self._secret,
            'refresh_token': token['refresh_token'],
            'scope': self._scope  #'https://graph.microsoft.com/mail.read'
        }
        response = requests.post(self._authority + "/oauth2/v2.0/token", data=data)
        self._set_token(parse(response))

    def _set_token(self, token):
        if self._save_cache_handler is not None:
            self._save_cache_handler(str(token))
        self._token = token

    def get_token(self):
        token = self._token
        if token is None:
            if self._load_cache_handler is not None:
                token = json.loads(self._load_cache_handler())
        return token
