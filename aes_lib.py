# AES-GCM : chiffrement de texte ET d'images (fichiers)
# Installation : pip install cryptography
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag


# ---------- Fonctions de base (octets) ----------
def encrypt_bytes(data, key):
    nonce = os.urandom(12)                       # nonce aleatoire, unique
    return nonce + AESGCM(key).encrypt(nonce, data, None)   # nonce + chiffre + tag


def decrypt_bytes(data, key):
    nonce, encrypted = data[:12], data[12:]
    return AESGCM(key).decrypt(nonce, encrypted, None)


# ---------- Texte ----------
def encrypt_text(text, key):
    return encrypt_bytes(text.encode("utf-8"), key).hex()


def decrypt_text(hex_text, key):
    return decrypt_bytes(bytes.fromhex(hex_text), key).decode("utf-8")


# ---------- Fichiers (images, pdf, ...) ----------
def encrypt_file(src, dst, key):
    with open(src, "rb") as f:
        data = f.read()
    with open(dst, "wb") as f:
        f.write(encrypt_bytes(data, key))


def decrypt_file(src, dst, key):
    with open(src, "rb") as f:
        data = f.read()
    with open(dst, "wb") as f:
        f.write(decrypt_bytes(data, key))


# ---------- Programme principal ----------
# print("1 : Chiffrer un texte")
# print("2 : Dechiffrer un texte")
# print("3 : Chiffrer une image")
# print("4 : Dechiffrer une image")
# choice = input("Votre choix (1, 2, 3 ou 4) : ")

# if choice not in ("1", "2", "3", "4"):
#     print("Choix invalide")
# else:
#     key = input("Entrez la cle (exactement 16 caracteres) : ").encode("utf-8")
#     if len(key) != 16:
#         print("Erreur : la cle doit faire exactement 16 octets (AES-128)")
#     else:
#         try:
#             if choice == "1":
#                 text = input("Entrez le texte : ")
#                 print("Texte chiffre (hex) :", encrypt_text(text, key))

#             elif choice == "2":
#                 text = input("Entrez le texte chiffre (hex) : ")
#                 print("Texte dechiffre :", decrypt_text(text.strip(), key))

#             elif choice == "3":
#                 src = input("Nom de l'image (ex: photo.jpg) : ")
#                 encrypt_file(src, src + ".enc", key)
#                 print("Image chiffree enregistree dans :", src + ".enc")

#             else:
#                 src = input("Nom du fichier chiffre (ex: photo.jpg.enc) : ")
#                 dst = input("Nom de l'image a recuperer (ex: photo_dec.jpg) : ")
#                 decrypt_file(src, dst, key)
#                 print("Image dechiffree enregistree dans :", dst)

#         except FileNotFoundError:
#             print("Erreur : fichier introuvable")
#         except InvalidTag:
#             print("Erreur : cle incorrecte ou donnees modifiees")
#         except ValueError:
#             print("Erreur : donnees invalides")