#!/usr/bin/env python
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from sys import argv
from utils import *

description = """
A password manager
Pman is a stateless password manager written in python. This program is intended to be used as CLI software however a web
implementation of Pman is also available at gwstuart.github.io/projects/pman.html
"""

parser = ArgumentParser(prog="pman", description=description, formatter_class=RawDescriptionHelpFormatter)

parser.add_argument("get", nargs="?", help="generate password")
parser.add_argument("-u", "--user", action="store_true", help="auto generate user")
parser.add_argument("-s", "--save", action="store_true", help="save credentials to database")
parser.add_argument("-l", "--list", action="store_true", help="list stored credentials")
parser.add_argument("-db", "-data", "--database", action="store_true", help="open database in editor")
parser.add_argument("-rm", "-r", "-del", "--remove", help="remove stored credentials")
parser.add_argument("-n", "-len", "--length", help="specify password length")
parser.add_argument("-x", "--exclude", help="exclude special characters")
# command to edit/update values in db
# add a -a command to append text to name

args = parser.parse_args()

if args.get:
    name = extract_name(args.get)

    flags = extract_flags(args.get)
    if flags:
        print("Note custom flags were found for this entry and applied")
        args.length, args.exclude = flags
    length = int(args.length) if args.length else 0

    password = generate_password(name, length=length, exclude=args.exclude)
    print(f"Password: {password}")

    if args.user:
        username = generate_username(name)
        print(f"Username: {username}")

    if args.save:
        save_data(name, length, args.exclude, args.user)
    
    if not args.save and not args.user: # prints user data if found in database
        fetch_username(name)

if args.list:
    list_db()

if args.database:
    open_db()

if args.remove:
    remove(args.remove)

if len(argv) == 1:
    parser.print_help()
