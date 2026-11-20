def vigenere(text, key, mode):
    """mode = 1 : chiffrer  |  mode = 2 : dechiffrer"""
    key = key.upper()
    result = ""
    i = 0 
    for ch in text:
        if ch.isascii() and ch.isalpha():
            k = ord(key[i % len(key)]) - ord('A')
            if mode == 2:
                k = -k
            base = ord('A') if ch.isupper() else ord('a')
            x = ord(ch) - base
            result += chr((x + k) % 26 + base)
            i += 1         
        else:
            result += ch    
    return result



def vigenere_cypher():

    print("Hey, welcome to the Vigenere cipher")

    choice = 0
    while choice not in (1, 2):
        try:
            choice = int(input("\nDo you want to encrypt (1) or decrypt (2) a text? "))
        except ValueError:
            choice = 0

    # ask for the key until it contains only letters
    key = ""
    while key == "":
        key = input("\nEnter the key (letters only): ").strip()
        if not (key.isascii() and key.isalpha()):
            print("Invalid key: use letters only (A-Z), no spaces, digits or accents. Try again.")
            key = ""

    if choice == 1:
        mssg = input("\nEnter the message: ")
        print("Encrypted:", vigenere(mssg, key, 1))
    else:
        mssg = input("\nEnter the encrypted message: ")
        print("Decrypted:", vigenere(mssg, key, 2))


# vigenere_cypher()

