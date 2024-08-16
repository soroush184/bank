# bank/models.py

from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.national_code}"


class BankAccount(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='accounts')
    account_id = models.AutoField(primary_key=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"Account ID: {self.account_id}, Balance: {self.balance}"
