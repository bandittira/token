from eth_account import Account

# Generate a new Ethereum account
new_account = Account.create()

# Display the address and private key
print(f'Address: {new_account.address}')
print(f'Private Key: {new_account.key.hex()}')