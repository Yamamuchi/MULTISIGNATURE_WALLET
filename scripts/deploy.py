from brownie import MultiSignatureWallet, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3 as web3
import os


def deploy_wallet():
    account = get_account()
    address = account
    # address = os.getenv("PUBLIC_KEY")

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        if len(MockV3Aggregator) <= 0:
            deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    user_input = int(
        input("(1) Use lastest deployment\n(2) Deploy new contract\nSubmit answer: ")
    )

    if user_input == 1:
        multi_signature_wallet = MultiSignatureWallet[-1]
        print(multi_signature_wallet)
    elif user_input == 2:
        multi_signature_wallet = MultiSignatureWallet.deploy(
            price_feed_address,
            [address],
            1,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get("verify"),
        )

    user_input = int(
        input("(1) Submit tx\n(2) Confirm tx\n(3) Execute tx\nSubmit answer: ")
    )
    if user_input == 1:
        _address = input("Enter decimal address: ")
        _amount = int(input("Enter amount: "))
        _data = hex(int(input("Enter data: ")))
        submit_transaction(multi_signature_wallet, account, _address, _amount, _data)
    elif user_input == 2 or user_input == 3:
        _tx_index = input("Enter tx index: ")
        if user_input == 2:
            confirm_transaction(multi_signature_wallet, account, _tx_index)
        else:
            execute_transaction(multi_signature_wallet, account, _tx_index)


def submit_transaction(multi_signature_wallet, account, address, amount, data):
    print("Submitting transaction...")
    tx = multi_signature_wallet.submitTransaction(
        address, amount, data, {"from": account}
    )
    tx.wait(1)
    print("Successfully submitted transaction")


def confirm_transaction(multi_signature_wallet, account, tx_index):
    print("Confirming transaction...")
    tx = multi_signature_wallet.confirmTransaction(tx_index, {"from": account})
    tx.wait(1)
    print("Successfully confirmed transaction")


def execute_transaction(multi_signature_wallet, account, tx_index):
    print("Executing transaction...")
    tx = multi_signature_wallet.executeTransaction(tx_index, {"from": account})
    tx.wait(1)
    print("Successfully executed transaction")


def main():
    deploy_wallet()
