from binascii import unhexlify

from riftcrypto.exceptions import PortalSerializerException
from riftcrypto.transactions.serializers.base import BaseSerializer


class HtlcClaimSerializer(BaseSerializer):
    """Serializer handling timelock claim data"""

    def serialize(self):
        self.bytes_data += unhexlify(self.transaction["asset"]["claim"]["lockTransactionId"])
        unlock_secret_bytes = unhexlify(self.transaction["asset"]["claim"]["unlockSecret"].encode())
        if len(unlock_secret_bytes) != 32:
            raise PortalSerializerException("Unlock secret must be 32 bytes long")
        self.bytes_data += unlock_secret_bytes
        return self.bytes_data
