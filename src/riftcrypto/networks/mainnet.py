from datetime import datetime

from riftcrypto.networks.base import Network


class ArkMainnet(Network):
    name = "ark_mainnet"
    epoch = datetime(2017, 3, 21, 13, 00, 00)
    version = 23
    wif = 170


class SolarMainnet(Network):
    name = "solar_mainnet"
    epoch = datetime(2022, 3, 28, 18, 00, 00)
    version = 63
    wif = 252
