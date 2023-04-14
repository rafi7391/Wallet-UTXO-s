from flask import Flask, request, jsonify
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Connection to Bitcoin Core
rpc_user = "your_rpc_username"
rpc_password = "your_rpc_password"
rpc_port = "your_rpc_port"
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/")

app = Flask(__name__)

@app.route("/wallet/create", methods=["POST"])
def create_wallet():
    n_required = request.json["n_required"]
    pubkeys = request.json["pubkeys"]
    # Creation of a new multi-signature wallet
    wallet_address = rpc_connection.addmultisigaddress(n_required, pubkeys)
    # Return the wallet address
    return jsonify({"wallet_address": wallet_address}), 200

@app.route("/wallet/add_signatory", methods=["POST"])
def add_signatory():
    # Get the wallet address and public key of the new signatory
    wallet_address = request.json["wallet_address"]
    pubkey = request.json["pubkey"]
    # Adding the new signatory to the wallet
    result = rpc_connection.addmultisigaddress(2, [pubkey], wallet_address)
    return jsonify(result), 200

@app.route("/wallet/send", methods=["POST"])
def send():
    # details of the sending address, recipient address, and amount
    sending_address = request.json["sending_address"]
    recipient_address = request.json["recipient_address"]
    amount = request.json["amount"]
    # Send the transaction from the sending address to the recipient address
    result = rpc_connection.sendfrom(sending_address, recipient_address, amount)
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)
