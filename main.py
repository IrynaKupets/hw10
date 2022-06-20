from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, name):
        self.value = name


class Phone(Field):
    def __init__(self, phone):
        self.value = phone


# Record реализует методы для добавления/удаления/редактирования объектов Phone.
class Record:
    def __init__(self, name: Name, phone: Phone = None):
        self.name = name
        self.phone = phone

    def add_phone(self, phone: Phone):
        self.phone.value.append(phone)

    def del_phone(self, phone: Phone):
        self.phone.value.remove(phone)

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        self.del_phone(old_phone)
        self.add_phone(new_phone)

    def __repr__(self):
        return f"{self.name.value}: {self.phone.value}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def show_phone_numbers(self, name: Name):
        return self.data[name].phone.value


phone_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "Please, enter the name and number"
        except ValueError:
            return "Enter a valid number"
        except KeyError:
            return "No such name in phonebook"

    return wrapper


@input_error
def add_user(*args):
    name = Name(args[0])
    phone = Phone([p for p in args[1:]])
    rec = Record(name, phone)
    if rec.name.value not in phone_book:
        phone_book.add_record(rec)
    else:
        return f"The name {name.value} already exists. To change number please use the 'change {name.value}' command"
    return f"Contact {name.value} added successfully"


@input_error
def add_number(*args):
    phone_book[args[0]].add_phone(args[1])
    return f"Phone number {args[1]} is successfully added for user {args[0]}"


@input_error
def del_number(*args):
    phone_book[args[0]].del_phone(args[1])
    return f"Phone number {args[1]} is successfully deleted"


@input_error
def change_number(*args):
    phone_book[args[0]].change_phone(args[1], args[2])
    return f"Phone number for {args[0]} is successfully changed from {args[1]} to {args[2]}"


@input_error
def phone(*args):
    return phone_book.show_phone_numbers(args[0])


def show_all(*args):
    lst = ["{:^10}: {:>10}".format(k, str(v)) for k, v in phone_book.items()]
    return "\n".join(lst)


def hello(*args):
    return "How can I help you?"


def exit(*args):
    return "Good bye!"


COMMANDS = {hello: ["hello", "hi"],
            change_number: ["change"],
            phone: ["phone"],
            exit: ["exit", "close", "good bye", ".", "bye"],
            add_user: ["add user"],
            add_number: ["add number", "add phone"],
            show_all: ["show all", "show"],
            del_number: ["delete", "del"]
            }


def parse_command(user_input: str):
    for k, v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                return k, tuple(user_input[len(i):].strip().split(" "))


def main():
    while True:
        user_input = input("Enter your command ")
        try:
            result, data = parse_command(user_input)
            print(result(*data))
            if result is exit:
                break
        except TypeError:
            print(f"No such command. Consider using one from a list: {[v for v in COMMANDS.values()]}")


if __name__ == "__main__":
    main()
