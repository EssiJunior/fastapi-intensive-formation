import pytest
from application.cal import add,subs,div,mult

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("a,b,expected", [
    (3,2,5),
    (5,5,10),
    (1,2,3)
])
def test_add(a,b,expected):
    print("Testing...")
    assert add(a,b) == expected 
    
def test_subs():
    print("Testing...")
    assert subs(2,5) == -3 

def test_div():
    print("Testing...")
    assert div(5,5) == 1

class BankAccount:
    def __init__ (self, amount=0):
        self.amount = amount
    def remove(self, amount):
        self.amount -= amount
    def deposit(self, amount):
        self.amount += amount
        
def test_init_account(bank_account):
    assert bank_account.amount == 50

def test_DEPOSIT(bank_account):
    bank_account.deposit(10)
    assert bank_account.amount == 60

def test_remove(bank_account):
    bank_account.remove(10)
    assert bank_account.amount == 40