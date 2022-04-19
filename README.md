# JumpGate

A portal between ecosystems.

`pyenv virtualenv 3.8.9 jumpgate && echo jumpgate > .python-version`

`pip install ."[dev]"`

**❗ THIS LIBRARY IS STILL UNDER HEAVY DEVELOPMENT AND IS NOT READY TO BE USED WITH REAL FUNDSU ❗**

### Run a swap 

USER A (has DARK)

```bash
PYTHONPATH=src/ python src/jumpgate/main.py -f "ark_devnet:safdjn asdgjn 0-2o3asfdmkgsadiouaw49k96-:10" -t "ark_testnet:safdjn asdgjn 0-2o3asfdmkgsadiouaw49k96-:10" --initiator
```

USER B (has TARK)

```bash
PYTHONPATH=src/ python src/jumpgate/main.py -f "ark_testnet:235sd asdgjn 0-2o3asfdmkgsadiouaw49k96-:10" -t "ark_devnet:235sd asdgjn 0-2o3asfdmkgsadiouaw49k96-:10"
```


## TODO

### Short term
- [ ] Wait for enough confirmations
- [ ] Check locked balances
- [ ] Write tests for `jumpgate`
- [ ] Make HTLC lock created by non-initiator shorter than initiators HTLC
- [ ] Check if tx is accepted and broadcasted as expected and raise error if not


### Other
- [ ] Improve UI
- [ ] Clearer error messaging
- [ ] Add currency symbols or tickers to Networks
- [ ] Extend Wallet class to suppor other non-ark based networks (BTC, ETH, SOL, BSC, AVAX)
