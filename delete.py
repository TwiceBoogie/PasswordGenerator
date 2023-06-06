with open("passwords.json", "r+") as file:
    file.seek(0)
    file.truncate()
    file.close()
