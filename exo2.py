from math import gcd


def check_key(a):
    if gcd(a, 26) != 1:
        raise ValueError("Invalid key: gcd(a, 26) must be equal to 1")


def affine_encrypt(text, a, b):
    check_key(a)
    result = ""
    for ch in text.upper():
        if ch.isalpha():
            x = ord(ch) - ord('A')
            result += chr((a * x + b) % 26 + ord('A'))
        else:
            result += ch
    return result


def affine_decrypt(text, a, b):
    check_key(a)
    a_inv = pow(a, -1, 26)
    result = ""
    for ch in text.upper():
        if ch.isalpha():
            y = ord(ch) - ord('A')
            result += chr((a_inv * (y - b)) % 26 + ord('A'))
        else:
            result += ch
    return result


def affine_cypher():

    print("Hey, welcome to the Affine cipher")

    choice = 0
    while choice not in (1, 2):
        try:
            choice = int(input("\nDo you want to encrypt (1) or decrypt (2) a text? "))
        except ValueError:
            choice = 0

    # ask for the key (a, b) until a is valid
    a = None
    while a is None:
        try:
            a = int(input("\nEnter a (must be coprime with 26): "))
            b = int(input("Enter b: "))
        except ValueError:
            print("Numbers only, try again.")
            a = None
            continue

        if gcd(a, 26) != 1:
            print("Invalid key: gcd(a, 26) must be 1 "
                  "(valid a: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25), try again.")
            a = None

    if choice == 1:
        mssg = input("\nEnter the message: ")
        print("Encrypted:", affine_encrypt(mssg, a, b))
    else:
        mssg = input("\nEnter the encrypted message: ")
        print("Decrypted:", affine_decrypt(mssg, a, b))


# affine_cypher()


# print("1 : Chiffrer")
# print("2 : Dechiffrer")
# choice = input("Votre choix (1 ou 2) : ")

# if choice not in ("1", "2"):
#     print("Choix invalide")
# else:
#     a = int(input("Entrez a : "))
#     b = int(input("Entrez b : "))
#     text = input("Entrez le texte : ")

#     try:
#         if choice == "1":
#             print("Texte chiffre :", affine_encrypt(text, a, b))
#         else:
#             print("Texte dechiffre :", affine_decrypt(text, a, b))
#     except ValueError as e:
#         print("Erreur :", e)