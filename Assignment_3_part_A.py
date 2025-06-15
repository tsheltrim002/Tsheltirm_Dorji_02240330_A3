import tkinter as tk
from tkinter import messagebox

# Custom Exceptions
class BankingException(Exception):
    """Base class for banking exceptions"""
    pass

class InsufficientFundsError(BankingException):
    """Raised when account has insufficient funds"""
    pass

class InvalidAmountError(BankingException):
    """Raised when an invalid amount is entered"""
    pass

class InvalidChoiceError(BankingException):
    """Raised when an invalid menu choice is made"""
    pass

class InvalidAccountError(BankingException):
    """Raised when an invalid account is referenced"""
    pass

class BankAccount:
    """Represents a bank account with basic operations"""
    def __init__(self, account_number, account_holder, balance=0.0, mobile_balance=0.0):
        """
        Initialize a bank account
        
        Args:
            account_number (str): Unique account identifier
            account_holder (str): Account holder's name
            balance (float): Initial account balance
            mobile_balance (float): Initial mobile credit balance
        """
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        self.mobile_balance = mobile_balance
    
    def deposit(self, amount):
        """
        Deposit money into the account
        
        Args:
            amount (float): Amount to deposit
            
        Raises:
            InvalidAmountError: If amount is not positive
        """
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")
        self.balance += amount
    
    def withdraw(self, amount):
        """
        Withdraw money from the account
        
        Args:
            amount (float): Amount to withdraw
            
        Raises:
            InvalidAmountError: If amount is not positive
            InsufficientFundsError: If account has insufficient funds
        """
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds for withdrawal")
        self.balance -= amount
    
    def transfer(self, target_account, amount):
        """
        Transfer money to another account
        
        Args:
            target_account (BankAccount): Account to receive funds
            amount (float): Amount to transfer
            
        Raises:
            InvalidAmountError: If amount is not positive
            InsufficientFundsError: If account has insufficient funds
            InvalidAccountError: If target account is invalid
        """
        if not isinstance(target_account, BankAccount):
            raise InvalidAccountError("Invalid target account")
        if amount <= 0:
            raise InvalidAmountError("Transfer amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds for transfer")
        
        self.balance -= amount
        target_account.balance += amount
    
    def top_up_mobile(self, amount):
        """
        Top up mobile credit from account balance
        
        Args:
            amount (float): Amount to top up
            
        Raises:
            InvalidAmountError: If amount is not positive
            InsufficientFundsError: If account has insufficient funds
        """
        if amount <= 0:
            raise InvalidAmountError("Top-up amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds for mobile top-up")
        
        self.balance -= amount
        self.mobile_balance += amount
    
    def get_balance(self):
        """Get current account balance"""
        return self.balance
    
    def get_mobile_balance(self):
        """Get current mobile credit balance"""
        return self.mobile_balance
    
    def __str__(self):
        """String representation of account"""
        return (f"Account: {self.account_number}\n"
                f"Holder: {self.account_holder}\n"
                f"Balance: ${self.balance:.2f}\n"
                f"Mobile Credit: ${self.mobile_balance:.2f}")

class BankingApp:
    """Handles core banking operations"""
    def __init__(self):
        """Initialize banking application with sample accounts"""
        self.accounts = {
            "1001": BankAccount("1001", "Alice Smith", 1000.0),
            "1002": BankAccount("1002", "Bob Johnson", 1500.0),
            "1003": BankAccount("1003", "Charlie Brown", 500.0)
        }
    
    def get_account(self, account_number):
        """
        Retrieve account by number
        
        Args:
            account_number (str): Account number
            
        Returns:
            BankAccount: The account object
            
        Raises:
            InvalidAccountError: If account doesn't exist
        """
        account = self.accounts.get(account_number)
        if not account:
            raise InvalidAccountError(f"Account {account_number} not found")
        return account
    
    def process_user_input(self, choice, account_number, data):
        """
        Process user banking operations
        
        Args:
            choice (str): Menu choice
            account_number (str): Account to operate on
            data (dict): Additional operation data
            
        Returns:
            str: Operation result message
            
        Raises:
            BankingException: For any banking errors
        """
        account = self.get_account(account_number)
        
        if choice == "deposit":
            amount = float(data["amount"])
            account.deposit(amount)
            return f"Deposited ${amount:.2f}. New balance: ${account.balance:.2f}"
        
        elif choice == "withdraw":
            amount = float(data["amount"])
            account.withdraw(amount)
            return f"Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}"
        
        elif choice == "balance":
            return (f"Account Balance: ${account.balance:.2f}\n"
                    f"Mobile Credit: ${account.mobile_balance:.2f}")
        
        elif choice == "transfer":
            target_account = self.get_account(data["target_account"])
            amount = float(data["amount"])
            account.transfer(target_account, amount)
            return (f"Transferred ${amount:.2f} to account {target_account.account_number}\n"
                    f"New balance: ${account.balance:.2f}")
        
        elif choice == "top_up":
            amount = float(data["amount"])
            account.top_up_mobile(amount)
            return (f"Topped up mobile with ${amount:.2f}\n"
                    f"Account Balance: ${account.balance:.2f}\n"
                    f"Mobile Credit: ${account.mobile_balance:.2f}")
        
        else:
            raise InvalidChoiceError("Invalid operation choice")

class BankingGUI:
    """Provides a graphical interface for banking operations"""
    def __init__(self, root):
        """
        Initialize the banking GUI
        
        Args:
            root (tk.Tk): Root window
        """
        self.root = root
        self.root.title("Banking Application")
        self.banking_app = BankingApp()
        
        # Create widgets
        self.create_widgets()
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Account selection
        tk.Label(self.root, text="Account Number:").grid(row=0, column=0, padx=5, pady=5)
        self.account_entry = tk.Entry(self.root)
        self.account_entry.grid(row=0, column=1, padx=5, pady=5)
        self.account_entry.insert(0, "1001")
        
        # Operation selection
        tk.Label(self.root, text="Operation:").grid(row=1, column=0, padx=5, pady=5)
        self.operation_var = tk.StringVar(value="balance")
        operations = [
            ("Check Balance", "balance"),
            ("Deposit", "deposit"),
            ("Withdraw", "withdraw"),
            ("Transfer", "transfer"),
            ("Top Up Mobile", "top_up")
        ]
        
        for i, (text, value) in enumerate(operations):
            rb = tk.Radiobutton(
                self.root, 
                text=text, 
                variable=self.operation_var, 
                value=value
            )
            rb.grid(row=2+i, column=0, columnspan=2, sticky="w", padx=5)
        
        # Amount input
        tk.Label(self.root, text="Amount:").grid(row=7, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=7, column=1, padx=5, pady=5)
        
        # Target account for transfer
        tk.Label(self.root, text="Target Account:").grid(row=8, column=0, padx=5, pady=5)
        self.target_entry = tk.Entry(self.root)
        self.target_entry.grid(row=8, column=1, padx=5, pady=5)
        
        # Execute button
        self.execute_btn = tk.Button(
            self.root, 
            text="Execute", 
            command=self.execute_operation
        )
        self.execute_btn.grid(row=9, column=0, columnspan=2, pady=10)
        
        # Result display
        self.result_text = tk.Text(self.root, height=10, width=40)
        self.result_text.grid(row=10, column=0, columnspan=2, padx=5, pady=5)
        self.result_text.config(state=tk.DISABLED)
    
    def execute_operation(self):
        """Execute the selected banking operation"""
        account_number = self.account_entry.get()
        operation = self.operation_var.get()
        amount = self.amount_entry.get()
        target_account = self.target_entry.get()
        
        # Prepare data dictionary
        data = {
            "amount": amount,
            "target_account": target_account
        }
        
        try:
            # Process the operation
            result = self.banking_app.process_user_input(
                operation, 
                account_number, 
                data
            )
            self.show_result(result)
        except BankingException as e:
            self.show_error(str(e))
    
    def show_result(self, message):
        """Display operation result"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.config(state=tk.DISABLED)
    
    def show_error(self, error_message):
        """Display error message"""
        messagebox.showerror("Banking Error", error_message)

def main():
    """Run the banking application GUI"""
    root = tk.Tk()
    app = BankingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()