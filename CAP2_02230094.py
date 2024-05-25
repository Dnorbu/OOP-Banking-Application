#Dorji Norbu
# first year ECE 
# module code: CSF101

import random  # Import random module to generate random account numbers
import os  # Import os module for file manipulation


# Define Account class
class Account:
    def __init__(self, account_number, password, account_type, balance=0):
        """
        Constructor to initialize account attributes
        :param account_number: Unique account number
        :param password: Password for the account
        :param account_type: Type of the account (Personal/Business)
        :param balance: Initial balance of the account (default is 0)
        """
        self.account_number = account_number  # Initialize account number
        self.password = password  # Initialize password
        self.account_type = account_type  # Initialize account type
        self.balance = balance  # Initialize balance

    def deposit(self, amount):
        """
        Method to deposit money into the account
        :param amount: Amount of money to deposit
        """
        self.balance += amount  # Increase balance by the deposit amount
        print(f"Deposited Nu.{amount}. Your new balance is Nu.{self.balance}")

    def withdraw(self, amount):
        """
        Method to withdraw money from the account
        :param amount: Amount of money to withdraw
        :return: True if withdrawal is successful, False if insufficient funds
        """
        if self.balance >= amount:
            self.balance -= amount  # Decrease balance by the withdrawal amount
            print(f"Withdrew Nu.{amount}. Your new balance is Nu.{self.balance}")
            return True
        else:
            print("Insufficient funds")
            return False  # Withdrawal unsuccessful due to insufficient funds

    def __str__(self):
        """
        String representation of the account
        :return: String containing account details
        """
        return f"Account Number: {self.account_number}\nAccount Type: {self.account_type}\nBalance: Nu.{self.balance}"


# Define Bank class
class Bank:
    def __init__(self):
        """
        Constructor to initialize the bank with an empty dictionary of accounts
        """
        self.accounts = {}

    def create_account(self, account_type):
        """
        Method to create a new account
        :param account_type: Type of the account (Personal/Business)
        :return: Created Account object
        """
        account_number = random.randint(100000000, 999999999)  # Generate a random account number
        password = input("Create a password: ")  # Ask user to create a password
        account = Account(account_number, password, account_type)
        self.accounts[account_number] = account  # Add the account to the dictionary
        self.save_account_info(account)  # Save account information to file
        return account

    def save_account_info(self, account):
        """
        Method to save account information to a file
        :param account: Account object to save
        """
        with open("accounts.txt", "a") as file:
            file.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n")

    def load_accounts(self):
        """
        Method to load accounts from file into memory
        """
        if os.path.exists("accounts.txt"):  # Check if file exists
            with open("accounts.txt", "r") as file:  # Open the file in read mode
                lines = file.readlines()  # Read all lines from the file
                for line in lines:  # Iterate over each line in the lines list
                    account_data = line.strip().split(",")  # Split each line into account data using comma as delimiter
                    account_number, password, account_type, balance = account_data  # Unpack the account data
                    # Create a new Account object with the unpacked data and add it to the accounts dictionary
                    self.accounts[int(account_number)] = Account(
                        int(account_number), password, account_type, float(balance)
                    )

    def authenticate(self, account_number, password):
        """
        Method to authenticate a user based on account number and password
        :param account_number: Account number to authenticate
        :param password: Password to authenticate
        :return: Account object if authentication is successful, None otherwise
        """
        account = self.accounts.get(account_number)
        if account and account.password == password:  # Check if the password entered matches the stored password
            return account
        else:
            return None

    def delete_account(self, account_number):
        """
        Method to delete an account
        :param account_number: Account number to delete
        """
        if account_number in self.accounts:  # Check if the account exists in self.accounts
            del self.accounts[account_number]  # Delete the account from the dictionary
            self.update_file()  # Update the file to reflect the deletion

    def update_file(self):
        """
        Method to update the file with account information
        """
        with open("accounts.txt", "w") as file:  # Open the file in write mode to overwrite with updated information
            for account_number, account in self.accounts.items():  # Iterate over each account in the dictionary
                file.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n")  # Write each account's information to the file

    def transfer_money(self, sender_account_number, receiver_account_number, amount):
        """
        Method to transfer money from one account to another
        :param sender_account_number: Account number of the sender
        :param receiver_account_number: Account number of the receiver
        :param amount: Amount of money to transfer
        """
        sender_account = self.accounts.get(sender_account_number)
        receiver_account = self.accounts.get(receiver_account_number)
        if sender_account and receiver_account:
            if sender_account.balance >= amount:
                sender_account.withdraw(amount)  # Withdraw amount from sender's account
                receiver_account.deposit(amount)  # Deposit amount into receiver's account
                self.update_file()  # Update the file to reflect the transfer
                print("Transfer successful.")
                print(f"Transferred Nu.{amount} to account {receiver_account.account_number}")
            else:
                print("Insufficient funds.")
        else:
            print("One or both accounts do not exist.")


# Define main function
def main():
    bank = Bank()  # Create a Bank object
    bank.load_accounts()  # Load existing accounts from file

    while True:  # Banking application loop
        print("\nWelcome to the Bank of Bhutan!")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice option number: ")

        if choice == "1":
            account_type = input("Enter account type (Personal/Business): ").capitalize()  # Ask for the type of account
            name = input("Enter your full name: ")
            account = bank.create_account(account_type)  # Create a new account
            print("Your account is created successfully! Thank you!")
            print(f"Mr/Mrs. {name}, your account number is: {account.account_number}")
            print(f"Mr/Mrs. {name}, your password is: {account.password}")

        elif choice == "2":
            account_number = int(input("Enter account number: "))
            password = input("Enter your password: ")
            account = bank.authenticate(account_number, password)  # Authenticate the user
            if account:
                print("Your login was successful!")
                while True:
                    print("\n1. Check Balance")  # Options after login
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Delete Account")
                    print("5. Transfer Money")
                    print("6. Logout")
                    option = input("Enter your choice: ")

                    if option == "1":
                        print(account)  # Print account details

                    elif option == "2":
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)  # Deposit money into account
                        bank.update_file()  # Update file with new balance

                    elif option == "3":
                        amount = float(input("Enter amount to withdraw: "))
                        if account.withdraw(amount):  # Withdraw money from account
                            bank.update_file()  # Update file with new balance

                    elif option == "4":
                        confirm = input("Are you sure you want to delete your account? (yes/no): ")
                        if confirm.lower() == "yes":
                            bank.delete_account(account_number)  # Delete the account
                            print("Account deleted successfully.")
                            break

                    elif option == "5":
                        receiver_account_number = int(input("Enter receiver's account number: "))
                        amount = float(input("Enter amount to transfer: "))
                        bank.transfer_money(account_number, receiver_account_number, amount)  # Transfer money

                    elif option == "6":
                        print("Logged out successfully.")
                        break

                    else:
                        print("Invalid option!")

            else:
                print("Invalid account number or password!")

        elif choice == "3":
            print("Thank you for visiting the Bank of Bhutan. Goodbye!")
            break  # Exit the loop

        else:
            print("Invalid choice!")


if __name__ == "__main__":  # Check if the script is being run directly by the interpreter
    main()
