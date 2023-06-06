# This app will generate a 20 alphanumeric characters long, each
# containing upper, lower, and punctuation characters.
# It will also ask the user if they would like to write it in a encrypted txt
# file where they can save more passwords.
from encrypt import EncryptFile
from rich.console import Console
from rich.table import Table
import os.path
import datetime
import string
import secrets


class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None


class PasswordGenerator:
    def __init__(self):
        self.head = None
        self.tail = None

    def __iter__(self):
        node = self.head
        while node:
            yield node
            node = node.next

    def insert(self, value, location):
        newNode = Node(value)
        if self.head is None:
            self.head = newNode
            self.tail = newNode
        else:
            if location == 0:
                newNode.next = self.head
                self.head = newNode
            elif location == -1:
                newNode.next = None
                self.tail.next = newNode
                self.tail = newNode
            else:
                tempNode = self.head
                index = 0
                while index < location - 1:
                    tempNode = tempNode.next
                    index += 1
                nextNode = tempNode.next
                tempNode.next = newNode
                newNode.next = nextNode
                if tempNode == self.tail:
                    self.tail = newNode

    def erase(self):
        if self.head is None:
            print("There is no data saved in memory to erase.")
        else:
            self.head = None
            self.tail = None

    def table_output(self, data):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Date", justify="center")
        table.add_column("Domain Name", justify="center")
        table.add_column("Password", justify="center")
        table.add_column("Change Pass (90 days)", justify="center")
        print()
        count = 0
        for x in data:
            table.add_row(str(count), x["date"], x["name"],
                          x["password"], x["change_pass"])
            count += 1
        console.print(table)

    def random_password(self):
        name = console.input(
            "What is the Domain name you want save your new password for?: ")
        incl = string.digits + string.ascii_letters
        rand_pass = ''.join(secrets.choice(incl) for i in range(20))
        start_date = datetime.date.today()
        change_pass = start_date + datetime.timedelta(days=90)
        console.print(
            f"Your new random password has been created. Make sure to create or add to your json file", style=body)
        great = dict(date=str(start_date), name=name,
                     password=rand_pass, change_pass=str(change_pass))
        return great


console = Console(color_system="auto")
colors = {
    "grass": "#397754",
    "pink": "#f2ebe9",
    "lime_green": "#70be51",
    "orange": "#eb6b40",
    "purple": "#9b45b2"
}
header = f"bold {colors['grass']} on {colors['pink']}"
body = f"bold {colors['purple']}"


def display():
    console.print(
        "Make sure you're in your Desktop dir so you can find your txt file easier if you choose this option.", style=header, justify="center")
    console.print("Password Generator", style=header, justify="center")
    print()
    print("COMMAND MENU")
    print("Create pass - create a secure password and display it on the screen")
    print("Create file - create an encrypted txt file")
    print("Encrypt - encrypt your file before you leave")
    print("Decrypt - view your encrypted passwords")
    print("View - view your passwords")
    print("Add - add a new password to your encrypted txt file")
    print("Erase - erase all your passwords from your encrypted txt file")
    print("Exit - exit the program")


def main():
    display()
    user = PasswordGenerator()
    encrypt = EncryptFile()
    count = 0

    while True:
        command = input("Command: ")
        if command.lower() == "create pass":
            if count > 1:
                print(
                    "You should consider using command 'Create' if you haven't created an encrypted file.")
            result = user.random_password()
            user.insert(result, -1)
            user.table_output([node.value for node in user])
            count += 1

        elif command.lower() == "create file":
            encrypt.write_data([node.value for node in user])
            key = encrypt.load_key()
            encrypt.encrypt_file(key)
            user.erase()
            print("Your 'passwords.json file has been created and encrypted")
            print("Make sure you decrypt your file to see the passwords")

        elif command.lower() == "decrypt":
            file = os.path.exists("passwords.json")
            key_exist = os.path.exists("filekey.key")
            if file and key_exist:
                key = encrypt.load_key()
                encrypt.decrypt_file(key)
                print("Your file has been decrypted")
            else:
                print("Make sure both 'passwords.json' and 'filekey.key' exist")

        elif command.lower() == "encrypt":
            file = os.path.exists("passwords.json")
            key_exist = os.path.exists("filekey.key")
            if file and key_exist:
                key = encrypt.load_key()
                encrypt.encrypt_file(key)
                print("Your file has been encrypted")
            else:
                print("Make sure both 'passwords.json' and 'filekey.key' exist")

        elif command.lower() == "view":
            file = os.path.exists("passwords.json")
            key_exist = os.path.exists("filekey.key")
            if file and key_exist:
                data = encrypt.load_data_from_file()
                for x in data:
                    user.insert(x, -1)
                user.table_output([node.value for node in user])
                user.erase()
            else:
                print("Make sure both 'passwords.json' and 'filekey.key' exist")

        elif command.lower() == "add":
            file = os.path.exists("passwords.json")
            key_exist = os.path.exists("filekey.key")
            if file and key_exist:
                data = encrypt.load_data_from_file()
                mem_data = [node.value for node in user]
                for x in mem_data:
                    data.append(x)
                encrypt.replace_file(data)
                user.erase()
                print("Your new passwords have been added successfully")
            else:
                print("Make sure both 'passwords.json' and 'filekey.key' exist")

        elif command.lower() == "erase":
            valid = input(
                "Are you sure? Once you do, there is no going back(y/n): ")
            if valid.lower() == "y":
                file = os.path.exists("passwords.json")
                key_exist = os.path.exists("filekey.key")
                if file and key_exist:
                    os.remove("passwords.json")
                    os.remove("filekey.key")
                    print("Your passwords have been deleted from both mem and file")
                    count = 0
                else:
                    print("Both files must be present in order to erase them")

        elif command.lower() == "exit":
            break
        else:
            print("Not a valid command. Please try again.\n")

        print()


if __name__ == "__main__":
    main()
