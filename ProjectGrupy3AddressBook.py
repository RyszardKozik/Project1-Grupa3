from collections import UserDict
import re
import pickle
from datetime import datetime


class Field:
    """Base class for entry fields."""
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        pattern = re.compile(r"^\d{9}$")
        return pattern.match(value) is not None


class Email(Field):
    def __init__(self, value):
        if not self.validate_email(value):
            raise ValueError("Invalid email address")
        super().__init__(value)

    @staticmethod
    def validate_email(value):
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return pattern.match(value) is not None


class Birthday(Field):
    def __init__(self, value):
        if not self.validate_birthday(value):
            raise ValueError("Invalid birthday")
        super().__init__(value)

    @staticmethod
    def validate_birthday(value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False


class Address(Field):
    def __init__(self, street, city, postal_code, country):
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.country = country
        super().__init__(value=f"{street}, {city}, {postal_code}, {country}")


class Note:
    """Class representing a note with content and tags."""
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.tags = []

    def add_tag(self, tag):
        """Adds a tag to the note."""
        self.tags.append(tag)

    def remove_tag(self, tag):
        """Removes a tag from the note."""
        self.tags.remove(tag)

    def __str__(self):
        return f"Title: {self.title}, Content: {self.content}, Tags: {', '.join(tag.name for tag in self.tags)}"


class Record:
    def __init__(self, name: Name, birthday: Birthday = None):
        self.id = None  # The ID will be assigned by AddressBook
        self.name = name
        self.phones = []
        self.emails = []
        self.birthday = birthday
        self.address = None  # Add a new property to store the address
        self.notes = []  # Add a new property to store notes

    def add_address(self, address: Address):
        """Adds an address."""
        self.address = address

    def add_phone(self, phone: Phone):
        """Adds a phone number."""
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        """Removes a phone number."""
        self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        """Changes a phone number."""
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def add_email(self, email: Email):
        """Adds an email address."""
        self.emails.append(email)

    def remove_email(self, email: Email):
        """Removes an email address."""
        self.emails.remove(email)

    def edit_email(self, old_email: Email, new_email: Email):
        """Changes an email address."""
        self.remove_email(old_email)
        self.add_email(new_email)

    def add_note(self, note: Note):
        """Adds a note."""
        self.notes.append(note)

    def remove_note(self, note: Note):
        """Removes a note."""
        self.notes.remove(note)

    def edit_note(self, old_note: Note, new_note: Note):
        """Changes a note."""
        self.remove_note(old_note)
        self.add_note(new_note)

    def edit_name(self, new_name: Name):
        """Changes the first and last name."""
        self.name = new_name

    def days_to_birthday(self):
        """Returns the number of days to the next birthday."""
        if not self.birthday or not self.birthday.value:
            return "No birthday set"
        today = datetime.now()
        bday = datetime.strptime(self.birthday.value, "%Y-%m-%d")
        next_birthday = bday.replace(year=today.year)
        if today > next_birthday:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __str__(self):
        """Returns a string representation of the entry, including the ID."""
        phones = ', '.join(phone.value for phone in self.phones)
        emails = ', '.join(email.value for email in self.emails)
        birthday_str = f", Birthday: {self.birthday.value}" if self.birthday else ""
        days_to_bday_str = f", Days to birthday: {self.days_to_birthday()}" if self.birthday else ""
        address_str = f"\nAddress: {self.address.value}" if self.address else ""
        notes_str = '\n'.join(str(note) for note in self.notes)
        return f"ID: {self.id}, Name: {self.name.value}, Phones: {phones}, Email: {emails}{birthday_str}{days_to_bday_str}{address_str}\nNotes:\n{notes_str}"


class Tag:
    """Class representing a tag for categorizing notes."""
    def __init__(self, name):
        self.name = name


class Notebook:
    def __init__(self):
        self.notes = []
        self.tags = []

    def create_note(self):
        """Creates a note with user input, including tags."""
        title = input("Enter the note title: ")
        content = input("Enter the note content: ")
        note = Note(title, content)

        # Adding tags
        while True:
            tag_input = input("Enter a tag (or press Enter to finish adding tags): ").strip()
            if not tag_input:
                break
            tag = Tag(tag_input)
            note.add_tag(tag)

        self.notes.append(note)
        print("Note created.")

    def show_notes_with_tags(self):
        """Displays all notes with their tags."""
        if not self.notes:
            print("No notes available.")
        else:
            for idx, note in enumerate(self.notes, start=1):
                print(f"{idx}. {note}")
                if note.tags:
                    print("   Tags:", ', '.join(tag.name for tag in note.tags))
                print()

    def delete_note(self, note_id):
        """Deletes a note based on ID."""
        try:
            note_id = int(note_id)
            if 1 <= note_id <= len(self.notes):
                del self.notes[note_id - 1]
                print(f"Deleted note with ID: {note_id}.")
            else:
                print("Note with the specified ID not found.")
        except ValueError:
            print("Invalid ID. Please enter a number.")

    def create_tag(self):
        """Creates a new tag."""
        tag_name = input("Enter the tag name: ")
        tag = Tag(tag_name)
        self.tags.append(tag)
        print("Tag created.")

    def show_tags(self):
        """Displays all tags."""
        if not self.tags:
            print("No tags available.")
        else:
            print("Tags:", ', '.join(tag.name for tag in self.tags))

    def save_notes(self, filename='notebook.pkl'):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self.notes, file)
            print("Saved the notes.")
        except Exception as e:
            print(f"Error saving the notes: {e}")

    def load_notes(self, filename='notebook.pkl'):
        try:
            with open(filename, 'rb') as file:
                self.notes = pickle.load(file)
            print("Restored the notes.")
        except FileNotFoundError:
            print("File not found, creating a new notebook.")
        except Exception as e:
            print(f"Error loading the notes: {e}")

    def load_data(self):
        self.load_notes()


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.next_id = 1
        self.free_ids = set()

    def add_record(self, record: Record):
        """Adds an entry to the address book with ID management."""
        while self.next_id in self.data or self.next_id in self.free_ids:
            self.next_id += 1
        if self.free_ids:
            record.id = min(self.free_ids)
            self.free_ids.remove(record.id)
        else:
            record.id = self.next_id
            self.next_id += 1
        self.data[record.id] = record
        print(f"Added entry with ID: {record.id}.")

    def delete_record_by_id(self):
        """Deletes a record based on ID."""
        user_input = input("Enter the ID of the record you want to delete: ").strip()
        record_id_str = user_input.replace("ID: ", "").strip()

        try:
            record_id = int(record_id_str)
            if record_id in self.data:
                del self.data[record_id]
                self.free_ids.add(record_id)
                print(f"Deleted record with ID: {record_id}.")
            else:
                print("Record with the specified ID not found.")
        except ValueError:
            print("Invalid ID. Please enter a number.")

    def find_record(self, search_term):
        """Finds entries containing the exact phrase provided."""
        found_records = []
        for record in self.data.values():
            if search_term.lower() in record.name.value.lower():
                found_records.append(record)
                continue
            for phone in record.phones:
                if search_term in phone.value:
                    found_records.append(record)
                    break
            for email in record.emails:
                if search_term in email.value:
                    found_records.append(record)
                    break
        return found_records

    def find_records_by_name(self, name):
        """Finds records that match the given name and surname."""
        matching_records = []
        for record_id, record in self.data.items():
            if name.lower() in record.name.value.lower():
                matching_records.append((record_id, record))
        return matching_records

    def delete_record(self):
        """Deletes the record based on the selected ID after searching by name."""
        name_to_delete = input("Enter the name of the person you want to delete: ")
        matching_records = self.find_records_by_name(name_to_delete)

        if not matching_records:
            print("No matching records found.")
            return

        print("Found the following matching records:")
        for record_id, record in matching_records:
            print(f"ID: {record_id}, Record: {record}")

        try:
            record_id_to_delete = int(input("Enter the ID of the record you want to delete: "))
            if record_id_to_delete in self.data:
                del self.data[record_id_to_delete]
                self.free_ids.add(record_id_to_delete)  # Add the ID back to the free ID pool
                print(f"Deleted record with ID: {record_id_to_delete}.")
            else:
                print("Record with the specified ID not found.")
        except ValueError:
            print("Invalid ID. Please enter a number.")

    def show_all_records(self):
        """Displays all entries in the address book."""
        if not self.data:
            print("Address book is empty.")
            return
        for name, record in self.data.items():
            print(record)

    def __iter__(self):
        """Returns an iterator over the address book records."""
        self.current = 0
        return self

    def __next__(self):
        if self.current < len(self.data):
            records = list(self.data.values())[self.current:self.current+5]
            self.current += 5
            return records
        else:
            raise StopIteration


def edit_record(book):
    """Edits an existing record in the address book."""
    name_to_edit = input("Enter the name of the person you want to edit: ")
    if name_to_edit in book.data:
        record = book.data[name_to_edit]
        print(f"Editing: {name_to_edit}.")

        # Name and surname edit
        new_name_input = input("Enter the name and surname (press Enter to keep the current): ")
        if new_name_input.strip():
            record.edit_name(Name(new_name_input))
            print("Updated name and surname.")

        # Phone number edit
        if record.phones:
            print("Current phone numbers: ")
            for idx, phone in enumerate(record.phones, start=1):
                print(f"{idx}. {phone.value}")
            phone_to_edit = input("Enter the index of the phone number you want to edit "
                                  "(press Enter to keep the current): ")
            if phone_to_edit.isdigit():
                idx = int(phone_to_edit) - 1
                if 0 <= idx < len(record.phones):
                    new_phone_number = input("Enter the new phone number: ")
                    if new_phone_number.strip():
                        record.edit_phone(record.phones[idx], Phone(new_phone_number))
                        print("Phone number updated.")
                    else:
                        print("No changes made.")
                else:
                    print("Invalid phone index.")
            else:
                print("Skipped phone number edit.")
        else:
            print("No phone numbers.")

        # E-mail edit
        if record.emails:
            print("Current email addresses: ")
            for idx, email in enumerate(record.emails, start=1):
                print(f"{idx}. {email.value}")
            email_to_edit = input("Enter the index of the email address you want to edit "
                                  "(press Enter to keep the current): ")
            if email_to_edit.isdigit():
                idx = int(email_to_edit) - 1
                if 0 <= idx < len(record.emails):
                    new_email = input("Enter the new email address: ")
                    if new_email.strip():
                        record.edit_email(record.emails[idx], Email(new_email))
                        print("Email address updated.")
                    else:
                        print("No changes made.")
                else:
                    print("Invalid email index.")
            else:
                print("Skipped email address edit.")
        else:
            print("No email addresses.")

        # Note edit
        if record.notes:
            print("Current notes: ")
            for idx, note in enumerate(record.notes, start=1):
                print(f"{idx}. {note}")
            note_to_edit = input("Enter the index of the note you want to edit "
                                 "(press Enter to keep the current): ")
            if note_to_edit.isdigit():
                idx = int(note_to_edit) - 1
                if 0 <= idx < len(record.notes):
                    new_note_title = input("Enter the new note title: ")
                    new_note_content = input("Enter the new note content: ")
                    new_note = Note(new_note_title, new_note_content)
                    record.edit_note(record.notes[idx], new_note)
                    print("Note updated.")
                else:
                    print("Invalid note index.")
            else:
                print("Skipped note edit.")
        else:
            print("No notes.")

        print("Entry updated.")
    else:
        print("Entry not found.")


def save_address_book(book, filename='address_book.pkl'):
    try:
        with open(filename, 'wb') as file:
            pickle.dump(book.data, file)
        print("Saved the address book.")
    except Exception as e:
        print(f"Error saving the address book: {e}")


def load_address_book(filename='address_book.pkl'):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        book = AddressBook()
        book.data = data
        print("Restored the address book.")
        return book
    except FileNotFoundError:
        print("File not found, creating a new address book.")
        return AddressBook()
    except Exception as e:
        print(f"Error loading the address book: {e}")
        return AddressBook()


def input_phone():
    """Asks the user to enter a phone number."""
    while True:
        try:
            number = input("Enter the phone number in the format '123456789' (press Enter to skip): ")
            if not number:
                return None
            return Phone(number)
        except ValueError as e:
            print(e)


def input_email():
    """Asks the user to enter an email address."""
    while True:
        try:
            address = input("Enter the email address (press Enter to skip): ")
            if not address:
                return None
            return Email(address)
        except ValueError as e:
            print(e)


def create_record():
    """Creates an entry in the address book based on user input."""
    name_input = input("Enter the name and surname: ")
    name = Name(name_input)

    birthday = None
    while True:
        birthday_input = input("Enter the date of birth (YYYY-MM-DD) or press Enter to skip: ")
        if not birthday_input:
            break
        try:
            birthday = Birthday(birthday_input)
            break
        except ValueError as e:
            print(e)

    record = Record(name, birthday)

    while True:
        try:
            phone_input = input("Enter the phone number (or press Enter to finish adding numbers): ")
            if not phone_input:
                break
            phone = Phone(phone_input)
            record.add_phone(phone)
        except ValueError as e:
            print(e)

    while True:
        try:
            email_input = input("Enter the email address (or press Enter to finish adding email addresses): ")
            if not email_input:
                break
            email = Email(email_input)
            record.add_email(email)
        except ValueError as e:
            print(e)

    # New functionality: Adding an address
    add_address = input("Do you want to add an address? (y/n): ").lower().strip()
    if add_address in ['y']:
        street = input("Enter the street: ")
        city = input("Enter the city: ")
        postal_code = input("Enter the postal code: ")
        country = input("Enter the country name: ")
        address = Address(street, city, postal_code, country)
        record.add_address(address)

    # New functionality: Adding a note
    add_note = input("Do you want to add a note? (y/n): ").lower().strip()
    if add_note in ['y']:
        note_title = input("Enter the note title: ")
        note_content = input("Enter the note content: ")
        note = Note(note_title, note_content)
        record.add_note(note)

    return record


def main():
    notebook = Notebook()
    notebook.load_data()
    book = load_address_book()

    while True:
        action = input("Choose action: \nManage Contacts (c), Manage Notes (n), or Quit (q): ")
        if action == 'c':
            while True:
                contact_action = input(
                    "Choose action: \nAdd contact (a), Find contact (f), "
                    "Delete contact (d), Edit contact (e), Show all contacts (s), Go back (q): ")
                if contact_action == 'a':
                    record = create_record()
                    book.add_record(record)
                    print("Added contact.")
                elif contact_action == 'f':
                    search_term = input("Enter the search phrase: ")
                    found = book.find_record(search_term)
                    for record in found:
                        print(record)
                elif contact_action == 'd':
                    book.delete_record_by_id()
                    print("Deleted contact.")
                elif contact_action == 'e':
                    edit_record(book)
                    print("Contact updated.")
                elif contact_action == 's':
                    book.show_all_records()
                elif contact_action == 'q':
                    break
                else:
                    print("Unknown action, please try again.")
        elif action == 'n':
            while True:
                note_action = input(
                    "Choose action for notes: \nAdd note (a), Show notes (s), "
                    "Delete note (d), Create tag (t), Show tags (g), Go back (q): ")
                if note_action == 'a':
                    notebook.create_note()
                    print("Added note.")
                elif note_action == 's':
                    notebook.show_notes_with_tags()
                elif note_action == 'd':
                    note_id = input("Enter the ID of the note you want to delete: ")
                    notebook.delete_note(note_id)
                    print("Deleted note.")
                elif note_action == 't':
                    notebook.create_tag()
                    print("Tag created.")
                elif note_action == 'g':
                    notebook.show_tags()
                elif note_action == 'q':
                    break
                else:
                    print("Unknown action, please try again.")
        elif action == 'q':
            break
        else:
            print("Unknown action, please try again.")

    notebook.save_notes()
    save_address_book(book)


if __name__ == "__main__":
    main()
