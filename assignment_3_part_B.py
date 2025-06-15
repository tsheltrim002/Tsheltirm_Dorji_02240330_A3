import unittest
from banking_app import BankAccount, BankingApp, InsufficientFundsError, InvalidAmountError, InvalidAccountError

class TestBankAccount(unittest.TestCase):
    """Tests for BankAccount class"""
    
    def setUp(self):
        """Set up a test account"""
        self.account = BankAccount("12345", "Test User", 1000.0)
    
    def test_deposit_valid(self):
        """Test valid deposit"""
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500.0)
    
    def test_deposit_negative(self):
        """Test negative deposit amount"""
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(-100)
    
    def test_deposit_zero(self):
        """Test zero deposit amount"""
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(0)
    
    def test_withdraw_valid(self):
        """Test valid withdrawal"""
        self.account.withdraw(500)
        self.assertEqual(self.account.balance, 500.0)
    
    def test_withdraw_insufficient_funds(self):
        """Test withdrawal with insufficient funds"""
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(1500)
    
    def test_withdraw_negative(self):
        """Test negative withdrawal amount"""
        with self.assertRaises(InvalidAmountError):
            self.account.withdraw(-100)
    
    def test_transfer_valid(self):
        """Test valid transfer"""
        target = BankAccount("67890", "Target User", 500.0)
        self.account.transfer(target, 300)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(target.balance, 800.0)
    
    def test_transfer_insufficient_funds(self):
        """Test transfer with insufficient funds"""
        target = BankAccount("67890", "Target User", 500.0)
        with self.assertRaises(InsufficientFundsError):
            self.account.transfer(target, 1500)
    
    def test_transfer_invalid_account(self):
        """Test transfer to invalid account"""
        with self.assertRaises(InvalidAccountError):
            self.account.transfer("not_an_account", 100)
    
    def test_top_up_valid(self):
        """Test valid mobile top-up"""
        self.account.top_up_mobile(100)
        self.assertEqual(self.account.balance, 900.0)
        self.assertEqual(self.account.mobile_balance, 100.0)
    
    def test_top_up_insufficient_funds(self):
        """Test top-up with insufficient funds"""
        with self.assertRaises(InsufficientFundsError):
            self.account.top_up_mobile(1500)
    
    def test_top_up_negative(self):
        """Test negative top-up amount"""
        with self.assertRaises(InvalidAmountError):
            self.account.top_up_mobile(-100)

class TestBankingApp(unittest.TestCase):
    """Tests for BankingApp class"""
    
    def setUp(self):
        """Set up banking app with test accounts"""
        self.app = BankingApp()
    
    def test_get_valid_account(self):
        """Test retrieving valid account"""
        account = self.app.get_account("1001")
        self.assertEqual(account.account_holder, "Alice Smith")
    
    def test_get_invalid_account(self):
        """Test retrieving invalid account"""
        with self.assertRaises(InvalidAccountError):
            self.app.get_account("9999")
    
    def test_process_deposit(self):
        """Test processing valid deposit"""
        result = self.app.process_user_input("deposit", "1001", {"amount": "500"})
        self.assertIn("Deposited $500.00", result)
        self.assertIn("$1500.00", result)
    
    def test_process_invalid_deposit(self):
        """Test processing invalid deposit"""
        with self.assertRaises(InvalidAmountError):
            self.app.process_user_input("deposit", "1001", {"amount": "-100"})
    
    def test_process_withdraw(self):
        """Test processing valid withdrawal"""
        result = self.app.process_user_input("withdraw", "1001", {"amount": "500"})
        self.assertIn("Withdrew $500.00", result)
        self.assertIn("$500.00", result)
    
    def test_process_invalid_withdraw(self):
        """Test processing invalid withdrawal"""
        with self.assertRaises(InsufficientFundsError):
            self.app.process_user_input("withdraw", "1001", {"amount": "2000"})
    
    def test_process_transfer(self):
        """Test processing valid transfer"""
        data = {"amount": "300", "target_account": "1002"}
        result = self.app.process_user_input("transfer", "1001", data)
        self.assertIn("Transferred $300.00 to account 1002", result)
        self.assertIn("$700.00", result)
    
    def test_process_invalid_transfer(self):
        """Test processing invalid transfer"""
        data = {"amount": "2000", "target_account": "1002"}
        with self.assertRaises(InsufficientFundsError):
            self.app.process_user_input("transfer", "1001", data)
    
    def test_process_top_up(self):
        """Test processing valid mobile top-up"""
        result = self.app.process_user_input("top_up", "1001", {"amount": "100"})
        self.assertIn("Topped up mobile with $100.00", result)
        self.assertIn("Account Balance: $900.00", result)
        self.assertIn("Mobile Credit: $100.00", result)
    
    def test_process_invalid_top_up(self):
        """Test processing invalid mobile top-up"""
        with self.assertRaises(InsufficientFundsError):
            self.app.process_user_input("top_up", "1001", {"amount": "2000"})
    
    def test_process_invalid_choice(self):
        """Test processing invalid menu choice"""
        with self.assertRaises(InvalidChoiceError):
            self.app.process_user_input("invalid_choice", "1001", {})

if __name__ == "__main__":
    unittest.main()