from getpass import getpass
from os import path, system  
from random import seed, randint, choice
from platform import system as platform_system
from hashlib import sha256
from argon2 import PasswordHasher

data_file = path.dirname(__file__) + "/data.txt"  # location of pman data file
if not path.exists(data_file):  # check if the file exists if not create it
    with open(data_file, "w") as f:
        f.write("Saved user data for pman\n")

def extract_name(url: str) -> str:
    """ Extracts the website name from a url """
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
    
    return url  # returns the extracted website name as a string

def get_key() -> str:
    """ Returns the user key from the key file (if it exists) """

    key_file = path.dirname(__file__) + "/key"
    if path.exists(key_file):
        with open(key_file, "r") as f:
            return f.readlines()[0].strip()  # returns the key as a string
    return ""

def base10(text) -> int:  # converts argon hash (base 64) to a base 10 integer
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"
    base = 64
    text_length = len(text)

    result = 0
    for i, character in enumerate(text):
        result += characters.index(character) * (base ** (text_length - i - 1))

    return result  # returns the text as an integer

def get_password(name, key, message, legacy=False) -> int:
    """ Prompts user for a master password and returns hashed password"""
    passwd = getpass(message)  # might be security risks with storing this in memory
    
    if legacy:
        return int(sha256(f"{passwd + name + key}".encode("utf-8")).hexdigest(), 16)
    else:
        hasher = PasswordHasher(time_cost=4, memory_cost=1048576, parallelism=6, hash_len=32, salt_len=2)
        hashed = hasher.hash(passwd + name + key, salt=b"pmanPman")  # maybe could do something clever with the salt
        result = hashed.split("$")[-1]

        return base10(result)  # returns the hashed password as an integer

def generate_password(name, length=0, exclude=False, confirm=False, legacy=False) -> str:
    """  """
    key = get_key()  # user chosen key

    encrypted_passwd = get_password(name, key, "Master Password: ", legacy=legacy)

    if confirm: # if the user wishes to confirm their password
        encrypted_confirm = get_password(name, key, "Confirm Password: ", legacy=legacy)

        if encrypted_confirm != encrypted_passwd:
            print("Passwords do not match")
            quit()

    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()<>[]{}+=-_"
    base = len(characters)

    if exclude:  # exclude certain characters specified by user
        for x in exclude:
            characters = characters.replace(x, "")

    new = ""  # convert the integer hash into a multicharacter string
    while encrypted_passwd != 0:
        new = characters[encrypted_passwd % base] + new
        encrypted_passwd //= base
    
    if length:  # shorten the password length if specified by the user
        new = new[:length]

    return new  # return the password as a string

def generate_username(name): # randomaly generates a username
    # this function could be improved in future
    seed(sum([ord(x) for x in name]))

    prefixes = ["", "Mr", "Mrs"]
    noun = ["Cookie", "Pizza", "Penguin", "Flower", "Camel"]
    adjective = ["Muncher", "Destroyer", "Machine", "Killer"]
    number = str(randint(0, 99))

    username = choice(prefixes) + choice(noun) + choice(adjective) + number
    return username  # returns the random username as a string

def query(name):  # query the pman data file for a given application name
    with open(data_file, "r") as f:
        lines = f.readlines()[1:]
        for line in lines:
            if name.lower() == line.strip().split("~~~")[0].lower():
                # returns the line number and full information of the match
                return lines.index(line), line.strip().split("~~~")
    return False  # returns false if no match was found

def save_data(name, length, exclude, username):  # save data in the database
    if query(name):  # check if data is already present
        print("A password was already found in the database")
        if input("Would you like to procede (y/N): ") != "y": 
            quit()

    print("Optionally provide additional information to be saved")

    # review this username saving section
    if username:  # prompt the user to optionally save a username
        save = input("Save username (Y/n): ")
        if save == "n":
            username = ""
        else:
            username = generate_username(name) 
    else:
        username = input("Username: ")
    
    description = input("Description: ")
    
    with open(data_file, "a") as f:  # write data to the data file
        f.write(f"{name}~~~{username}~~~{description}~~~")
        if length or exclude:
            f.write(f"{length}:{exclude}")
        f.write("\n")

    print("Saved user credentials")

def fetch_username(name):  # fetch username associated with a saved name
    result = query(name)
    if not result: return

    if result[1][1]:
        print(f"Username: {result[1][1]}")
    if result[1][2]:
        print(f"Description: {result[1][2]}")

def list_db():  # lists all data present in the data file
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

def open_db():  # opens the data file using preferred text editor
    os_type = platform_system()

    print(f"Opening: {data_file}")

    if os_type == "Windows":
        system(f"start {data_file}")
    elif os_type == "Linux":
        system(f"$EDITOR {data_file}") 
    else:  # still need to add support for macos (probably same as linux)
        print(f"Sorry is {os_type} is unsupported")

def remove(name):  # remove item with given name from the data file
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

def extract_flags(name):  # extract the flags associated with a given name from the data file
    entry = query(name)
    if entry:
        flags = query(name)[1][-1].split(":")
        if flags != [""]:
            return flags
    return False
