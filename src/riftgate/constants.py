from enum import Enum

from riftcrypto.constants import (
    TRANSACTION_HTLC_CLAIM,
    TRANSACTION_HTLC_LOCK,
    TRANSACTION_HTLC_REFUND,
)


class HTLC_TRANSACTION_TYPE(Enum):
    def __str__(self):
        return int(self.value)

    HTLC_LOCK = TRANSACTION_HTLC_LOCK  # 8
    HTLC_CLAIM = TRANSACTION_HTLC_CLAIM  # 9
    HTLC_REFUND = TRANSACTION_HTLC_REFUND  # 10


HTLC_TRANSACTION_TYPES = [item.value for item in HTLC_TRANSACTION_TYPE]

ARKTOSHI = 100_000_000
