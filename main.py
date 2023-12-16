from collections import UserDict
from tabulate import tabulate
from collections import defaultdict
from datetime import datetime, timedelta
from constants import MOCKED_INPUTS, TEST_RECORDS,  AVAILABLE_COMMANDS
from helpers import format_error_msg, format_success_msg, format_warning_msg, format_underline_msg, parse_input

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit():
            raise ValueError(f"Invalid phone number '{value}'. Phone number must be digits only")
        if len(value) != 10:
            raise ValueError(f"Invalid phone number '{value}'. Phone number must be 10 digits long")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Birthday cannot be empty")
        super().__init__(value)

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = None
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        return "Phone number added."
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return "Birthday added."
    
    def show_birthday(self):
        if self.birthday:
            return f"Birthday: {self.birthday}"
        
        return "No birthday set"

    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        raise KeyError(f"Phone number '{value}' not found.")

    def edit_phone(self, old_value, new_value):
        phone = self.find_phone(old_value)
        phone.value = new_value
        return "Phone number changed."

    def delete_phone(self, value):
        phone = self.find_phone(value)
        self.phones.remove(phone)
        return "Phone number deleted."

    def __str__(self):
        phone_list = '; '.join(p.value for p in self.phones) if self.phones else 'No phones'
        return f"Contact name: {self.name.value}, phones: {phone_list}"

class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value in self.data:
            raise KeyError(f"Contact '{record.name.value}' already exists.")
        self.data[record.name.value] = record
        return "Contact added."

    def find(self, name):
        if not name in self.data:
            raise KeyError(f"Contact '{name}' not found.")
        return self.data[name]

    def delete(self, name):
        if not name in self.data:
            raise KeyError(f"Contact '{name}' not found.")
        del self.data[name]
        return "Contact deleted."
    
    def get_birthdays_per_week(self):
        today = datetime.today().date()
        start_of_next_week = today + timedelta(days=7 - today.weekday())
        end_of_next_week = start_of_next_week + timedelta(days=4)

        birthdays = defaultdict(list)

        for name, record in self.data.items():
            if(record.birthday == None):
                continue

            birthday = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            day_of_week = birthday_this_year.weekday()

            if birthday_this_year >= start_of_next_week - timedelta(days=2) and birthday_this_year < start_of_next_week:
                birthdays['Monday'].append(name)
            elif start_of_next_week <= birthday_this_year <= end_of_next_week and day_of_week < 5:
                day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][day_of_week]
                birthdays[day_name].append(name)

        return birthdays
        
    def __str__(self):
        table = []
        for name, record in self.data.items():
            table.append([name, '; '.join(p.value for p in record.phones), record.birthday])
        return tabulate(table, headers=['Name', 'Phone', 'Birthday'], tablefmt='orgtbl')

class CommandHandler:
    def __init__(self, book):
        self.book = book
        self.init_test_records()

    def init_test_records(self):
        for name, value in TEST_RECORDS.items():
            record = Record(name)
            if value["birthday"]:
                record.add_birthday(value["birthday"])

            for phone in value['phones']:
                record.add_phone(phone)

            self.book.add_record(record)

    def handle_add(self, args):
        if len(args) < 2:
            raise ValueError("Name and phone must be specified")
        new_record = Record(args[0])
        new_record.add_phone(args[1])
        return self.book.add_record(new_record)

    def handle_find(self, name):
        return self.book.find(name)

    def handle_change(self, args):
        if len(args) < 3:
            raise ValueError("Name, old and new phone must be specified")
        record = self.book.find(args[0])
        return record.edit_phone(args[1], args[2])

    def handle_delete_record(self, name):
        return self.book.delete(name)

    def handle_add_phone(self, args):
        if len(args) < 2:
            raise ValueError("Name and phone must be specified")
        record = self.book.find(args[0])
        return record.add_phone(args[1])

    def handle_delete_phone(self, args):
        if len(args) < 2:
            raise ValueError("Name and phone must be specified")
        record = self.book.find(args[0])
        return record.delete_phone(args[1])
    
    def handle_add_birthday(self, args):
        if len(args) < 2:
            raise ValueError("Name and birthday must be specified")
        
        try:
            datetime.strptime(args[1], '%d.%m.%Y')
            record = self.book.find(args[0])
            return record.add_birthday(args[1])
        except ValueError:
            raise ValueError("Incorrect data format, should be DD.MM.YYYY")
    
    def handle_show_birthday(self, args):
        if len(args) < 1:
            raise ValueError("Name must be specified")
        record = self.book.find(args[0])
        return record.show_birthday()
    
    def handle_birthdays(self):
        return self.book.get_birthdays_per_week()
    
    def autotest(self):
        for input_cmd in MOCKED_INPUTS:
            print(f"\nExecuting command: {format_warning_msg(input_cmd)}")
            command, *args = parse_input(input_cmd)
            self.execute_command(command, args)

    def execute_command(self, command, args):
        try:
            if command == "autotest":
                self.autotest()
                return
            elif command == "all":
                print(self.book)
                return
            if command == "add":
                print(format_success_msg(self.handle_add(args)))
            elif command == "find":
                print(self.handle_find(args[0]))
            elif command == "change":
                print(format_success_msg(self.handle_change(args)))
            elif command == "delete":
                print(format_success_msg(self.handle_delete_record(args[0])))
            elif command == "find-phone":
                record = self.book.find(args[0])
                print(record)
            elif command == "add-phone":
                print(format_success_msg(self.handle_add_phone(args)))
            elif command == "delete-phone":
                print(format_success_msg(self.handle_delete_phone(args)))
            elif command == "add-birthday":
                print(format_success_msg(self.handle_add_birthday(args)))
            elif command == "show-birthday":
                print(format_success_msg(self.handle_show_birthday(args)))
            elif command == "birthdays":
                birthdays = self.handle_birthdays()
                for day, names in birthdays.items():
                    print(f"{format_underline_msg(day)}: {', '.join(names)}")
            elif command == "hello":
                print("How can I help you?")
            elif command == "help":
                print("Available Commands:")
                
                for command, data in AVAILABLE_COMMANDS.items():
                    print(f"  - {data['preview']}: {data['description']}")
            else:
                print(format_error_msg("Invalid command."))
        except (KeyError, ValueError) as e:
            print(format_error_msg(str(e)))

def main():
    book = AddressBook()
    handler = CommandHandler(book)

    print("Welcome to the assistant bot!")

    while True:
        try: 
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit", "bye"]:
                print("Good bye!")
                break

            handler.execute_command(command, args)
        except KeyboardInterrupt:
            print("\nGood bye!")
            return


if __name__ == "__main__":
    main()