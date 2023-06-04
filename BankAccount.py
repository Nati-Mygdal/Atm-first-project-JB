import json, random
class BankAccount:
    def __init__(self,account_name,pin) -> None:
        self.account_name = account_name
        self.pin = pin
        with open('accounts.json') as file: #make sure not to make twice the same sn, if prog has more then 1mil users, extend randint range.
            data = json.load(file)
        sns = [account_dict['sn'] for account_dict in data]
        self.account_sn = random.randint(1,1000000)
        while self.account_sn in sns:
            self.account_sn = random.randint(1,1000000)
        self.balance = 0
    
    def save_info(self):        #take info from json,make asked changes, return updated file to json.
        with open('accounts.json') as file:
            data = json.load(file)
        in_data = False        
        for account_dict in data:
            if account_dict['sn'] == self.account_sn:
                account_dict['balance'] = self.balance
                account_dict['pin'] = self.pin
                in_data = True
            else:
                continue
        if not in_data:        #take info from json file, add new user, return updated file to json.
            account_data = {"name":self.account_name,
                        "sn":self.account_sn,
                        "balance":self.balance,
                        "pin":self.pin}
            data.append(account_data)
        with open('accounts.json','w',) as file:
            json.dump(data,file,indent=3)
        print(f"Account saved.")

    def deposit(self,amount): #add money to self balance.
        if amount <= 0:
            print('Must deposit a positive number.')
        else:
            self.balance += amount
            print(f"Balance was updated, new balance: {self.balance}$")
        self.save_info() #update new balance to json file.
    
    def withdraw(self,amount): #take money from self balance.
        if amount <= 0:
            print("Withdraw failed, must withdraw above 0$")
        elif amount > self.balance:
            print(f"Withdraw failed, your current max amount to withdraw is {self.balance}$.")
        else:
            self.balance -= amount
            print(f"Balance was updated, new balance: {self.balance}$")
        self.save_info() #update new balance to json file.

    def transfer(self,reciever_sn,amount): #check valid amount, move money from user to another.
        if amount > 0:
            if self.balance >= amount:
                with open('accounts.json') as file:
                    all_info = json.load(file)
                for acc in all_info:
                    find_account = False
                    if reciever_sn == acc['sn']:
                        self.balance -= amount                        
                        acc['balance'] += amount            
                        find_account = True                                           
                        with open('accounts.json','w') as file: #update file with reciever's account new balance.
                            json.dump(all_info,file,indent=3)
                        print(f'Money was transfered! New balance:{self.balance}$')
                        self.save_info() #update giving account's balance
                        break
                if not find_account:
                    print("The account you want to transfer to wasn't found.")
            else:
                print(f'Amount to transfer cant be higher then balance. Current balance: {self.balance}$')
        else:
            print("Amount must be more than 0.")

        
                
    def show_balance(self):
        print(f"Current balance: {self.balance}$")
    
    def change_pin(self,new_pin):
        if len(new_pin) == 4:
            if not (all(dig.isdigit() for dig in new_pin)):
                raise Exception('pin cannot contain letters.')
            else:
                self.pin = new_pin
                self.save_info()
        else:
            raise Exception('pin must be 4 digits long')        
            