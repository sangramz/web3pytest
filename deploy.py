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
my_address = "0x0b09b007968b701e51C17b51BD587aae94bB4e36"
private_key = "50d9b4e3f2ef00e0c03ac0e48774ccc8ad77a97fc58f815786b1b3131f6e7f29"

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
tx_receipt= w3.eth.wait_for_transaction_receipt(tx_hash)

#To interact with a Contract we need Contract Address and Contract ABI
simple_storage= w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(simple_storage.functions.retrieveNo().call())
store_transaction= simple_storage.functions.storeNumber(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn= w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
send_store_tx= w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt= w3.eth.wait_for_transaction_receipt(send_store_tx)
print(simple_storage.functions.retrieveNo().call())
