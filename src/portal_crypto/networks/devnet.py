from datetime import datetime

from portal_crypto.networks.base import Network


class ArkDevnet(Network):
    name = "ark_devnet"
    epoch = datetime(2017, 3, 21, 13, 00, 00)
    version = 30
    wif = 170
