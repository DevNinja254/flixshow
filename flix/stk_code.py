import requests
import base64
from datetime import datetime
from .mpesa_config import *
  
def sendStkPush(Amount, phoneNumber):
    token = TOKEN
    timestamp = TIMESTAMP
    shortCode = SHORT_CODE#sandbox -174379
    passkey = PASS_KEY
    stk_password = STK_PASSWORD
    
    #choose one depending on you development environment
    #sandbox
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    #live
    # url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    
    requestBody = {
        "BusinessShortCode": shortCode,
        "Password": stk_password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline", #till "CustomerBuyGoodsOnline"
        "Amount": Amount,
        "PartyA": phoneNumber,
        "PartyB": shortCode,
        "PhoneNumber": phoneNumber,
        "CallBackURL": "https://comic-finch-strongly.ngrok-free.app/stk/",
        "AccountReference": "account",
        "TransactionDesc": "test",
    }
    
    try:
        response = requests.post(url, json=requestBody, headers=headers)
        return response.json()
    except Exception as e:
        print('Error:', str(e))