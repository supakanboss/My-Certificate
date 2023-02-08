from Key import *
print("1 : Create Key")
print("2 : List Key")

num = int(input("Input Functions Number: "))

while True:
    if num == 1:
        Create_Key()
        num = int(input("Input Functions Number: "))
    elif num == 2:
        List_Key()
        num = int(input("Input Functions Number: "))
    else:
        break
