from collections import UserDict

from datetime import datetime, date

from collections import defaultdict


class Birthday:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Record(Birthday):
    def __init__(self, value):
        super().__init__(value)

        if isinstance(datetime.strptime(value, '%d.%m.%Y'), datetime):
            self.value = value
        else:
            self.value = "00.00.0000"


class Phone(Birthday):
    def __init__(self, value):
        super().__init__(value)

        self.value = (
            str(value)
            .strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )

        if len(self.value) != 10:
            self.value = "0000000000"


class AddressBook(UserDict):
    def errors(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except KeyError:
                return f"User with current name not founded."

            except IndexError:
                return f"User not selected."

            except TypeError:
                return f"User not found."

            except ValueError:
                return "Give me name and phone please."

        return inner

    @errors
    def add_contact(self, args):
        name, arg_phone = args
        print("name:", name)
        phone = Phone(arg_phone)
        self.contacts[name] = phone
        return "Contact added."

    @errors
    def select_contact(self, args):
        name = args[0]
        # user_consist is type None mean that
        # name is absent in contacts
        user_consist = type(self.contacts[name])
        phone = self.contacts.get(name)
        return f"Contact: {phone}."

    @errors
    def change_contact(self, args):
        name, phone = args
        # user_consist is type None mean that
        # name is absent in contacts
        user_consist = type(self.contacts[name])
        self.contacts[name] = phone
        return "Contact changed."

    def all_contacts(self):
        self.list_phones = dict()
        for key, value in self.contacts.items():
            try:
                is_phone = int(value)
                self.list_phones[key] = value

            except:
                pass

        return self.list_phones

    def contacts(self, contacts):
        self.contacts = contacts
        return self.contacts

    def get_birthdays_per_week(self, users):
        birthday_list = []
        birthday_sorted = []
        today = datetime.today().date()
        schedule = defaultdict(list)
        title = ''

        def create_birthday_list():
            for user in users:
                name = user["name"]
                birthday = user["birthday"].date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday.replace(year=today.year+1)
                delta_days = (birthday_this_year - today).days

                if delta_days < 7:
                    birthday_list.append(
                        {birthday_this_year.weekday(): [name]})

        def sorted_birthday_list(birthdays):
            nonlocal birthday_sorted
            birthday_dict = {}

            for weekday in birthdays:
                for key, value in dict(weekday).items():
                    if key in birthday_dict.keys():
                        temp = ''
                        temp = birthday_dict[key]
                        temp += value
                        birthday_dict[key] = temp
                        break

                    birthday_dict[key] = value

            birthday_sorted = sorted(birthday_dict.items())
            return birthday_sorted

        def create_schedule():
            weekdays_dict = {
                0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
                3: 'Thursday', 4: 'Friday', 5: 'Saturday',
                6: 'Sunday', 7: 'Monday Next Week'
            }

            weekend = []

            for key, value in birthday_sorted:
                if key >= 5:
                    weekend += value
                else:
                    schedule[weekdays_dict[key]] = value

            schedule[weekdays_dict[7]] = weekend

        def printing_list():
            nonlocal title
            for key, value in schedule.items():
                title += key+':'+', '.join(value)+'\n'
            title = title.removesuffix('\n')

        create_birthday_list()
        sorted_birthday_list(birthday_list)
        create_schedule()
        printing_list()

        return title

    @errors
    def add_birthday(self, args):
        name, birthday = args
        record = Record(birthday)
        self.contacts[name] = record.value
        return "Birthday added"

    @errors
    def show_birthday(self, args):
        name = args[0]
        # user_consist is type None mean that
        # name is absent in contacts
        user_consist = type(self.contacts[name])
        return self.contacts[name]

    def all_birthdays(self):
        self.list_users_birthdays = []

        def create_dict_birthdays():
            nonlocal self
            dict_birthdays = dict()
            for key, value in self.contacts.items():
                try:
                    is_date = isinstance(datetime.strptime(
                        value, '%d.%m.%Y'), datetime)
                    dict_birthdays[key] = value

                except:
                    pass
            return dict_birthdays

        def create_list_birthdays(input_dict):
            list_birthdays = []
            for key, value in dict(input_dict).items():
                d, m, y = value.split(".")

                list_birthdays.append(
                    {'name': key, "birthday": datetime(int(y), int(m), int(d))})

            return list_birthdays

        dict_users_birthdays = create_dict_birthdays()
        self.list_users_birthdays = create_list_birthdays(dict_users_birthdays)
        return self.list_users_birthdays


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    book = AddressBook()
    book.contacts = dict()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(book.add_contact(args))

        elif command == "all":
            print(book.all_contacts())

        elif command == "change":
            print(book.change_contact(args))

        elif command == "phone":
            print(book.select_contact(args))

        elif command == "add-birthday":
            print(book.add_birthday(args))

        elif command == "show-birthday":
            print(book.show_birthday(args))

        elif command == "birthdays":
            get_all_birthdays = book.all_birthdays()
            print(book.get_birthdays_per_week(get_all_birthdays))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
