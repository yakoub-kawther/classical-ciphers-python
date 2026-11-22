
from ceaser_cipher import ceaser_cypher
from exo2 import affine_cypher
from exo3 import vigenere_cypher
from hill_cypher import hill_cypher
from rsa_scratch import rsa_cipher
from aes_cypher import aes_cypher
from aes2 import aes_cypher as aes


def ask_choice(prompt, options):
    while True:
        c = input(prompt).strip()
        if c in options:
            return c
        print("Invalid choice.")


if __name__ == "__main__":
 MENU = """
1 : Caesar
2 : Affine
3 : Vigenere
4 : Hill 
5 : AES-128
6 : RSA
0 : Quit
"""

ACTIONS = {
    "1": ceaser_cypher,
    "2": affine_cypher,
    "3": vigenere_cypher,
    "4": hill_cypher,
    "5": aes,
    "6": rsa_cipher,
}

while True:
    print(MENU)
    choice = input("Enter the algorithm that you want to use: ").strip()

    if choice == "0":
        print("Bye!")
        break
    elif choice in ACTIONS:
        ACTIONS[choice]()
    else:
        print("Invalid choice.")