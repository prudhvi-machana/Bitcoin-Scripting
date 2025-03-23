from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from pprint import pprint

# RPC Configuration
RPC_USER = "StandUp"
RPC_PASS = "6305f1b2dbb3bc5a16cd0f4aac7e1eba"
RPC_HOST = "127.0.0.1"
RPC_PORT = "18332"
WALLET_NAME = "MyNewWallet"

def connect_rpc(wallet=None):
    """Connects to the Bitcoin Core RPC."""
    url = f"http://{RPC_USER}:{RPC_PASS}@{RPC_HOST}:{RPC_PORT}"
    if wallet:
        url += f"/wallet/{wallet}"
    return AuthServiceProxy(url)

def ensure_wallet():
    """Checks if the wallet exists, loads or creates it if necessary."""
    rpc_client = connect_rpc()
    
    loaded_wallets = rpc_client.listwallets()
    if WALLET_NAME not in loaded_wallets:
        print(f"Wallet '{WALLET_NAME}' is not loaded. Trying to load it...")
        try:
            rpc_client.loadwallet(WALLET_NAME)
            print(f"Wallet '{WALLET_NAME}' loaded successfully.")
        except JSONRPCException as e:
            if "Wallet file verification failed" in str(e):
                print(f"Wallet '{WALLET_NAME}' does not exist. Creating a new one...")
                rpc_client.createwallet(WALLET_NAME)
                print(f"Wallet '{WALLET_NAME}' created successfully.")
            else:
                raise e  

    return connect_rpc(WALLET_NAME)

def get_segwit_address(rpc_client):
    """Generates a new SegWit Bech32 address (starts with 'bc1' or 'tb1' in testnet)."""
    return rpc_client.getnewaddress("", "bech32")

def generate_blocks(rpc_client, num):
    """Mines blocks to generate Bitcoin."""
    miner_address = get_segwit_address(rpc_client)
    rpc_client.generatetoaddress(num, miner_address)

def send_bitcoins(rpc_client, to_address, amount):
    """Sends Bitcoin and mines a block for confirmation."""
    txid = rpc_client.sendtoaddress(to_address, amount)
    print(f"Transaction {txid} sent, mining a block to confirm...")
    generate_blocks(rpc_client, 1)
    return txid

def decode_transaction(rpc_client, txid, target_address):
    """Decodes a transaction and extracts ScriptPubKey for the given address."""
    try:
        raw_tx = rpc_client.gettransaction(txid, True)
        decoded_tx = rpc_client.decoderawtransaction(raw_tx['hex'])

        print("\nDecoded Transaction:")
        pprint(decoded_tx)

        print("\nExtracting ScriptPubKey...")
        for vout in decoded_tx['vout']:
            if 'address' in vout['scriptPubKey'] and vout['scriptPubKey']['address'] == target_address:
                print(f"ScriptPubKey for {target_address}: {vout['scriptPubKey']['hex']}")
                return vout['scriptPubKey']['hex']

        print(f"Address {target_address} not found in the outputs.")
        return None

    except JSONRPCException as e:
        print(f"RPC Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

# ---- Main Execution ----
try:
    rpc_client = ensure_wallet()
    print(f"Connected to wallet '{WALLET_NAME}'.")

    wallet_info = rpc_client.getwalletinfo()
    print("Wallet Info:")
    pprint(wallet_info)

    print("Mining 101 blocks to get initial balance...")
    generate_blocks(rpc_client, 101)

    address_A = get_segwit_address(rpc_client)
    address_B = get_segwit_address(rpc_client)
    address_C = get_segwit_address(rpc_client)
    print(f"SegWit Address A: {address_A}")
    print(f"SegWit Address B: {address_B}")
    print(f"SegWit Address C: {address_C}")

    print("Sending 1 BTC from A to B...")
    txid1 = send_bitcoins(rpc_client, address_B, 1.0)
    print(f"Transaction 1 TXID: {txid1}")

    print("\nDecoding Transaction to Extract ScriptPubKey for Address B...")
    script_pubkey_B = decode_transaction(rpc_client, txid1, address_B)

    print("Sending 0.5 BTC from B to C...")
    txid2 = send_bitcoins(rpc_client, address_C, 0.5)
    print(f"Transaction 2 TXID: {txid2}")

    final_balance = rpc_client.getbalance()
    print(f"Final Balance: {final_balance} BTC")

except JSONRPCException as e:
    print(f"RPC Error: {e}")
except Exception as e:
    print(f"Error: {e}")
