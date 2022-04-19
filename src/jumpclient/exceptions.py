class PortalClientException(Exception):
    pass


class PortalClientParameterException(PortalClientException):
    pass


class PortalClientHTTPException(PortalClientException):
    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop("response", None)
        super().__init__(*args, **kwargs)
