# BankAccount
A Python class that can simulate current (checking), savings, and balance accounts
```python
class Account:
    
    # Initiation of classes managed by Account
    def __init__(self):
        self.account_holder = self.Account_Holder()
        self.atm_card_validator = self.ATM_card_validator()
        self.login = self.Login()
        ...
        self.currentaccount = self.CurrentAccount()  # aka 'checking' account
        self.savingsaccount = self.SavingsAccount()
        self.businessaccount = self.BusinessAccount()
        ...         
    class ATM_card_validator(Account_Holder):
        
        '''Determines whether a number is a valid ATM card number.
        Based on the Luhn formula.
        This version uses https://en.wikipedia.org/wiki/Luhn_algorithm'''
        
        def access_transactions_balances(self):
            
            df1 = ''
            df1a = ''
            card_number = input("Enter card number with no spaces : ")
            
            # Implementing formula
            l = [k for k in card_number]
            ...
```
