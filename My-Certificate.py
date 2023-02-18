import os
import datetime
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def generate_key_pair():
    # Generate a 2048 bit RSA key pair
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    # Serialize the private key to PEM format
    private_key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(b'coconut')
    )
    # Serialize the public key to PEM format
    public_key = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    # Write the private and public key to file
    with open('private_key.pem', 'wb') as f:
        f.write(private_key)

    os.chmod('private_key.pem', 0o700)

    with open('public_key.pem', 'wb') as f:
        f.write(public_key)


def Signature(message):

    password = input("Enter Password Of Private Key : ")
    # Read the private key from the file
    with open('private_key.pem', 'rb') as f:
        private_pem = f.read()
        private_key = load_pem_private_key(
            private_pem,
            password=password.encode(),
            backend=default_backend()
        )

    # Sign the message with the private key
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA512()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA512()
    )

    with open('Signature.txt', 'wb') as f:
        f.write(signature)


def Valid_Signature(Certificate, Signature, Public_Key, current_date, expiration_date):
    # Read the public key from the file
    with open(Public_Key, 'rb') as f:
        public_pem = f.read()
        public_key = serialization.load_pem_public_key(public_pem)

    # Read the Certificate from the file
    with open(Certificate, 'r') as f:
        Certificate = f.read()

    # Read the Signature from the file
    with open(Signature, 'rb') as f:
        Signature = f.read()

    # Hash the Certificate using SHA-512
    Certificate = Certificate.encode('utf-8')
    hash_object = hashlib.sha512(Certificate)
    Certificate_hash = hash_object.digest()

    if current_date <= expiration_date:
        print(
            "The expiration date has been verified. and expiration date :", expiration_date)
    else:
        print("Expired")
        exit()

    try:
        public_key.verify(
            Signature,
            Certificate_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA512()
        ),
        print("Certificate นี้ถูกค้อง")
    except:
        print("Certificate นี้ไม่ถูกค้อง")


def main():
    generate_key_pair()

    Data = []
    while True:
        name = input("ชื่อผู้ทำ Project : ")

        Data.append(name)

        student_number = input("รหัสนักศึกษา : ")
        Data.append(student_number)

        Project = input("ชื่อ Project : ")
        Data.append(Project)

        expiration_date = input("วันหมดอายุของใบรับรอง (YYYY-MM-DD): ")
        Data.append(expiration_date)

        Grade = input("Grade : ")
        Data.append(Grade)

        Public_benefit = input("Public benefit score : ")
        Data.append(Public_benefit)
        break

    # Concatenate the inputs into a single string
    message = ''.join(Data)
    with open('Certificate.txt', 'w') as f:
        f.write(message)

    # Hash the message using SHA-512
    message = message.encode('utf-8')
    hash_object = hashlib.sha512(message)
    message_hash = hash_object.digest()

    Signature(message_hash)

    if input("You want to Validate Signature Enter(ok) : ") == "ok":
        current_date = datetime.datetime.now()
        expiration_date = datetime.datetime.strptime(
            expiration_date, '%Y-%m-%d')
        Valid_Signature('Certificate.txt', 'Signature.txt',
                        'public_Key.pem', current_date, expiration_date)
    else:
        exit


if __name__ == "__main__":
    main()
