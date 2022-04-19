from binascii import hexlify
from time import sleep

import click

from portal.constants import ARKTOSHI
from portal.wallet import Wallet
from portal_crypto.networks.devnet import ArkDevnet
from portal_crypto.networks.testnet import ArkTestnet, SolarTestnet

NETWORK_MAPPING = {
    "ark_devnet": ArkDevnet,
    "solar_testnet": SolarTestnet,
    "ark_testnet": ArkTestnet,
}


@click.command()
@click.option(
    "-f",
    "--from",
    "_from",
    required=True,
    help="network:passphrase:amount",
)
@click.option(
    "-t",
    "--to",
    "to",
    required=True,
    help="network:passphrase:amount",
)
@click.option(
    "--initiator",
    default=False,
    required=False,
    is_flag=True,
    help="",
)
def main(_from: str, to: str, initiator: bool):
    # TODO: create mappings that ark's devnet == solar's testnet

    from_network, from_passphrase, from_amount = _from.split(":")
    from_wallet = Wallet(
        NETWORK_MAPPING[from_network], from_passphrase, int(int(from_amount) * ARKTOSHI)
    )

    to_network, to_passphrase, to_amount = to.split(":")
    to_wallet = Wallet(NETWORK_MAPPING[to_network], to_passphrase, int(int(to_amount) * ARKTOSHI))

    print("You wallet addresses are:")
    print(f"{from_wallet._network.name}: {from_wallet.address}")
    print(f"{to_wallet._network.name}: {to_wallet.address}")
    print(
        "Share these addresses with your counterparty and get your counterptarty's addresses as well."
    )

    # they have the opposite direction, meaning "from" wallet is SXP and "to" is ARK
    # counterparty_from = input("Counterparty's from address: ")
    counterparty_to = input("Counterparty's to address: ")

    if initiator:
        status, lock_id, secret_code = from_wallet.create_htlc_lock(counterparty_to)
        if not status:
            raise Exception("There was na issue creating a HTLC Lock transaction")

        # # wait for to_wallet htlc lock to pop up
        lock = to_wallet.wait_for_htlc_lock()
        print(
            f"HTLC Lock appeared on {to_wallet._network.name} with amount {int(lock['amount']) / ARKTOSHI}"
        )

        # TODO: check balance of locked fundsu
        # TODO: wait for confirmation

        # claim the funds from to_wallet
        balance_before = to_wallet.get_balance()
        status = to_wallet.create_htlc_claim(lock["lockId"], hexlify(secret_code).decode())
        sleep(16)
        balance_after = to_wallet.get_balance()
        print(
            f"{(balance_after - balance_before) / ARKTOSHI} coins added to your wallet on {to_wallet._network.name}"
        )
    else:
        lock = to_wallet.wait_for_htlc_lock()
        print(
            f"HTLC Lock appeared on {to_wallet._network.name} with amount {int(lock['amount']) / ARKTOSHI}"
        )

        # TODO: check balance of locked fundsu
        # TODO: wait for confirmation
        # TODO: make this htlc lock SHORTER than the initiator's htlc lock

        # create a HTLC lock using the same secret hash that counterparty used to create
        status, lock_id, _ = from_wallet.create_htlc_lock(counterparty_to, lock["secretHash"])
        if not status:
            raise Exception("There was na issue creating a HTLC Lock transaction")

        # wait for counterparty to claim your fundsu so you can use the secret code to claim the
        # funds they have locked
        unlock = from_wallet.wait_for_htlc_unlock(lock_id)
        print(
            f"HTLC Unlock appeared on {from_wallet._network.name} with amount {int(lock['amount']) / ARKTOSHI}"
        )

        # claim fundsu
        balance_before = to_wallet.get_balance()
        status = to_wallet.create_htlc_claim(
            lock["lockId"], unlock["asset"]["claim"]["unlockSecret"]
        )
        sleep(16)
        balance_after = to_wallet.get_balance()

        print(
            f"{(balance_after - balance_before) / ARKTOSHI} coins added to your wallet on {to_wallet._network.name}"
        )

    print("DONE!")


if __name__ == "__main__":
    main()
