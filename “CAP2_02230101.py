################################
# Pema Tashi
# 1st year ECE
# 02230101
################################
# REFERENCES
# https://www.youtube.com/watch?v=BRssQPHZMrc
# https://www.freecodecamp.org/news/how-to-build-an-online-banking-system-python-oop-tutorial/
################################

import os # operating system, it helps to check if a file exist.
import random # to generate random numbers, mainly for account numbers and passwords.
import string # for string constants, like digits and letters(ascii_letters), for generating random passwords.

# Base Account class
class Account:
    def __init__(self, account_number, password, account_type, balance=0.0):  # initializing account number, password, account type and balance
        self.account_number = account_number
        self.password = password
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):  # Method deposit to add amount to the balance
        self.balance += amount
        print(f"Deposited Nu {amount}. New balance: Nu {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance: # using conditional statement so that if the amount you typed is more than the balance left in the account it will show that it is insufficient.
            print("Insufficient amount!")
        else:
            self.balance -= amount # subtracting the balance in the account by the amount the user put in.
            print(f"Withdrew Nu {amount}. New balance: Nu {self.balance}")

    def check_balance(self):
        print(f"Current balance: Nu {self.balance}") # simply printing the current balance.

    def transfer(self, target_account, amount): 
        if amount > self.balance: # if the amount you want to transfer is more than the balance you have. 
            print("Insufficient amount!")
        elif target_account is None: # if nothing is written 
            print("Target account does not exist!")
        else:
            self.balance -= amount # deducting money from the account
            target_account.balance += amount # adding the money to a target account
            print(f"Transferred Nu {amount} to account number {target_account.account_number}. balance left: Nu {self.balance}")

 #the following two classes are inherited from the Account class and initializing the base class with "Savings" or "Business" as the account type.
class SavingsAccount(Account): # Inheritance
    def __init__(self, account_number, password, balance=0.0):
        super().__init__(account_number, password, "Savings", balance)

class BusinessAccount(Account): # Inheritance
    def __init__(self, account_number, password, balance=0.0):
        super().__init__(account_number, password, "Business", balance)

class MyBankingApp: # This class is to Manage the banking operations and account data
    accounts_file = "accounts.txt" # accounts_file holds the name of the file ("accounts.txt") to store account data.

    def __init__(self): # Loads accounts from the file upon initialization.
        self.accounts = self.load_accounts()

    def load_accounts(self):
        if not os.path.exists(self.accounts_file): # os.path.exists(path) is a function from the os.path module in Python, which returns True if the file specified by path exists, and if not then False. 
            return {}

        accounts = {} # Initializes an empty dictionary called to store the loaded account information.
        with open(self.accounts_file, "r") as f:#  Opens the file self.accounts_file (i.e., "accounts.txt") in read mode ("r") and uses a with statement to ensure the file is properly closed after its contents are read.
            for line in f: 
                account_number, password, account_type, balance = line.strip().split(",") # removes any whitespace from the line and then splits the line.
                if account_type == "Savings": 
                    accounts[account_number] = SavingsAccount(account_number, password, float(balance))  # Create a SavingsAccount object and add it to the dictionary if the account type is "Savings".
                elif account_type == "Business": 
                    accounts[account_number] = BusinessAccount(account_number, password, float(balance)) # Create a BusinessAccount object and add it to the dictionary if the account type is "Business".
        return accounts

    def save_accounts(self):
        with open(self.accounts_file, "w") as f:
            for account in self.accounts.values(): # Iterates over each account 
                 # Writing the account information to the file like the format below.
                f.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n") # Each line in the file represents one account, with fields separated by commas.

    def create_account_number(self):
        return ''.join(random.choices(string.digits, k=9)) # Generates a random 9-digit account number

    def create_password(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=7)) #  Generates a random 7-character password.

    def create_account(self, account_type):
        account_number = self.create_account_number() # Generates a unique account number. 
        password = self.create_password() # Generate a random password.
    
    # Checking the account type and creating the corresponding account object(SavingsAccount and Business).
        if account_type == "Savings":
            account = SavingsAccount(account_number, password)
        elif account_type == "Business":
            account = BusinessAccount(account_number, password)
        else:
            print("Invalid account type") # Printing an error message if the account typed is invalid and return.
            return

        self.accounts[account_number] = account # Adding the new account to the self.accounts dictionary.
        self.save_accounts() # Saving the accounts data to the file.
        print(f"Your account is created. Account Number: {account_number}, Password: {password}")

    def login(self, account_number, password):
        account = self.accounts.get(account_number) #  Retrieving the account object associated with the provided account_number from the self.accounts dictionary.
        
        # Checking if the account exists and if the password is correct.
        if account and account.password == password:
            print("Login successful.")
            return account
        else:
            print(" Your account number or password is invalid.")
            return None

    def delete_account(self, account_number): # initializing delete account.

        # Checking if the account number exists in the dictionary of account.
        if account_number in self.accounts:
            del self.accounts[account_number] # deleting the account number.
            self.save_accounts() # saving the account data
            print(f"Account {account_number} has been deleted.")
        else:
            print("Account not found.") # printing error message 

    def find_account(self, account_number):
        return self.accounts.get(account_number) # Retrieving an account object by account number.

def main():
    app = MyBankingApp() # initializing banking app
    while True: # Using while loop to continuously display the main menu and handle user input until the user chooses to exit.
        print("\nPresenting to you the Banking App")
        print("1. Create New Account")
        print("2. Login")
        print("3. Exit")
        choice_1 = input("Enter your choice: ")

        if choice_1 == "1": # letting the user to enter account type and creating it.
            account_type = input("Enter account type (Savings/Business): ")
            app.create_account(account_type)
        elif choice_1 == "2": # letting the user to enter account number and password.
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            account = app.login(account_number, password)
            if account:
                while True: # if the login is successful it will allow the user to choose the following sub choice.
                    print("\n1. Check Account Balance")
                    print("2. Deposit money")
                    print("3. Withdraw money")
                    print("4. Transfer money")
                    print("5. Delete Account")
                    print("6. Logout")
                    choice_2 = input("Please enter your choice: ")

                    if choice_2 == "1":
                        account.check_balance() # checking balance
                    elif choice_2 == "2":
                        amount = float(input("Enter amount to deposit: ")) # depositing amount
                        account.deposit(amount)
                        app.save_accounts() # saving the updated account data.
                    elif choice_2 == "3":
                        amount = float(input("Enter amount to withdraw: ")) # withdrawing money.
                        account.withdraw(amount)
                        app.save_accounts()

                        # transfering money
                    elif choice_2 == "4":
                        target_account_number = input("Enter target account number: ") 
                        amount = float(input("Enter amount to transfer: "))
                        target_account = app.find_account(target_account_number) # finding the target account.
                        account.transfer(target_account, amount)
                        app.save_accounts()

                        # deleting account
                    elif choice_2 == "5":
                        app.delete_account(account_number)
                        break
                    elif choice_2 == "6": # logging out
                        break
                    else:
                        print("Invalid choice!")
        elif choice_1 == "3": # Exiting
            break
        else: # error message
            print("Invalid choice")

if __name__ == "__main__":
    main()

