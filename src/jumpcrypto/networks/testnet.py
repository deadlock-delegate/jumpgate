from datetime import datetime

from jumpcrypto.networks.base import Network


class ArkTestnet(Network):
    name = "ark_testnet"
    epoch = datetime(2017, 3, 21, 13, 00, 00)
    version = 23
    wif = 186


class SolarTestnet(Network):
    name = "solar_testnet"
    epoch = datetime(2022, 3, 16, 18, 00, 00)
    version = 30
    wif = 252
