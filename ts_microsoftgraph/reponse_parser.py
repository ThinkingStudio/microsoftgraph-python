from ts_microsoftgraph import exceptions


def parse(response):
    status_code = response.status_code
    if 'application/json' in response.headers['Content-Type']:
        r = response.json()
    else:
        r = response.content
    if status_code in (200, 201, 202):
        return r
    elif status_code == 204:
        return None
    elif status_code == 400:
        raise exceptions.BadRequest(r)
    elif status_code == 401:
        raise exceptions.Unauthorized(r)
    elif status_code == 403:
        raise exceptions.Forbidden(r)
    elif status_code == 404:
        raise exceptions.NotFound(r)
    elif status_code == 405:
        raise exceptions.MethodNotAllowed(r)
    elif status_code == 406:
        raise exceptions.NotAcceptable(r)
    elif status_code == 409:
        raise exceptions.Conflict(r)
    elif status_code == 410:
        raise exceptions.Gone(r)
    elif status_code == 411:
        raise exceptions.LengthRequired(r)
    elif status_code == 412:
        raise exceptions.PreconditionFailed(r)
    elif status_code == 413:
        raise exceptions.RequestEntityTooLarge(r)
    elif status_code == 415:
        raise exceptions.UnsupportedMediaType(r)
    elif status_code == 416:
        raise exceptions.RequestedRangeNotSatisfiable(r)
    elif status_code == 422:
        raise exceptions.UnprocessableEntity(r)
    elif status_code == 429:
        raise exceptions.TooManyRequests(r)
    elif status_code == 500:
        raise exceptions.InternalServerError(r)
    elif status_code == 501:
        raise exceptions.NotImplemented(r)
    elif status_code == 503:
        raise exceptions.ServiceUnavailable(r)
    elif status_code == 504:
        raise exceptions.GatewayTimeout(r)
    elif status_code == 507:
        raise exceptions.InsufficientStorage(r)
    elif status_code == 509:
        raise exceptions.BandwidthLimitExceeded(r)
    else:
        if r['error']['innerError']['code'] == 'lockMismatch':
            # File is currently locked due to being open in the web browser
            # while attempting to reupload a new version to the drive.
            # Thus temporarily unavailable.
            raise exceptions.ServiceUnavailable(r)
        raise exceptions.UnknownError(r)
