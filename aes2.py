# AES-128 : implementation pedagogique (10 tours)
# Etapes : AddRoundKey, SubBytes, ShiftRows, MixColumns

# ---------- Calcul dans GF(2^8) ----------
def xtime(a):
    """multiplication par 2 dans GF(2^8)"""
    a <<= 1
    if a & 0x100:
        a ^= 0x11B
    return a & 0xFF


def gmul(a, b):
    """multiplication de a par b dans GF(2^8)"""
    r = 0
    while b:
        if b & 1:
            r ^= a
        a = xtime(a)
        b >>= 1
    return r


# ---------- Construction de la S-box ----------
def make_sbox():
    sbox = [0] * 256
    for x in range(256):
        # inverse de x dans GF(2^8) (0 reste 0)
        inv = 0
        if x:
            for y in range(1, 256):
                if gmul(x, y) == 1:
                    inv = y
                    break
        # transformation affine
        s = inv
        for i in range(1, 5):
            s ^= ((inv << i) | (inv >> (8 - i))) & 0xFF
        sbox[x] = s ^ 0x63
    return sbox


SBOX = make_sbox()
INV_SBOX = [0] * 256
for i, v in enumerate(SBOX):
    INV_SBOX[v] = i

# ---------- Key Expansion ----------
def key_expansion(key):
    """key : 16 octets -> 11 cles de tour (chacune 16 octets)"""
    w = [list(key[4 * i:4 * i + 4]) for i in range(4)]
    rcon = 1
    for i in range(4, 44):
        t = w[i - 1][:]
        if i % 4 == 0:
            t = t[1:] + t[:1]                 # RotWord
            t = [SBOX[b] for b in t]          # SubWord
            t[0] ^= rcon
            rcon = xtime(rcon)
        w.append([w[i - 4][j] ^ t[j] for j in range(4)])
    return [sum(w[4 * r:4 * r + 4], []) for r in range(11)]


# ---------- Les 4 operations (state = liste de 16 octets, par colonnes) ----------
def add_round_key(s, rk):
    return [s[i] ^ rk[i] for i in range(16)]


def sub_bytes(s):
    return [SBOX[b] for b in s]


def inv_sub_bytes(s):
    return [INV_SBOX[b] for b in s]


def shift_rows(s):
    # octet (ligne r, colonne c) = s[r + 4*c] ; ligne r decalee de r vers la gauche
    return [s[r + 4 * ((c + r) % 4)] for c in range(4) for r in range(4)]


def inv_shift_rows(s):
    return [s[r + 4 * ((c - r) % 4)] for c in range(4) for r in range(4)]


def mix_columns(s):
    out = []
    for c in range(4):
        a = s[4 * c:4 * c + 4]
        out += [
            gmul(a[0], 2) ^ gmul(a[1], 3) ^ a[2] ^ a[3],
            a[0] ^ gmul(a[1], 2) ^ gmul(a[2], 3) ^ a[3],
            a[0] ^ a[1] ^ gmul(a[2], 2) ^ gmul(a[3], 3),
            gmul(a[0], 3) ^ a[1] ^ a[2] ^ gmul(a[3], 2),
        ]
    return out


def inv_mix_columns(s):
    out = []
    for c in range(4):
        a = s[4 * c:4 * c + 4]
        out += [
            gmul(a[0], 14) ^ gmul(a[1], 11) ^ gmul(a[2], 13) ^ gmul(a[3], 9),
            gmul(a[0], 9) ^ gmul(a[1], 14) ^ gmul(a[2], 11) ^ gmul(a[3], 13),
            gmul(a[0], 13) ^ gmul(a[1], 9) ^ gmul(a[2], 14) ^ gmul(a[3], 11),
            gmul(a[0], 11) ^ gmul(a[1], 13) ^ gmul(a[2], 9) ^ gmul(a[3], 14),
        ]
    return out


# ---------- Chiffrement / dechiffrement d'un bloc de 16 octets ----------
def encrypt_block(block, round_keys):
    s = add_round_key(list(block), round_keys[0])
    for r in range(1, 10):
        s = sub_bytes(s)
        s = shift_rows(s)
        s = mix_columns(s)
        s = add_round_key(s, round_keys[r])
    s = sub_bytes(s)            # dernier tour : sans MixColumns
    s = shift_rows(s)
    s = add_round_key(s, round_keys[10])
    return bytes(s)


def decrypt_block(block, round_keys):
    s = add_round_key(list(block), round_keys[10])
    for r in range(9, 0, -1):
        s = inv_shift_rows(s)
        s = inv_sub_bytes(s)
        s = add_round_key(s, round_keys[r])
        s = inv_mix_columns(s)
    s = inv_shift_rows(s)
    s = inv_sub_bytes(s)
    s = add_round_key(s, round_keys[0])
    return bytes(s)


# ---------- Texte quelconque : padding + blocs ----------
def encrypt_text(text, key):
    rk = key_expansion(key)
    data = text.encode("utf-8")
    pad = 16 - len(data) % 16
    data += bytes([pad]) * pad                      # padding PKCS7
    out = b"".join(encrypt_block(data[i:i + 16], rk) for i in range(0, len(data), 16))
    return out.hex()


def decrypt_text(hex_text, key):
    rk = key_expansion(key)
    data = bytes.fromhex(hex_text)
    if len(data) == 0 or len(data) % 16 != 0:
        raise ValueError("Le texte chiffre doit contenir un multiple de 16 octets")
    out = b"".join(decrypt_block(data[i:i + 16], rk) for i in range(0, len(data), 16))
    pad = out[-1]
    if pad < 1 or pad > 16:
        raise ValueError("Cle incorrecte ou texte chiffre invalide")
    return out[:-pad].decode("utf-8")


# ---------- Interactive menu ----------
def ask_key():
    # same rules as before: keep letters/digits, then pad with x, re-enter or trim to 16
    key = "".join(ch for ch in input("Enter your key (must be 16 letters / 128 bits): ") if ch.isalnum())

    while len(key) < 16:
        c = input(
            "Key is less than 128 bits.\n"
            "Enter a new key (1) or fill the rest with x (2): "
        )
        if c == "1":
            key = "".join(ch for ch in input("Enter a new key: ") if ch.isalnum())
        elif c == "2":
            key = key + "x" * (16 - len(key))
        else:
            print("Invalid choice.")

    if len(key) > 16:
        print("This key is too long, we gonna ignore the rest")
        key = key[:16]

    print("key:", key)
    return key.encode("utf-8")


def aes_cypher():
    choice = input("You wanna encrypt (1) or decrypt (2): ").strip()

    if choice == "1":
        mssg = input("Enter your message: ")
        key = ask_key()
        print("encrypted mssg is :", encrypt_text(mssg, key))

    elif choice == "2":
        cipher_hex = input("Enter the ciphertext as plain hex text: ").strip().replace(" ", "")
        key = ask_key()
        try:
            print("decrypted mssg is :", decrypt_text(cipher_hex, key))
        except ValueError as e:
            print("Error:", e)

    else:
        print("Invalid choice.")


