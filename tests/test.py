def test_account_create():
    from account import Account
    a = Account("test")
    assert a.address == "test"
