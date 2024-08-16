# bank/queries.py

from bank.models import Person, BankAccount
from django.db import transaction
from django.db.models import F, Sum

# 1. List the owner of each account and its balance
def list_account_owners():
    accounts = BankAccount.objects.select_related('person').all()
    for account in accounts:
        print(f"Owner: {account.person.first_name} {account.person.last_name}, Balance: {account.balance}")

# 2. Get the account with the highest balance
def account_with_max_balance():
    max_balance_account = BankAccount.objects.order_by('-balance').first()
    print(f"Account ID: {max_balance_account.account_id}, Balance: {max_balance_account.balance}")

# 3. Get the 5 accounts with the lowest balance
def five_accounts_with_min_balance():
    min_balance_accounts = BankAccount.objects.order_by('balance')[:5]
    for account in min_balance_accounts:
        print(f"Account ID: {account.account_id}, Balance: {account.balance}")

# 4. Transfer funds between accounts
@transaction.atomic
def transfer_funds(source_account_id, target_account_id, amount):
    source_account = BankAccount.objects.select_for_update().get(account_id=source_account_id)
    target_account = BankAccount.objects.select_for_update().get(account_id=target_account_id)

    if source_account.balance >= amount:
        source_account.balance -= amount
        target_account.balance += amount

        source_account.save()
        target_account.save()
        print("Transfer successful")
    else:
        print("Insufficient funds")

# 5. List accounts where the account ID is greater than the balance
def list_accounts_with_id_greater_than_balance():
    accounts = BankAccount.objects.filter(account_id__gt=F('balance'))
    for account in accounts:
        print(f"Account ID: {account.account_id}, Balance: {account.balance}")

# 6. List accounts where the owner's national code is greater than the balance
def list_accounts_with_national_code_greater_than_balance():
    accounts = BankAccount.objects.filter(person__national_code__gt=F('balance'))
    for account in accounts:
        print(f"Account ID: {account.account_id}, Balance: {account.balance}")

# 7. Accounts with balance greater than 10 million or less than 1 million
def accounts_with_specific_balance_ranges():
    # Without Index
    accounts = BankAccount.objects.filter(balance__gt=10000000) | BankAccount.objects.filter(balance__lt=1000000)
    for account in accounts:
        print(f"Account ID: {account.account_id}, Balance: {account.balance}")

    # Adding index on balance column
    from django.db import connection
    with connection.schema_editor() as schema_editor:
        schema_editor.execute("CREATE INDEX balance_index ON bank_bankaccount (balance)")

    # Query after indexing
    accounts = BankAccount.objects.filter(balance__gt=10000000) | BankAccount.objects.filter(balance__lt=1000000)
    for account in accounts:
        print(f"Account ID: {account.account_id}, Balance: {account.balance}")

# 8. Get the total balance for each person in the bank
def total_balance_per_person():
    people_balances = Person.objects.annotate(total_balance=Sum('accounts__balance'))
    for person in people_balances:
        print(f"Person: {person.first_name} {person.last_name}, Total Balance: {person.total_balance}")
