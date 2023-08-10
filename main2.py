from collections import UserDict
#class Field
class Field:
    def __init__(self, value = None):
        self._value = value
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, new_value):
        if self.is_valid(new_value):
            self._value = new_value
        else:
            raise ValueError("Invalid field value")
    def is_valid(self, value):
        return bool(value.strip())
    
#class AddressBook
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
   
#class Record
class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []
    def add_phone(self, phone):
        self.phones.append(phone)
    def remove_phone(self, phone):
        self.phones.remove(phone)
    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone
    def __str__(self):
        return f"Name: {self.name.value}, Phones: {', '.join(str(phone) for phone in self.phones)}"

#class Name
class Name(Field):
    def is_valid(self, value):
        return value is not None and value.isalpha() and value.strip()
 
#class Phone
class Phone(Field):
    def __init__(self, number):
        self.number = number
    def is_valid(self, value):
        return value is not None and 4 <= len(value) <= 15
    def __str__(self):
        return self.number
    
#write error
def print_error(message):
    print("Error: " , message)
#generate the errors
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Error: Contact not found."
        except ValueError:
            return "Error: Invalid input. Please enter name and phone number."
        except IndexError:
            return "Error: Invalid input. Please enter name and phone number."
    return inner

#presents all contacts
@input_error
def show_all_contacts(phone_book):
    result = "Contacts:\n"
    for record in phone_book.data.values():
        result += str(record) + "\n"
    return result

#using the function can add new contact
@input_error
def add_contact(phone_book, name, phone):
    the_name = Name(name)
    the_phone = Phone(phone)
    # If the contact already exists, update its phone list
    if the_name.is_valid(name) and the_phone.is_valid(phone):
        if name in phone_book.data:
            existing_record = phone_book.data[name]
            existing_record.add_phone(the_phone)
        else:
            new_record = Record(the_name)
            new_record.add_phone(the_phone)
            phone_book.add_record(new_record)
        return f"Contact '{name}' with phone '{phone}' has been added."
    raise ValueError

#change the phone
@input_error
def change_phone(phone_book, name, old_phone, new_phone):
    if name not in phone_book.data:
        raise KeyError
    existing_record = phone_book.data[name]
    phone_new = Phone(new_phone)
    if phone_new.is_valid(new_phone):
        for num in existing_record.phones:
            if str(num) == old_phone:
                existing_record.edit_phone(num, phone_new)
                return f"Phone number for {name} has been changed to {new_phone}."
    raise ValueError

#get the phone
@input_error
def get_phone(phone_book, name):
    if name not in phone_book.data:
        raise KeyError
    existing_record = phone_book.data[name]
    phone_numbers = ', '.join(str(phone) for phone in existing_record.phones)
    result = f"Phone numbers for {name}: {phone_numbers}"
    return result

#delete the phone
@input_error
def delete_phone(phone_book, name, phone):
    if name not in phone_book.data:
        raise KeyError
    existing_record = phone_book.data[name]
    for num in existing_record.phones:
        if str(num) == phone:
            existing_record.remove_phone(num)
            return f"Phone number {phone} has been deleted from {name}."
    raise ValueError
    
#the main function
def main():
    #dictionary with the commands
    phone_book = AddressBook()
    commands = {
        "hello": lambda: print("How can I help you?\n"),
        "good bye": lambda: print("Good bye!"),
        "close": lambda: print("Good bye!"),
        "exit": lambda: print("Good bye!"),
        "show all": lambda: print(show_all_contacts(phone_book)),
        "add": lambda: print(add_contact(phone_book,user_devided[1], user_devided[2])) if len(user_devided) == 3 else print_error("write name and phone."),
        "change": lambda: print(change_phone(phone_book,user_devided[1], user_devided[2], user_devided[3])) if len(user_devided) == 4 else print_error("write name and phone."),
        "phone": lambda: print(get_phone(phone_book, user_devided[1])) if len(user_devided) == 2 else print_error("write name."),
        "delete": lambda: print(delete_phone(phone_book,user_devided[1], user_devided[2])) if len(user_devided) == 3 else print_error("write name and phone.")
    }
    while True:
        user_input = input("Write command \t")
        user_devided = user_input.split(maxsplit=3)
        result_text = ""
        for char in user_input:
            if char != " ":
                result_text += char.lower()
            else: break
            
        if result_text in commands:
            commands[result_text]()
            if result_text in ["close", "exit"]:
                break
        elif user_input.lower() in commands:
            commands[user_input.lower()]()
            if user_input.lower() == "good bye":
                break
        else:
            print("Invalid command. Use 'hello', 'add', 'change', 'phone', 'show all', 'good bye', 'close', or 'exit'")

if __name__ == '__main__':
    main()

