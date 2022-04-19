from datetime import datetime

from jumpcrypto.configuration.network import get_network, set_custom_network, set_network
from jumpcrypto.networks.devnet import ArkDevnet
from jumpcrypto.networks.mainnet import ArkMainnet
from jumpcrypto.networks.testnet import ArkTestnet


def test_get_network():
    result = get_network()
    assert result["version"] == 30


def test_set_network():
    # test main net
    set_network(ArkMainnet)
    result = get_network()
    assert result["version"] == 23
    assert result["wif"] == 170
    # test test net
    set_network(ArkTestnet)
    result = get_network()
    assert result["version"] == 23
    assert result["wif"] == 186
    set_network(ArkDevnet)  # set back to devnet so other tests don't fail


def test_set_custom_network():
    epoch_time = datetime(2017, 1, 1, 13, 00, 00)
    set_custom_network(epoch_time, 11, 130)
    result = get_network()
    assert result["version"] == 11
    assert result["wif"] == 130
    assert result["epoch"] == epoch_time
    set_network(ArkDevnet)  # set back to devnet so other tests don't fail
