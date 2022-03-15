from web3 import Web3
import json

with open("/home/ubuntu/cloud/chain/0x/code/platform/packages/contracts/deployments/metis/UserPositions.json") as f:
    info_json = json.load(f)
abi = info_json["abi"]

metis_url = "https://andromeda.metis.io/?owner=1088"
w3 = Web3(Web3.HTTPProvider(metis_url))
w3.isConnected()
user_positions_address = "0x2a5352C810D0C1cC1e907Db0552459B46a82433B"

contract_instance = w3.eth.contract(address=user_positions_address, abi=abi)
contract_instance.functions.totalTokenBalance().call()
