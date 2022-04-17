class PortalException(Exception):
    pass


class PortalParameterException(PortalException):
    pass


class PortalHTTPException(PortalException):
    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop("response", None)
        super().__init__(*args, **kwargs)
