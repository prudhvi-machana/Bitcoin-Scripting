# Bitcoin-Scripting

## Team

*Team Name:* [HASHPA]

### Team Members:

- Lawadya Yashwanth Chowhan ( 230001046 )
- M . Mohan Prudhvi Sai  ( 230001047)
- M. Rishik Preetham ( 230001048 )



## Overview

This project demonstrates the creation and execution of Bitcoin transactions using *Bitcoin Core RPC API*. It covers two transaction types:

- \\*Legacy Transactions (P2PKH) - \\*legacy.py**
- \\*SegWit Transactions (P2SH-P2WPKH) - \\*segwit.py**

The scripts automate wallet setup, address generation, fund transfers, transaction decoding, and mining confirmation.

---

## Prerequisites

Ensure you have the following installed:

- *Bitcoin Core* (configured for testnet usage)
- \\*Python \\*
- **python-bitcoinrpc*\\* library\\

### Install Dependencies

sh
pip install python-bitcoinrpc


---

## Configuration

The scripts use *Bitcoin Core's RPC* to interact with the network. Ensure bitcoin.conf has the following settings:

ini
regtest=1
server=1
rpcuser=StandUp
rpcpassword=6305f1b2dbb3bc5a16cd0f4aac7e1eba

[regtest]
rpcallowip=127.0.0.1
rpcport=18332
paytxfee=0.0005   
fallbackfee=0.0002 
mintxfee=0.00001 
txconfirmtarget=6


Start Bitcoin Core in testnet mode:

sh
bitcoind 


---

## Running the Scripts

Both scripts follow a similar execution flow:

1. Create/load a Bitcoin wallet.
2. Generate appropriate addresses (Legacy or SegWit).
3. Mine blocks to generate an initial balance.
4. Send BTC transactions and decode them.
5. Confirm transactions by mining blocks.
6. Display wallet balances.

### Run legacy.py for Legacy Transactions

sh
python legacy.py


### Run segwit.py for SegWit Transactions

sh
python segwit.py


---

## Key Functions Explained

### 1. *Wallet Setup*

Ensures the wallet exists, otherwise creates and loads it.

python
def ensure_wallet():
    rpc_client = connect_rpc()
    if WALLET_NAME not in rpc_client.listwallets():
        rpc_client.createwallet(WALLET_NAME)
    return connect_rpc(WALLET_NAME)


### 2. *Generating Addresses*

#### Legacy (legacy.py)

python
def get_legacy_address(rpc_client):
    return rpc_client.getnewaddress("", "legacy")


#### SegWit (segwit.py)

python
def get_segwit_address(rpc_client):
    return rpc_client.getnewaddress("", "bech32")


### 3. *Mining Blocks*

Generates blocks to get BTC balance for transactions.

python
def generate_blocks(rpc_client, num):
    miner_address = get_legacy_address(rpc_client)  # Legacy script
    rpc_client.generatetoaddress(num, miner_address)


python
def generate_blocks(rpc_client, num):
    miner_address = get_segwit_address(rpc_client)  # SegWit script
    rpc_client.generatetoaddress(num, miner_address)


### 4. *Sending Bitcoin*

Transfers BTC and mines a block for confirmation.

python
def send_bitcoins(rpc_client, to_address, amount):
    txid = rpc_client.sendtoaddress(to_address, amount)
    generate_blocks(rpc_client, 1)
    return txid


### 5. *Decoding Transactions*

Extracts ScriptPubKey from transactions.

python
def decode_transaction(rpc_client, txid, target_address):
    raw_tx = rpc_client.gettransaction(txid, True)
    decoded_tx = rpc_client.decoderawtransaction(raw_tx['hex'])
    return [vout['scriptPubKey']['hex'] for vout in decoded_tx['vout'] if 'address' in vout['scriptPubKey'] and vout['scriptPubKey']['address'] == target_address]


---

## Expected Output

### 1. *Initial Wallet Info*

sh
Connected to wallet 'MyNewWallet'.
Wallet Info: {"balance": 0.0, "txcount": 0}
Mining 101 blocks to get initial balance...


### 2. *Generated Addresses*

#### Legacy (legacy.py)

sh
Legacy Address A: mxxx...
Legacy Address B: mxxx...
Legacy Address C: mxxx...


#### SegWit (segwit.py)

sh
SegWit Address A: tb1xxx...
SegWit Address B: tb1xxx...
SegWit Address C: tb1xxx...


### 3. *Transaction Execution*

sh
Sending 1 BTC from A to B...
Transaction TXID: abc123...
Decoding Transaction to Extract ScriptPubKey...
ScriptPubKey: 76a914...
Sending 0.5 BTC from B to C...
Final Balance: 0.5 BTC


---

## Conclusion

This project successfully automates Bitcoin transactions in a *testnet environment, demonstrating **Legacy (P2PKH)* and *SegWit (P2SH-P2WPKH)* transactions, along with mining and decoding.

---

##
