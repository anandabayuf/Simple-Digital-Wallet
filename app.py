import os
import time

from xendit import Xendit, XenditError, BalanceAccountType
import xendit
from flask import Flask, request, render_template

app = Flask(__name__)

def getbalance():
    api_key = "xnd_development_akq2fAKnrapVrL2s25v0lnoqUq8hG2lZ729qj53Voa4NZ35LVDxuQObLQCZf"
    xendit_instance = Xendit(api_key=api_key)
    Balance = xendit_instance.Balance

    balance = Balance.get(
        account_type=BalanceAccountType.CASH,
    )

    return balance

@app.route("/")
def main():
    return render_template("MainPage.html")

@app.route("/bayardenganovo")
def payWithOvoPage():
    return render_template("PayWithOvoPage.html")

@app.route("/lihatsaldo")
def seeBalancePage():
    return render_template("SeeBalancePage.html", data=getbalance())

@app.route("/bayardenganovo/pay", methods=["POST"])
def pay():
    name = request.form.get("name")
    amount = request.form.get("amount")
    phone = request.form.get("phone_number")
    args = {
        "external_id": f"ovo-pay-{int(time.time())}",
        "amount": amount,
        "phone": phone,
    }
    xendit_instance = Xendit(api_key="xnd_development_akq2fAKnrapVrL2s25v0lnoqUq8hG2lZ729qj53Voa4NZ35LVDxuQObLQCZf")
    getbalance()
    try:
        ovo_payment = xendit_instance.EWallet.create_ovo_payment(**args)
        return vars(ovo_payment)
    except XenditError as e:
        return vars(e)


@app.route("/webhook", methods=["POST"])
def catch_webhook():
    print(request.json)
    return {}

if __name__ == "__main__":
    app.run(debug=True)


