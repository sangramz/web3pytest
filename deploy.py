from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os

install_solc("0.6.0")


with open("./simpleStorage.sol", 'r') as file:
    simple_storage_file = file.read()

#Compiling
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"simpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm,sourceMap"]}
            }
        }
    },
    solc_version="0.6.0",
)

#JSON File Creation
with open("complied_code.JSON", "w") as file:
    json.dump(compiled_sol, file)

#get bytecode
bytecode = compiled_sol["contracts"]["simpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get ABI
abi= compiled_sol["contracts"]["simpleStorage.sol"]["SimpleStorage"]["abi"]

#connecting to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xc352Bfb826c58e1b0e5535B283152aA288576D62"
private_key = os.getenv(PRIVATE_KEY)

#creating the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
#get nonce- latest transaction
nonce = w3.eth.getTransactionCount(my_address)

#Build Transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
#Sign the Transaction
signed_txn= w3.eth.account.sign_transaction(transaction, private_key=private_key)
#Send this Transaction
tx_hash= w3.eth.send_raw_transaction(signed_txn.rawTransaction)