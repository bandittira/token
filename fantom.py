from web3 import Web3

# Connect to Fantom Testnet
w3 = Web3(Web3.HTTPProvider('https://rpc.testnet.fantom.network/'))

# Check connection
print(w3.is_connected())
