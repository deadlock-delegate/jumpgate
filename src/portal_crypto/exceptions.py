class PortalCryptoException(Exception):
    pass


class PortalSerializerException(PortalCryptoException):
    """Raised when there's a serializer related issue"""


class PortalInvalidTransaction(PortalCryptoException):
    """Raised when transaction is not valid"""
