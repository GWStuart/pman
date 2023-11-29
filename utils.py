import getpass
import os
import random
import platform
from hashlib import sha256

data_file = os.path.dirname(__file__) + "/data.txt"

def extract_name(url):
    url = url.replace("https://", "")
    url = url.replace("http://", "")

    if "/" in url:
        slash = url.index("/")
        url = url[:slash]

    dots = url.count(".")
    if dots == 1:
        dot = url.index(".")
        url = url[:dot]
    elif dots > 1:
        dot = url.index(".") + 1
        url = url[dot:]
        dot = url.index(".")
        url = url[:dot]
    
    return url

def generate_password(name, length=0, exclude=False, confirm=False):
    passwd = getpass.getpass("Master Password: ")  # Might be security risks with storing this in memory
    encrypted_passwd = int(sha256(f"{passwd + name}".encode("utf-8")).hexdigest(), 16)

    if confirm: # if the user wishes to confirm their password
        confirm_passwd = getpass.getpass("Confirm Password: ")
        encrypted_confirm = int(sha256(f"{confirm_passwd + name}".encode("utf-8")).hexdigest(), 16)

        if encrypted_confirm != encrypted_passwd:
            print("Passwords do not match")
            quit()

    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()<>[]{}+=-_"
    if exclude:
        for x in exclude:
            characters = characters.replace(x, "")

    base = len(characters)

    new = ""
    while encrypted_passwd != 0:
        new = characters[encrypted_passwd % base] + new
        encrypted_passwd //= base
    
    if length:
        new = new[:length]

    return new

def generate_username(name): # Could be improved in future
    random.seed(sum([ord(x) for x in name]))

    prefixes = ["", "Mr", "Mrs"]
    noun = ["Cookie", "Pizza", "Penguin", "Flower", "Camel"]
    adjective = ["Muncher", "Destroyer", "Machine", "Killer"]
    number = str(random.randint(0, 99))

    username = random.choice(prefixes) + random.choice(noun) + random.choice(adjective) + number
    return username

def query(name):
    with open(data_file, "r") as f:
        lines = f.readlines()[1:]
        for line in lines:
            if name.lower() == line.strip().split("~~~")[0].lower():
                return lines.index(line), line.strip().split("~~~")
    return False

def save_data(name, length, exclude, username):
    if query(name):
        print("A password was already found in the database")
        if input("Would you like to procede (y/N): ") != "y": quit()

    print("Optionally provide additional information to be saved")

    if username:
        save = input("Save username (Y/n): ")
        if save == "n":
            username = ""
        else:
            username = generate_username(name) 
    else:
        username = input("Username: ")
    
    description = input("Description: ")
    
    with open(data_file, "a") as f:
        f.write(f"{name}~~~{username}~~~{description}~~~")
        if length or exclude:
            f.write(f"{length}:{exclude}")
        f.write("\n")

    print("Saved user credentials")

def fetch_username(name):
    result = query(name)
    if not result: return

    if result[1][1]:
        print(f"Username: {result[1][1]}")
    if result[1][2]:
        print(f"Description: {result[1][2]}")

def list_db():
    headings = ["Name", "Username", "Description", "Flags"]
    with open(data_file, "r") as f:
        lines = f.readlines()[1:]

        data = []
        lengths = list(map(len, headings))
        for line in lines:
            line = line.strip().split("~~~")
            data.append(line)
            for i in range(len(headings)):
                lengths[i] = len(line[i]) if len(line[i]) > lengths[i] else lengths[i]
    
    string = f" {{:<{lengths[0] + 5}}} {{:<{lengths[1] + 5}}} {{:<{lengths[2] + 5}}} {{:<{lengths[3] + 5}}}"
    print(f"\033[1m{string}\033[0m".format(*headings))
    for line in data:
        print(string.format(*line))

def open_db():
    os_type = platform.system()

    print(f"Opening: {data_file}")

    if os_type == "Windows":
        os.system(f"start {data_file}")
    elif os_type == "Linux":
        os.system(f"$EDITOR {data_file}") 
    else:
        print(f"Sorry is {os_type} is unsupported")

def remove(name):
    result = query(name)
    if result:
        [print(f"\033[1m{x}\033[0m: {y}") for x, y in zip(["Name", "Username", "Description"], result[1])]
        procede = input("Is this the correct entry (y/N)? ")
        if procede == "y": # Not sure if there is a better way of deleting the line
            with open(data_file, "r") as fr:
                lines = fr.readlines()
                with open(data_file, "w") as fw:
                    for i, line in enumerate(lines):
                        if i != result[0] + 1:
                            fw.write(line)
            print("Entry deleted")
        else:
            print("No action was taken")
    else:
        print(f'Sorry "{name}" was not found in the database')

def extract_flags(name):
    with open(data_file, "r") as f:
        lines = f.readlines()[1:]
        for line in lines:
            if name.lower() == line.strip().split("~~~")[0].lower(): # might be able to use query() here idk
                flags = line.strip().split("~~~")[3]
                if flags:
                    return flags.split(":")
                else:
                    return False

    return False
