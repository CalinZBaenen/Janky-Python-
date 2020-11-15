from language.Janky import *
parser = JankyParser()
while True:
    result = parser.parse(input())
    print(result)