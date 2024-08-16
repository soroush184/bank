# bank/management/commands/create_random_data.py

from django.core.management.base import BaseCommand
from faker import Faker
from bank.models import Person, BankAccount

class Command(BaseCommand):
    help = 'Create random data for Person and BankAccount models'

    def handle(self, *args, **kwargs):
        fake = Faker()
        people = []
        accounts = []

        for _ in range(10000):
            person = Person(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                national_code=fake.unique.numerify(text='##########')
            )
            people.append(person)

        Person.objects.bulk_create(people)

        for person in Person.objects.all():
            accounts.append(
                BankAccount(
                    person=person,
                    balance=fake.random_number(digits=7)
                )
            )
            accounts.append(
                BankAccount(
                    person=person,
                    balance=fake.random_number(digits=7)
                )
            )

        BankAccount.objects.bulk_create(accounts)

        self.stdout.write(self.style.SUCCESS('Successfully created random data'))
