from collections import UserDict
import re
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self.value = value  # Використовуйте сеттер для ініціалізації значення

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must contain 10 digits.")
        self._value = value

    @staticmethod
    def validate(phone):
        return bool(re.match(r"^\d{10}$", phone))


class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not self.validate(value):
            raise ValueError("Birthday must be in the format YYYY-MM-DD.")
        self._value = value

    @staticmethod
    def validate(birthday):
        try:
            datetime.strptime(birthday, '%Y-%m-%d')
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        found = False
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                found = True
                break

        if not found:
            raise ValueError(f"No phone number {old_phone} found to edit.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def days_to_birthday(self):
        if not self.birthday:
            raise ValueError("Birthday is not set for this contact.")
        
        now = datetime.now()
        bday = datetime.strptime(self.birthday.value, '%Y-%m-%d').replace(year=now.year)
        
        if bday < now:
            bday = bday.replace(year=now.year + 1)
        
        return (bday - now).days

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}" + (f", birthday: {self.birthday.value}" if self.birthday else "")

import pickle

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, n):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i:i + n]
    def save(self, filename='addressbook.pickle'):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load(self, filename='addressbook.pickle'):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self.data = {}

    def search(self, search_string):
        search_results = AddressBook()
        for name, record in self.data.items():
            if search_string.lower() in name.lower():
                search_results.add_record(record)
            else:
                for phone in record.phones:
                    if search_string in phone.value:
                        search_results.add_record(record)
                        break
        return search_results

book = AddressBook()

john_record = Record("John", "1990-01-01")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Print all records
for record in book.iterator(1):
    print(record)

# Days to John's next birthday
print(john_record.days_to_birthday())

# Зберігаємо адресну книгу на диск
book.save()

# Відновлюємо адресну книгу з диска
book.load()

# Демонструємо пошук
search_query = "123"  # Припустимо, ви шукаєте записи, що містять "123"
found_records = book.search(search_query)
for name, record in found_records.items():
    print(record)
