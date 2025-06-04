# Imports
import random
from datetime import datetime
import sys

################# Classes #################

# Class Account: handles account information instances
class Account:
    def __init__(self, accountNumber, accountFirstName, accountLastName, accountSSN, accountPIN, accountBalance):
        self.accountNumber = accountNumber
        self.accountFirstName = accountFirstName
        self.accountLastName = accountLastName
        self.accountSSN = accountSSN
        self.accountPIN = accountPIN
        self.accountBalance = int(accountBalance)
        self.dateCreated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def deposit(self, depositCents):
        if depositCents <= 0:
            print("Deposit must be a positive amount.")
            return False
        self.accountBalance += depositCents
        print(f"Deposit successful. New balance: ${self.accountBalance / 100:.2f}")
        return True

    def withdraw(self, withdrawCents):
        if withdrawCents <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if withdrawCents > self.accountBalance:
            print("Insufficient funds.")
            return False
        self.accountBalance -= withdrawCents
        print(f"Withdrawal successful. New balance: ${self.accountBalance / 100:.2f}")
        return True

    def __str__(self):
        return (
            f"Account Number: {self.accountNumber}\n"
            f"Name: {self.accountFirstName} {self.accountLastName}\n"
            f"SSN: {self.accountSSN}\n"
            f"PIN: {self.accountPIN}\n"
            f"Balance: ${self.accountBalance / 100:.2f}\n"
            f"Date Created: {self.dateCreated}"
        )

    def isValidPin(self, pinInput):
        return self.accountPIN == pinInput

# Class Bank: handles account list and new account creation. Limit of 100 accounts.
class Bank:
    def __init__(self, capacity=100):
        self.accounts = [None] * capacity  # Fixed-size list of 100 accounts

    def addAccountToBank(self, account):
        for i in range(len(self.accounts)):
            if self.accounts[i] is None:
                self.accounts[i] = account
                return True
        print("No more accounts available")
        return False

    def removeAccountFromBank(self, account): #remove account from list
        for i in range(len(self.accounts)):
            if self.accounts[i] is not None and self.accounts[i].accountNumber == account.accountNumber:
                self.accounts[i] = None
                return

    def findAccount(self, accountNumber): #method to find account
        for account in self.accounts:
            if account is not None and account.accountNumber == accountNumber:
                return account
        return None

    def addMonthlyInterest(self): #calculate monthly interest
        apr_confirm = input("Add monthly interest to all accounts? (y/n): ")
        if apr_confirm.lower() == "y":
            try:
                apr = float(input("Enter annual interest rate (e.g., 2.75 for 2.75%): "))
                monthly_rate = apr / 12 / 100
                for account in self.accounts:
                    if account is not None:
                        interest = int(account.accountBalance * monthly_rate)
                        account.accountBalance += interest
                        print(f"Added ${interest / 100:.2f} interest to account {account.accountNumber}")
            except ValueError:
                print("Invalid APR entered.")
        else:
            print("Interest addition cancelled.")

    def create_new_account(self):
        # Generate unique account number
        while True:
            accountNumber = random.randint(10000000, 99999999)
            if not self.findAccount(accountNumber):
                break
        firstName = input("Enter your first name: ")
        lastName = input("Enter your last name: ")
        ssn = 'XXX-XX-' + NewAcctSSN()
        pin = newAcctPIN()
        balance = InitialDeposit()

        new_account = Account(accountNumber, firstName, lastName, ssn, pin, balance)
        
        if self.addAccountToBank(new_account):
            return new_account
        else:
            return None

# Class CoinCollector: handles coin deposits with dictionary
class CoinCollector:
    def __init__(self):
        self.coin_values = {
            "P": 1,
            "N": 5,
            "D": 10,
            "Q": 25,
            "H": 50,
            "W": 100
        }

    def parseChange(self, coin_string: str) -> int:
        total = 0
        for coin in coin_string.upper():
            if coin in self.coin_values:
                total += self.coin_values[coin]
        return total

# Class BankManager: handles new visitor experience with app. Displays initial menu to log in, sign up or exit.
class BankManager:
    @staticmethod
    def main():
        myBank = Bank()
        while True:
            print("""~~~~ : Welcome to our banking app! : ~~~~
What do you want to do?
1  - Log In
2  - Sign up
3  - Exit""")
            try:
                visitorInput = int(input("Select an option: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if visitorInput > 3 or visitorInput < 1:
                print("Invalid entry. Please try again.")
            elif visitorInput == 1: #use PIN and last 4 of SSN to log in
                login(myBank)
            elif visitorInput == 2: #create new account process
                print("~~~~: Apply for Account :~~~~")
                new_account = myBank.create_new_account()
                if new_account:
                    print("~~~~ Account approved! ~~~~")
                    print("Your account details:")
                    print(new_account)
                else:
                    print("Account creation failed.")
            elif visitorInput == 3: #exit program
                print("Exiting Program.")
                sys.exit()

    @staticmethod
    def bank_menu(matched_account, myBank):
        """Main menu after login for the authenticated user."""
        while True: #main bank menu options print
            print("""
~~~~ : Bank Options : ~~~~
1 - Open another account
2 - Get Account information and balance
3 - Change PIN
4 - Deposit Money
5 - Transfer Money Between Accounts
6 - Withdraw Money
7 - ATM Withdrawal
8 - Deposit Change
9 - Close Account
10 - Add monthly Interest to all accounts
11 - Logout
""")
            try: #error handling
                userInput = int(input("Select an option: "))
            except ValueError:
                print("Invalid input.")
                continue

            if userInput == 1: # starts new account process
                new_account = myBank.create_new_account()
                if new_account:
                    print("New account created successfully.")
                    print(new_account)
                else:
                    print("Failed to create new account.")
            
            elif userInput == 2: #validates account number, and pin number
                acct_number = input("Enter an account number: ")
                try:
                    account = myBank.findAccount(int(acct_number))
                    if account:
                        pinInput = input("Enter PIN: ")
                        if account.isValidPin(pinInput):
                            print(account)
                        else:
                            print("Invalid PIN.")
                    else:
                        print("Account not found.")
                except ValueError:
                    print("Invalid account number.")

            elif userInput == 3: #change PIN
                acct_number = input("Enter an account number: ")
                try:
                    account = myBank.findAccount(int(acct_number)) #validate acct number
                    if account:
                        pinInput = input("Enter current PIN: ")
                        if account.isValidPin(pinInput):
                            while True:
                                new_pin1 = input("Enter new PIN: ") #new pin
                                new_pin2 = input("Confirm new PIN: ") #conf new pin
                                if new_pin1 == new_pin2 and len(new_pin1) == 4 and new_pin1.isdigit():
                                    account.accountPIN = new_pin2
                                    print("PIN updated.")
                                    break
                                else:
                                    print("PIN did not match or format was incorrect. Try again.") #error handling
                        else:
                            print("Invalid current PIN.")
                    else:
                        print("Account not found.")
                except ValueError:
                    print("Invalid account number.")

            elif userInput == 4: #deposit to acct
                acct_number = input("Enter an account number: ")
                try:
                    account = myBank.findAccount(int(acct_number))
                    if account:
                        pinInput = input("Enter PIN: ")
                        if account.isValidPin(pinInput):
                            try:
                                deposit_input = float(input("Enter amount to deposit in dollars and cents (e.g. 2.57): "))
                                if deposit_input <= 0:
                                    print("Amount cannot be negative.")
                                else:
                                    account.deposit(int(round(deposit_input * 100)))
                            except ValueError:
                                print("Invalid amount.")
                        else:
                            print("Invalid PIN.")
                    else:
                        print("Account not found.")
                except ValueError:
                    print("Invalid account number.")

            elif userInput == 5: #transfer between two accts
                tnsfrFrom = input("Enter the account number to transfer from: ")
                try:
                    from_account = myBank.findAccount(int(tnsfrFrom))
                    if not from_account:
                        print("Source account not found.")
                        continue
                    from_pin = input(f"Enter the PIN for account {tnsfrFrom}: ")
                    if not from_account.isValidPin(from_pin):
                        print("Invalid PIN for source account.")
                        continue

                    tnsfrTo = input("Enter the account number to transfer to: ")
                    to_account = myBank.findAccount(int(tnsfrTo))
                    if not to_account:
                        print("Destination account not found.")
                        continue
                    to_pin = input(f"Enter the PIN for account {tnsfrTo}: ")
                    if not to_account.isValidPin(to_pin):
                        print("Invalid PIN for destination account.")
                        continue

                    try:
                        tnsfrAmount = float(input("Enter amount to transfer in dollars and cents (e.g. 2.57): "))
                        if tnsfrAmount <= 0:
                            print("Amount must be positive.")
                        else:
                            tnsfrCents = int(round(tnsfrAmount * 100))
                            if from_account.accountBalance < tnsfrCents:
                                print("Insufficient funds.")
                            else:
                                from_account.accountBalance -= tnsfrCents
                                to_account.accountBalance += tnsfrCents
                                print(f"Successfully transferred ${tnsfrAmount:.2f} to account {to_account.accountNumber}.")
                                print(f"New balance of source account: ${from_account.accountBalance / 100:.2f}")
                    except ValueError:
                        print("Invalid amount.")
                except ValueError:
                    print("Invalid account number.")

            elif userInput == 6: #withdraw from acct
                acct_number = input("Enter an account number: ")
                try:
                    account = myBank.findAccount(int(acct_number))
                    if account:
                        pinInput = input("Enter current PIN: ")
                        if account.isValidPin(pinInput):
                            try:
                                withdraw_input = float(input("Enter an amount to withdraw in dollars and cents (e.g. 2.57): "))
                                if withdraw_input <= 0:
                                    print("Amount must be positive.")
                                else:
                                    account.withdraw(int(round(withdraw_input * 100)))
                            except ValueError:
                                print("Invalid amount entered.")
                        else:
                            print("Invalid PIN.")
                    else:
                        print("Account not found.")
                except ValueError:
                    print("Invalid account number.")

            elif userInput == 7: #ATM withdrawal
                acct_number = input("Enter an account number: ")
                try:
                    account = myBank.findAccount(int(acct_number))
                    if account:
                        pinInput = input("Enter current PIN: ")
                        if account.isValidPin(pinInput):
                            try:
                                withdraw_input = int(input("Enter an amount to withdraw in dollars (no cents) in multiples of $5 (limit: $1000): "))
                                if withdraw_input < 5 or withdraw_input > 1000 or withdraw_input % 5 != 0:
                                    print("Invalid amount. Must be a multiple of $5 between $5 and $1000.")
                                else:
                                    withdraw_cents = withdraw_input * 100
                                    if withdraw_cents > account.accountBalance:
                                        print("Insufficient funds.")
                                    else:
                                        account.accountBalance -= withdraw_cents
                                        bills = [20, 10, 5]
                                        breakdown = {}
                                        remaining = withdraw_input
                                        for bill in bills:
                                            count = remaining // bill
                                            if count:
                                                breakdown[bill] = count
                                                remaining %= bill
                                        print("Dispense the following bills:")
                                        for bill, count in breakdown.items():
                                            print(f"Number of ${bill} bills: {count}")
                                        print(f"New balance: ${account.accountBalance / 100:.2f}")
                            except ValueError:
                                print("Invalid input. Please enter a whole number.")
                        else:
                            print("Invalid PIN.")
                    else:
                        print("Account not found.")
                except ValueError:
                    print("Invalid account number.")

            elif userInput == 8: #Coin parser
                acct_number = input("Enter an account number: ")
                try:
                    account = myBank.findAccount(int(acct_number))
                    if account:
                        pinInput = input("Enter current PIN: ")
                        if account.isValidPin(pinInput):
                            coin_input = input("Deposit coins (P=penny, N=nickel, D=dime, Q=quarter, H=half-dollar, W=dollar): ").upper()
                            change_machine = CoinCollector()
                            total_cents = change_machine.parseChange(coin_input)
                            valid_chars = set(change_machine.coin_values.keys())
                            invalid_coins = [ch for ch in coin_input if ch not in valid_chars]
                            if invalid_coins:
                                print(f"Ignored invalid coins: {' '.join(invalid_coins)}")
                            if total_cents > 0:
                                account.deposit(total_cents)
                            else:
                                print("No valid coins entered. Deposit canceled.")
                        else:
                            print("Invalid PIN.")
                    else:
                        print("Account not found.")
                except ValueError:
                    print("Invalid account number.")

            elif userInput == 9: #Account closure
                acct_number = input("Enter an account number: ")
                try:
                    account = myBank.findAccount(int(acct_number))
                    if account:
                        pinInput = input("Enter current PIN: ")
                        if account.isValidPin(pinInput):
                            myBank.removeAccountFromBank(account)
                            print("Account closed.")
                        else:
                            print("Invalid PIN.")
                    else:
                        print("Account not found.")
                except ValueError:
                    print("Invalid account number.")

            elif userInput == 10:
                myBank.addMonthlyInterest()

            elif userInput == 11:
                print("Logging out...")
                break

# addtl Functions

def NewAcctSSN(): 
    while True:
        SSNInput = input("Enter your 9-digit SSN (no dashes): ")
        if len(SSNInput) == 9 and SSNInput.isdigit():
            return SSNInput[5:]
        else:
            print("Invalid SSN. Please enter exactly 9 digits with no dashes.")

def newAcctPIN():
    while True:
        PINInput = input("Select a 4 digit PIN: ")
        PINConf = input("Please confirm your 4 digit PIN: ")
        if len(PINInput) == 4 and PINInput.isdigit() and PINInput == PINConf:
            return PINInput
        elif PINInput != PINConf:
            print("PIN Confirmation does not match. Please try again.")
        else:
            print("Invalid PIN #. Please try again.")

def InitialDeposit():
    while True:
        Init = input("Enter an initial deposit for your account: ")
        try:
            amount = float(Init)
            if amount < 0:
                print("Deposit must be a positive number.")
            else:
                return int(amount * 100)
        except ValueError:
            print("Invalid input. Please enter a number.")

def login(myBank):
    while True:
        print("~~~~: User Login :~~~~")
        visAcc = input("Enter the last 4 digits of your SSN: ")

        # Validate input to ensure it's exactly 4 digits
        if not visAcc.isdigit() or len(visAcc) != 4:
            print("Invalid input. Please enter exactly 4 digits.")
            continue

        matched_account = None
        for acc in myBank.accounts:
            if acc and acc.accountSSN[-4:] == visAcc:
                matched_account = acc
                break

        if not matched_account:
            print("\nUser does not exist.\n")
            print("1 - Try again")
            print("2 - Return to main menu")
            print("3 - Exit Program")
            userDNE = input("Make a selection: ")
            if userDNE == "2":
                return
            elif userDNE == "3":
                print("Exiting program.")
                sys.exit()
            else:
                continue

        visPin = input("Enter your PIN: ")
        if matched_account.isValidPin(visPin):
            print("Login successful.")
            BankManager.bank_menu(matched_account, myBank)
            break
        else:
            print("Incorrect PIN.")
            print("1 - Try again")
            print("2 - Return to main menu")
            print("3 - Exit Program")
            userOption = input("Make a selection: ")
            if userOption == "2":
                return
            elif userOption == "3":
                print("Exiting program.")
                sys.exit()
            else:
                continue

# Run the program
if __name__ == "__main__":
    BankManager.main()