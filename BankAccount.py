# -*- coding: utf-8 -*-
"""
Completed on Wed Jul 21 05:09:46 2021
Name: BankAccount.py
Purpose: Simulates current (checking), savings, and business back aaccounts
@author: Charles Umesi (charlesumesi)
"""

from abc import ABC, abstractmethod
import os
import sys
import datetime
import pandas as pd


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None  # default='warn'
# You may want to enable (i.e., hashtag) chained_assignment until you are comfortable with your data


class Account:
    
    # Initiation of classes managed by Account
    def __init__(self):
        self.account_holder = self.Account_Holder()
        self.atm_card_validator = self.ATM_card_validator()
        self.login = self.Login()
        self.menu = self.Menu()
        self.setup_s = self.Setup_S()
        self.setup_b = self.Setup_B()
        self.setup_sgivenb = self.Setup_SgivenB()
        self.setup_bgivens = self.Setup_BgivenS()
        self.mergeanddoubleremover = self.MergeAndDoubleRemover()
        self.menu_cs = self.Menu_CS()
        self.menu_cb = self.Menu_CB()
        self.menu_csb = self.Menu_CSB()
        self.currentaccount = self.CurrentAccount()  # aka 'checking' account
        self.savingsaccount = self.SavingsAccount()
        self.businessaccount = self.BusinessAccount()
        self.transfer_cs = self.Transfer_CS()
        self.transfer_cb = self.Transfer_CB()
        self.transfer_csb = self.Transfer_CSB()
        
    '''Abstract class'''
    
    class Account_Holder(ABC):
        
        def access_transactions_balances(self):
            pass
        
    '''Subclasses'''
    
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
            m = l[:-1]
            n = m[::-1]
            o = [str(2*int(i)) for i in n[0::2]]
            p = ''.join(o)
            q = n[1::2]
            
            r = ''            
            try:
                r = sum(list(map(int, p))) + sum(list(map(int, q))) + int(l[-1]) 
                if r%10 == 0:
                    df1 = {'Value':[int(card_number[-11:])]}
                    df1a = pd.DataFrame(df1)
                    df1a.to_csv('OceansEleven.csv',index=False)
                    del(l,m,n,o,p,q)
                    return Account.Login.access_transactions_balances(self)
                else:
                    print('The number entered is not a valid ATM card number.')
                    sys.exit()
            except:
                sys.exit()                     
        
    class Login(Account_Holder):
        
        '''Accesses and enables creation of pin.'''
        
        def access_transactions_balances(self):
                        
            df2 = pd.read_csv('OceansEleven.csv')
            df3a = ''
            df3b = ''
            df4 = ''
            parameter = ''
            bottleneck = ''
            pin = ''
            new_pin = ''
            current = {'C1':['S BODY (CURRENT) 11223344 (10-20-30)'],'C2':['Start'],'C3':[0]}

            if (os.path.isfile('Parameter'+str(df2.loc[0,'Value'])+'.csv') == True) and (os.path.isfile('Bottleneck'+str(df2.loc[0,'Value'])+'.csv') == True):
                df3a = pd.read_csv('Parameter'+str(df2.loc[0,'Value'])+'.csv')
                df3b = pd.read_csv('Bottleneck'+str(df2.loc[0,'Value'])+'.csv')
                pin = eval(input('Enter pin : '))
                if pin + eval(str(df2.loc[0,'Value'])) == eval(str(df3a.loc[0,'Parameter'])):
                    print('Welcome Some Body')
                    return Account.Menu.access_transactions_balances(self)
                else:
                    os.remove('OceansEleven.csv')
                    print('Incorrect pin entered.')
                    sys.exit()    
            else:
                new_pin = eval(input('Enter a new pin for your card (between 1000 and 999999) : '))
                if (int(new_pin) == float(new_pin)):
                    if new_pin in range(1000,1000000):
                        parameter = {'Parameter':[new_pin + eval(str(df2.loc[0,'Value']))]}
                        bottleneck = {'C1': ['CURRENT ACCOUNT (11223344 | 10-20-30)'], 'C2': [0]}
                        df3a = pd.DataFrame(parameter)
                        df3a.to_csv('Parameter'+str(df2.loc[0,'Value'])+'.csv',index=False)
                        df3b = pd.DataFrame(bottleneck)
                        df3b.to_csv('Bottleneck'+str(df2.loc[0,'Value'])+'.csv',index=False)
                        df4 = pd.DataFrame(current)
                        df4.to_csv('CurrentAccount'+str(df2.loc[0,'Value'])+'.csv',index=False)
                        os.remove('OceansEleven.csv')
                        print('Pin accepted.')
                        return Account.ATM_card_validator.access_transactions_balances(self)
                    else:
                        print('Out of range.')
                        return Account.ATM_card_validator.access_transactions_balances(self)               
                else:
                    os.remove('OceansEleven.csv')
                    print('Invalid choice of pin.')
                    return Account.ATM_card_validator.access_transactions_balances(self)
                
    class Menu(Account_Holder):
        
        '''Main menu for bank account.'''
        
        def access_transactions_balances(self):
            
            df5 = pd.read_csv('OceansEleven.csv')
            df6 = pd.read_csv('Bottleneck'+str(df5.loc[0,'Value'])+'.csv')
            df6_list = list(zip(df6['C1'],df6['C2']))
            df7 = pd.read_csv('CurrentAccount'+str(df5.loc[0,'Value'])+'.csv')
            df7_list = list(zip(df7['C1'],df7['C2'],df7['C3']))
            opensav = ''
            openbus = '' 
                                  
            transaction_choice = input('Select type of transaction\n1. Deposit or withdraw money (current account)\n2. View transactions\n3. View savings account\n   (also shows your business account if you have one)\n4. View business account\n   (also shows your savings account if you have one)\n5. View all accounts\n6. Exit : ')
            if transaction_choice == '1':
                return Account.CurrentAccount.access_transactions_balances(self)
            elif transaction_choice == '2':
                if os.path.isfile('Bottleneck_CSB'+str(df5.loc[0,'Value'])+'.csv') == True:
                    return Account.Menu_CSB.access_transactions_balances(self)
                elif (os.path.isfile('Bottleneck_CS'+str(df5.loc[0,'Value'])+'.csv')==True) and (os.path.isfile('Bottleneck_CB'+str(df5.loc[0,'Value'])+'.csv')==True):
                    return Account.MergeAndDoubleRemover.access_transactions_balances(self)
                elif (os.path.isfile('Bottleneck_CS'+str(df5.loc[0,'Value'])+'.csv')==True) and (os.path.isfile('Bottleneck_CB'+str(df5.loc[0,'Value'])+'.csv')==False):
                    return Account.Menu_CS.access_transactions_balances(self)
                elif (os.path.isfile('Bottleneck_CS'+str(df5.loc[0,'Value'])+'.csv')==False) and (os.path.isfile('Bottleneck_CB'+str(df5.loc[0,'Value'])+'.csv')==True):
                    return Account.Menu_CB.access_transactions_balances(self)
                elif (os.path.isfile('Bottleneck_CS'+str(df5.loc[0,'Value'])+'.csv')==False) and (os.path.isfile('Bottleneck_CB'+str(df5.loc[0,'Value'])+'.csv')==False):
                    for i in df7_list:
                        if i[2] >= 0:
                            print(i[0],i[1],' £'+"%.2f"%(i[2]))
                        elif i[2] < 0:
                            print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                    return Account.Menu.access_transactions_balances(self)                           
            elif transaction_choice == '3':
                if os.path.isfile('Bottleneck_CSB'+str(df5.loc[0,'Value'])+'.csv') == True:
                    return Account.Menu_CSB.access_transactions_balances(self)
                elif os.path.isfile('Bottleneck_CS'+str(df5.loc[0,'Value'])+'.csv') == True:
                    if os.path.isfile('Bottleneck_CB'+str(df5.loc[0,'Value'])+'.csv') == True:
                        return Account.MergeAndDoubleRemover.access_transactions_balances(self)
                    else:
                        return Account.Menu_CS.access_transactions_balances(self)
                else:
                    opensav = input('You currently do not have a savings account.\nDo you wish to open one? (Y/N) : ')
                    if opensav == 'Y' or opensav == 'y':
                        return Account.Setup_S.access_transactions_balances(self)
                    elif opensav == 'N' or opensav == 'n':
                        return Account.Menu.access_transactions_balances(self)
                    else:
                        print('Your response cannot be processed.')
                        return Account.Menu.access_transactions_balances(self)  
            elif transaction_choice == '4':
                if os.path.isfile('Bottleneck_CSB'+str(df5.loc[0,'Value'])+'.csv') == True:
                    return Account.Menu_CSB.access_transactions_balances(self)
                elif os.path.isfile('Bottleneck_CB'+str(df5.loc[0,'Value'])+'.csv') == True:
                    if os.path.isfile('Bottleneck_CS'+str(df5.loc[0,'Value'])+'.csv') == True:
                        return Account.MergeAndDoubleRemover.access_transactions_balances(self)
                    else:
                        return Account.Menu_CB.access_transactions_balances(self)
                else:
                    openbus = input('You currently do not have a business account.\nDo you wish to open one? (Y/N) : ')
                    if openbus== 'Y' or openbus == 'y':
                        return Account.Setup_B.access_transactions_balances(self)
                    elif openbus == 'N' or openbus == 'n':
                        return Account.Menu.access_transactions_balances(self)
                    else:
                        print('Your response cannot be processed.')
                        return Account.Menu.access_transactions_balances(self)
            elif transaction_choice == '5':
                if os.path.isfile('Bottleneck_CSB'+str(df5.loc[0,'Value'])+'.csv') == True:
                    return Account.Menu_CSB.access_transactions_balances(self)
                elif (os.path.isfile('Bottleneck_CS'+str(df5.loc[0,'Value'])+'.csv')==True) and (os.path.isfile('Bottleneck_CB'+str(df5.loc[0,'Value'])+'.csv')==True):
                    return Account.MergeAndDoubleRemover.access_transactions_balances(self)
                elif (os.path.isfile('Bottleneck_CS'+str(df5.loc[0,'Value'])+'.csv')==True) and (os.path.isfile('Bottleneck_CB'+str(df5.loc[0,'Value'])+'.csv')==False):
                    return Account.Menu_CS.access_transactions_balances(self)
                elif (os.path.isfile('Bottleneck_CS'+str(df5.loc[0,'Value'])+'.csv')==False) and (os.path.isfile('Bottleneck_CB'+str(df5.loc[0,'Value'])+'.csv')==True):
                    return Account.Menu_CB.access_transactions_balances(self)
                elif (os.path.isfile('Bottleneck_CS'+str(df5.loc[0,'Value'])+'.csv')==False) and (os.path.isfile('Bottleneck_CB'+str(df5.loc[0,'Value'])+'.csv')==False):
                    for i in df6_list:
                        print(i[0],'£'+"%.2f"%(i[1]))
                    return Account.Menu.access_transactions_balances(self)   
            elif transaction_choice == '6':
                sys.exit()                    
            else:               
                print('Your response cannot be processed.')
                return Account.Menu.access_transactions_balances(self)
                
    class Setup_S(Account_Holder):
        
        '''Creates new savings account if requested and none already present.'''
        
        def access_transactions_balances(self):      
            
            current_date = datetime.datetime.now().strftime("%d %b %Y")
            
            df8 = pd.read_csv('OceansEleven.csv')
            df9 = pd.read_csv('Bottleneck'+str(df8.loc[0,'Value'])+'.csv')
            caveat = ''
            opening_amount = ''          
            savings = {'C1':['S BODY (SAVINGS) 11556677 (10-20-30)'],'C2':['Start'],'C3':[0]}
            df10 = pd.DataFrame(savings)
            df10_payline = ''
            df10_paylinedf = ''
            df10_extend = ''
            df10_reset = ''
            df10_dict = ''
            df10_again = ''
            bottleneck_S = ''
            bottleneck_Sdf = ''
            bottleneck_CS = ''
            bottleneck_CS_reset = ''
            bottleneck_CS_dict = ''
            bottleneck_CS_again = ''
                  
            # Search specifically for pre-existing business account
            if os.path.isfile('Bottleneck_CB'+str(df8.loc[0,'Value'])+'.csv') == True:
                return Account.Setup_SgivenB.access_transactions_balances(self)
            else:     
                caveat = input('You are about to open a savings account.\nThis account attracts a once-compounded yearly interest of 2%.\nDo you accept? (Y/N) : ')
                if caveat == 'Y' or caveat == 'y':
                    opening_amount = input('Enter opening amount : £')
                    try:
                        eval(opening_amount)
                        df10_payline = {'C1':[current_date],'C2':['Paid in'],'C3':[eval(opening_amount)]}
                        df10_paylinedf = pd.DataFrame(df10_payline)
                        df10_extend = pd.concat([df10,df10_paylinedf])
                        df10_reset = df10_extend.reset_index()
                        df10_dict = df10_reset.to_dict()
                        df10_dict.pop('index')
                        df10_again = pd.DataFrame(df10_dict)
                        df10_again.to_csv('SavingsAccount'+str(df8.loc[0,'Value'])+'.csv',index=False)
                        bottleneck_S = {'C1': ['SAVINGS ACCOUNT (11556677 | 10-20-30)'], 'C2': [df10_again['C3'].sum()]}
                        bottleneck_Sdf = pd.DataFrame(bottleneck_S)
                        bottleneck_CS = pd.concat([df9,bottleneck_Sdf])
                        bottleneck_CS_reset = bottleneck_CS.reset_index()
                        bottleneck_CS_dict = bottleneck_CS_reset.to_dict()
                        bottleneck_CS_dict.pop('index')
                        bottleneck_CS_again = pd.DataFrame(bottleneck_CS_dict)
                        bottleneck_CS_again.to_csv('Bottleneck_CS'+str(df8.loc[0,'Value'])+'.csv',index=False)
                    except:
                        print('Invalid input.')
                    finally:
                        return Account.Menu.access_transactions_balances(self)
                elif caveat == 'N' or caveat == 'n':
                    return Account.Menu.access_transactions_balances(self)
                else:
                    print('Your response cannot be processed.')
                    return Account.Menu.access_transactions_balances(self) 
  
    class Setup_B(Account_Holder):
        
        '''Creates new business account if requested and none already present.'''
        
        def access_transactions_balances(self):
            
            current_date = datetime.datetime.now().strftime("%d %b %Y")
            
            df8 = pd.read_csv('OceansEleven.csv')
            df9 = pd.read_csv('Bottleneck'+str(df8.loc[0,'Value'])+'.csv')
            caveat = ''
            opening_amount = ''          
            business = {'C1':['S BODY (BUSINESS) 11889900 (10-20-30)'],'C2':['Start'],'C3':[0]}
            df10 = pd.DataFrame(business)
            df10_payline = ''
            df10_paylinedf = ''
            df10_extend = ''
            df10_reset = ''
            df10_dict = ''
            df10_again = ''
            bottleneck_B = ''
            bottleneck_Bdf = ''
            bottleneck_CB = ''
            bottleneck_CB_reset = ''
            bottleneck_CB_dict = ''
            bottleneck_CB_again = ''
            
            # Search specifically for pre-existing savings account
            if os.path.isfile('Bottleneck_CS'+str(df8.loc[0,'Value'])+'.csv') == True:
                return Account.Setup_BgivenS.access_transactions_balances(self)
            else:     
                caveat = input('You are about to open a business account.\nFor this account, £0.50 is charged per expense and the monthly charge is £5.00\nalthough the first 12 months have no monthly charges.\nDo you accept? (Y/N) : ')
                if caveat == 'Y' or caveat == 'y':
                    opening_amount = input('Enter opening amount : £')
                    try:
                        eval(opening_amount)
                        df10_payline = {'C1':[current_date],'C2':['Paid in'],'C3':[eval(opening_amount)]}
                        df10_paylinedf = pd.DataFrame(df10_payline)
                        df10_extend = pd.concat([df10,df10_paylinedf])
                        df10_reset = df10_extend.reset_index()
                        df10_dict = df10_reset.to_dict()
                        df10_dict.pop('index')
                        df10_again = pd.DataFrame(df10_dict)
                        df10_again.to_csv('BusinessAccount'+str(df8.loc[0,'Value'])+'.csv',index=False)
                        bottleneck_B = {'C1': ['BUSINESS ACCOUNT (11889900 | 10-20-30)'], 'C2': [df10_again['C3'].sum()]}
                        bottleneck_Bdf = pd.DataFrame(bottleneck_B)
                        bottleneck_CB = pd.concat([df9,bottleneck_Bdf])
                        bottleneck_CB_reset = bottleneck_CB.reset_index()
                        bottleneck_CB_dict = bottleneck_CB_reset.to_dict()
                        bottleneck_CB_dict.pop('index')
                        bottleneck_CB_again = pd.DataFrame(bottleneck_CB_dict)
                        bottleneck_CB_again.to_csv('Bottleneck_CB'+str(df8.loc[0,'Value'])+'.csv',index=False)
                    except:
                        print('Invalid input.')
                    finally:
                        return Account.Menu.access_transactions_balances(self)
                elif caveat == 'N' or caveat == 'n':
                    return Account.Menu.access_transactions_balances(self)
                else:
                    print('Your response cannot be processed.')
                    return Account.Menu.access_transactions_balances(self)  
                                    
    class Setup_SgivenB(Account_Holder):
        
        '''Creates new savings account if requested and none already present and business account already present.'''
        
        def access_transactions_balances(self):
                   
            current_date = datetime.datetime.now().strftime("%d %b %Y")
            
            df12 = pd.read_csv('OceansEleven.csv')
            df13 = pd.read_csv('Bottleneck_CB'+str(df12.loc[0,'Value'])+'.csv')
            opening_amount = ''
            
            savings = {'C1':['S BODY (SAVINGS) 11556677 (10-20-30)'],'C2':['Start'],'C3':[0]}                
            
            bottleneck_savingsline = ''
            bottleneck_savingslinedf = ''
            
            bottleneck_currentline = df13[df13['C1']=='CURRENT ACCOUNT (11223344 | 10-20-30)']
            bottleneck_businessline = df13[df13['C1']=='BUSINESS ACCOUNT (11889900 | 10-20-30)']
            bottleneck_CSB = ''
            bottleneck_CSB_reset = ''
            bottleneck_CSB_dict = ''
            bottleneck_CSB_again = ''
            
            df14 = pd.DataFrame(savings)
            df14_newline = ''
            df14_newlinedf = ''
            df14_extend = ''
            df14_reset = ''
            df14_dict = ''
            df14_again = ''
            
            caveat = input('You are about to open a savings account.\nThis account attracts a once-compounded yearly interest of 2%.\nDo you accept? (Y/N) : ')
            if caveat == 'Y' or caveat == 'y':
                opening_amount = input('Enter opening amount : £')
                try:
                    eval(opening_amount)
                    df14_newline = {'C1':[current_date],'C2':['Paid in'],'C3':[eval(opening_amount)]}
                    df14_newlinedf = pd.DataFrame(df14_newline)
                    df14_extend = pd.concat([df14,df14_newlinedf])
                    df14_reset = df14_extend.reset_index()
                    df14_dict = df14_reset.to_dict()
                    df14_dict.pop('index')
                    df14_again = pd.DataFrame(df14_dict)
                    df14_again.to_csv('SavingsAccount'+str(df12.loc[0,'Value'])+'.csv',index=False)
                    bottleneck_savingsline = {'C1': ['SAVINGS ACCOUNT (11556677 | 10-20-30)'], 'C2': [df14_again['C3'].sum()]}
                    bottleneck_savingslinedf = pd.DataFrame(bottleneck_savingsline)
                    bottleneck_CSB = pd.concat([bottleneck_currentline,bottleneck_savingslinedf,bottleneck_businessline])
                    bottleneck_CSB_reset = bottleneck_CSB.reset_index()
                    bottleneck_CSB_dict = bottleneck_CSB_reset.to_dict()
                    bottleneck_CSB_dict.pop('index')
                    bottleneck_CSB_again = pd.DataFrame(bottleneck_CSB_dict)
                    bottleneck_CSB_again.to_csv('Bottleneck_CSB'+str(df12.loc[0,'Value'])+'.csv',index=False)
                except:
                    print('Invalid input.')
                finally:
                    return Account.Menu.access_transactions_balances(self)
            elif caveat == 'N' or caveat == 'n':
                return Account.Menu.access_transactions_balances(self)
            else:
                print('Your response cannot be processed.')
                return Account.Menu.access_transactions_balances(self)
            
    class Setup_BgivenS(Account_Holder):
        
        '''Creates new business account if requested and none already present and savings account already present.'''
        
        def access_transactions_balances(self):
                   
            current_date = datetime.datetime.now().strftime("%d %b %Y")
            
            df12 = pd.read_csv('OceansEleven.csv')
            df13 = pd.read_csv('Bottleneck_CS'+str(df12.loc[0,'Value'])+'.csv')
            opening_amount = ''
            
            business = {'C1':['S BODY (BUSINESS) 11889900 (10-20-30)'],'C2':['Start'],'C3':[0]}
            
            bottleneck_businessline = ''
            bottleneck_businesslinedf = ''  
            bottleneck_CSB = ''
            
            df14 = pd.DataFrame(business)
            df14_newline = ''
            df14_newlinedf = ''
            df14_extend = ''
            df14_reset = ''
            df14_dict = ''
            df14_again = ''
            bottleneck_CSB_reset = ''
            bottleneck_CSB_dict = ''
            bottleneck_CSB_again = ''
            
            caveat = input('You are about to open a business account.\nFor this account, £0.50 is charged per expense and the monthly charge is £5.00\nalthough the first 12 months have no monthly charges.\nDo you accept? (Y/N) : ')
            if caveat == 'Y' or caveat == 'y':
                opening_amount = input('Enter opening amount : £')
                try:
                    eval(opening_amount)
                    df14_newline = {'C1':[current_date],'C2':['Paid in'],'C3':[eval(opening_amount)]}
                    df14_newlinedf = pd.DataFrame(df14_newline)
                    df14_extend = pd.concat([df14,df14_newlinedf])
                    df14_reset = df14_extend.reset_index()
                    df14_dict = df14_reset.to_dict()
                    df14_dict.pop('index')
                    df14_again = pd.DataFrame(df14_dict)
                    df14_again.to_csv('BusinessAccount'+str(df12.loc[0,'Value'])+'.csv',index=False)
                    bottleneck_businessline = {'C1': ['BUSINESS ACCOUNT (11889900 | 10-20-30)'], 'C2': [df14_again['C3'].sum()]}
                    bottleneck_businesslinedf = pd.DataFrame(bottleneck_businessline)
                    bottleneck_CSB = pd.concat([df13,bottleneck_businesslinedf])
                    bottleneck_CSB_reset = bottleneck_CSB.reset_index()
                    bottleneck_CSB_dict = bottleneck_CSB_reset.to_dict()
                    bottleneck_CSB_dict.pop('index')
                    bottleneck_CSB_again = pd.DataFrame(bottleneck_CSB_dict)
                    bottleneck_CSB_again.to_csv('Bottleneck_CSB'+str(df12.loc[0,'Value'])+'.csv',index=False)
                except:
                    print('Invalid input.')
                finally:
                    return Account.Menu.access_transactions_balances(self)
            elif caveat == 'N' or caveat == 'n':
                return Account.Menu.access_transactions_balances(self)
            else:
                print('Your response cannot be processed.')
                return Account.Menu.access_transactions_balances(self)
    
    class MergeAndDoubleRemover(Account_Holder):
        
        '''For the unlikely situation that the three accounts are not all linked to the same person
        where the three accounts exists for that person.'''
        
        def access_transactions_balances(self):
            
            df16 = pd.read_csv('OceansEleven.csv')
            df17 = pd.read_csv('CurrentAccount'+str(df16.loc[0,'Value'])+'.csv')
            df18 = pd.read_csv('Bottleneck_CS'+str(df16.loc[0,'Value'])+'.csv')
            df19 = pd.read_csv('Bottleneck_CB'+str(df16.loc[0,'Value'])+'.csv')
            
            bottleneck_currentline = {'C1': ['CURRENT ACCOUNT (11223344 | 10-20-30)'], 'C2': [df17['C3'].sum()]}        
            bottleneck_savingsline = df18[df18['C1']=='SAVINGS ACCOUNT (11556677 | 10-20-30)']
            bottleneck_businessline = df19[df19['C1']=='BUSINESS ACCOUNT (11889900 | 10-20-30)']
            
            df20 = pd.DataFrame(bottleneck_currentline)
            bottleneck_CSB = pd.concat([df20,bottleneck_savingsline,bottleneck_businessline])
            bottleneck_CSB_reset = bottleneck_CSB.reset_index()
            bottleneck_CSB_dict = bottleneck_CSB_reset.to_dict()
            bottleneck_CSB_dict.pop('index')
            bottleneck_CSB_again = pd.DataFrame(bottleneck_CSB_dict)
            bottleneck_CSB_again.to_csv('Bottleneck_CSB'+str(df16.loc[0,'Value'])+'.csv',index=False)           
            bottleneck_CSB_again.to_csv('Bottleneck_CSB'+str(df16.loc[0,'Value'])+'.csv',index=False)
            os.remove('Bottleneck_CS'+str(df16.loc[0,'Value'])+'.csv')
            os.remove('Bottleneck_CB'+str(df16.loc[0,'Value'])+'.csv')
            
            return Account.Menu_CSB.access_transactions_balances(self)
        
    class Menu_CS(Account_Holder):
        
        '''Menu if person has only current (checking) and savings accounts.'''
        
        def access_transactions_balances(self):
            
            current_date = datetime.datetime.now().strftime("%d %b %Y")
            a = datetime.datetime.strptime(current_date, "%d %b %Y")                
            
            df5 = pd.read_csv('OceansEleven.csv')
            df6 = pd.read_csv('Bottleneck_CS'+str(df5.loc[0,'Value'])+'.csv')
            df6_cust_view = df6
            df6_cust_view2 = df6
            df6_cust_view3 = df6
            df7_c = pd.read_csv('CurrentAccount'+str(df5.loc[0,'Value'])+'.csv')
            df7_c_list = list(zip(df7_c['C1'],df7_c['C2'],df7_c['C3']))                
            df7_s = pd.read_csv('SavingsAccount'+str(df5.loc[0,'Value'])+'.csv')
            df7_s_list = list(zip(df7_s['C1'],df7_s['C2'],df7_s['C3']))
            
            first_date = df7_s_list[1][0]
            b = datetime.datetime.strptime(first_date, "%d %b %Y")
            d = a - b
            
            # df6_cust_view arithmetic -> prepares list for savings account balance, Option 1
            a_dailysavingsbalance = (df6.loc[1,'C2'])/d.days
            rate = 0.02
            daily_c_interest = a_dailysavingsbalance * rate
            interest_4df6_c_v = daily_c_interest * d.days
            df6_cust_view.loc[1,'C2'] = df6.loc[1,'C2'] + interest_4df6_c_v               
            df6_cust_view_list = list(zip(df6_cust_view['C1'],df6_cust_view['C2']))   
            
            # df6_cust_view2 arithmetic -> prepares list for savings account balance, Option 2
            total_4df6_c_v2 = (df7_s.loc[1,'C3'])*(1+rate)**(d.days/365)
            df6_cust_view2.loc[1,'C2'] = total_4df6_c_v2
            df6_cust_view2_list = list(zip(df6_cust_view2['C1'],df6_cust_view2['C2']))
            interest_4df6_c_v2 = df6_cust_view2.loc[1,'C2'] - df7_s.loc[1,'C3']
            
            # df6_cust_view3-related -> prepares list for savings account balance, Option 3
            df6_cust_view3.loc[1,'C2'] = df6_cust_view.loc[1,'C2']
            df6_cust_view3_list = list(zip(df6_cust_view3['C1'],df6_cust_view3['C2']))
            
            # df7_s_c_v arithmetic -> prepares list for savings account transactions, Transactions 1
            df7_s_c_v_savingsline = {'C1':[current_date],'C2':['Total interest'],'C3':[interest_4df6_c_v]}
            df7_s_c_v_savingslinedf = pd.DataFrame(df7_s_c_v_savingsline)
            df7_s_c_v_extend = pd.concat([df7_s,df7_s_c_v_savingslinedf])
            df7_s_c_v_extendlist = list(zip(df7_s_c_v_extend['C1'],df7_s_c_v_extend['C2'],df7_s_c_v_extend['C3']))
            
            # df7_s_c_v2 arithmetic -> prepares list for savings account transactions, Transactions 2
            df7_s_c_v2_savingsline = {'C1':[current_date], 'C2': ['Total interest'], 'C3': [interest_4df6_c_v2]}
            df7_s_c_v2_savingslinedf = pd.DataFrame(df7_s_c_v2_savingsline)
            df7_s_c_v2_extend = pd.concat([df7_s,df7_s_c_v2_savingslinedf])
            df7_s_c_v2_extendlist = list(zip(df7_s_c_v2_extend['C1'],df7_s_c_v2_extend['C2'],df7_s_c_v2_extend['C3']))
            
            # df7_s_c_v3 arithmetic -> prepares list for savings account transactions, Transactions 3
            df7_s_c_v3_savingsline = {'C1':[current_date], 'C2': ['Contact bank for interest review'], 'C3': [0]}
            df7_s_c_v3_savingslinedf = pd.DataFrame(df7_s_c_v3_savingsline)
            df7_s_c_v3_extend = pd.concat([df7_s,df7_s_c_v3_savingslinedf])
            df7_s_c_v3_extendlist = list(zip(df7_s_c_v3_extend['C1'],df7_s_c_v3_extend['C2'],df7_s_c_v3_extend['C3']))                
            
            # Print current and savings account balances
            if d.days <= 365 and len(df7_s_list) > 2:
                # Uses option 1
                for i in df6_cust_view_list:
                    print(i[0],'£'+"%.2f"%(i[1]))
                print('Note: The savings balance will stay fixed until review a year from opening savings account unless you: \n(a) Add further funds or \n(b) Withdraw further funds')
            elif (d.days > 365 and len(df7_s_list) == 2) or (d.days <= 365 and len(df7_s_list) == 2):
                # Uses option 2
                for i in df6_cust_view2_list:
                    print(i[0],'£'+"%.2f"%(i[1]))
            else:
                # Uses option 3
                for i in df6_cust_view3_list:
                    print(i[0],'£'+"%.2f"%(i[1]))
                print('YOUR SAVINGS ACCOUNT IS DUE FOR REVIEW, CONTACT BANK.')

            # Selecting type of transaction
            which_account = ''
            transaction_choice = input('Select type of transaction\n1. Deposit or withdraw money\n2. View transactions\n3. Transfer between accounts\n4. Return to main menu\n5. Exit : ')
            if transaction_choice == '1':
                which_account = input('Which account? (C/S): ')
                if which_account == 'C' or which_account == 'c':
                    return Account.CurrentAccount.access_transactions_balances(self)
                elif which_account == 'S' or which_account == 's':
                    return Account.SavingsAccount.access_transactions_balances(self)
                else:
                    print('Your response cannot be processed.')
                    return Account.Menu_CS.access_transactions_balances(self)
            elif transaction_choice == '2':
                which_account = input('Which account? (C/S)')
                if which_account == 'C' or which_account == 'c':
                    for i in df7_c_list:                
                        if i[2] >= 0:
                            print(i[0],i[1],' £'+"%.2f"%(i[2]))
                        elif i[2] < 0:
                            print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                    return Account.Menu_CS.access_transactions_balances(self)
                elif which_account == 'S' or which_account == 's':
                    if d.days <= 365 and len(df7_s_list) > 2:
                        # Uses transactions 1
                        for i in df7_s_c_v_extendlist:
                            if i[2] >= 0:
                                print(i[0],i[1],' £'+"%.2f"%(i[2]))
                            elif i[2] < 0:
                                print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                        return Account.Menu_CS.access_transactions_balances(self)
                    elif (d.days > 365 and len(df7_s_list) == 2) or (d.days <= 365 and len(df7_s_list) == 2):
                        # Uses transactions 2
                        for i in df7_s_c_v2_extendlist:
                            if i[2] >= 0:
                                print(i[0],i[1],' £'+"%.2f"%(i[2]))
                            elif i[2] < 0:
                                print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                        return Account.Menu_CS.access_transactions_balances(self)                                 
                    else:
                        # Uses transactions 3
                        for i in df7_s_c_v3_extendlist:
                            if i[2] >= 0:
                                print(i[0],i[1],' £'+"%.2f"%(i[2]))
                            elif i[2] < 0:
                                print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                        return Account.Menu_CS.access_transactions_balances(self)
                else:
                    print('Your response cannot be processed.')
                    return Account.Menu_CS.access_transactions_balances(self)
            elif transaction_choice == '3':
                return Account.Transfer_CS.access_transactions_balances(self)
            elif transaction_choice == '4':
                return Account.Menu.access_transactions_balances(self)
            elif transaction_choice == '5':
                sys.exit()
            else:
                print('Your response cannot be processed.')
                return Account.Menu.access_transactions_balances(self)
            
    class Menu_CB(Account_Holder):
        
        '''Menu if person has only current (checking) and business accounts.'''
        
        def access_transactions_balances(self):
                            
            current_date = datetime.datetime.now().strftime("%d %b %Y")
            a = datetime.datetime.strptime(current_date, "%d %b %Y")                
            
            df5 = pd.read_csv('OceansEleven.csv')
            df6 = pd.read_csv('Bottleneck_CB'+str(df5.loc[0,'Value'])+'.csv')
            df6_cust_view = df6
            df6_cust_view2 = df6
            df7_c = pd.read_csv('CurrentAccount'+str(df5.loc[0,'Value'])+'.csv')
            df7_c_list = list(zip(df7_c['C1'],df7_c['C2'],df7_c['C3']))
            df7_b = pd.read_csv('BusinessAccount'+str(df5.loc[0,'Value'])+'.csv')
            df7_b_list = list(zip(df7_b['C1'],df7_b['C2'],df7_b['C3']))
            
            first_date = df7_b_list[1][0]
            c = datetime.datetime.strptime(first_date, "%d %b %Y")
            e = a - c
                     
            # df6_cust_view -> includes total money-out fees into business balance calculation, Option 1
            expense_fee = 0.5
            df6_cust_view_feelist = []
            for i in df7_b_list:
                if i[2] < 0:
                    df6_cust_view_feelist.append(i[2])
            df6_cust_view.loc[1,'C2'] = df6.loc[1,'C2'] - expense_fee*len(df6_cust_view_feelist)
            df6_cust_view_list = list(zip(df6_cust_view['C1'],df6_cust_view['C2']))
            
            # df6_cust_view2 -> includes total money-out and applicable monthly fees into business balance calculation, Option 2
            monthly_charge = 5
            df7_b_monthly = e.days/30 - 12  # Declaring this df7_b prefixed variable here is necessary!
            df6_cust_view2_feelist = []
            for i in df7_b_list:
                if i[2] < 0:
                    df6_cust_view2_feelist.append(i[2])  
            df6_cust_view2.loc[1,'C2'] = df6.loc[1,'C2'] - expense_fee*len(df6_cust_view2_feelist) - monthly_charge*df7_b_monthly
            df6_cust_view2_list = list(zip(df6_cust_view2['C1'],df6_cust_view2['C2']))

            # df7_b expenses charge arithmetic -> includes total money-out fees into list for business account transactions
            df7_b_expensesline = {'C1':[current_date], 'C2': ['Expense fees'], 'C3': [-expense_fee*len(df6_cust_view_feelist)]}
            df7_b_expenseslinedf = pd.DataFrame(df7_b_expensesline)
            df7_b_extend = pd.concat([df7_b,df7_b_expenseslinedf])
            df7_b_extendlist = list(zip(df7_b_extend['C1'],df7_b_extend['C2'],df7_b_extend['C3']))
            
            # df7_b monthly charge arithmetic, together with df7_b_expensesline -> includes total monthly fees into list for business account transactions
            # Note: df7_b_monthly (= e.days/30 - 12) has already been declared
            df7_b_monthlyline = {'C1':[current_date], 'C2': ['Total monthly charges'], 'C3': [-monthly_charge*df7_b_monthly]}
            df7_b_monthlylinedf = pd.DataFrame(df7_b_monthlyline)
            df7_b_extend2 = pd.concat([df7_b,df7_b_expenseslinedf,df7_b_monthlylinedf])
            df7_b_extend2list = list(zip(df7_b_extend2['C1'],df7_b_extend2['C2'],df7_b_extend2['C3']))
            
            # Print current and business account balances
            if e.days <= 365:
                # Uses option 1 for business balance
                for i in df6_cust_view_list:
                    print(i[0],'£'+"%.2f"%(i[1]))
            elif e.days > 365:
                # Uses option 2 for business balance
                for i in df6_cust_view2_list:
                    print(i[0],'£'+"%.2f"%(i[1]))              
                                    
            # Selecting type of transaction
            which_account = ''
            transaction_choice = input('Select type of transaction\n1. Deposit or withdraw money\n2. View transactions\n3. Transfer between accounts\n4. Return to main menu\n5. Exit : ')
            if transaction_choice == '1':
                which_account = input('Which account? (C/B): ')
                if which_account == 'C' or which_account == 'c':
                    return Account.CurrentAccount.access_transactions_balances(self)
                elif which_account == 'B' or which_account == 'b':
                    return Account.BusinessAccount.access_transactions_balances(self)
                else:
                    print('Your response cannot be processed.')
                    return Account.Menu_CB.access_transactions_balances(self)
            elif transaction_choice == '2':
                which_account = input('Which account? (C/B): ')
                if which_account == 'C' or which_account == 'c':
                    for i in df7_c_list:             
                        if i[2] >= 0:
                            print(i[0],i[1],' £'+"%.2f"%(i[2]))
                        elif i[2] < 0:
                            print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                    return Account.Menu_CB.access_transactions_balances(self)
                elif which_account == 'B' or which_account == 'b':
                    if e.days <= 365:
                        # Only includes money-out fees
                        for i in df7_b_extendlist:               
                            if i[2] >= 0:
                                print(i[0],i[1],' £'+"%.2f"%(i[2]))
                            elif i[2] < 0:
                                print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                        return Account.Menu_CB.access_transactions_balances(self)
                    elif e.days > 365:
                        # Includes both money-out and applicable monthly fees
                        for i in df7_b_extend2list:                 
                            if i[2] >= 0:
                                print(i[0],i[1],' £'+"%.2f"%(i[2]))
                            elif i[2] < 0:
                                print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                        return Account.Menu_CB.access_transactions_balances(self)
                else:
                    print('Your response cannot be processed.')
                    return Account.Menu_CB.access_transactions_balances(self)
            elif transaction_choice == '3':
                return Account.Transfer_CB.access_transactions_balances(self)
            elif transaction_choice == '4':
                return Account.Menu.access_transactions_balances(self)
            elif transaction_choice == '5':
                sys.exit()
            else:
                print('Your response cannot be processed.')
                return Account.Menu_CB.access_transactions_balances(self)
            
    class Menu_CSB(Account_Holder):
        
        '''Menu if person has current (checking), savings, and business accounts.'''
        
        def access_transactions_balances(self):
            
            current_date = datetime.datetime.now().strftime("%d %b %Y")
            a = datetime.datetime.strptime(current_date, "%d %b %Y")                
            
            df5 = pd.read_csv('OceansEleven.csv')
            df6 = pd.read_csv('Bottleneck_CSB'+str(df5.loc[0,'Value'])+'.csv')
            df6_cust_viewS = df6
            df6_cust_view2S = df6
            df6_cust_view3S = df6
            df6_cust_viewB = df6
            df6_cust_view2B = df6
            df7_c = pd.read_csv('CurrentAccount'+str(df5.loc[0,'Value'])+'.csv')
            df7_c_list = list(zip(df7_c['C1'],df7_c['C2'],df7_c['C3']))                
            df7_s = pd.read_csv('SavingsAccount'+str(df5.loc[0,'Value'])+'.csv')
            df7_s_list = list(zip(df7_s['C1'],df7_s['C2'],df7_s['C3']))
            df7_b = pd.read_csv('BusinessAccount'+str(df5.loc[0,'Value'])+'.csv')
            df7_b_list = list(zip(df7_b['C1'],df7_b['C2'],df7_b['C3']))
            
            first_dateS = df7_s_list[1][0]
            first_dateB = df7_b_list[1][0]
            b = datetime.datetime.strptime(first_dateS, "%d %b %Y")
            c = datetime.datetime.strptime(first_dateB, "%d %b %Y")
            d = a - b
            e = a - c
            
            # df6 -> provides dataframe row for current account balance
            CurAcctLine = df6[df6['C1']=='CURRENT ACCOUNT (11223344 | 10-20-30)']
            
            # df6_cust_viewS arithmetic -> prepares dataframe row for savings account balance, Option 1
            a_dailysavingsbalance = (df6.loc[1,'C2'])/d.days
            rate = 0.02
            daily_c_interest = a_dailysavingsbalance * rate
            interest_4df6_c_v = daily_c_interest * d.days
            df6_cust_viewS.loc[1,'C2'] = df6.loc[1,'C2'] + interest_4df6_c_v               
            SavAcctLine = df6_cust_viewS[df6_cust_viewS['C1']=='SAVINGS ACCOUNT (11556677 | 10-20-30)']
            
            # df6_cust_view2S arithmetic -> prepares dataframe row  for savings account balance, Option 2
            total_4df6_c_v2S = (df7_s.loc[1,'C3'])*(1+rate)**(d.days/365)
            df6_cust_view2S.loc[1,'C2'] = total_4df6_c_v2S
            SavAcctLine2 = df6_cust_view2S[df6_cust_view2S['C1']=='SAVINGS ACCOUNT (11556677 | 10-20-30)']
            interest_4df6_c_v2 = df6_cust_view2S.loc[1,'C2'] - df7_s.loc[1,'C3']
            
            # df6_cust_view3S-related -> prepares dataframe row for savings account balance, Option 3
            df6_cust_view3S.loc[1,'C2'] = df6_cust_viewS.loc[1,'C2']
            SavAcctLine3 = df6_cust_view3S[df6_cust_view3S['C1']=='SAVINGS ACCOUNT (11556677 | 10-20-30)']
            
            # df6_cust_viewB -> includes total money-out fees into dataframe row for business balance calculation, Option 1
            expense_fee = 0.5
            df6_cust_viewB_feelist = []
            for i in df7_b_list:
                if i[2] < 0:
                    df6_cust_viewB_feelist.append(i[2]) 
            df6_cust_viewB.loc[2,'C2'] = df6.loc[2,'C2'] - expense_fee*len(df6_cust_viewB_feelist)
            BusAcctLine = df6_cust_viewB[df6_cust_viewB['C1']=='BUSINESS ACCOUNT (11889900 | 10-20-30)']
            
            # df6_cust_view2B -> includes total money-out and applicable monthly fees into dataframe row for business balance calculation, Option 2
            monthly_charge = 5
            df7_b_monthly = e.days/30 - 12 # Declaring this df7_b prefixed variable here is necessary!
            df6_cust_view2B_feelist = []
            for i in df7_b_list:
                if i[2] < 0:
                    df6_cust_view2B_feelist.append(i[2]) 
            df6_cust_view2B.loc[2,'C2'] = df6.loc[2,'C2'] - expense_fee*len(df6_cust_view2B_feelist) - monthly_charge*df7_b_monthly
            BusAcctLine2 = df6_cust_view2B[df6_cust_view2B['C1']=='BUSINESS ACCOUNT (11889900 | 10-20-30)']
            
            # Create new dataframe from newly created dataframe rows for balances for all three account types
            df6_combo = pd.concat([CurAcctLine,SavAcctLine,BusAcctLine]) # Savings, option 1; Business, Option 1
            df6_combo2 = pd.concat([CurAcctLine,SavAcctLine2,BusAcctLine]) # Savings, option 2; Business, option 1 
            df6_combo3 = pd.concat([CurAcctLine,SavAcctLine3,BusAcctLine]) # Savings, option 3; Business, option 1
            df6_combo4 = pd.concat([CurAcctLine,SavAcctLine,BusAcctLine2]) # Savings, option 1; Business, option 2
            df6_combo5 = pd.concat([CurAcctLine,SavAcctLine2,BusAcctLine2]) # Savings, option 2; Business, option 2
            df6_combo6 = pd.concat([CurAcctLine,SavAcctLine3,BusAcctLine2]) # Savings, option 3; Business, option 2
            
            # Create lists from above new dataframes
            df6_combo_list = list(zip(df6_combo['C1'],df6_combo['C2']))
            df6_combo2_list = list(zip(df6_combo2['C1'],df6_combo2['C2']))
            df6_combo3_list = list(zip(df6_combo3['C1'],df6_combo3['C2']))
            df6_combo4_list = list(zip(df6_combo4['C1'],df6_combo4['C2']))
            df6_combo5_list = list(zip(df6_combo5['C1'],df6_combo5['C2']))
            df6_combo6_list = list(zip(df6_combo6['C1'],df6_combo6['C2']))
            
            # df7_s_c_v arithmetic -> prepares list for savings account transactions, Transactions 1
            df7_s_c_v_savingsline = {'C1':[current_date], 'C2': ['Total interest'], 'C3': [interest_4df6_c_v]}
            df7_s_c_v_savingslinedf = pd.DataFrame(df7_s_c_v_savingsline)
            df7_s_c_v_extend = pd.concat([df7_s,df7_s_c_v_savingslinedf])
            df7_s_c_v_extendlist = list(zip(df7_s_c_v_extend['C1'],df7_s_c_v_extend['C2'],df7_s_c_v_extend['C3']))
            
            # df7_s_c_v2 arithmetic -> prepares list for savings account transactions, Transactions 2
            df7_s_c_v2_savingsline = {'C1':[current_date], 'C2': ['Total interest'], 'C3': [interest_4df6_c_v2]}
            df7_s_c_v2_savingslinedf = pd.DataFrame(df7_s_c_v2_savingsline)
            df7_s_c_v2_extend = pd.concat([df7_s,df7_s_c_v2_savingslinedf])
            df7_s_c_v2_extendlist = list(zip(df7_s_c_v2_extend['C1'],df7_s_c_v2_extend['C2'],df7_s_c_v2_extend['C3']))
            
            # df7_s_c_v3 arithmetic -> prepares list for savings account transactions, Transactions 3
            df7_s_c_v3_savingsline = {'C1':[current_date], 'C2': ['Contact bank for interest review'], 'C3': [0]}
            df7_s_c_v3_savingslinedf = pd.DataFrame(df7_s_c_v3_savingsline)
            df7_s_c_v3_extend = pd.concat([df7_s,df7_s_c_v3_savingslinedf])
            df7_s_c_v3_extendlist = list(zip(df7_s_c_v3_extend['C1'],df7_s_c_v3_extend['C2'],df7_s_c_v3_extend['C3']))                
                
            # df7_b expenses charge arithmetic -> includes total money-out fees into list for business account transactions
            df7_b_expensesline = {'C1':[current_date], 'C2': ['Expense fees'], 'C3': [-expense_fee*len(df6_cust_viewB_feelist)]}
            df7_b_expenseslinedf = pd.DataFrame(df7_b_expensesline)
            df7_b_extend = pd.concat([df7_b,df7_b_expenseslinedf])
            df7_b_extendlist = list(zip(df7_b_extend['C1'],df7_b_extend['C2'],df7_b_extend['C3']))
            
            # df7_b monthly charge arithmetic, together with df7_b_expensesline -> includes total monthly fees into list for business account transactions
            # Note: df7_b_monthly (= e.days/30 - 12) has already been declared
            df7_b_monthlyline = {'C1':[current_date], 'C2': ['Total monthly charges'], 'C3': [-monthly_charge*df7_b_monthly]}
            df7_b_monthlylinedf = pd.DataFrame(df7_b_monthlyline)
            df7_b_extend2 = pd.concat([df7_b,df7_b_expenseslinedf,df7_b_monthlylinedf])
            df7_b_extend2list = list(zip(df7_b_extend2['C1'],df7_b_extend2['C2'],df7_b_extend2['C3']))                                

            # Print current, savings and business account balances
            if (d.days <= 365) and (len(df7_s_list) > 2) and (e.days <= 365):
                # Uses option 1 for savings and option 1 for business
                for i in df6_combo_list:
                    print(i[0],'£'+"%.2f"%(i[1]))
                print('Note: This new savings balance will stay fixed until review a year from opening savings account unless you: \n(a) Add further funds or \n(b) Withdraw further funds')
            elif (d.days <= 365) and (len(df7_s_list) == 2) and (e.days <= 365):
                # Uses option 2 for savings and option 1 for business
                for i in df6_combo2_list:
                    print(i[0],'£'+"%.2f"%(i[1]))
            elif (d.days > 365) and (len(df7_s_list) == 2) and (e.days <= 365):
                # Uses option 2 for savings and option 1 for business
                for i in df6_combo2_list:
                    print(i[0],'£'+"%.2f"%(eval(i[1])))
            elif (d.days > 365) and (len(df7_s_list) > 2) and (e.days <= 365):
                # Uses option 3 for savings and option 1 for business
                for i in df6_combo3_list:
                    print(i[0],'£'+"%.2f"%(i[1]))
            elif d.days <= 365 and (len(df7_s_list) > 2) and (e.days > 365):
                # Uses option 1 for savings and option 2 for business
                for i in df6_combo4_list:
                    print(i[0],'£'+"%.2f"%(i[1]))
                print('Note: This new savings balance will stay fixed until review a year from opening savings account unless you: \n(a) Add further funds or \n(b) Withdraw further funds')
            elif (d.days <= 365) and (len(df7_s_list) == 2) and (e.days > 365):
                # Uses option 2 for savings and option 2 for business
                for i in df6_combo5_list:
                    print(i[0],'£'+"%.2f"%(i[1]))
            elif (d.days > 365) and (len(df7_s_list) == 2) and (e.days > 365):
                # Uses option 2 for savings and option 2 for business
                for i in df6_combo5_list:
                    print(i[0],'£'+"%.2f"%(i[1]))
            elif (d.days > 365) and (len(df7_s_list) > 2) and (e.days > 365):
                # Uses option 3 for savings and option 2 for business
                for i in df6_combo6_list:
                    print(i[0],'£'+"%.2f"%(i[1]))
                print('YOUR SAVINGS ACCOUNT IS DUE FOR REVIEW, CONTACT BANK.')
                    
            # Selecting type of transaction
            which_account = ''
            transaction_choice = input('Select type of transaction\n1. Deposit or withdraw money\n2. View transactions\n3. Transfer between accounts\n4. Return to main menu\n5. Exit : ')
            if transaction_choice == '1':
                which_account = input('Which account? (C/S/B): ')
                if which_account == 'C' or which_account == 'c':
                    return Account.CurrentAccount.access_transactions_balances(self)
                elif which_account == 'S' or which_account == 's':
                    return Account.SavingsAccount.access_transactions_balances(self)
                elif which_account == 'B' or which_account == 'b':
                    return Account.BusinessAccount.access_transactions_balances(self)                    
                else:
                    print('Your response cannot be processed.')
                    return Account.Menu_CSB.access_transactions_balances(self)
            elif transaction_choice == '2':
                which_account = input('Which account? (C/S/B): ')
                if which_account == 'C' or which_account == 'c':
                    for i in df7_c_list:
                        if i[2] >= 0:
                            print(i[0],i[1],' £'+"%.2f"%(i[2]))
                        elif i[2] < 0:
                            print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                    return Account.Menu_CSB.access_transactions_balances(self)                          
                elif which_account == 'S' or which_account == 's':
                    if d.days <= 365 and len(df7_s_list) > 2:
                        # Uses savings, option 1
                        for i in df7_s_c_v_extendlist:
                            if i[2] >= 0:
                                print(i[0],i[1],' £'+"%.2f"%(i[2]))
                            elif i[2] < 0:
                                print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                        return Account.Menu_CSB.access_transactions_balances(self)                                     
                    elif (d.days > 365 and len(df7_s_list) == 2) or (d.days <= 365 and len(df7_s_list) == 2):
                        # Uses savings, option 2
                        for i in df7_s_c_v2_extendlist:               
                            if i[2] >= 0:
                                print(i[0],i[1],' £'+"%.2f"%(i[2]))
                            elif i[2] < 0:
                                print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                        return Account.Menu_CSB.access_transactions_balances(self) 
                    else:
                        # Uses savings, option 3
                        for i in df7_s_c_v3_extendlist:
                            if i[2] >= 0:
                                print(i[0],i[1],' £'+"%.2f"%(i[2]))
                            elif i[2] < 0:
                                print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                        return Account.Menu_CSB.access_transactions_balances(self) 
                elif which_account == 'B' or which_account == 'b':
                    if e.days <= 365:
                        # Only includes money-out fees
                        for i in df7_b_extendlist:
                            if i[2] >= 0:
                                print(i[0],i[1],' £'+"%.2f"%(i[2]))
                            elif i[2] < 0:
                                print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                        return Account.Menu_CSB.access_transactions_balances(self)                                
                    elif e.days > 365:
                        # Includes both money-out and applicable monthly fees
                        for i in df7_b_extend2list:
                            if i[2] >= 0:
                                print(i[0],i[1],' £'+"%.2f"%(i[2]))
                            elif i[2] < 0:
                                print(i[0],i[1],'-£'+"%.2f"%(i[2]*-1))
                        return Account.Menu_CSB.access_transactions_balances(self) 
                else:
                    print('Your response cannot be processed.')
                    return Account.Menu_CSB.access_transactions_balances(self)
            elif transaction_choice == '3':
                return Account.Transfer_CSB.access_transactions_balances(self)
            elif transaction_choice == '4':
                Account.Menu.access_transactions_balances(self)
            elif transaction_choice == '5':
                sys.exit()
            else:
                print('Your response cannot be processed.')
                return Account.Menu_CSB.access_transactions_balances(self)
            
    class CurrentAccount(Account_Holder):
        
        '''Transactions for current (checking) account (except transfers to/from savings or business accounts)'''
        
        def access_transactions_balances(self):
            
            current_date = datetime.datetime.now().strftime("%d %b %Y")             
            
            df21 = pd.read_csv('OceansEleven.csv')
            df22 = ''
            df23 = pd.read_csv('CurrentAccount'+str(df21.loc[0,'Value'])+'.csv')
            df23_payline = ''
            df23_paylinedf = ''
            df23_extend = ''
            df23_reset = ''
            df23_dict = ''
            df23_extend_again =''
 
            enter_amount = ''
            deposit_or_withdraw = input('Choose: \n1. Deposit \n2. Withdraw\n3. Return to main menu\n4. Exit')
            if deposit_or_withdraw == '1':
                enter_amount = input('Enter amount : £')
                try:
                    eval(enter_amount)
                    if os.path.isfile('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv') == True:
                        df22 = pd.read_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv')
                        df23_payline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                        df23_paylinedf = pd.DataFrame(df23_payline)
                        df23_extend = pd.concat([df23,df23_paylinedf])
                        df23_reset = df23_extend.reset_index()
                        df23_dict = df23_reset.to_dict()
                        df23_dict.pop('index')
                        df23_extend_again = pd.DataFrame(df23_dict)             
                        df22.loc[0,'C2'] = df23_extend_again['C3'].sum()
                        df22.to_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        df23_extend_again.to_csv('CurrentAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                    elif os.path.isfile('Bottleneck_CS'+str(df21.loc[0,'Value'])+'.csv') == True:
                        df22 = pd.read_csv('Bottleneck_CS'+str(df21.loc[0,'Value'])+'.csv')
                        df23_payline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                        df23_paylinedf = pd.DataFrame(df23_payline)
                        df23_extend = pd.concat([df23,df23_paylinedf])
                        df23_reset = df23_extend.reset_index()
                        df23_dict = df23_reset.to_dict()
                        df23_dict.pop('index')
                        df23_extend_again = pd.DataFrame(df23_dict)             
                        df22.loc[0,'C2'] = df23_extend_again['C3'].sum()
                        df22.to_csv('Bottleneck_CS'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        df23_extend_again.to_csv('CurrentAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                    elif os.path.isfile('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv') == True:
                        df22 = pd.read_csv('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv')
                        df23_payline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                        df23_paylinedf = pd.DataFrame(df23_payline)
                        df23_extend = pd.concat([df23,df23_paylinedf])
                        df23_reset = df23_extend.reset_index()
                        df23_dict = df23_reset.to_dict()
                        df23_dict.pop('index')
                        df23_extend_again = pd.DataFrame(df23_dict)             
                        df22.loc[0,'C2'] = df23_extend_again['C3'].sum()
                        df22.to_csv('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        df23_extend_again.to_csv('CurrentAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                    elif os.path.isfile('Bottleneck'+str(df21.loc[0,'Value'])+'.csv') == True:
                        df22 = pd.read_csv('Bottleneck'+str(df21.loc[0,'Value'])+'.csv')
                        df23_payline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                        df23_paylinedf = pd.DataFrame(df23_payline)
                        df23_extend = pd.concat([df23,df23_paylinedf])
                        df23_reset = df23_extend.reset_index()
                        df23_dict = df23_reset.to_dict()
                        df23_dict.pop('index')
                        df23_extend_again = pd.DataFrame(df23_dict)             
                        df22.loc[0,'C2'] = df23_extend_again['C3'].sum()
                        df22.to_csv('Bottleneck'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        df23_extend_again.to_csv('CurrentAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                except:
                    print('Invalid input')
                finally:
                    return Account.CurrentAccount.access_transactions_balances(self)
            elif deposit_or_withdraw == '2':
                enter_amount = input('Enter amount : £')                        
                try:
                    eval(enter_amount)
                    if eval(enter_amount) > df23['C3'].sum():
                        print('Insufficient funds')
                    elif eval(enter_amount) <= df23['C3'].sum():
                        if os.path.isfile('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv') == True:
                            df22 = pd.read_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv')
                            df23_payline = {'C1':[current_date], 'C2': ['Paid out'], 'C3': [eval('-'+enter_amount)]}
                            df23_paylinedf = pd.DataFrame(df23_payline)
                            df23_extend = pd.concat([df23,df23_paylinedf])
                            df23_reset = df23_extend.reset_index()
                            df23_dict = df23_reset.to_dict()
                            df23_dict.pop('index')
                            df23_extend_again = pd.DataFrame(df23_dict)             
                            df22.loc[0,'C2'] = df23_extend_again['C3'].sum()
                            df22.to_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv',index=False)
                            df23_extend_again.to_csv('CurrentAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        elif os.path.isfile('Bottleneck_CS'+str(df21.loc[0,'Value'])+'.csv') == True:
                            df22 = pd.read_csv('Bottleneck_CS'+str(df21.loc[0,'Value'])+'.csv')
                            df23_payline = {'C1':[current_date], 'C2': ['Paid out'], 'C3': [eval('-'+enter_amount)]}
                            df23_paylinedf = pd.DataFrame(df23_payline)
                            df23_extend = pd.concat([df23,df23_paylinedf])
                            df23_reset = df23_extend.reset_index()
                            df23_dict = df23_reset.to_dict()
                            df23_dict.pop('index')
                            df23_extend_again = pd.DataFrame(df23_dict)             
                            df22.loc[0,'C2'] = df23_extend_again['C3'].sum()
                            df22.to_csv('Bottleneck_CS'+str(df21.loc[0,'Value'])+'.csv',index=False)
                            df23_extend_again.to_csv('CurrentAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        elif os.path.isfile('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv') == True:
                            df22 = pd.read_csv('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv')
                            df23_payline = {'C1':[current_date], 'C2': ['Paid out'], 'C3': [eval('-'+enter_amount)]}
                            df23_paylinedf = pd.DataFrame(df23_payline)
                            df23_extend = pd.concat([df23,df23_paylinedf])
                            df23_reset = df23_extend.reset_index()
                            df23_dict = df23_reset.to_dict()
                            df23_dict.pop('index')
                            df23_extend_again = pd.DataFrame(df23_dict)             
                            df22.loc[0,'C2'] = df23_extend_again['C3'].sum()
                            df22.to_csv('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv',index=False)
                            df23_extend_again.to_csv('CurrentAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        elif os.path.isfile('Bottleneck'+str(df21.loc[0,'Value'])+'.csv') == True:
                            df22 = pd.read_csv('Bottleneck'+str(df21.loc[0,'Value'])+'.csv')
                            df23_payline = {'C1':[current_date], 'C2': ['Paid out'], 'C3': [eval('-'+enter_amount)]}
                            df23_paylinedf = pd.DataFrame(df23_payline)
                            df23_extend = pd.concat([df23,df23_paylinedf])
                            df23_reset = df23_extend.reset_index()
                            df23_dict = df23_reset.to_dict()
                            df23_dict.pop('index')
                            df23_extend_again = pd.DataFrame(df23_dict)             
                            df22.loc[0,'C2'] = df23_extend_again['C3'].sum()
                            df22.to_csv('Bottleneck'+str(df21.loc[0,'Value'])+'.csv',index=False)
                            df23_extend_again.to_csv('CurrentAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                except:
                    print('Invalid input')
                finally:
                    return Account.CurrentAccount.access_transactions_balances(self)
            elif deposit_or_withdraw == '3':
                return Account.Menu.access_transactions_balances(self)
            elif deposit_or_withdraw == '4':
                sys.exit()
            else:
                print('Your response cannot be processed.')
                return Account.CurrentAccount.access_transactions_balances(self)
    
    class SavingsAccount(Account_Holder):
        
        '''Transactions for savings account (except transfers to/from current (checking) or business accounts)'''
        
        def access_transactions_balances(self):
            
            current_date = datetime.datetime.now().strftime("%d %b %Y")             
            
            df21 = pd.read_csv('OceansEleven.csv')
            df22 = ''
            df23 = pd.read_csv('SavingsAccount'+str(df21.loc[0,'Value'])+'.csv')
            df23_payline = ''
            df23_paylinedf = ''
            df23_extend = ''
            df23_reset = ''
            df23_dict = ''
            df23_extend_again =''
            
            enter_amount = ''
            deposit_or_withdraw = input('Choose: \n1. Deposit \n2. Withdraw\n3. Return to main menu\n4. Exit')
            if deposit_or_withdraw == '1':
                enter_amount = input('Enter amount : £')
                try:
                    eval(enter_amount)
                    if os.path.isfile('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv') == True:
                        df22 = pd.read_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv')
                        df23_payline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                        df23_paylinedf = pd.DataFrame(df23_payline)
                        df23_extend = pd.concat([df23,df23_paylinedf])
                        df23_reset = df23_extend.reset_index()
                        df23_dict = df23_reset.to_dict()
                        df23_dict.pop('index')
                        df23_extend_again = pd.DataFrame(df23_dict)             
                        df22.loc[1,'C2'] = df23_extend_again['C3'].sum()
                        df22.to_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        df23_extend_again.to_csv('SavingsAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                    elif os.path.isfile('Bottleneck_CS'+str(df21.loc[0,'Value'])+'.csv') == True:
                        df22 = pd.read_csv('Bottleneck_CS'+str(df21.loc[0,'Value'])+'.csv')
                        df23_payline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                        df23_paylinedf = pd.DataFrame(df23_payline)
                        df23_extend = pd.concat([df23,df23_paylinedf])
                        df23_reset = df23_extend.reset_index()
                        df23_dict = df23_reset.to_dict()
                        df23_dict.pop('index')
                        df23_extend_again = pd.DataFrame(df23_dict)             
                        df22.loc[1,'C2'] = df23_extend_again['C3'].sum()
                        df22.to_csv('Bottleneck_CS'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        df23_extend_again.to_csv('SavingsAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                except:
                    print('Invalid input')
                finally:
                    return Account.SavingsAccount.access_transactions_balances(self)     
            elif deposit_or_withdraw == '2':
                enter_amount = input('Enter amount : £')                        
                try:
                    eval(enter_amount)
                    if eval(enter_amount) > df23['C3'].sum():
                        print('Insufficient funds')
                    elif eval(enter_amount) <= df23['C3'].sum():
                        if os.path.isfile('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv') == True:
                            df22 = pd.read_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv')
                            df23_payline = {'C1':[current_date], 'C2': ['Paid out'], 'C3': [eval('-'+enter_amount)]}
                            df23_paylinedf = pd.DataFrame(df23_payline)
                            df23_extend = pd.concat([df23,df23_paylinedf])
                            df23_reset = df23_extend.reset_index()
                            df23_dict = df23_reset.to_dict()
                            df23_dict.pop('index')
                            df23_extend_again = pd.DataFrame(df23_dict)             
                            df22.loc[1,'C2'] = df23_extend_again['C3'].sum()
                            df22.to_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv',index=False)
                            df23_extend_again.to_csv('SavingsAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        elif os.path.isfile('Bottleneck_CS'+str(df21.loc[0,'Value'])+'.csv') == True:
                            df22 = pd.read_csv('Bottleneck_CS'+str(df21.loc[0,'Value'])+'.csv')
                            df23_payline = {'C1':[current_date], 'C2': ['Paid out'], 'C3': [eval('-'+enter_amount)]}
                            df23_paylinedf = pd.DataFrame(df23_payline)
                            df23_extend = pd.concat([df23,df23_paylinedf])
                            df23_reset = df23_extend.reset_index()
                            df23_dict = df23_reset.to_dict()
                            df23_dict.pop('index')
                            df23_extend_again = pd.DataFrame(df23_dict)             
                            df22.loc[1,'C2'] = df23_extend_again['C3'].sum()
                            df22.to_csv('Bottleneck_CS'+str(df21.loc[0,'Value'])+'.csv',index=False)
                            df23_extend_again.to_csv('SavingsAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                except:
                    print('Invalid input')
                finally:
                    return Account.SavingsAccount.access_transactions_balances(self)  
            elif deposit_or_withdraw == '3':
                return Account.Menu.access_transactions_balances(self)
            elif deposit_or_withdraw == '4':
                sys.exit()
            else:
                print('Your response cannot be processed.')
                return Account.Menu.access_transactions_balances(self)
            
    class BusinessAccount(Account_Holder):
        
        '''Transactions for business account (except transfers to/from current (checking) or savings accounts)'''
        
        def access_transactions_balances(self):
            
            current_date = datetime.datetime.now().strftime("%d %b %Y")
            a = datetime.datetime.strptime(current_date, "%d %b %Y")  
            
            df21 = pd.read_csv('OceansEleven.csv')
            df22 = ''
            df23 = pd.read_csv('BusinessAccount'+str(df21.loc[0,'Value'])+'.csv')
            df23_list = list(zip(df23['C1'],df23['C2'],df23['C3']))
            df23_payline = ''
            df23_paylinedf = ''
            df23_extend = ''
            df23_reset = ''
            df23_dict = ''
            df23_extend_again =''
            
            first_date = df23_list[1][0]
            c = datetime.datetime.strptime(first_date, "%d %b %Y")
            e = a - c
            
            # Expense_fee-related
            expense_fee = 0.5
            df22_feelist = []
            for i in df23_list:
                if i[2] < 0:
                    df22_feelist.append(i[2])
            
            # Monthly_charge-related
            monthly_charge = 5
            df23_monthly = e.days/30 - 12
            df22_feelist2 = []
            for i in df23_list:
                if i[2] < 0:
                    df22_feelist2.append(i[2]) 
            
            enter_amount = ''              
            deposit_or_withdraw = input('Choose: \n1. Deposit \n2. Withdraw\n3. Return to main menu\n4. Exit')
            if deposit_or_withdraw == '1':
                enter_amount = input('Enter amount : £')
                try:
                    eval(enter_amount)
                    if os.path.isfile('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv') == True:
                        df22 = pd.read_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv')
                        df23_payline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                        df23_paylinedf = pd.DataFrame(df23_payline)
                        df23_extend = pd.concat([df23,df23_paylinedf])
                        df23_reset = df23_extend.reset_index()
                        df23_dict = df23_reset.to_dict()
                        df23_dict.pop('index')
                        df23_extend_again = pd.DataFrame(df23_dict)             
                        df22.loc[2,'C2'] = df23_extend_again['C3'].sum()
                        df22.to_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        df23_extend_again.to_csv('BusinessAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                    elif os.path.isfile('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv') == True:
                        df22 = pd.read_csv('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv')
                        df23_payline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                        df23_paylinedf = pd.DataFrame(df23_payline)
                        df23_extend = pd.concat([df23,df23_paylinedf])
                        df23_reset = df23_extend.reset_index()
                        df23_dict = df23_reset.to_dict()
                        df23_dict.pop('index')
                        df23_extend_again = pd.DataFrame(df23_dict)             
                        df22.loc[1,'C2'] = df23_extend_again['C3'].sum()
                        df22.to_csv('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        df23_extend_again.to_csv('BusinessAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                except:
                    print('Invalid input')
                finally:
                    return Account.BusinessAccount.access_transactions_balances(self)  
            elif deposit_or_withdraw == '2':
                enter_amount = input('Enter amount : £')
                try:
                    eval(enter_amount)
                    if os.path.isfile('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv') == True:
                        df22 = pd.read_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv')
                        if e.days <= 365:
                            if eval(enter_amount) > (df23['C3'].sum() - expense_fee*len(df22_feelist) - expense_fee):
                                print('Insufficient funds')  # Note: The 'extra' expense_fee is for the withdrawwl being attempted now
                            elif eval(enter_amount) <= (df23['C3'].sum() - expense_fee - expense_fee*len(df22_feelist)):
                                df22 = pd.read_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv')
                                df23_payline = {'C1':[current_date], 'C2': ['Paid out'], 'C3': [eval('-'+enter_amount)]}
                                df23_paylinedf = pd.DataFrame(df23_payline)
                                df23_extend = pd.concat([df23,df23_paylinedf])
                                df23_reset = df23_extend.reset_index()
                                df23_dict = df23_reset.to_dict()
                                df23_dict.pop('index')
                                df23_extend_again = pd.DataFrame(df23_dict)             
                                df22.loc[2,'C2'] = df23_extend_again['C3'].sum()
                                df22.to_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv',index=False)
                                df23_extend_again.to_csv('BusinessAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        elif e.days > 365:
                            if eval(enter_amount) > (df23['C3'].sum() - expense_fee*len(df22_feelist) - expense_fee - monthly_charge*df23_monthly):
                                print('Insufficient funds') # Note: The 'extra' expense_fee covers the withdrawal being attempted now
                            elif eval(enter_amount) <= (df23['C3'].sum() - expense_fee - expense_fee*len(df22_feelist) - monthly_charge*df23_monthly):
                                df22 = pd.read_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv')
                                df23_payline = {'C1':[current_date], 'C2': ['Paid out'], 'C3': [eval('-'+enter_amount)]}
                                df23_paylinedf = pd.DataFrame(df23_payline)
                                df23_extend = pd.concat([df23,df23_paylinedf])
                                df23_reset = df23_extend.reset_index()
                                df23_dict = df23_reset.to_dict()
                                df23_dict.pop('index')
                                df23_extend_again = pd.DataFrame(df23_dict)             
                                df22.loc[2,'C2'] = df23_extend_again['C3'].sum()
                                df22.to_csv('Bottleneck_CSB'+str(df21.loc[0,'Value'])+'.csv',index=False)
                                df23_extend_again.to_csv('BusinessAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                    elif os.path.isfile('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv') == True:
                        df22 = pd.read_csv('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv')
                        if e.days <= 365:
                            if eval(enter_amount) > (df23['C3'].sum() - expense_fee*len(df22_feelist) - expense_fee):
                                print('Insufficient funds') # Note: The 'extra' expense_fee covers the withdrawal being attempted now
                            elif eval(enter_amount) <= (df23['C3'].sum() - expense_fee*len(df22_feelist) - expense_fee):
                                df22 = pd.read_csv('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv')
                                df23_payline = {'C1':[current_date], 'C2': ['Paid out'], 'C3': [eval('-'+enter_amount)]}
                                df23_paylinedf = pd.DataFrame(df23_payline)
                                df23_extend = pd.concat([df23,df23_paylinedf])
                                df23_reset = df23_extend.reset_index()
                                df23_dict = df23_reset.to_dict()
                                df23_dict.pop('index')
                                df23_extend_again = pd.DataFrame(df23_dict)             
                                df22.loc[1,'C2'] = df23_extend_again['C3'].sum()
                                df22.to_csv('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv',index=False)
                                df23_extend_again.to_csv('BusinessAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                        elif e.days > 365:
                            if eval(enter_amount) > (df23['C3'].sum() - expense_fee*len(df22_feelist) - expense_fee - monthly_charge*df23_monthly):
                                print('Insufficient funds') # Note: The 'extra' expense_fee covers the withdrawal being attempted now
                            elif eval(enter_amount) <= (df23['C3'].sum() - expense_fee*len(df22_feelist) - expense_fee - monthly_charge*df23_monthly):
                                df22 = pd.read_csv('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv')
                                df23_payline = {'C1':[current_date], 'C2': ['Paid out'], 'C3': [eval('-'+enter_amount)]}
                                df23_paylinedf = pd.DataFrame(df23_payline)
                                df23_extend = pd.concat([df23,df23_paylinedf])
                                df23_reset = df23_extend.reset_index()
                                df23_dict = df23_reset.to_dict()
                                df23_dict.pop('index')
                                df23_extend_again = pd.DataFrame(df23_dict)             
                                df22.loc[1,'C2'] = df23_extend_again['C3'].sum()
                                df22.to_csv('Bottleneck_CB'+str(df21.loc[0,'Value'])+'.csv',index=False)
                                df23_extend_again.to_csv('BusinessAccount'+str(df21.loc[0,'Value'])+'.csv',index=False)
                except:
                    print('Invalid input')
                finally:
                    return Account.BusinessAccount.access_transactions_balances(self)
            elif deposit_or_withdraw == '3':
                return Account.Menu.access_transactions_balances(self)
            elif deposit_or_withdraw == '4':
                sys.exit()
            else:
                print('Your response cannot be processed.')
                return Account.Menu.access_transactions_balances(self)
                                            
    class Transfer_CS(Account_Holder):
        
        '''Transfers between current (checking) and savings accounts if person has only those accounts'''
        
        def access_transactions_balances(self):
            
            current_date = datetime.datetime.now().strftime("%d %b %Y")
            
            df24 = pd.read_csv('OceansEleven.csv')
            df25 = pd.read_csv('Bottleneck_CS'+str(df24.loc[0,'Value'])+'.csv')
            df26_c = pd.read_csv('CurrentAccount'+str(df24.loc[0,'Value'])+'.csv')
            df26_cline = ''
            df26_clinedf = ''
            df26_cxtend = ''
            df26_creset = ''
            df26_cdict = ''
            df26_cxtend_again =''
            df26_s = pd.read_csv('SavingsAccount'+str(df24.loc[0,'Value'])+'.csv')
            df26_sline = ''
            df26_slinedf = ''
            df26_sxtend = ''
            df26_sreset = ''
            df26_sdict = ''
            df26_sxtend_again =''
            
            enter_amount = input('Enter amount : £')
            select_source = input('From which account (C/S)?\n(R to return to main menu) : ')
            if select_source == 'C' or select_source == 'c':
                try:
                    eval(enter_amount)
                    if eval(enter_amount) <= df26_c['C3'].sum():
                        df26_cline = {'C1':[current_date], 'C2': ['Transferred'], 'C3': [eval('-'+enter_amount)]}                            
                        df26_clinedf = pd.DataFrame(df26_cline)
                        df26_cxtend = pd.concat([df26_c,df26_clinedf])
                        df26_creset = df26_cxtend.reset_index()
                        df26_cdict = df26_creset.to_dict()
                        df26_cdict.pop('index')
                        df26_cxtend_again = pd.DataFrame(df26_cdict)             
                        df25.loc[0,'C2'] = df26_cxtend_again['C3'].sum()
                        df26_cxtend_again.to_csv('CurrentAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                        df26_sline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                        df26_slinedf = pd.DataFrame(df26_sline)
                        df26_sxtend = pd.concat([df26_s,df26_slinedf])
                        df26_sreset = df26_sxtend.reset_index()
                        df26_sdict = df26_sreset.to_dict()
                        df26_sdict.pop('index')
                        df26_sxtend_again = pd.DataFrame(df26_sdict)             
                        df25.loc[1,'C2'] = df26_sxtend_again['C3'].sum()
                        df25.to_csv('Bottleneck_CS'+str(df24.loc[0,'Value'])+'.csv',index=False)
                        df26_sxtend_again.to_csv('SavingsAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                    elif eval(enter_amount) > df26_c['C3'].sum():
                        print('Insufficient funds')
                except:
                    print('Invalid input')
                finally:
                    return Account.Menu_CS.access_transactions_balances(self)
            elif select_source == 'S' or select_source == 's':
                try:
                    eval(enter_amount)
                    if eval(enter_amount) <= df26_s['C3'].sum():
                        df26_sline = {'C1':[current_date], 'C2': ['Transferred'], 'C3': [eval('-'+enter_amount)]}                            
                        df26_slinedf = pd.DataFrame(df26_sline)
                        df26_sxtend = pd.concat([df26_s,df26_slinedf])
                        df26_sreset = df26_sxtend.reset_index()
                        df26_sdict = df26_sreset.to_dict()
                        df26_sdict.pop('index')
                        df26_sxtend_again = pd.DataFrame(df26_sdict)             
                        df25.loc[1,'C2'] = df26_sxtend_again['C3'].sum()
                        df26_sxtend_again.to_csv('SavingsAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                        df26_cline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                        df26_clinedf = pd.DataFrame(df26_cline)
                        df26_cxtend = pd.concat([df26_c,df26_clinedf])
                        df26_creset = df26_cxtend.reset_index()
                        df26_cdict = df26_creset.to_dict()
                        df26_cdict.pop('index')
                        df26_cxtend_again = pd.DataFrame(df26_cdict)             
                        df25.loc[0,'C2'] = df26_cxtend_again['C3'].sum()
                        df25.to_csv('Bottleneck_CS'+str(df24.loc[0,'Value'])+'.csv',index=False)
                        df26_cxtend_again.to_csv('CurrentAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)                          
                    elif eval(enter_amount) > df26_s['C3'].sum():
                        print('Insufficient funds')
                except:
                    print('Invalid input')
                finally:
                    return Account.Menu_CS.access_transactions_balances(self)
            elif select_source == 'R' or select_source == 'r':
                return Account.Menu.access_transactions_balances(self)
            else:
                print('Your response cannot be processed.')
                return Account.Menu.access_transactions_balances(self)
            
    class Transfer_CB(Account_Holder):
        
        '''Transfers between current (checking) and business accounts if person has only those accounts'''
        
        def access_transactions_balances(self):
            
            current_date = datetime.datetime.now().strftime("%d %b %Y")
            a = datetime.datetime.strptime(current_date, "%d %b %Y")  
            
            df24 = pd.read_csv('OceansEleven.csv')
            df25 = pd.read_csv('Bottleneck_CB'+str(df24.loc[0,'Value'])+'.csv')
            df26_c = pd.read_csv('CurrentAccount'+str(df24.loc[0,'Value'])+'.csv')
            df26_cline = ''
            df26_clinedf = ''
            df26_cxtend = ''
            df26_creset = ''
            df26_cdict = ''
            df26_cxtend_again =''
            df26_b = pd.read_csv('BusinessAccount'+str(df24.loc[0,'Value'])+'.csv')
            df26_blist = list(zip(df26_b['C1'],df26_b['C2'],df26_b['C3']))
            df26_bline = ''
            df26_blinedf = ''
            df26_bxtend = ''
            df26_breset = ''
            df26_bdict = ''
            df26_bxtend_again =''
            
            first_date = df26_blist[1][0]
            c = datetime.datetime.strptime(first_date, "%d %b %Y")
            e = a - c                
            
            # Expense_fee-related
            expense_fee = 0.5
            df25_feelist = []
            for i in df26_blist:
                if i[2] < 0:
                    df25_feelist.append(i[2])
            
            # Monthly_charge-related
            monthly_charge = 5
            df26_monthly = e.days/30 - 12
            
            # Data handling
            enter_amount = input('Enter amount : £')
            select_source = input('From which account (C/B)?\n(R to return to main menu) : ')
            if select_source == 'C' or select_source == 'c':
                try:
                    eval(enter_amount)
                    if eval(enter_amount) <= df26_c['C3'].sum():
                        df26_cline = {'C1':[current_date], 'C2': ['Transferred'], 'C3': [eval('-'+enter_amount)]}                            
                        df26_clinedf = pd.DataFrame(df26_cline)
                        df26_cxtend = pd.concat([df26_c,df26_clinedf])
                        df26_creset = df26_cxtend.reset_index()
                        df26_cdict = df26_creset.to_dict()
                        df26_cdict.pop('index')
                        df26_cxtend_again = pd.DataFrame(df26_cdict)             
                        df25.loc[0,'C2'] = df26_cxtend_again['C3'].sum()
                        df26_cxtend_again.to_csv('CurrentAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                        df26_bline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                        df26_blinedf = pd.DataFrame(df26_bline)
                        df26_bxtend = pd.concat([df26_b,df26_blinedf])
                        df26_breset = df26_bxtend.reset_index()
                        df26_bdict = df26_breset.to_dict()
                        df26_bdict.pop('index')
                        df26_bxtend_again = pd.DataFrame(df26_bdict)             
                        df25.loc[1,'C2'] = df26_bxtend_again['C3'].sum()
                        df25.to_csv('Bottleneck_CB'+str(df24.loc[0,'Value'])+'.csv',index=False)
                        df26_bxtend_again.to_csv('BusinessAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)                           
                    elif eval(enter_amount) > df26_c['C3'].sum():
                        print('Insufficient funds')
                except:
                    print('Invalid input')
                finally:
                    return Account.Menu_CB.access_transactions_balances(self)
            elif select_source == 'B' or select_source == 'b':
                try:
                    eval(enter_amount)
                    if e.days <= 365:
                        if eval(enter_amount) > (df26_b['C3'].sum() - expense_fee*len(df25_feelist) - expense_fee):
                            print('Insufficient funds') # Note: The 'extra' expense_fee is for the withdrawwl being attempted now
                        elif eval(enter_amount) <= (df26_b['C3'].sum() - expense_fee*len(df25_feelist) - expense_fee):
                            df26_bline = {'C1':[current_date], 'C2': ['Transferred'], 'C3': [eval('-'+enter_amount)]}         
                            df26_blinedf = pd.DataFrame(df26_bline)
                            df26_bxtend = pd.concat([df26_b,df26_blinedf])
                            df26_breset = df26_bxtend.reset_index()
                            df26_bdict = df26_breset.to_dict()
                            df26_bdict.pop('index')
                            df26_bxtend_again = pd.DataFrame(df26_bdict)             
                            df25.loc[1,'C2'] = df26_bxtend_again['C3'].sum()
                            df26_bxtend_again.to_csv('BusinessAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                            df26_cline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                            df26_clinedf = pd.DataFrame(df26_cline)
                            df26_cxtend = pd.concat([df26_c,df26_clinedf])
                            df26_creset = df26_cxtend.reset_index()
                            df26_cdict = df26_creset.to_dict()
                            df26_cdict.pop('index')
                            df26_cxtend_again = pd.DataFrame(df26_cdict)             
                            df25.loc[0,'C2'] = df26_cxtend_again['C3'].sum()
                            df25.to_csv('Bottleneck_CB'+str(df24.loc[0,'Value'])+'.csv',index=False)
                            df26_cxtend_again.to_csv('CurrentAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                    elif e.days > 365:
                        if eval(enter_amount) > (df26_b['C3'].sum() - expense_fee*len(df25_feelist) - expense_fee - monthly_charge*df26_monthly):
                            print('Insufficient funds') # Note: The 'extra' expense_fee is for the withdrawwl being attempted now
                        elif eval(enter_amount) <= (df26_b['C3'].sum() - expense_fee*len(df25_feelist) - expense_fee - monthly_charge*df26_monthly):
                            df26_bline = {'C1':[current_date], 'C2': ['Transferred'], 'C3': [eval('-'+enter_amount)]}         
                            df26_blinedf = pd.DataFrame(df26_bline)
                            df26_bxtend = pd.concat([df26_b,df26_blinedf])
                            df26_breset = df26_bxtend.reset_index()
                            df26_bdict = df26_breset.to_dict()
                            df26_bdict.pop('index')
                            df26_bxtend_again = pd.DataFrame(df26_bdict)             
                            df25.loc[1,'C2'] = df26_bxtend_again['C3'].sum()
                            df26_bxtend_again.to_csv('BusinessAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                            df26_cline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                            df26_clinedf = pd.DataFrame(df26_cline)
                            df26_cxtend = pd.concat([df26_c,df26_clinedf])
                            df26_creset = df26_cxtend.reset_index()
                            df26_cdict = df26_creset.to_dict()
                            df26_cdict.pop('index')
                            df26_cxtend_again = pd.DataFrame(df26_cdict)             
                            df25.loc[0,'C2'] = df26_cxtend_again['C3'].sum()
                            df25.to_csv('Bottleneck_CB'+str(df24.loc[0,'Value'])+'.csv',index=False)
                            df26_cxtend_again.to_csv('CurrentAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                except:
                    print('Invalid input')
                finally:
                    return Account.Menu_CB.access_transactions_balances(self)
            elif select_source == 'R' or select_source == 'r':
                return Account.Menu.access_transactions_balances(self)
            else:
                print('Your response cannot be processed.')
                return Account.Menu.access_transactions_balances(self)
            
    class Transfer_CSB(Account_Holder):
        
        '''Transfers between current (checking), savings, and business accounts if person has all of those accounts'''
        
        def access_transactions_balances(self):
            
            current_date = datetime.datetime.now().strftime("%d %b %Y")
            a = datetime.datetime.strptime(current_date, "%d %b %Y")      
            
            df24 = pd.read_csv('OceansEleven.csv')
            df25 = pd.read_csv('Bottleneck_CSB'+str(df24.loc[0,'Value'])+'.csv')
            df26_c = pd.read_csv('CurrentAccount'+str(df24.loc[0,'Value'])+'.csv')
            df26_cline = ''
            df26_clinedf = ''
            df26_cxtend = ''
            df26_creset = ''
            df26_creset = ''
            df26_cdict = ''
            df26_cxtend_again =''
            df26_s = pd.read_csv('SavingsAccount'+str(df24.loc[0,'Value'])+'.csv')
            df26_sline = ''
            df26_slinedf = ''
            df26_sxtend = ''
            df26_sreset = ''
            df26_sreset = ''
            df26_sdict = ''
            df26_sxtend_again =''
            df26_b = pd.read_csv('BusinessAccount'+str(df24.loc[0,'Value'])+'.csv')
            df26_blist = list(zip(df26_b['C1'],df26_b['C2'],df26_b['C3']))
            df26_bline = ''
            df26_blinedf = ''
            df26_bxtend = ''
            df26_breset = ''
            df26_breset = ''
            df26_bdict = ''
            df26_bxtend_again =''
            
            first_date = df26_blist[1][0]
            c = datetime.datetime.strptime(first_date, "%d %b %Y")
            e = a - c
            
            # Expense_fee-related
            expense_fee = 0.5
            df25_feelist = []
            for i in df26_blist:
                df25_feelist.append(i[2])
       
            # Monthly_charge-related
            monthly_charge = 5
            df26_monthly = e.days/30 - 12
            df25_feelist2 = []
            for i in df26_blist:
                if i[2] < 0:
                    df25_feelist2.append(i[2])
            
            select_destination = ''
            enter_amount = input('Enter amount : £')
            select_source = input('From which account (C/S/B)?\n(R to return to main menu) : ')
            if select_source == 'C' or select_source == 'c':
                select_destination = input('To which account (S/B)? : ')
                if select_destination == 'S' or select_destination == 's':
                    try:
                        eval(enter_amount)
                        if eval(enter_amount) <= df26_c['C3'].sum():
                            df26_cline = {'C1':[current_date], 'C2': ['Transferred'], 'C3': [eval('-'+enter_amount)]}                            
                            df26_clinedf = pd.DataFrame(df26_cline)
                            df26_cxtend = pd.concat([df26_c,df26_clinedf])
                            df26_creset = df26_cxtend.reset_index()
                            df26_cdict = df26_creset.to_dict()
                            df26_cdict.pop('index')
                            df26_cxtend_again = pd.DataFrame(df26_cdict)             
                            df25.loc[0,'C2'] = df26_cxtend_again['C3'].sum()
                            df26_cxtend_again.to_csv('CurrentAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                            df26_sline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                            df26_slinedf = pd.DataFrame(df26_sline)
                            df26_sxtend = pd.concat([df26_s,df26_slinedf])
                            df26_sreset = df26_sxtend.reset_index()
                            df26_sdict = df26_sreset.to_dict()
                            df26_sdict.pop('index')
                            df26_sxtend_again = pd.DataFrame(df26_sdict)             
                            df25.loc[1,'C2'] = df26_sxtend_again['C3'].sum()
                            df25.to_csv('Bottleneck_CSB'+str(df24.loc[0,'Value'])+'.csv',index=False)
                            df26_sxtend_again.to_csv('SavingsAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                        elif eval(enter_amount) > df26_c['C3'].sum():
                            print('Insufficient funds')
                    except:
                        print('Invalid input')
                    finally:
                        return Account.Menu_CSB.access_transactions_balances(self)
                elif select_destination == 'B' or select_destination == 'b':
                    try:
                        eval(enter_amount)
                        if eval(enter_amount) <= df26_c['C3'].sum():
                            df26_cline = {'C1':[current_date], 'C2': ['Transferred'], 'C3': [eval('-'+enter_amount)]}                            
                            df26_clinedf = pd.DataFrame(df26_cline)
                            df26_cxtend = pd.concat([df26_c,df26_clinedf])
                            df26_creset = df26_cxtend.reset_index()
                            df26_cdict = df26_creset.to_dict()
                            df26_cdict.pop('index')
                            df26_cxtend_again = pd.DataFrame(df26_cdict)             
                            df25.loc[0,'C2'] = df26_cxtend_again['C3'].sum()
                            df26_cxtend_again.to_csv('CurrentAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                            df26_bline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                            df26_blinedf = pd.DataFrame(df26_bline)
                            df26_bxtend = pd.concat([df26_b,df26_blinedf])
                            df26_breset = df26_bxtend.reset_index()
                            df26_bdict = df26_breset.to_dict()
                            df26_bdict.pop('index')
                            df26_bxtend_again = pd.DataFrame(df26_bdict)             
                            df25.loc[2,'C2'] = df26_bxtend_again['C3'].sum()
                            df25.to_csv('Bottleneck_CSB'+str(df24.loc[0,'Value'])+'.csv',index=False)
                            df26_bxtend_again.to_csv('BusinessAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)                           
                        elif eval(enter_amount) > df26_c['C3'].sum():
                            print('Insufficient funds')
                    except:
                        print('Invalid input')
                    finally:
                        return Account.Menu_CSB.access_transactions_balances(self)
                else:
                    print('Your response cannot be processed.')
                    return Account.Menu.access_transactions_balances(self)
            
            elif select_source == 'S' or select_source == 's':
                select_destination = input('To which account (C/B)? : ')
                if select_destination == 'C' or select_destination == 'c':
                    try:
                        eval(enter_amount)
                        if eval(enter_amount) <= df26_s['C3'].sum():
                            df26_sline = {'C1':[current_date], 'C2': ['Transferred'], 'C3': [eval('-'+enter_amount)]}                            
                            df26_slinedf = pd.DataFrame(df26_sline)
                            df26_sxtend = pd.concat([df26_s,df26_slinedf])
                            df26_sreset = df26_sxtend.reset_index()
                            df26_sdict = df26_sreset.to_dict()
                            df26_sdict.pop('index')
                            df26_sxtend_again = pd.DataFrame(df26_sdict)             
                            df25.loc[1,'C2'] = df26_sxtend_again['C3'].sum()
                            df26_sxtend_again.to_csv('SavingsAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                            df26_cline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                            df26_clinedf = pd.DataFrame(df26_cline)
                            df26_cxtend = pd.concat([df26_c,df26_clinedf])
                            df26_creset = df26_cxtend.reset_index()
                            df26_cdict = df26_creset.to_dict()
                            df26_cdict.pop('index')
                            df26_cxtend_again = pd.DataFrame(df26_cdict)             
                            df25.loc[0,'C2'] = df26_cxtend_again['C3'].sum()
                            df25.to_csv('Bottleneck_CSB'+str(df24.loc[0,'Value'])+'.csv',index=False)
                            df26_cxtend_again.to_csv('CurrentAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)                             
                        elif eval(enter_amount) > df26_s['C3'].sum():
                            print('Insufficient funds')
                    except:
                        print('Invalid input')
                    finally:
                        return Account.Menu_CSB.access_transactions_balances(self)
                elif select_destination == 'B' or select_destination == 'b':
                    try:
                        eval(enter_amount)
                        if eval(enter_amount) <= df26_s['C3'].sum():
                            df26_sline = {'C1':[current_date], 'C2': ['Transferred'], 'C3': [eval('-'+enter_amount)]}                            
                            df26_slinedf = pd.DataFrame(df26_sline)
                            df26_sxtend = pd.concat([df26_s,df26_slinedf])
                            df26_sreset = df26_sxtend.reset_index()
                            df26_sdict = df26_sreset.to_dict()
                            df26_sdict.pop('index')
                            df26_sxtend_again = pd.DataFrame(df26_sdict)             
                            df25.loc[1,'C2'] = df26_sxtend_again['C3'].sum()
                            df26_sxtend_again.to_csv('SavingsAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                            df26_bline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                            df26_blinedf = pd.DataFrame(df26_bline)
                            df26_bxtend = pd.concat([df26_b,df26_blinedf])
                            df26_breset = df26_bxtend.reset_index()
                            df26_bdict = df26_breset.to_dict()
                            df26_bdict.pop('index')
                            df26_bxtend_again = pd.DataFrame(df26_bdict)             
                            df25.loc[2,'C2'] = df26_bxtend_again['C3'].sum()
                            df25.to_csv('Bottleneck_CSB'+str(df24.loc[0,'Value'])+'.csv',index=False)
                            df26_bxtend_again.to_csv('BusinessAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                        elif eval(enter_amount) > df26_s['C3'].sum():
                            print('Insufficient funds')
                    except:
                        print('Invalid input')
                    finally:
                        return Account.Menu_CSB.access_transactions_balances(self)
                else:
                    print('Your response cannot be processed.')
                    return Account.Menu_CSB.access_transactions_balances(self)
            
            elif select_source == 'B' or select_source == 'b':
                select_destination = input('To which account (C/S)? : ')
                if select_destination == 'C' or select_destination == 'c':
                    try:
                        eval(enter_amount)
                        if e.days <= 365:
                            if eval(enter_amount) > (df26_b['C3'].sum() - expense_fee*len(df25_feelist) - expense_fee):
                                print('Insufficient funds') # Note: The 'extra' expense_fee is for the withdrawwl being attempted now
                            elif eval(enter_amount) <= (df26_b['C3'].sum() - expense_fee*len(df25_feelist) - expense_fee):
                                df26_bline = {'C1':[current_date], 'C2': ['Transferred'], 'C3': [eval('-'+enter_amount)]}         
                                df26_blinedf = pd.DataFrame(df26_bline)
                                df26_bxtend = pd.concat([df26_b,df26_blinedf])
                                df26_breset = df26_bxtend.reset_index()
                                df26_bdict = df26_breset.to_dict()
                                df26_bdict.pop('index')
                                df26_bxtend_again = pd.DataFrame(df26_bdict)             
                                df25.loc[2,'C2'] = df26_bxtend_again['C3'].sum()
                                df26_bxtend_again.to_csv('BusinessAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)                            
                                df26_cline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                                df26_clinedf = pd.DataFrame(df26_cline)
                                df26_cxtend = pd.concat([df26_c,df26_clinedf])
                                df26_creset = df26_cxtend.reset_index()
                                df26_cdict = df26_creset.to_dict()
                                df26_cdict.pop('index')
                                df26_cxtend_again = pd.DataFrame(df26_cdict)             
                                df25.loc[0,'C2'] = df26_cxtend_again['C3'].sum()
                                df25.to_csv('Bottleneck_CSB'+str(df24.loc[0,'Value'])+'.csv',index=False)
                                df26_cxtend_again.to_csv('CurrentAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                        elif e.days > 365:
                            if eval(enter_amount) > (df26_b['C3'].sum() - expense_fee*len(df25_feelist) - expense_fee - monthly_charge*df26_monthly):
                                print('Insufficient funds') # Note: The 'extra' expense_fee is for the withdrawwl being attempted now
                            elif eval(enter_amount) <= (df26_b['C3'].sum() - expense_fee - expense_fee*len(df25_feelist) - monthly_charge*df26_monthly):
                                df26_bline = {'C1':[current_date], 'C2': ['Transferred'], 'C3': [eval('-'+enter_amount)]}         
                                df26_blinedf = pd.DataFrame(df26_bline)
                                df26_bxtend = pd.concat([df26_b,df26_blinedf])
                                df26_breset = df26_bxtend.reset_index()
                                df26_bdict = df26_breset.to_dict()
                                df26_bdict.pop('index')
                                df26_bxtend_again = pd.DataFrame(df26_bdict)             
                                df25.loc[2,'C2'] = df26_bxtend_again['C3'].sum()
                                df26_bxtend_again.to_csv('BusinessAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)                            
                                df26_cline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                                df26_clinedf = pd.DataFrame(df26_cline)
                                df26_cxtend = pd.concat([df26_c,df26_clinedf])
                                df26_creset = df26_cxtend.reset_index()
                                df26_cdict = df26_creset.to_dict()
                                df26_cdict.pop('index')
                                df26_cxtend_again = pd.DataFrame(df26_cdict)             
                                df25.loc[0,'C2'] = df26_cxtend_again['C3'].sum()
                                df25.to_csv('Bottleneck_CSB'+str(df24.loc[0,'Value'])+'.csv',index=False)
                                df26_cxtend_again.to_csv('CurrentAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                    except:
                        print('Invalid input')
                    finally:
                        return Account.Menu_CSB.access_transactions_balances(self)
                elif select_destination == 'S' or select_destination == 's':
                    try:
                        eval(enter_amount)
                        if e.days <= 365:
                            if eval(enter_amount) > (df26_b['C3'].sum() - expense_fee*len(df25_feelist) - expense_fee):
                                print('Insufficient funds') # Note: The 'extra' expense_fee is for the withdrawwl being attempted now
                            elif eval(enter_amount) <= (df26_b['C3'].sum() - expense_fee*len(df25_feelist) - expense_fee):
                                df26_bline = {'C1':[current_date], 'C2': ['Transferred'], 'C3': [eval('-'+enter_amount)]}         
                                df26_blinedf = pd.DataFrame(df26_bline)
                                df26_bxtend = pd.concat([df26_b,df26_blinedf])
                                df26_breset = df26_bxtend.reset_index()
                                df26_bdict = df26_breset.to_dict()
                                df26_bdict.pop('index')
                                df26_bxtend_again = pd.DataFrame(df26_bdict)             
                                df25.loc[2,'C2'] = df26_bxtend_again['C3'].sum()
                                df26_bxtend_again.to_csv('BusinessAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                                df26_sline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                                df26_slinedf = pd.DataFrame(df26_sline)
                                df26_sxtend = pd.concat([df26_s,df26_slinedf])
                                df26_sreset = df26_sxtend.reset_index()
                                df26_sdict = df26_sreset.to_dict()
                                df26_sdict.pop('index')
                                df26_sxtend_again = pd.DataFrame(df26_sdict)             
                                df25.loc[1,'C2'] = df26_sxtend_again['C3'].sum()
                                df25.to_csv('Bottleneck_CSB'+str(df24.loc[0,'Value'])+'.csv',index=False)
                                df26_sxtend_again.to_csv('SavingsAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                        elif e.days > 365:
                            if eval(enter_amount) > (df26_b['C3'].sum() - expense_fee*len(df25_feelist) - expense_fee - monthly_charge*df26_monthly):
                                print('Insufficient funds') # Note: The 'extra' expense_fee is for the withdrawwl being attempted now
                            elif eval(enter_amount) <= (df26_b['C3'].sum() - expense_fee - expense_fee*len(df25_feelist) - monthly_charge*df26_monthly):
                                df26_bline = {'C1':[current_date], 'C2': ['Transferred'], 'C3': [eval('-'+enter_amount)]}         
                                df26_blinedf = pd.DataFrame(df26_bline)
                                df26_bxtend = pd.concat([df26_b,df26_blinedf])
                                df26_breset = df26_bxtend.reset_index()
                                df26_bdict = df26_breset.to_dict()
                                df26_bdict.pop('index')
                                df26_bxtend_again = pd.DataFrame(df26_bdict)             
                                df25.loc[2,'C2'] = df26_bxtend_again['C3'].sum()
                                df26_bxtend_again.to_csv('BusinessAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                                df26_sline = {'C1':[current_date], 'C2': ['Paid in'], 'C3': [eval(enter_amount)]}
                                df26_slinedf = pd.DataFrame(df26_sline)
                                df26_sxtend = pd.concat([df26_s,df26_slinedf])
                                df26_sreset = df26_sxtend.reset_index()
                                df26_sdict = df26_sreset.to_dict()
                                df26_sdict.pop('index')
                                df26_sxtend_again = pd.DataFrame(df26_sdict)             
                                df25.loc[1,'C2'] = df26_sxtend_again['C3'].sum()
                                df25.to_csv('Bottleneck_CSB'+str(df24.loc[0,'Value'])+'.csv',index=False)
                                df26_sxtend_again.to_csv('SavingsAccount'+str(df24.loc[0,'Value'])+'.csv',index=False)
                    except:
                        print('Invalid input')
                    finally:
                        return Account.Menu_CSB.access_transactions_balances(self)
                else:
                    print('Your response cannot be processed.')
                    return Account.Menu.access_transactions_balances(self)
            elif select_source == 'R' or select_source == 'r':
                return Account.Menu.access_transactions_balances(self)
            else:
                print('Your response cannot be processed.')
                return Account.Menu.access_transactions_balances(self)
                        
'__main__'
a = Account()
b = a.ATM_card_validator()
c = b.access_transactions_balances()
