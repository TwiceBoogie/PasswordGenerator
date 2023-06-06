from cryptography.fernet import Fernet
import json


class EncryptFile:
    def __init__(self):
        # I was going to do something with this for
        # another function but decided not to.
        self._key = None

    def write_key(self):
        key = Fernet.generate_key()
        with open("filekey.key", "wb") as key_file:
            key_file.write(key)
            key_file.close()

    def load_key(self):
        self._key = open("filekey.key", "rb").read()
        return self._key

    def write_data(self, data):
        with open("passwords.json", "w") as outfile:
            new_dict = {}
            count = 0
            for x in range(len(data)):
                new_dict[str(count)] = data[x]
                count += 1
            json.dump(new_dict, outfile)
            outfile.close()
        self.write_key()

    def encrypt_file(self, key):
        f = Fernet(key)
        with open("passwords.json", "rb") as file:
            file_data = file.read()
            file.close()

        encrypted_data = f.encrypt(file_data)
        with open("passwords.json", "wb") as file:
            file.write(encrypted_data)
            file.close()

    def decrypt_file(self, key):
        f = Fernet(key)
        with open("passwords.json", "rb") as file:
            encrypted_data = file.read()
            file.close()

        decrypted_data = f.decrypt(encrypted_data)
        with open("passwords.json", "wb") as file:
            file.write(decrypted_data)
            file.close()

    def load_data_from_file(self):
        try:
            with open("passwords.json", "r") as file:
                file_data = json.load(file)
                file.close()
        except json.decoder.JSONDecodeError:
            print("Error decoding file")
            return False
        else:
            return [v for v in file_data.values()]

    def replace_file(self, data):
        # with open("passwords.json", "r+") as file:
        #     file.seek(0)
        #     file.truncate()
        #     file.close()
        with open("passwords.json", "w") as outfile:
            new_dict = {}
            count = 0
            print(data)
            for x in data:
                new_dict[str(count)] = x
                count += 1
            json.dump(new_dict, outfile)
            outfile.close()
