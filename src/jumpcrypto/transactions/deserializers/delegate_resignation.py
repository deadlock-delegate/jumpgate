from binascii import hexlify

from jumpcrypto.transactions.deserializers.base import BaseDeserializer


class DelegateResignationDeserializer(BaseDeserializer):
    def deserialize(self):
        self.transaction.parse_signatures(hexlify(self.serialized).decode(), self.asset_offset)

        return self.transaction
