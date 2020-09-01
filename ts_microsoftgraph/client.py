import base64
import mimetypes
import requests
import ts_microsoftgraph.exceptions
from ts_microsoftgraph.auth import Auth
from ts_microsoftgraph.decorators import token_required
from ts_microsoftgraph.reponse_parser import parse


class Client(object):
    RESOURCE = 'https://graph.microsoft.com/'
    def __init__(self, auth: Auth, api_version='v1.0', context='me'):
        self._api_version = api_version
        self._base_url = self.RESOURCE + self._api_version + '/'
        self._auth = auth
        self.token = auth.get_token()
        self._context = context

    def try_for_valid_token(self) -> bool:
        """
        try to get a valid token, either through currently cached token or using a token refresh
        :return: Boolean indicating if we have a valid token or need to perform a complete auth flow.
            TRUE is valid token
            FALSE is perform the login flow
        """
        try:
            output = self.me()
            return True
        except ts_microsoftgraph.exceptions.Unauthorized as uex:
            try:
                self._auth.refresh_token()
                output = self.me() #TODO: change this as it can fail in shared mailbox context
                return True
            except ts_microsoftgraph.exceptions.Unauthorized as uex:
                return False

    @token_required
    def me(self, params=None):
        """Retrieve the properties and relationships of user object.

        Note: Getting a user returns a default set of properties only (businessPhones, displayName, givenName, id,
        jobTitle, mail, mobilePhone, officeLocation, preferredLanguage, surname, userPrincipalName).
        Use $select to get the other properties and relationships for the user object.

        Args:
            params: A dict.

        Returns:
            A dict.

        """
        return self._get(self._base_url + self._context, params=params)

    @token_required
    def subscription_create(self, change_type, notification_url, resource, expiration_datetime, client_state=None):
        """Creating a subscription is the first step to start receiving notifications for a resource.

        Args:
            change_type: The event type that caused the notification. For example, created on mail receive, or updated
            on marking a message read.
            notification_url:
            resource: The URI of the resource relative to https://graph.microsoft.com.
            expiration_datetime: The expiration time for the subscription.
            client_state: The clientState property specified in the subscription request.

        Returns:
            A dict.

        """
        data = {
            'changeType': change_type,
            'notificationUrl': notification_url,
            'resource': resource,
            'expirationDateTime': expiration_datetime,
            'clientState': client_state
        }
        return self._post(self._base_url + 'subscriptions', json=data)

    @token_required
    def subscription_renew(self, subscription_id, expiration_datetime):
        """The client can renew a subscription with a specific expiration date of up to three days from the time
        of request. The expirationDateTime property is required.


        Args:
            subscription_id:
            expiration_datetime:

        Returns:
            A dict.

        """
        data = {
            'expirationDateTime': expiration_datetime
        }
        return self._patch(self._base_url + 'subscriptions/{}'.format(subscription_id), json=data)

    @token_required
    def subscription_delete(self, subscription_id):
        """The client can stop receiving notifications by deleting the subscription using its ID.

        Args:
            subscription_id:

        Returns:
            None.

        """
        return self._delete(self._base_url + 'subscriptions/{}'.format(subscription_id))

    # Mail
    @token_required
    def message_folder_list(self, params=None):
        """Retrieve the list of mailbox folders.
        Args:
            params:
        Returns:
            A dict.
        """
        return self._get(self._base_url + self._context + '/mailFolders/', params=params)

    @token_required
    def message_list(self, folder_id, params=None):
        """Retrieve the list of messages in a mailbox folder.
        Args:
            folder_id: selected mail folder.
            params:
        Returns:
            A dict.
        """
        return self._get(self._base_url + self._context + '/mailFolders/{id}/messages'.format(id=folder_id), params=params)

    @token_required
    def message_list_next(self, last_response_payload):
        if "@odata.nextLink" in last_response_payload.keys():
            return self._get(last_response_payload["@odata.nextLink"])
        else:
            return None

    @token_required
    def message_get(self, message_id, params=None, mime_content=False):
        """Retrieve the properties and relationships of a message object.
        Args:
            message_id: A dict.
            params:
        Returns:
            A dict.
        """
        return self._get(self._base_url + self._context + '/messages/' + message_id + ("" if not mime_content else "/$value"), params=params)

    @token_required
    def message_send(self, subject=None, recipients=None, body='', content_type='HTML', attachments=None):
        """Helper to send email from current user.

        Args:
            subject: email subject (required)
            recipients: list of recipient email addresses (required)
            body: body of the message
            content_type: content type (default is 'HTML')
            attachments: list of file attachments (local filenames)

        Returns:
            Returns the response from the POST to the sendmail API.
        """

        # Verify that required arguments have been passed.
        if not all([subject, recipients]):
            raise ValueError('sendmail(): required arguments missing')

        # Create recipient list in required format.
        recipient_list = [{'EmailAddress': {'Address': address}} for address in recipients]

        # Create list of attachments in required format.
        attached_files = []
        if attachments:
            for filename in attachments:
                b64_content = base64.b64encode(open(filename, 'rb').read())
                mime_type = mimetypes.guess_type(filename)[0]
                mime_type = mime_type if mime_type else ''
                attached_files.append(
                    {'@odata.type': '#microsoft.graph.fileAttachment', 'ContentBytes': b64_content.decode('utf-8'),
                     'ContentType': mime_type, 'Name': filename})

        # Create email message in required format.
        email_msg = {'Message': {'Subject': subject,
                                 'Body': {'ContentType': content_type, 'Content': body},
                                 'ToRecipients': recipient_list,
                                 'Attachments': attached_files},
                     'SaveToSentItems': 'true'}

        # Do a POST to Graph's sendMail API and return the response.
        return self._post(self._base_url + self._context + '/microsoft.graph.sendMail', json=email_msg)

    # Onenote
    @token_required
    def onenote_list(self):
        """Retrieve a list of notebook objects.

        Returns:
            A dict.

        """
        return self._get(self._base_url + self._context + '/onenote/notebooks')

    @token_required
    def onenote_get(self, notebook_id):
        """Retrieve the properties and relationships of a notebook object.

        Args:
            notebook_id:

        Returns:
            A dict.

        """
        return self._get(self._base_url + self._context + '/onenote/notebooks/' + notebook_id)

    @token_required
    def onenote_sections(self, notebook_id):
        """Retrieve the properties and relationships of a notebook object.

        Args:
            notebook_id:

        Returns:
            A dict.

        """
        return self._get(self._base_url + self._context + '/onenote/notebooks/{}/sections'.format(notebook_id))

    @token_required
    def onenote_create_page(self, section_id, files):
        """Create a new page in the specified section.

        Args:
            section_id:
            files:

        Returns:
            A dict.

        """
        return self._post(self._base_url + self._context + '/onenote/sections/{}/pages'.format(section_id), files=files)

    @token_required
    def onenote_list_pages(self, params=None):
        """Create a new page in the specified section.

        Args:
            params:

        Returns:
            A dict.

        """
        return self._get(self._base_url + self._context + '/onenote/pages', params=params)

    # Calendar
    @token_required
    def calendar_events(self):
        """Get a list of event objects in the user's mailbox. The list contains single instance meetings and
        series masters.

        Currently, this operation returns event bodies in only HTML format.

        Returns:
            A dict.

        """
        return self._get(self._base_url + self._context + '/events')

    @token_required
    def calendar_create_event(self, subject, content, start_datetime, start_timezone, end_datetime, end_timezone,
                              location, calendar=None, **kwargs):
        """
        Create a new calendar event.

        Args:
            subject: subject of event, string
            content: content of event, string
            start_datetime: in the format of 2017-09-04T11:00:00, dateTimeTimeZone string
            start_timezone: in the format of Pacific Standard Time, string
            end_datetime: in the format of 2017-09-04T11:00:00, dateTimeTimeZone string
            end_timezone: in the format of Pacific Standard Time, string
            location:   string
            attendees: list of dicts of the form:
                        {"emailAddress": {"address": a['attendees_email'],"name": a['attendees_name']}
            calendar:

        Returns:
            A dict.

        """
        # TODO: attendees
        # attendees_list = [{
        #     "emailAddress": {
        #         "address": a['attendees_email'],
        #         "name": a['attendees_name']
        #     },
        #     "type": a['attendees_type']
        # } for a in kwargs['attendees']]
        body = {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": content
            },
            "start": {
                "dateTime": start_datetime,
                "timeZone": start_timezone
            },
            "end": {
                "dateTime": end_datetime,
                "timeZone": end_timezone
            },
            "location": {
                "displayName": location
            },
            # "attendees": attendees_list
        }
        url = (self._context + '/calendars/{}/events'.format(calendar)) if calendar is not None else (self._context + '/events')
        return self._post(self._base_url + url, json=body)

    @token_required
    def calendar_create(self, name):
        body = {
            'name': '{}'.format(name)
        }
        return self._post(self._base_url + self._context + '/calendars', json=body)

    @token_required
    def calendars_list(self):
        return self._get(self._base_url + self._context + '/calendars')

    # Outlook
    @token_required
    def contacts_list(self, data_id=None, params=None):
        return self._get(self._base_url + self._context + "/contacts" + ("" if data_id is None else ("/" + data_id)), params=params)

    @token_required
    def contact_create(self, **kwargs):
        return self._post(self._base_url + self._context + "/contacts"  , **kwargs)

    @token_required
    def contact_create_in_folder(self, folder_id, **kwargs):
        return self._post(self._base_url + self._context + "/contactFolders/" + folder_id + "/contacts", **kwargs)


    @token_required
    def contact_folders(self, params=None):
        return self._get(self._base_url + self._context + "/contactFolders", params=params)

    @token_required
    def contact_create_folder(self, **kwargs):
        return self._post(self._base_url + self._context + "/contactFolders", **kwargs)

    #removed BETA calls
    def _get(self, url, **kwargs):
        return self._request('GET', url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request('POST', url, **kwargs)

    def _put(self, url, **kwargs):
        return self._request('PUT', url, **kwargs)

    def _patch(self, url, **kwargs):
        return self._request('PATCH', url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request('DELETE', url, **kwargs)

    def _request(self, method, url, headers=None, **kwargs):
        _headers = {
            'Accept': 'application/json',
        }
        _headers['Authorization'] = 'Bearer ' + self.token['access_token']
        if headers:
            _headers.update(headers)
        if 'files' not in kwargs:
            # If you use the 'files' keyword, the library will set the Content-Type to multipart/form-data
            # and will generate a boundary.
            _headers['Content-Type'] = 'application/json'
        print(method)
        print(url)
        print(str(kwargs))
        return parse(requests.request(method, url, headers=_headers, **kwargs))

