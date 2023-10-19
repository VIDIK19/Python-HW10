def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "There's no such name!"
        except ValueError:
            return "Enter valid command!"
        except IndexError:
            return "Give me name and phone please"
    return inner

contacts = {}

@input_error
def add_contact(name, phone):
    contacts[name.capitalize()] = phone
    return f'Contact {name.capitalize()} has been saved!'

@input_error
def change_phone(name, phone):
    if name.capitalize() in contacts:
        contacts[name.capitalize()] = phone
        return f'Phone number for {name.capitalize()} has been changed!'
    else:
        return f"No contact named {name.capitalize()}."

@input_error
def show_phone(name):
    return contacts[name.capitalize()]

@input_error
def show_all():
    result = ""
    for name, phone in contacts.items():
        result += f'{name} {phone}\n'
    return result.strip()

def main():
    while True:
        command = input("Enter command: ").lower()
        
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add "):
            _, name, phone = command.split()
            print(add_contact(name, phone))
        elif command.startswith("change "):
            _, name, phone = command.split()
            print(change_phone(name, phone))
        elif command.startswith("phone "):
            _, name = command.split(maxsplit=1)
            print(show_phone(name))
        elif command == "show all":
            print(show_all())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("I don't understand this command!")

if __name__ == "__main__":
    main()
