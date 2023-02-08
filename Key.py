from Crypto.PublicKey import RSA


New_key = RSA.generate(2048)

def Create_Key():
    global New_key

    Private_key = New_key.exportKey("PEM")
    Public_key = New_key.publickey().exportKey("PEM")

    Pri = open("private_key.pem", "wb")
    Pri.write(Private_key)

    Pub = open("public_key.pem", "wb")
    Pub.write(Public_key)


def List_Key():

    Private_key = open('private_key.pem', 'r')
    print(Private_key.read())

    Public_key = open('public_key.pem', 'r')
    print(Public_key.read())
