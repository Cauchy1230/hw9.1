#!/usr/bin/python3
from algosdk import account, encoding
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction

#Connect to Algorand node maintained by PureStake
#Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
   "X-API-Key": algod_token,
}

acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance

def send_tokens( receiver_pk, tx_amount ):
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last
    send_amount = 1

    #Your code here
#     private_key, address = account.generate_account()
#     mnemonic_secret = 'H4V73MCJT2JJPTTIQ2LH2T7OA4GEDCB4GE4M57NPCXG2DKXPEVJQ'
#     sk = mnemonic.to_private_key(mnemonic_secret)
#     pk = mnemonic.to_public_key(mnemonic_secret)
    address = 'EOH4RTMJE67RIZ62MD4QVR72EFOCTHCWYAWBXGLRPUJE456774U5LPP5RU'
    private_key = '2hBdL5+ibhxsCNofTV5AnRfpFaPUJNjhr6x094lCQTQjj8jNiSe/FGfaYPkKx/ohXCmcVsAsG5lxfRJOd9//KQ=='
    txn = transaction.PaymentTxn(address, fee=send_amount, first=first_valid_round, last=last_valid_round,
                             gh=gen_hash, receiver=receiver_pk, amt=tx_amount)
    SignedTxn = txn.sign(private_key)
    tx_id = acl.send_transaction(txn=SignedTxn)
    sender_pk = address

    return sender_pk, tx_id

# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return

