from help_functions import is_prime
import random
from math import gcd
from PIL import Image , UnidentifiedImageError
import json
import os

"""
steps : 
encryption
1- choose 2 primes p and q
2- comute n = p*q
3- compute euler = (p-1)(q-1)
4- choose e randomly while 1<e<euler and e is a prime number
5- privite key (n , e )
6- encrypted mssg n^e mod n

decryption
1- d= e^-1 mod euler
2- decrypted_mssg = encrypted_mssg ^ d mod n

"""

def generate_keys(p, q):
    if not is_prime(p) or not is_prime(q) or p == q:
        return None
    n = p * q
    if n <= 36:                       
        return None
    euler = (p - 1) * (q - 1)

    e = random.randrange(2, euler)
    while gcd(e, euler) != 1:
        e = random.randrange(2, euler)
    d = pow(e, -1, euler)

    return (e, n), (d, n) 



def encryption(mssg, p, q):
    keys = generate_keys(p, q)
    if keys is None:                     # invalid primes or n too small
        print("Invalid keys: p and q must be different primes with p*q > 36")
        return None
    public, private = keys
    e, n = public

    letters = []
    for i in mssg:
        if 'A' <= i <= 'Z':
            k = ord(i) - 64             
        elif 'a' <= i <= 'z':
            k = ord(i) - 97+27
        elif '0' <= i <= '9':
            k = ord(i) - 48 + 53         
        else:
            continue
        letters.append(k)

    c = []
    for k in letters:
        c.append(pow(k, e, n))           # c = k^e mod n

    return c, public, private             # cipher public , private


def decryption(mssg, private_key):
    d, n = private_key
    result = ""
    for x in mssg:
        k = pow(x, d, n)
        if k <= 26:
            result += chr(k + 64)            # uppercase
        elif k <= 52:
            result += chr(k - 27 + 97)       # lowercase
        else:
            result += chr(k - 53 + 48)       # digit
    return result
    


# c, public, private = encryption("HELLO7", 101, 113)
# print(c, public, private)
# print(decryption(c, private))            # HELLO7

def encrypt_image(path, p, q):

    
    keys = generate_keys(p, q)

    if keys is None:
        print("Invalid keys")
        return None

    public, private = keys
    e, n = public

    
    img = Image.open(path).convert("RGB")


    cipher = []

    for pixel in img.getdata():
        for value in pixel:
            encrypted = pow(value, e, n)
            cipher.append(encrypted)

    # Create encrypted preview
    preview = Image.new("RGB", img.size)
    pixels = []

    for i in range(0, len(cipher), 3):
        r = cipher[i] % 256
        g = cipher[i + 1] % 256
        b = cipher[i + 2] % 256

        pixels.append((r, g, b))

    preview.putdata(pixels)
    preview.save("encrypted_preview.png")

    return cipher, img.size, private

result = encrypt_image("photo.png", 17, 19)

def decrypt_image(cipher, size, private_key):
    d, n = private_key

    values = []
    for c in cipher:
        values.append(pow(c, d, n))     # m = c^d mod n

    pixels = []
    for i in range(0, len(values), 3):  # group back into (R, G, B)
        pixels.append((values[i], values[i + 1], values[i + 2]))

    img = Image.new("RGB", size)
    img.putdata(pixels)
    return img




def rsa_cipher():

    print("Hey, welcome to RSA")

    # 1) what do we work on?
    kind = 0
    while kind not in (1, 2):
        try:
            kind = int(input("\nWork on a message (1) or a picture (2)? "))
        except ValueError:
            kind = 0

    # 2) encrypt or decrypt?
    choice = 0
    while choice not in (1, 2):
        try:
            choice = int(input("Do you want to encrypt (1) or decrypt (2)? "))
        except ValueError:
            choice = 0

    # ---------------- MESSAGE ----------------
    if kind == 1:
        if choice == 1:
            mssg = input("\nEnter the message: ")

            result = None
            while result is None:
                try:
                    p = int(input("Enter a prime p: "))
                    q = int(input("Enter a prime q: "))
                except ValueError:
                    print("Numbers only, try again.")
                    continue
                result = encryption(mssg, p, q)

            cipher, public, private = result
            print("\nEncrypted:", *cipher)
            print("Public key  (e, n):", public)
            print("Private key (d, n):", private, "(keep it, you need it to decrypt)")

        else:
            while True:
                try:
                    cipher = [int(x) for x in input("\nEnter the encrypted numbers (separated by spaces): ").split()]
                    d = int(input("Enter d: "))
                    n = int(input("Enter n: "))
                    break
                except ValueError:
                    print("Numbers only, try again.")

            print("Decrypted:", decryption(cipher, (d, n)))

    # ---------------- PICTURE ----------------
    else:
        if choice == 1:
            path = input("\nEnter the picture path: ")
            while True:
              try:
               Image.open(path).verify()      # checks it's a valid image
               break
              except (FileNotFoundError, UnidentifiedImageError, OSError):
                    path = input("Not a valid picture, try again: ")

               
            result = None
              
            while result is None:
                try:
                    p = int(input("Enter a prime p: "))
                    q = int(input("Enter a prime q: "))
                except ValueError:
                    print("Numbers only, try again.")
                    continue
                result = encrypt_image(path, p, q)

            cipher, size, private = result

            # save the cipher so we can decrypt later
            with open("encrypted_image.json", "w") as f:
                json.dump({"cipher": cipher, "size": list(size)}, f)

            print("\nEncrypted data saved in: encrypted_image.json")
            print("Preview saved in: encrypted_preview.png")
            print("Private key (d, n):", private, "(keep it, you need it to decrypt)")

        else:
            path = input("\nEnter the encrypted file (e.g. encrypted_image.json): ")
            while not os.path.isfile(path):
                path = input("File not found, try again: ")

            while True:
                try:
                    d = int(input("Enter d: "))
                    n = int(input("Enter n: "))
                    break
                except ValueError:
                    print("Numbers only, try again.")

            with open(path) as f:
                data = json.load(f)

            img = decrypt_image(data["cipher"], tuple(data["size"]), (d, n))
            img.save("decrypted.png")
            print("Decrypted picture saved in: decrypted.png")


# rsa_cipher()

