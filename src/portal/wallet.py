from hashlib import sha256
from time import sleep

from portal.utils import generate_rand
from portal_client.client import PortalClient
from portal_client.exceptions import PortalClientHTTPException
from portal_crypto.identity.address import address_from_passphrase
from portal_crypto.networks.base import Network
from portal_crypto.transactions.builder.htlc_claim import HtlcClaim
from portal_crypto.transactions.builder.htlc_lock import HtlcLock
from portal_crypto.transactions.builder.htlc_refund import HtlcRefund

LOCK_TIME = 100  # 100 blocks

API_SERVERS = {
    "ark_devnet": "http://65.21.251.224:4003/api",
    "ark_testnet": "http://localhost:4003/api",
    "solar_testnet": "http://51.158.174.36:6003/api",
}


class Wallet:
    amount: int
    client: PortalClient

    _passphrase: str
    _network: Network
    _secret_code: str

    def __init__(self, network: Network, passphrase: str, amount: int) -> None:
        self._passphrase = passphrase
        self._network = network
        self.amount = amount
        self.client = PortalClient(API_SERVERS[network.name])

    @property
    def address(self):
        return address_from_passphrase(self._passphrase, self._network.version)

    def _get_current_height(self) -> int:
        resp = self.client.blocks.last()
        data = resp.get("data")
        return int(data["height"])

    def _get_last_nonce(self) -> int:
        try:
            resp = self.client.wallets.get(self.address)
        except PortalClientHTTPException:
            return 0

        data = resp.get("data")
        return int(data["nonce"])

    def _get_locks(self):
        resp = self.client.locks.all(page=1, limit=100, recipientId=self.address, isExpired="false")
        locks = resp.get("data")
        return locks

    def _get_unlock(self, lock_id: str):
        criteria = {"ids": [lock_id]}
        resp = self.client.locks.unlocked(criteria, page=1, limit=100)
        locks = resp.get("data")
        return locks

    def _generate_secret_code(self) -> bytes:
        self._secret_code = sha256(generate_rand()).hexdigest()[:32].encode()
        print(f"You're secret code is: {self._secret_code}")
        return self._secret_code

    def _broadcast(self, transaction) -> bool:
        resp = self.client.transactions.create([transaction.to_dict()])
        if not resp.get("data"):
            raise Exception("somethign went wrong")

        # data = resp["data"]
        # TODO: check if tx got accepted and broadcasted as expected
        return True

    def get_balance(self) -> int:
        resp = self.client.wallets.get(self.address)
        data = resp.get("data")
        return int(data["balance"])

    def create_htlc_lock(self, recipient: str, secret_hash: str = None) -> bool:
        """
        Create a HTLC Lock transaction
        """
        current_height = self._get_current_height()
        current_nonce = self._get_last_nonce()
        secret_code = None

        if not secret_hash:
            secret_code = self._generate_secret_code()
            secret_hash = sha256(secret_code).hexdigest()

        transaction = HtlcLock(
            recipient_id=recipient,
            amount=self.amount,
            secret_hash=secret_hash,
            expiration_type=2,  # EpochTimestamp =1, BlockHeight = 2
            expiration_value=current_height
            + LOCK_TIME,  # TODO: the 2nd locktime needs to be smaller than initial one
        )
        transaction.set_network(self._network)
        transaction.set_nonce(current_nonce + 1)
        transaction.schnorr_sign(self._passphrase)
        status = self._broadcast(transaction)
        return status, transaction.transaction.get_id(), secret_code

    def create_htlc_claim(self, transaction_id: str, secret_code_hex: str) -> bool:
        """
        Create a HTLC Claim transaction
        """
        current_nonce = self._get_last_nonce()

        transaction = HtlcClaim(transaction_id, secret_code_hex)
        transaction.set_network(self._network)
        transaction.set_nonce(current_nonce + 1)
        transaction.schnorr_sign(self._passphrase)
        return self._broadcast(transaction)

    def create_htlc_refund(self, transaction_id) -> bool:
        """
        Create a HTLC Claim transaction
        """
        current_nonce = self._get_last_nonce()

        transaction = HtlcRefund(transaction_id)
        transaction.set_network(self._network)
        transaction.set_nonce(current_nonce + 1)
        transaction.schnorr_sign(self._passphrase)
        return self._broadcast(transaction)

    def wait_for_htlc_lock(self):
        print(f"... Waiting for a HTLC Lock to appear on {self._network.name}")
        while True:
            locks = self._get_locks()
            if len(locks) == 0:
                sleep(8)
                continue

            # TODO: improve this nonsense here
            for lock in locks:
                # return the 1st lock that shows up
                return lock

            sleep(8)

    def wait_for_htlc_unlock(self, lock_id: str):
        print(f"... Waiting for counterparty to claim the funds on {self._network.name}")
        while True:
            locks = self._get_unlock(lock_id)
            if len(locks) == 0:
                sleep(8)
                continue

            return locks[0]
