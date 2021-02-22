#!/usr/bin/env python3

import csv
import sys
sys.path.insert(0, '/home/eirik/Programmering/Sbanken-i-terminal/')
from  Helpers import create_authenticated_http_session,get_accounts,get_transactions,getTransactionDate,getPayee,getMemo, getOut, getIn

def getAccount(http_session, customerId, accountNo):
    accounts = get_accounts(
        http_session, 
        customerId)

    for account in accounts:
        if account['accountNumber'] == accountNo:
            return account
    
    return None


def main():
    # enable_debug_logging()
    
    import api_settings
    import pprint

    http_session = create_authenticated_http_session(api_settings.CLIENTID, api_settings.SECRET)

    # customer_info = get_customer_information(http_session, api_settings.CUSTOMERID)
    # pprint.pprint(customer_info)

    #pprint.pprint(accounts)

    accountNo = '97133248955'
    account = getAccount(http_session, api_settings.CUSTOMERID, accountNo)
    
    if account == None:
        print('Account not found!')
        exit(1)

    months = 1
    # if months == '':
    #     months = 1
    # months = int(months)
    # if months > 12:
    #     months = 12

    transactions = get_transactions(
        http_session, 
        api_settings.CUSTOMERID,
        account['accountId'],
        months)
    #pprint.pprint(transactions)

    # with open(account['name']+'_'+account['accountNumber']+'.csv', 'w', encoding='utf-8') as csvfile:
    #     ktowriter = csv.writer(
    #         csvfile, 
    #         delimiter=',',
    #         quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     ktowriter.writerow(['Date', 'Payee', 'Memo', 'Outflow', 'Inflow'])
    print(f"{'Date':10s} {'Payee':20s} {'Memo':20s}  {'OUT':10s} {'INN':10s}")
    print(80*'-')
    for item in transactions:
        date = getTransactionDate(item)
        payee = getPayee(item)
        memo = getMemo(item)
        outflow = getOut(item)
        inflow = getIn(item)
        
        
        #if item['transactionTypeCode'] == 710:
        #Typecasting 
        if type(outflow)==float:
            outflow=str(outflow)
        if type(inflow)== float:
            inflow =str(inflow)
            
        print(f"{date:10s} {payee[:20]:20s} {memo[:20]:20s}  {outflow:10s} {inflow:10s}")

if __name__ == "__main__":
    main()
