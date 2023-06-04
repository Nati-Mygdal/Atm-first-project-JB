from BankAccount import BankAccount as ba
import json, getpass

def to_cont(): #check if user wish to continue makinng actions in his account.
    to_continue = input('Do you want to make another action ? (0) No | (1) Yes\n')
    if to_continue == '1': return True
    elif to_continue == '0': return False
    else:
        print("Input invalid, leaving account's page.")
        return False

def check_action(name): #check which action user wants to make.
    return input(f"""
                    Welcome {name}, what action would you like to do?
                    Withdraw           (1)
                    Deposit            (2)
                    Transfer           (3)
                    Change secret code (4)
                    Show balance       (5)
                    Return             (6)
                    """)

def pin_check(pin):
    return (len(pin)==4 and (all(dig.isdigit() for dig in pin)))

while True:
    start_program = input("""
    Welcome to atm program, please select an action:
    1:  Create account
    2:  Enter account
    0:  Exit
                        Choose action's number to continue...
    """)
    if start_program == '1':                                   #Start creating account
        first_name = input('Please enter your first name\n')
        last_name = input('Please enter your last name\n')
        while not first_name.isalpha() or not last_name.isalpha():
            print('First and last name must contain letters only.')
            first_name = input('Please enter your first name\n')
            last_name = input('Please enter your last name\n')
        name = first_name.capitalize()+' '+last_name.capitalize()
        code = getpass.getpass('Please enter your secret code (4 digits..)\n')
        while not pin_check(code):                                  #Make sure code is valid.
            code = getpass.getpass('Input was incorrect, please enter a 4 digit code.\n')
        newacc = ba(name,code)
        newacc.save_info()
        print(f"""Account Created!
            To access your account you will need to remember account number and secret code.
            Account number: {newacc.account_sn}
            """)
        input('Press enter to continue...')
    elif start_program == '2':                                 #Enter options menu
        acc_sn = input('Enter account number\n')
        acc_code = getpass.getpass('Enter secret code\n')
        with open('accounts.json') as file:
            accounts_json = json.load(file)
        access_grant = False
        for account in accounts_json:
            if account['sn'] == int(acc_sn):
                if account['pin'] == acc_code:
                    curr_acc = ba(account['name'],account['pin'])   #Creat object to make changes with.
                    curr_acc.balance = account['balance']
                    curr_acc.account_sn = account['sn']         
                    access_grant = True
                    user_action = check_action(account['name'])
                    while user_action != '6':
                        if user_action == '1':
                            amount = input(f'Enter your amount to withdraw, amount availalble: {curr_acc.balance}$\n')
                            if amount.isdigit():
                                curr_acc.withdraw(int(amount))
                            else:
                                print('Must enter numbers, action failed.')
                            to_continue = to_cont()
                            if to_continue:                      
                                user_action = check_action(account['name'])
                            else:
                                break
                        elif user_action == '2':
                            amount = input('Enter amount to deposit\n')
                            if amount.isdigit():
                                curr_acc.deposit(int(amount))
                            else:
                                print('Must enter numbers, action failed.')
                            to_continue = to_cont()
                            if to_continue:                      
                                user_action = check_action(account['name'])
                            else:
                                break
                        elif user_action == '3':
                            other_sn = input("Enter reciever's account number\n")
                            if int(other_sn) != curr_acc.account_sn:
                                amount = input('Enter amount to transfer.\n')
                                if other_sn.isdigit() and amount.isdigit():
                                    curr_acc.transfer(int(other_sn),int(amount))
                                else:
                                    print('Action failed. Information was invalid.')
                            else:
                                print('Action failed. Cant transfer money to yourself.\nYou can use withdraw option to take money.')
                            to_continue = to_cont()
                            if to_continue:                      
                                user_action = check_action(account['name'])
                            else:
                                break
                        elif user_action == '4':
                            counter = 3
                            new_code = getpass.getpass('Please enter your new 4 digits code\n',)
                            while counter != 0 and not pin_check(new_code):
                                if len(new_code) != 4:
                                    print(f'code must be 4 digits long, you have {counter} more tries.')
                                if not (all(dig.isdigit() for dig in new_code)):
                                    print(f'code must contain numbers only, you have {counter} more tries.')
                                counter -= 1
                                new_code = getpass.getpass('Please enter your new 4 digits code\n',)
                            try:
                                
                                curr_acc.change_pin(new_code)
                            except Exception as e:
                                print('Changing secret code failed,',e)
                            to_continue = to_cont()
                            if to_continue:                      
                                user_action = check_action(account['name'])
                            else:
                                break
                        elif user_action == '5':
                            curr_acc.show_balance()
                            to_continue = to_cont()
                            if to_continue:                      
                                user_action = check_action(account['name'])
                            else:
                                break
                        else:
                            print('Invalid input, leaving accounts page.')
                            break
                
        if not access_grant:
            print('User information was not found or not true.')
        input('Press enter to continue...')
                            
    elif start_program == '0': #stop program
        print("Good Bye :)")
        break