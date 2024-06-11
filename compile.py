from solcx import compile_source, install_solc, set_solc_version

# Install and set the Solidity compiler version
install_solc('0.8.20')
set_solc_version('0.8.20')

# Read the Solidity file
with open('ERC20Token.sol', 'r') as file:
    contract_source_code = file.read()

# Compile the contract
compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:Point']

# Extract ABI and Bytecode
abi = contract_interface['abi']
bytecode = contract_interface['bin']
