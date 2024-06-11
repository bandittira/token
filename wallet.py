from web3 import Web3
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get private key and RPC URL from environment variables
private_key = os.getenv("PRIVATE_KEY")
rpc_url = os.getenv("RPC_URL")

# Initialize Web3 with an Ethereum node URL
w3 = Web3(Web3.HTTPProvider(rpc_url))

# Set the account
account = w3.eth.account.from_key(private_key)
w3.eth.defaultAccount = account.address

# Test connection by fetching the latest block number
try:
    block_number = w3.eth.block_number
    print(f'Connected to Ethereum blockchain. Latest block number: {block_number}')
except Exception as e:
    print(f'Error connecting to Ethereum blockchain: {e}')
