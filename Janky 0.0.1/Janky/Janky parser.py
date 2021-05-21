from resources.language.Janky import *
import os
import sys
os.system("title Janky parser v1.0.0")
parser = JankyParser(True)
print("Welcome to Python Janky perser 1.0.0, do 'print help' for help.")
print()
def throw(msg):
    print(msg)
    return False
def parse(packets):
    for packet in packets:
        command = packet["command"]
        values = packet["values"]
        code = packet["code"]
        errors = packet["errors"]
        for err in errors:
            print(err)
        if command == "print":
            strRep = ""
            for v in values:
                strRep += str(v)
            print(strRep)
        elif command == "println":
            strRep = ""
            for v in values:
                strRep += str(v)
            print(strRep+"\n")
        elif command == "clear":
            os.system("cls")
        elif command == "printforeach":
            print(f"Error: command 'printforeach' not supported at line {packet['line']}")
while True:
    code = parser.parse(input())
    parse(code)