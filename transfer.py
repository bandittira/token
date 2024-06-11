import os
from dotenv import load_dotenv
from web3 import Web3

# Load environment variables
load_dotenv()

# Set up Web3 provider for Fantom testnet
w3 = Web3(Web3.HTTPProvider('https://rpc.testnet.fantom.network/'))

# Load private key and contract address from environment variables
private_key = os.getenv("PRIVATE_KEY")
contract_address = os.getenv("CONTRACT_ADDRESS")

if not private_key:
    raise ValueError("Private key not found. Please set the PRIVATE_KEY environment variable.")
if not contract_address:
    raise ValueError("Contract address not found. Please set the CONTRACT_ADDRESS environment variable.")

# Set up account
account = w3.eth.account.from_key(private_key)
w3.eth.default_account = account.address

# Load the contract ABI
with open('PointABI.json', 'r') as file:
    contract_abi = file.read()

# Instantiate the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Define the recipient address
recipient_address = "0xEd99A50d0C6AfC1B50D1305FE230A7Bb2F220255"

# Function to transfer tokens
def transfer_tokens(amount):
    nonce = w3.eth.get_transaction_count(w3.eth.default_account)
    tx = contract.functions.transfer(recipient_address, amount).build_transaction({
    'gas': 3000000,  # Set a fixed gas limit
    'gasPrice': w3.to_wei('20', 'gwei'),
    'nonce': nonce,
})

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()

# Amount of tokens to transfer
amount_to_send = 10000 * 10**18  # Transfer 10,000 tokens

# Send tokens
tx_hash = transfer_tokens(amount_to_send)

# Wait for the transaction to be mined
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Check if the transaction was successful
if receipt.status == 1:
    print(f'Tokens transferred successfully. Transaction hash: {tx_hash}')
    print(f'Transaction receipt: {receipt}')
else:
    print('Transaction failed. Check transaction status.')
