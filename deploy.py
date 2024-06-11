import os
from dotenv import load_dotenv
from solcx import compile_source, install_solc, set_solc_version
from web3 import Web3

# Install and set the Solidity compiler version
install_solc('0.8.19')
set_solc_version('0.8.19')

# Read the Solidity file
with open('ERC20Token.sol', 'r') as file:
    contract_source_code = file.read()

# Compile the contract
compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:Point']
# Define the recipient wallet address
recipient_address = "0xEd99A50d0C6AfC1B50D1305FE230A7Bb2F220255"

# Extract ABI and Bytecode
abi = contract_interface['abi']
bytecode = contract_interface['bin']

w3 = Web3(Web3.HTTPProvider('https://rpc.testnet.fantom.network/'))

load_dotenv()
# Set up account
private_key = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(private_key)
w3.eth.defaultAccount = account.address

print(w3.eth.get_balance(account.address))

if not private_key:
    raise ValueError("Private key not found. Please set the PRIVATE_KEY environment variable.")
# Create the contract in Python
ERC20 = w3.eth.contract(abi=abi, bytecode=bytecode)
# Build transaction
transaction = ERC20.constructor(1000000000 * 10**18).build_transaction({
    'chainId': 250,  # Fantom testnet chain ID
    'gas': 1,
    'gasPrice': w3.to_wei('72', 'gwei'),
    'nonce': w3.eth.get_transaction_count(account.address),
})

# Sign transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send transaction
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

print(f'Contract deployed at address: {txn_receipt.contractAddress}')

# Contract address (from deployment receipt)
contract_address = txn_receipt.contractAddress

# Create a contract instance
contract_instance = w3.eth.contract(address=contract_address, abi=abi)

# Check the name and symbol of the token
# Check the name and symbol of the token
try:
    token_name = contract_instance.functions.name().call()
    token_symbol = contract_instance.functions.symbol().call()
    total_supply = contract_instance.functions.totalSupply().call()
    print(f'Token name: {token_name}')
    print(f'Token symbol: {token_symbol}')
    print(f'Total supply: {total_supply}')
except Exception as e:
    print(f'Error calling contract functions: {e}')

# Transfer tokens to recipient address
try:
    # Specify the amount of tokens to transfer
    amount_to_send = 10000 * 10**18  # Transfer 10,000 tokens

    # Build the transaction to transfer tokens
    tx_hash = contract_instance.functions.transfer(recipient_address, amount_to_send).transact()

    # Wait for the transaction to be mined
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    if receipt.status == 1:
        print(f'Tokens transferred successfully to {recipient_address}. Transaction hash: {tx_hash}')
        print(f'Transaction receipt: {receipt}')
    else:
        print('Transaction failed. Check transaction status.')
except Exception as e:
    print(f'Error transferring tokens: {e}')
