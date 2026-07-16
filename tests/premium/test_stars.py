# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import StarPayment

def test_star_payment_properties():
    pay = StarPayment(transaction_id="tx100", amount=500, date=1234567, source="Google Play")
    assert pay.transaction_id == "tx100"
    assert pay.amount == 500
    assert pay.source == "Google Play"
